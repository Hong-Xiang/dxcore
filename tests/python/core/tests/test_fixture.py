from dxl.core.test.fixture import FixturesManager
import unittest

class TestFixturesManager(unittest.TestCase):
    def test_persistent_path(self):
        assert FixturesManager.path == '/some/path?'
    
    def test_persistent_path_reset(self):
        FixturesManager.set_path('/some/path0')
        assert FixturesManager.path == '/some/path0'
        FixturesManager.reset()
        assert FixturesManager.path == '/some/path?'