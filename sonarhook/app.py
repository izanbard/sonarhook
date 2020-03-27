import hashlib
import hmac
import json
import os
from pathlib import Path

from azure.devops.connection import Connection
from flask import request, Flask, abort
from msrest.authentication import BasicAuthentication

ADO_PAT = os.environ.get("ADO_PAT").strip()
SONAR_WEBHOOK_SECRET = os.environ.get("SONAR_WEBHOOK_SECRET").strip()


def create_app(args):
    app = Flask(__name__)

    @app.route("/sonarhook", methods=['POST'])
    def prhook():
        input_json = request.get_json()
        if not valid_hmac_signature(request.data):
            abort(401)
        if not is_pr_of_correct_type(input_json):
            return "", 204
        return send_ado_pr_status(input_json)

    def send_ado_pr_status(input_json):
        config = get_config(args.config)
        if input_json["project"]["key"] not in config["repos"]:
            return "", 204
        org_url = config["repos"][input_json["project"]["key"]]["org_url"]
        project_id = config["repos"][input_json["project"]["key"]]["project_name"]
        pr_id = int(input_json["branch"]["name"])

        credentials = BasicAuthentication('', ADO_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        git_client = connection.clients_v5_1.get_git_client()

        repo_id = get_repo_id(config["repos"][input_json["project"]["key"]]["repo_name"], git_client, project_id)
        if repo_id is None:
            abort(404)

        context = {
            'genre': "SonarHook",
            'name': input_json["project"]["name"]
        }
        state = 'succeeded' if input_json["qualityGate"]["status"] == "OK" else 'failed'
        target_url = input_json["branch"]["url"]
        git_pr_status = {
            'context': context,
            'state': state,
            'target_url': target_url,
        }

        response = git_client.create_pull_request_status(
            status=git_pr_status,
            repository_id=repo_id,
            pull_request_id=pr_id,
            project=project_id
        )

        return "ok", 200

    def get_repo_id(name, client, project):
        repos = client.get_repositories(project=project)
        for repo in repos:
            if repo.name == name:
                return repo.id
        return None

    def get_config(filename):
        file = Path(os.path.join(os.getcwd(), filename))
        if not file.exists() or not file.is_file():
            abort(500)
        with open(file, "r") as fd:
            config = json.load(fd)
        return config

    def valid_hmac_signature(input_bytes):
        signature = hmac.new(SONAR_WEBHOOK_SECRET.encode(), input_bytes, hashlib.sha256)
        return signature.hexdigest() == request.headers['X-Sonar-Webhook-HMAC-SHA256']

    def is_pr_of_correct_type(input_json):
        pr_type = "PULL_REQUEST" == input_json['branch']['type']
        return pr_type

    return app
