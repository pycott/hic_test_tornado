import codecs


class CharCounterParser(object):
    def __init__(self, encoding):
        self.encoding = encoding
        self._bytes_read = 0
        self._chars_read = 0
        self._errors_count = 0
        codecs.register_error("strict", self._strict_handler)

    def parse_chunk(self, chunk):
        self._bytes_read += len(chunk)
        self._chars_read += len(codecs.decode(chunk, self.encoding, errors="strict"))

    def get_result(self):
        return {
            "bytes_readed": self._bytes_read,
            "chars_readed": self._chars_read + self._errors_count // 2,
        }

    def _strict_handler(self, exception):
        self._errors_count += 1
        return u"", exception.end
