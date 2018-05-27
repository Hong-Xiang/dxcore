import unittest
import uuid
from dxl.core.logger import Logger
from dxl.core.logger.backend import SimpleInMemoryBackend
import logging





class TestLogger(unittest.TestCase):
    def create_temp_logger(self):
        logger = Logger(uuid.uuid4())
        logger.backend = self.backend
        return logger

    def get_messages(self, nb_phases):
        return [uuid.uuid4() for _ in range(nb_phases)]

    def test_before(self):
        logger = self.create_temp_logger()

        @logger.before.info(self.message_aspect_before())
        def foo():
            backend.info(self.message_during_call())

        backend.info(self.message_after_definition())
        foo()
        backend.info(self.message_after_call())
        self.assertFunctionCallInfoIsCorrect()



