# coding=utf-8
import logging.config
import os

from constants import Size

DEBUG = True
BASE_DIR = os.path.dirname(__file__)

# *** tornado ***
APP_SETTINGS = {
    "debug": DEBUG,
    "autoreload": DEBUG,
    "xsrf_cookies": True,
    "cookie_secret": "@#$3452tgwesrg05ut467w34%^@#$%^#$%^356345tgiturweh58u1uvrwefsdfh",
    "template_path": os.path.join(BASE_DIR, 'templates'),
    "static_path": os.path.join(BASE_DIR, "static"),
}

HTTP_SERVER_SETTINGS = {
    "max_body_size": 10 * Size.GB,
    "max_buffer_size": 10 * Size.MB,
}

PORT = 8888

# *** logging ***
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        "verbose": {
            "format": "%(asctime)s: %(name)-1s: %(levelname)-1s: %(processName)-1s: %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "verbose",
            "stream": "ext://sys.stdout"
        }
    },

    "loggers": {
        "default": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },

        "parser": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
    },
})

# *** application ***
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
