import abc
import threading
from ..config import cnode, view


class Sourceable(object):

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def read(self, keys):
		"""read Cnode/Cview from a configuration tree ."""
		return

	@abc.abstractmethod
	def write(self, keys, config_obj, is_overwrite=False):
		"""add new configuration to a singleton config tree"""
		return


class AbstractProxy(object):

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def create_proxy(self):
		""" factory create method."""
		return


class Configuration(Sourceable):

	__root = None

	def __init__(self, root_node):
		if not isinstance(root_node, cnode.CNode):
			raise ValueError("root must be Cnode object.")
		self.set_root(root_node)

	def set_root(self, root):
		self.__root = root

	def get_root(self):
		return self.__root

	def read(self, keys)-> view.CView:
		if self.__root is not None:
			cv = view.CView(self.__root)
			return cv.get(keys)

	def __getitem__(self, keys):
		return self.read(keys)

	def write(self, keys, config_obj: [str, dict, cnode.CNode], is_overwrite=False):
		self.__root.update(keys, config_obj, overwrite_node=is_overwrite)


class ConfigProxy(AbstractProxy):

	"""a proxy for configuration."""
	_instance_lock = threading.Lock()
	__configs = {}

	def __init__(self, root, root_id):
		self.init_params = [root, root_id]
		self.create_proxy()

	def __new__(cls, *args, **kwargs):
		if not hasattr(ConfigProxy, '_instance'):
			with ConfigProxy._instance_lock:
				if not hasattr(ConfigProxy, '_instance'):
					ConfigProxy._instance = object.__new__(cls)
		return ConfigProxy._instance

	def create_proxy(self):
		return self.add_proxy(self.init_params[0], self.init_params[1])

	def add_proxy(self, config_obj: Configuration, config_id: str):
		"""assign a name(ID) for every config"""
		if not isinstance(config_obj, Configuration):
			raise ValueError('config_obj must be a Configuration object.')
		self.__configs[config_id] = config_obj

	def write(self, config_id, keys, config_obj, is_overwrite=False):
		return self.__configs[config_id].write(keys, config_obj, is_overwrite=is_overwrite)

	def read(self, config_id, config_key):
		return self.__configs[config_id].read(config_key)

	def __getitem__(self, item):
		return self.__configs[item]

	def get_root_node(self, config_id):
		if config_id not in self.__configs.keys():
			return None
		return self.__configs[config_id].get_root()

	def set_root_node(self, config_id, root):
		return self.__configs[config_id].set_root(root)


