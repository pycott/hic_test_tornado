# coding=utf-8
import json
import os
import re
from io import BytesIO

from tornado.web import RequestHandler, stream_request_body

from parser.char_counter_parser import CharCounterParser
from settings import logging, UPLOAD_DIR

logger = logging.getLogger(__package__)


class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


@stream_request_body
class UploadHandler(RequestHandler):
    FILE_DATA_PARSER = CharCounterParser
    UPLOAD_PARSE_READY = 0
    UPLOAD_PARSE_PENDING = 1

    def prepare(self):
        self.parser = self.FILE_DATA_PARSER("utf-8")
        boundary = self.request.headers.get("Content-Type").split("boundary=")[-1]
        self.boundary = bytes("--%s" % boundary, encoding="utf-8")
        self.state = self.UPLOAD_PARSE_READY
        self.output = None
        self.find_filename = re.compile(b'filename="(.*)"')

    def post(self, *args, **kwargs):
        self.safe_close_output()
        self.write(json.dumps(self.parser.get_result()))

    def on_connection_close(self):
        super().on_connection_close()
        self.safe_close_output()

    def safe_close_output(self):
        if self.output is not None and not self.output.closed:
            self.output.close()

    def data_received(self, data):
        buff = data.split(self.boundary)
        for index, part in enumerate(buff):
            if not part:
                continue
            if part == "--\r\n":
                break
            if self.state == self.UPLOAD_PARSE_PENDING:
                if len(buff) > 1:
                    chunk = part[:-3]
                    self.output.write(chunk)
                    self.parser.parse_chunk(chunk)
                    self.safe_close_output()
                    self.state = self.UPLOAD_PARSE_READY
                    continue
                else:
                    self.output.write(part)
                    self.parser.parse_chunk(part)
                    continue

            elif self.state == self.UPLOAD_PARSE_READY:
                stream = BytesIO(part)
                stream.readline()
                form_data_type_line = stream.readline()
                if form_data_type_line.find(b"filename") > -1:
                    filename = re.search(self.find_filename, form_data_type_line).groups()[0]

                    path = os.path.join(UPLOAD_DIR, filename.decode("utf-8"))
                    self.output = open(path, "wb")

                    stream.readline()
                    stream.readline()

                    body = stream.read()
                    if len(buff) > index + 1:
                        chunk = body[:-3]
                        self.output.write(chunk)
                        self.parser.parse_chunk(chunk)
                        self.state = self.UPLOAD_PARSE_READY
                    else:
                        self.output.write(body)
                        self.parser.parse_chunk(body)
                        self.state = self.UPLOAD_PARSE_PENDING
                else:
                    stream.readline()
                    self.state = self.UPLOAD_PARSE_READY
