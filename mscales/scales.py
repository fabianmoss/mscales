import numpy as np
import pandas as pd
from itertools import product


def generate_scales(c=2):
    """
    Generate all scales (binary vectors) for a given chromatic cardinality `c`.

    Parameters
    ----------
    c : int, optional
        chromatic cardinality, by default 2

    Returns
    -------
    pd.DataFrame
        DataFrame containing all scales.
    """

    a = np.asarray(list(product([0, 1], repeat=c)))
    df = pd.DataFrame(a)

    return df
