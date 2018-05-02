import unittest
from dxl.core.config import cnode, view


class TestHelpers(unittest.TestCase):
    def test_base_node(self):
        sub = cnode.CNode()
        c = cnode.CNode({'x': sub})
        self.assertIs(view.base_node(c, 'x'), sub)

    def test_base_node_of_root(self):
        sub = cnode.CNode()
        c = cnode.CNode({'x': sub})
        self.assertIs(view.base_node(c, '/'), c)

    def test_find_ancestors(self):
        c0 = cnode.CNode()
        c1 = cnode.CNode({'x': c0})
        c2 = cnode.CNode({'y': c1})
        nodes = view._find_ancestors(c2, c0)
        self.assertEqual(len(nodes), 2)
        self.assertIs(nodes[0], c2)
        self.assertIs(nodes[1], c1)


class TestConfigs(unittest.TestCase):
    def setUp(self):
        self.c = cnode.from_dict({
            'k1': 'v1',
            'k2': {
                'k2_1': 'v2_1',
                'k2_2': 'v2_2'
            },
            'k3': {
                'k3_1': {
                    'k3_3_1': 'v_3'
                },
                'k3_2': 'v3_0'
            }
        })

    def test_basic_dict(self):
        cv = view.CView(self.c)
        self.assertEqual(cv['k1'], 'v1')
        self.assertEqual(cv['k2']['k2_1'], 'v2_1')
        self.assertEqual(cv['k2']['k2_2'], 'v2_2')
        self.assertEqual(cv['k3']['k3_1']['k3_3_1'], 'v_3')

    def test_basepath1(self):
        cv = view.CView(self.c, view.base_node(self.c, 'k2'))
        self.assertEqual(cv['k2_1'], 'v2_1')

    def test_basepath2(self):
        cv = view.CView(self.c, view.base_node(self.c, 'k3/k3_1'))
        self.assertEqual(cv['k3_3_1'], 'v_3')

    def test_inherence(self):
        cv = view.CView(self.c, view.base_node(self.c, 'k3/k3_1'))
        self.assertEqual(cv['k3_2'], 'v3_0')

    def test_name(self):
        cv = view.CView(self.c)
        self.assertEqual(cv['k2/k2_1'], 'v2_1')

    def test_none(self):
        cv = view.CView(self.c)
        self.assertIsNone(cv['aaa'])

    def test_none_path(self):
        cv = view.CView(self.c)
        self.assertIsNone(cv['aaa/bbb'])

    def test_inherence_2(self):
        c = cnode.from_dict({'k1': {'k2': {'k3': 'v1'}, 'k4': 'v2'}})
        cv = view.CView(c, view.base_node(c, 'k1/k2'))
        self.assertEqual(cv['k4'], 'v2')
