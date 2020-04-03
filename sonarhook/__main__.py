from waitress import serve

from .api import create_api
from .app import Application

if __name__ == '__main__':
    try:
        app = Application()
    except FileNotFoundError:
        app.log.critical("exiting a failed app start")
        exit(1)
    app.log.info("creating API")
    api = create_api(app)
    app.log.info("starting server")
    serve(
        api,
        host=app.config["application"]["bind_address"],
        port=app.config["application"]["port"]
    )
