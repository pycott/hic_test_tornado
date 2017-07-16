# coding=utf-8
from parser.handlers import *

urlpatterns = [
    (r"/", IndexHandler),
    (r"/upload", UploadHandler),
]
