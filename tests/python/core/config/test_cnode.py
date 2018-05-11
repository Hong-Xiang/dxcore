import unittest
from dxl.core.config import cnode

class TestCNode(unittest.TestCase):
    def test_construct(self):
        c_sub = cnode.CNode({'x': 1, 'y': 2})
        c = cnode.CNode({'sub': c_sub, 'z': 3})
    
    def test_normal_dict(self):
        c = cnode.CNode({'x': 1, 'y': 2})
        assert len(c) == 2
        assert c['x'] == 1
        assert c['y'] == 2
        assert tuple(c.keys()) == ('x', 'y')
        assert tuple(c.values()) == (1, 2)
        assert [v for k, v in c.items()] == [1, 2]
        assert [k for k, v in c.items()] == ['x', 'y']

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

    def test_update_n(self):
        c = cnode.CNode({'x': 1})
        c = cnode.CNode({'y': 2, 's': c})
        self.assertEqual(c['y'], 2)
        c.update(cnode.QueryKey('y'), 3)
        self.assertEqual(c['y'], 3)
        self.assertEqual(c.read(['s', 'x']), 1)
        c = c.update('s', {'x': 2})
        self.assertEqual(c.read(['s', 'x']), 2)

    def test_update_self(self):
        c = cnode.CNode({'x': 1})
        c.update([], {'x': 2})
        self.assertEqual(c['x'], 2)
        c.update(None, {'x': 3})
        self.assertEqual(c['x'], 3)

    def test_basic_init(self):
        c = cnode.CNode()
        c.update('x', {'a': 1, 'b': 2})
        self.assertEqual(c.read(['x', 'a']), 1)


    def test_basic_dict(self):
        dct = {
            'f1': {
                'x': 0,
                'y': 1,
            },
            'z': 2,
        }
        c = cnode.CNode(dct)
        self.assertEqual(c.read(cnode.QueryKey(['z'])), 2)
        self.assertEqual(c.read(cnode.QueryKey(['f1', 'x'])), 0)
    
    def test_father(self):
        c = cnode.CNode({'x': 1, 'y': {'z': 2}})
        c2 = c['y']
        assert c2.father == c