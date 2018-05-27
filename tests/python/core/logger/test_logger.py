import unittest
import uuid
from dxl.core.logger import Logger
from dxl.core.logger.backend import SimpleInMemoryBackend
import logging

class TestLogger(unittest.TestCase):
    def create_temp_logger_and_simple_backend(self):
        from io import StringIO
        logger = Logger(uuid.uuid4())
        backend = SimpleInMemoryBackend()
        logger.backend = backend
        return logger, backend
    
    def get_messages(self, nb_phases):
        return [uuid.uuid4() for _ in nb_phases] 

    def test_before(self):
        logger, backend = self.create_temp_logger()
        messages = self.get_messages(4)
        m_def, m_before, m_run, m_after = messages 
        @logger.before.info(m_before)
        def foo():
            backend.info(m_run)
        backend.info(m_def)
        foo()
        backend.info(m_after)
        expected = tuple([backend.format(logging.INFO, m)] for m in messages)
        self.assertEqual(backend.content, (m_def, m_before, m_run, m_after))


            
