import numpy as np
from typing import Tuple


class VectorLowDim:
    dim = None

    def __init__(self, data):
        """
        """
        if isinstance(data, (list, tuple)):
            data = np.array(data)
        elif isinstance(data, VectorLowDim):
            data = np.array(data.data())
        self._data = data

    def to_tuple(self):
        return tuple(self._data.tolist())

    def data(self):
        return self._data

    @property
    def d(self):
        return self.data()


class CartesianDiscretization:
    def __init__(self, shape: Tuple[int], cell_shape: Tuple[float], origin: Tuple[float]):
        pass

    def shape(self) -> Tuple[int]:
        pass

    def origin(self) -> VectorLowDim:
        pass

    def cell_shape(self) -> VectorLowDim:
        pass

    def limits(self) -> Tuple[VectorLowDim]:
        pass


def sample_to_cartessian(points: np.ndarray, cartesian):
    """
    """
    pass
