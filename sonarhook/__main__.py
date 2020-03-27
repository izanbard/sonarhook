from waitress import serve
from .app import create_app
import argparse


SERVER_PORT = 9000
SERVER = "0.0.0.0"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="app.config.json"
    )
    return parser.parse_args()

if __name__ == '__main__':
    app = create_app(parse_arguments())
    serve(app, host=SERVER, port=SERVER_PORT)