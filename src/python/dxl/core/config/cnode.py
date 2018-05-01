from typing import Dict


class QueryKey:
    def __init__(self, keys):
        """
        `key`: All possible value which is converatble to key.
        """
        if not isinstance(keys, (list, tuple)):
            raise TypeError(
                "Expected keys to be list or tuple, got {}.".format(keys))
        self._keys = keys

    def head(self):
        return self._keys[0]

    def tail(self):
        return QueryKey(self._keys[1:])

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
        if len(key) == 1:
            return self._values.get(key.head())
        else:
            if not key.head() in self._children:
                return None
            return self._children.get(key.head()).read(key.tail())

    def children(self):
        return self._children

    def values(self):
        return self._values

    def __getitem__(self, key):
        if key in self._children:
            return self._children[key]
        elif key in self._values:
            return self._values[key]
        else:
            raise KeyError(key)

    def __iter__(self):
        return iter(list(self._children.keys()) + list(self._values.keys()))

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
        if len(key) == 1:
            self.assign(key.head(), node_or_value, allow_existed=False)
        else:
            if key.head() in self:
                raise ValueError("Key {} alread existed.".format(key.head()))
            c = CNode()
            c.create(key.tail(), node_or_value)
            self._children[key.head()] = c

    # def update(self, key:QueryKey, node_or_value):
    #     if len(key) == 1:
    #         self.assign(key.head())
    #     else:
    #         self._children[key.head()].update(key.tail(), node)
