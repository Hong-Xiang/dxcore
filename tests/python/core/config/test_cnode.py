import unittest
from dxl.core.config import cnode


class TestQueryKey(unittest.TestCase):
    def test_construct(self):
        k = cnode.QueryKey(['x', 'y', 'z'])

    def test_head(self):
        k = cnode.QueryKey(['x', 'y', 'z'])
        self.assertEqual(k.head(), 'x')

    def test_tail(self):
        k = cnode.QueryKey(['x', 'y', 'z'])
        self.assertIsInstance(k.tail(), cnode.QueryKey)
        self.assertEqual(k.tail().head(), 'y')
        self.assertEqual(k.tail().tail().head(), 'z')

    def test_len(self):
        k = cnode.QueryKey(['x', 'y', 'z'])
        self.assertEqual(len(k), 3)


class TestCNode(unittest.TestCase):
    def test_construct(self):
        c_sub = cnode.CNode({'x': 1, 'y': 2})
        c = cnode.CNode({'sub': c_sub, 'z': 3})

    def test_read_value_simple(self):
        c = cnode.CNode({'x': 1})
        self.assertEqual(c.read(cnode.QueryKey(['x'])), 1)

    def test_read_value_recursive(self):
        c_sub = cnode.CNode({'x': 1})
        c = cnode.CNode({'y': 2, 's': c_sub})
        self.assertEqual(c.read(cnode.QueryKey(['s', 'x'])), 1)

    def test_create(self):
        c = cnode.CNode()
        c.create(cnode.QueryKey(['x']), cnode.CNode({'y': 1}))
        self.assertEqual(c.read(cnode.QueryKey(['x', 'y'])), 1)

    def test_fast_read(self):
        c = cnode.CNode({'x': 1})
        c = cnode.CNode({'s': c, 'y': 2})
        self.assertEqual(c.read(['s', 'x']), 1)
        self.assertEqual(c.read('y'), 2)

    def test_fast_create(self):
        c = cnode.CNode()
        c.create('x', cnode.CNode({'y': 1}))
        self.assertEqual(c.read(cnode.QueryKey(['x', 'y'])), 1)

    def test_update_v(self):
        c = cnode.CNode({'x': 1})
        c = cnode.CNode({'y': 2, 's': c})
        self.assertEqual(c['y'], 2)
        c.update(cnode.QueryKey('y'), 3)
        self.assertEqual(c['y'], 3)


class TestFromDict(unittest.TestCase):
    def test_basic(self):
        dct = {
            'f1': {
                'x': 0,
                'y': 1,
            },
            'z': 2,
        }
        c = cnode.from_dict(dct)
        self.assertEqual(c.read(cnode.QueryKey(['z'])), 2)
        self.assertEqual(c.read(cnode.QueryKey(['f1', 'x'])), 0)