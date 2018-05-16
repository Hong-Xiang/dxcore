from dxl.core.config import create_config_tree, create_view
import unittest


class TestConfigAPI(unittest.TestCase):
    def test_basic(self):
        dct = {
            'aaa': {
                'bbb': {
                    'x': 1,
                    'y': 2,
                },
                'z': 3,
            }
        }
        c = create_config_tree(dct)
        v = create_view(c, 'aaa/bbb')
        self.assertEqual(v['x'], 1)
        self.assertEqual(v['y'], 2)
        self.assertEqual(v['z'], 3)
