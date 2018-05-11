import unittest
from dxl.core.config import query_key as qk


class TestQueryKey(unittest.TestCase):
    def test_construct(self):
        k = qk.QueryKey(['x', 'y', 'z'])

    def test_head(self):
        k = qk.QueryKey(['x', 'y', 'z'])
        self.assertEqual(k.head(), 'x')

    def test_head_none(self):
        k = qk.QueryKey()
        assert k.head() is None

    def test_tail(self):
        k = qk.QueryKey(['x', 'y', 'z'])
        self.assertIsInstance(k.tail(), qk.QueryKey)
        self.assertEqual(k.tail().head(), 'y')
        self.assertEqual(k.tail().tail().head(), 'z')

    def test_len(self):
        k = qk.QueryKey(['x', 'y', 'z'])
        self.assertEqual(len(k), 3)
