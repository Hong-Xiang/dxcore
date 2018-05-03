from typing import Dict
from enum import Enum


class QueryKey:
    def __init__(self, keys):
        """
        `key`: All possible value which is converatble to key.
        """
        if isinstance(keys, QueryKey):
            keys = keys._keys
        if isinstance(keys, str):
            keys = [keys]
        if not isinstance(keys, (list, tuple)):
            raise TypeError(
                "Expected keys to be list or tuple, got {}.".format(keys))
        self._keys = tuple(keys)

    def head(self):
        if len(self._keys) == 0:
            return None
        else:
            return self._keys[0]

    def tail(self):
        return QueryKey(self._keys[1:])

    def last(self):
        return QueryKey(tuple(self._keys[-1]))

    def __len__(self):
        return len(self._keys)


class CNode:
    def __init__(self, config=None):
        """
        `config`: initial configs, which should be a dict of CNode/value.
        """
        self._children = {}
        self._values = {}
        if config is None:
            config = {}
        for k, v in config.items():
            if isinstance(v, CNode):
                self._children[k] = v
            else:
                self._values[k] = v

    def read(self, key: QueryKey):
        """
        Find value curresponding to key.
        if len(key) == 1, then find it in self._values,
        else find it in self._children recuresivly.
        """
        key = QueryKey(key)
        if len(key) == 0:
            return self
        elif len(key) == 1:
            if key.head() in self._values:
                return self._values.get(key.head())
            else:
                return self._children.get(key.head())
        else:
            if not key.head() in self._children:
                return None
            return self._children.get(key.head()).read(key.tail())

    @property
    def children(self):
        return self._children

    @property
    def values(self):
        return self._values

    def get_kernel(self, key):
        if key in self._children:
            return self._children[key], True
        elif key in self._values:
            return self._values[key], True
        return None, False

    def __getitem__(self, key):
        v, f = self.get_kernel(key)
        if not f:
            raise KeyError(key)
        return v

    def get(self, key: str, value=None):
        v, f = self.get_kernel(key)
        if f:
            return v
        return value

    def __iter__(self):
        return iter(list(self._children.keys()) + list(self._values.keys()))

    def items(self):
        return tuple(list(self._children.items()) + list(self._values.items()))

    def keys(self):
        return tuple(list(self._children.keys()) + list(self._values.keys()))

    def assign(self, key: str, node_or_value, *, allow_existed=True):
        if isinstance(node_or_value, CNode):
            if not allow_existed and key in self._children:
                raise ValueError("Key {} alread existed.".format(key))
            if key in self._values:
                raise ValueError("Duplicated key {} in value.".format(key))
            self._children[key] = node_or_value
        else:
            if not allow_existed and key in self._values:
                raise ValueError("Key {} alread existed.".format(key))
            if key in self._children:
                raise ValueError("Duplicated key {} in children.".format(key))
            self._values[key] = node_or_value

    def create(self, key: QueryKey, node_or_value):
        """
        Create a new child node or value.
        """
        key = QueryKey(key)
        if len(key) == 0:
            raise ValueError("Can not create with empty key.")
        elif len(key) == 1:
            self.assign(key.head(), node_or_value, allow_existed=False)
        else:
            if key.head() in self:
                raise ValueError("Key {} alread existed.".format(key.head()))
            c = CNode()
            c.create(key.tail(), node_or_value)
            self._children[key.head()] = c

    def is_ancestor_of(self, n):
        for _, v in self._children.items():
            if v is n or v.is_ancestor_of(n):
                return True
        return False

    def update(self, key: QueryKey, node_or_value):
        """
        Updating config.
        If node_or_value is a value, update directly.
        If node_or_value is a CNode, check if this node exists.
            If not exists: direct assign.
            If exists: update each item of that node. 
        Note: the node_or_value argument is not assigned to the node tree.
        """
        key = QueryKey(key)
        if len(key) == 0:
            raise ValueError("Length of QueryKey can not be zero.")
        if len(key) > 1:
            if not key.head() in self._children:
                raise KeyError("Key {} not found.".format(key.head()))
            return self._children[key.head()].update(key.tail(), node_or_value)
        if not isinstance(node_or_value, CNode):
            self._values[key.head()] = node_or_value
            return self.assign(key.head(), node_or_value)
        self._children[key.head()].update(key.tail(), node)


class Keywords:
    EXPAND = '__expand__'


def from_dict(config_dict):
    def need_expand(v):
        if not isinstance(v, dict):
            return False
        if Keywords.EXPAND in v:
            return v[Keywords.EXPAND]
        return True

    config_parsed = {}
    for k, v in config_dict.items():
        if need_expand(v):
            config_parsed[k] = from_dict(v)
        else:
            config_parsed[k] = v
    return CNode(config_parsed)


class DefaultConfig:
    _current = None

    def __init__(self, cnode):
        pass

    @property
    def node(self):
        return self._current