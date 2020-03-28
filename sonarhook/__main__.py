from waitress import serve

from .api import create_api
from .app import Application

if __name__ == '__main__':
    app = Application()
    api = create_api(app)
    serve(
        api,
        host=app.config["application"]["bind_address"],
        port=app.config["application"]["port"]
    )
