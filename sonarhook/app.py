import requests
import os
import hmac
import hashlib

from flask import request, Flask, abort

circle_token = os.environ.get("CIRCLE_CI_TOKEN")
secret = "daveisachampion"


def create_app():
    app = Flask(__name__)

    @app.route("/sonarhook", methods=['POST'])
    def prhook():
        input_json = request.get_json()
        print(input_json)
        if not valid_hmac_signature(request.data):
            abort(404)
        if not is_pr_of_correct_type(input_json):
            return "", 204
        return send_ado_pr_status(input_json)

    def send_ado_pr_status(input_json):
        return "ok", 200

    def valid_hmac_signature(input_bytes):
        signature = hmac.new(secret.encode(), input_bytes, hashlib.sha256)
        print(signature.hexdigest())
        print(request.headers['X-Sonar-Webhook-HMAC-SHA256'])
        return signature.hexdigest() == request.headers['X-Sonar-Webhook-HMAC-SHA256']

    def is_pr_of_correct_type(input_json):
        return "PULL_REQUEST" == input_json['branch']['type']

    return app