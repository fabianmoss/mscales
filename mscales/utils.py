import numpy as np
from math import gcd


def G(c: int, d: int, g: int) -> np.ndarray:
    """
    Generate scale with size d in chromatic universe of cardinality c.
    Generator size is g specific (chromatic) steps.
    Notation G(c, d, g) after Wooldridge (1992) and Clough et al. (1999).

    Parameters
    ----------
    c : int
        chromatic cardinality
    d : int
        diatonic cardinality
    g : int
        generator size
    """
    specific_steps = np.array(sorted(list(set([(g * x) % c for x in range(d)]))))

    g = np.zeros(c, dtype=int)
    g[specific_steps] += 1

    return g


# test for given scale whether generated


def is_G(s: np.ndarray) -> bool:
    # TODO: does not work for transpositions!
    """
    Tests whether scale is generated.

    Parameters
    ----------
    s : np.ndarray
        Scale

    Returns
    -------
    bool
        Truth value
    """

    c = s.shape[0]
    d = int(s.sum())
    specific_steps = pcset(s)

    g = invmod(specific_steps, c)

    return np.array_equal(G(c, d, g), s)


def invmod(arr, c):
    gcd_ = gcd(*arr, c)
    if gcd_ != 1:
        return gcd_
    else:
        for g in range(2, c + 1):
            for i in arr:
                if (i % c) * (g % c) % c == 1:
                    return g
        raise Exception("The modular inverse does not exist.")


def is_DE(s: np.ndarray) -> bool:
    """Each generic interval comes in either one or two specific sizes."""

    arr = pcset(s)
    diff = np.abs(arr[:-1] - arr[1:])

    return 1 <= len(set(diff)) <= 2


def J(k: int, c: int, d: int, m: int) -> int:
    """
    J function after Clough & Douthett (1991)

    Parameters
    ----------
    k : int
        _description_
    c : int
        _description_
    d : int
        _description_
    m : int
        _description_

    Returns
    -------
    int
        _description_
    """
    return np.floor((c * k + m) / d).astype(int)


def transpose(s: np.ndarray, i: int) -> np.ndarray:
    """Transposition.

    Parameters
    ----------
    s : np.ndarray
        scale
    i : int
        interval

    Returns
    -------
    np.ndarray
        transposed scale
    """
    return np.roll(s, i)


def invert(s: np.ndarray, i: int = 0, c: int = 12) -> np.ndarray:
    """Inversion.

    Parameters
    ----------
    s : np.ndarray
        scale
    i : int, optional
        interval, by default 0
    c : int, optional
        chromatic cardinality, by default 12

    Returns
    -------
    np.ndarray
        _description_
    """
    return binary((i - pcset(s)) % c, c=c)


def pcset(s: np.ndarray) -> np.ndarray:
    return np.argwhere(s > 0).flatten()


def binary(pcset: np.ndarray, c: int) -> np.ndarray:
    """
    Converts a pc set to a binary vector representing the scale.

    Parameters
    ----------
    pcset : np.ndarray
        _description_
    c : int
        _description_

    Returns
    -------
    np.ndarray
        _description_
    """
    z = np.zeros(c).astype(int)
    z[pcset] += 1
    return z


print(transpose(1, 2))
