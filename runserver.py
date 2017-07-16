# coding=utf-8
import os

import logging
from tornado import ioloop, httpserver
from tornado.web import Application

import settings
from urls import urlpatterns

logger = logging.getLogger("default")


def prepare_project():
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)


if __name__ == "__main__":
    logger.info("server started")
    prepare_project()
    app = Application(urlpatterns, **settings.APP_SETTINGS)
    http_server = httpserver.HTTPServer(app, **settings.HTTP_SERVER_SETTINGS)
    http_server.listen(settings.PORT)
    ioloop.IOLoop.instance().start()
