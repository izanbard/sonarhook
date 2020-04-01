import argparse
import json
import os
from pathlib import Path
import string


class Application:
    args = None
    config = None
    ADO_PAT = None
    SONAR_WEBHOOK_SECRET = None

    def __init__(self):
        self.parse_arguments()
        self.get_config(self.args.config)
        self.ADO_PAT = os.environ.get("ADO_PAT")
        if type(self.ADO_PAT) is str:
            self.ADO_PAT = self.ADO_PAT.strip()
        self.SONAR_WEBHOOK_SECRET = os.environ.get("SONAR_WEBHOOK_SECRET")
        if type(self.SONAR_WEBHOOK_SECRET) is str:
            self.SONAR_WEBHOOK_SECRET = self.SONAR_WEBHOOK_SECRET.strip()

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--config",
            "-c",
            type=str,
            default="app.config.json"
        )
        self.args = parser.parse_args()
        self.args.config = self.clean_filename(self.args.config)
        return self.args

    def get_config(self, filename):
        file = Path(os.path.join(os.getcwd(), filename))
        if not file.exists() or not file.is_file():
            raise FileNotFoundError(f"specified config file not found - {file} - Aborting")
        with open(file, "r") as fd:
            self.config = json.load(fd)
        return self.config

    def clean_filename(self, dirty_filename):
        white_list=string.ascii_letters+string.digits+"-_."
        cleaned_filename = ''.join(c for c in dirty_filename if c in white_list)
        return cleaned_filename
