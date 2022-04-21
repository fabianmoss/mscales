import numpy as np
from itertools import product, combinations
from collections import Counter


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

        self.n_scales = scales.shape[0]

        return scales

    def pitch_classes(self):
        """
        Pitch-class representation for all scales.

        Returns
        -------
        list
            List of numpy arrays containing pitch classes
        """

        return [np.flatnonzero(row) for row in self.all()]

    def interval_vectors(self):
        """
        Interval vectors for all scales.

        Returns
        -------
        list
            List of Counters, representing all intervals mod 12.
        """

        return [Counter([(y - x) % 12 for (x, y) in combinations(pc, r=2)]) for pc in self.pitch_classes()]


# TODO: interval CLASS vectors (only from 0 to 6)
