import unittest
from dxl.core.logger import aspect
from dxl.core.logger.backend import SimpleInMemoryBackend
import uuid
import logging


class LoggerTestCase(unittest.TestCase):
    class FunctionCallMessages:
        AFTER_DEFINITION = 'after_definition'
        ASPECT_BEFORE = 'aspect_before'
        DURING_CALL = 'during_call'
        AFTER_CALL = 'after_call'

    def setUp(self):
        self.backend = SimpleInMemoryBackend()
        self.messages = []
        self.levels = None

    def tearDown(self):
        self.backend = None
        self.messages = []
        self.levels = None

    def expected_log(self):
        """
        Format expected INFO messages from 
        """
        if self.levels is None:
            level = [logging.INFO for _ in self.messages]
        return '\n'.join(
            [self.backend.format(l, m) for l, m in zip(level, self.messages)])

    def verify_messages(self, result):
        return result == self.expected_log()

    def test_verify_messages(self):
        messages = ['test0', 'test1']
        self.messages = messages
        test_backend = SimpleInMemoryBackend()
        for m in messages:
            test_backend.info(m)
        self.assertTrue(self.verify_messages(test_backend.content()))

    def assertMessagesAreCorrect(self):
        if not self.verify_messages(self.backend.content()):
            self.fail(
                'Verification failed.\nExpected:\n{}\nResult:\n{}\n'.format(
                    self.expected_log(), self.backend.content()))


class TestLoggerBeforeAspect(LoggerTestCase):
    def create_aspect(self):
        return aspect.LoggerBefore(self.backend)

    def test_create(self):
        a = self.create_aspect()
        self.assertIsInstance(a, aspect.LoggerBefore)
        self.assertIsInstance(a.backend, SimpleInMemoryBackend)

    def test_calledtime(self):
        a = self.create_aspect()
        self.messages = [
            self.FunctionCallMessages.AFTER_DEFINITION,
            self.FunctionCallMessages.ASPECT_BEFORE,
            self.FunctionCallMessages.DURING_CALL,
            self.FunctionCallMessages.AFTER_CALL
        ]

        @a.info(self.FunctionCallMessages.ASPECT_BEFORE)
        def foo():
            self.backend.info(self.FunctionCallMessages.DURING_CALL)

        self.backend.info(self.FunctionCallMessages.AFTER_DEFINITION)
        foo()
        self.backend.info(self.FunctionCallMessages.AFTER_CALL)
        self.assertMessagesAreCorrect()

    def test_args(self):
        a = self.create_aspect()
        self.messages = ['arg0: 1, arg1: 2']

        @a.info('arg0: {}, arg1: {}')
        def foo(a, b):
            pass

        foo(1, 2)
        self.assertMessagesAreCorrect()
