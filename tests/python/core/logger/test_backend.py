import unittest
import logging
from dxl.core.logger import backend


class TestSimpleInMemoryBackend(unittest.TestCase):
    def create_backend(self):
        return backend.SimpleInMemoryBackend()

    def test_info_format(self):
        b = self.create_backend()
        assert b.format(logging.INFO, 'test') == '[INFO] test'

    def test_info(self):
        b = self.create_backend()
        b.info('test')
        assert len(b) == 1
        assert b.content() == b.format(logging.INFO, 'test')
    
    def test_content_empty(self):
        b = self.create_backend()
        assert b.content() == ''
