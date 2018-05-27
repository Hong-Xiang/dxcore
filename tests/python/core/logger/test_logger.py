import unittest
import uuid
from dxl.core.logger import Logger
from dxl.core.logger.backend import SimpleInMemoryBackend
import logging

from .test_aspect import LoggerTestCase


class TestLogger(LoggerTestCase):
    def create_temp_logger(self):
        logger = Logger(self.backend)
        return logger

    def test_before(self):
        from dxl.core.logger.aspect import LoggerBefore
        logger = self.create_temp_logger()
        self.assertIsInstance(logger.before, LoggerBefore)

        messages = ['foo called.']
        self.messages = messages

        @logger.before.info(messages[0])
        def foo():
            pass

        foo()
        self.assertMessagesAreCorrect()
