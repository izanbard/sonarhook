import hashlib
import hmac
import json

from azure.devops.connection import Connection
from flask import request, Flask, abort
from msrest.authentication import BasicAuthentication

from .app import Application


def create_api(app: Application):
    api = Flask(__name__)

    @api.route("/healthcheck", methods=["GET"])
    def health_check():
        app.log.warn("received a Health check call")
        if "secret" not in request.args:
            app.log.info("404 after no health check secret")
            abort(404)
        if request.args["secret"] != app.config["application"]["health_check_secret"]:
            app.log.info("401 after bad secret passed in config")
            abort(401)
        return json.dumps(app.config), 200

    @api.route("/sonarhook", methods=['POST'])
    def sonar_hook():
        app.log.info("received sonarhook")
        input_json = request.get_json()
        app.log.debug(input_json)
        if not valid_hmac_signature(request.data):
            app.log.warn("invalid HMAC sig aborting")
            abort(401)
        if not is_pr_of_correct_type(input_json):
            app.log.info("Skipping non PR hook")
            return "", 204
        return send_ado_pr_status(input_json)

    def send_ado_pr_status(input_json):
        if input_json["project"]["key"] not in app.config["repos"]:
            app.log.info("skipping hook for project not in config")
            return "", 204
        project_id = app.config["repos"][input_json["project"]["key"]]["project_name"]
        app.log.debug("hook for project: %s", project_id)
        git_client = get_git_client(input_json)
        repo_id = get_repo_id(app.config["repos"][input_json["project"]["key"]]["repo_name"], git_client, project_id)
        if repo_id is None:
            app.log.warn("aborting no repo id in input json")
            abort(404)
        app.log.debug("hook for repo: %s", repo_id)

        pr_status = create_pr_status(input_json)
        app.log.debug("Sent Status")
        app.log.debug(pr_status)
        pr_id = int(input_json["branch"]["name"])
        app.log.debug("PR ID: %s", pr_id)
        response = git_client.create_pull_request_status(
            status=pr_status,
            repository_id=repo_id,
            pull_request_id=pr_id,
            project=project_id
        )

        return response.state, 200

    def create_pr_status(input_json):
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
        return git_pr_status

    def get_git_client(input_json):
        org_url = app.config["repos"][input_json["project"]["key"]]["org_url"]
        credentials = BasicAuthentication('', app.ADO_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        git_client = connection.clients_v5_1.get_git_client()
        return git_client

    def get_repo_id(name, client, project):
        repos = client.get_repositories(project=project)
        for repo in repos:
            if repo.name == name:
                return repo.id
        return None

    def valid_hmac_signature(input_bytes):
        signature = hmac.new(app.SONAR_WEBHOOK_SECRET.encode(), input_bytes, hashlib.sha256)
        return signature.hexdigest() == request.headers['X-Sonar-Webhook-HMAC-SHA256']

    def is_pr_of_correct_type(input_json):
        pr_type = "PULL_REQUEST" == input_json['branch']['type']
        return pr_type

    return api
