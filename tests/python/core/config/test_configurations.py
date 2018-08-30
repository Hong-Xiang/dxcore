
from dxl.core.config.configurations import Sourceable, Configuration, ConfigProxy, AbstractProxy
from dxl.core.config import cnode, view
import pdb

class Test_Sourceable:

	def test_inheritance(self):

		class A(Sourceable):

			def __init__(self):
				pass

			def read(self, config_path):
				return config_path

			def write(self, keys, config_obj, is_overwrite=False):
				return keys, config_obj
		obj = A()

		assert obj.read('/x/y/z') == '/x/y/z'
		assert obj.write('graph', {'x':1,'y':2}) ==('graph',{'x':1,'y':2})

class Test_AbstractProxy:

	def test_inheritance_proxy(self):

		class proxy(AbstractProxy):

			def __init__(self, a):
				self.a = a

			def create_proxy(self):
				self.a = 2
		p = proxy(1)
		p.create_proxy()
		assert p.a == 2


class Test_Configuration:

	def test_read_configs_node(self):
		root1 = cnode.CNode({'x':1})
		root2 = cnode.CNode({'y':2})
		a = Configuration(root1)
		b = Configuration(root2)
		assert a is not b
		assert a.read('x') == 1
		assert a['x'] == 1

	def test_write_configs(self):
		root1 = cnode.CNode({'x':1})
		a = Configuration(root1)
		a.write('x/y',2)
		a.write('x/z', {'z1':11, 'z2':22})
		a.write('x/y/d', cnode.CNode({'d1': 33}))
		assert a['x']['z']['z2'] == 22
		assert a['x']['y'] is not 2
		assert a['x']['y']['d']['d1'] == 33

	def test_write_configs_with_overwrite(self):
		root1 = cnode.CNode({'x':1})
		node1 = cnode.CNode({'z':3})
		node2 = cnode.CNode({'d':4})
		a = Configuration(root1)
		a.write('x/y',node2)
		a.write('x/y',node1,is_overwrite=False)
		assert a['x']['y']['d'] == 4
		a.write('x/y',node1,is_overwrite=True)
		assert a['x']['y']['d'] is None


class Test_ConfigProxy:

	def test_singleton(self):
		root1 = cnode.CNode({'x':1})
		root2 = cnode.CNode({'y':2})
		c1 = Configuration(root1)
		c2 = Configuration(root2)
		a = ConfigProxy(c1,'root1')
		b = ConfigProxy(c2,'root2')
		assert a is b
		assert b.get_root_node('root2')['y'] == 2

	def test_add_proxy(self):
		root1 = cnode.CNode({'x':1})
		root2 = cnode.CNode({'y':2})
		c1 = Configuration(root1)
		c2 = Configuration(root2)
		cp = ConfigProxy(c1,'root1')
		cp.add_proxy(c2,'root2')
		r2 = cp.get_root_node('root2')
		r1 = cp.get_root_node('root1')
		assert r2 is root2
		assert r1 is root1

	def test_write(self):
		root1 = cnode.CNode({'x': 1})
		c1 = Configuration(root1)
		cp = ConfigProxy(c1, 'root1')
		cp.write('root1','x/y',{'y1':3, 'y2':4})
		r = cp.get_root_node('root1')
		assert r['x']['y']['y1'] == 3
		assert r['x']['y']['y2'] == 4

	def test_read(self):
		node1 = cnode.CNode({'z':3})
		root1 = cnode.CNode({'x':1,'y':node1})
		c1 = Configuration(root1)
		cp = ConfigProxy(c1,'root1')
		assert cp.read('root1', 'y/z') == 3
		assert cp.read('root1', 'y')['z'] == 3
		assert cp['root1']['y']['z'] == 3

	def test_get_root_node(self):
		node1 = cnode.CNode({'x':1})
		c1 = Configuration(node1)
		cp = ConfigProxy(c1,'root1')
		assert cp.get_root_node('root1')['x'] == 1

	def test_set_root_node(self):
		node1 = cnode.CNode({'x':1})
		node2 = cnode.CNode({'y':2})
		c1 = Configuration(node1)
		cp = ConfigProxy(c1,'root1')
		cp.set_root_node('root1', node2)
		assert cp.get_root_node('root1')['y'] == 2

	def test_set_root_node_by_dic_way(self):
		node1 = cnode.CNode({'x':1})
		node2 = cnode.CNode({'y':2})
		c1 = Configuration(node1)
		cp = ConfigProxy(c1,'root1')
		cp['root1'] = node2
		assert cp['root1']['y'] == 2