import numpy as np
from itertools import product
from mscales import PitchClassSet, PitchClass


all_pcs = np.asarray(list(product([0, 1], repeat=12)))


def vec2set(v):
    """Transforms a binary pc vector to a pc set."""
    return set(np.flatnonzero(v))


n = 50
b = all_pcs[n, :]
s = vec2set(b)
s = {4, 8, 0}
S = PitchClassSet(s)
# print(b)
# print(S.normal_form())

print(PitchClass(3) == PitchClass(15))
