import argparse
import json
import os
import string
from pathlib import Path
import logging
from .ConfigNotFound import ConfigNotFound


class Application:
    args = None
    config = None
    ADO_PAT = None
    SONAR_WEBHOOK_SECRET = None
    log = None
    level = logging.INFO

    def __init__(self):
        self.log = logging.getLogger('sonarhook')
        self.log.setLevel(self.level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.log.addHandler(console_handler)
        self.log.critical("App started")
        self.parse_arguments()
        self.log.info("Parsed Arguments")
        self.get_config(self.args.config)
        self.log.info("Got Config")
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
            self.log.critical("Config file not found: %s", file)
            raise ConfigNotFound(f"specified config file not found - {file} - Aborting")
        with open(file, "r") as fd:
            self.config = json.load(fd)
        return self.config

    def clean_filename(self, dirty_filename):
        white_list = string.ascii_letters + string.digits + "-_./"
        cleaned_filename = ''.join(c for c in dirty_filename if c in white_list)
        return cleaned_filename
