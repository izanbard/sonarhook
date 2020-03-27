from waitress import serve
from .app import create_app


SERVER_PORT = 9000
SERVER = "0.0.0.0"


if __name__ == '__main__':
    app = create_app()
    serve(app, host=SERVER, port=SERVER_PORT)