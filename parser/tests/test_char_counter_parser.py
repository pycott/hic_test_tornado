import unittest

from parser.char_counter_parser import CharCounterParser


class CharCounterParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = CharCounterParser("utf-8")

    def test_parse_chunk_ascii(self):
        chunk = b"qwe123"
        correct_count = 6

        self.parser.parse_chunk(chunk)
        chars_read = self.parser.get_result()["chars_read"]
        self.assertEqual(chars_read, correct_count)

    def test_parse_chunk_unicode(self):
        chunk = b'\xd0\xba\xd0\xbe\xd1\x82\xd1\x8b'  # коты
        correct_count = 4

        self.parser.parse_chunk(chunk)
        chars_read = self.parser.get_result()["chars_read"]
        self.assertEqual(chars_read, correct_count)

    def test_parse_chunk_broken_unicode(self):
        chunk = b'\xd0\xba\xd0\xbe\xd1\x82\xd1'  # кот и половина буквы "ы"
        correct_count = 3

        self.parser.parse_chunk(chunk)
        chars_read = self.parser.get_result()["chars_read"]
        self.assertEqual(chars_read, correct_count)

    def test_parse_chunks_correction(self):
        chunks = [
            b'\xd0\xba\xd0\xbe\xd1\x82\xd1',  # кот и половина буквы "ы"
            b'\x8b\xd0\xba\xd0\xbe\xd1\x82\xd1\x8b',  # вторая половина буквы "ы" и коты
            b'\xd0\xba\xd0\xbe\xd1',  # ко и половина буквы "т"
        ]

        correct_count = 8
        self.parser.parse_chunk(chunks[0])
        self.parser.parse_chunk(chunks[1])
        chars_read = self.parser.get_result()["chars_read"]
        self.assertEqual(chars_read, correct_count)

        correct_count = 10
        self.parser.parse_chunk(chunks[2])
        chars_read = self.parser.get_result()["chars_read"]
        self.assertEqual(chars_read, correct_count)
