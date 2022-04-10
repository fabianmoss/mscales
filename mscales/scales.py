import numpy as np
from itertools import product


class Scales:
    """The base class for all scales."""

    def __init__(self, cardinality):
        self.cardinality = cardinality

    def all(self):
        """
        Return all scales (binary vectors) for a given chromatic cardinality `c`.

        Parameters
        ----------
        c : int, optional
            chromatic cardinality, by default 2

        Returns
        -------
        numpy.array
            Numpy array containing all scales.
        """

        scales = np.asarray(list(product([0, 1], repeat=self.cardinality)))

        return scales
