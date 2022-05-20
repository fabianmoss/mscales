import numpy as np
from itertools import combinations

# class PitchClass:

#     def __init__(self, p, c: int = 12):
#         self.p = p % c

#     def __repr__(self):
#         return f"PitchClass({self.p})"

#     def __str__(self):
#         return str(self.p)

#     def __neg__(self):
#         return -self.p

# def __add__(self, other):
#     return self.p + other.i

# def __sub__(self, other):
#     return self.p - other.i

# def __lt__(self, other):
#     """Not always a good idea.
#     Maybe replace with ternary relation from Harasim et al. (2016)"""
#     return self.p < other.p

# class Interval:
#     def __init__(self, i, c: int = 12):
#         self.i = i % c

# def __add__(self, other):
#     return self.i + other.p

# def __sub__(self, other):
#     return self.i - other.p


class PitchClassSet:
    def __init__(self, pcset, c: int = 12):
        self.c = c

        if isinstance(pcset, (set, list, tuple, np.ndarray, PitchClassSet)):
            self.pcs = np.array([p for p in list(pcset)])
        else:
            raise TypeError(f"I don't recognize the pitch-class input {type(pcset)}.")

    def __repr__(self):
        return f"PitchClassSet({self.pcs})"

    def __str__(self):
        return str(self.pcs)

    def __len__(self):
        return len(self.pcs)

    def transpose(self, n: int):
        return PitchClassSet((self.pcs + n) % self.c)

    def invert(self, n: int = 0):
        return PitchClassSet((n - self.pcs) % self.c)

    def complement(self) -> set:
        return PitchClassSet(np.setdiff1d(np.arange(self.c), self.pcs))

    def normal_form(self):
        rotations = np.asarray([list(s)[i : len(s)] + list(s)[0:i] for i in range(len(s))])

        for i in range(rotations.shape[1] - 1, 0, -1):
            min_diff = min([(r[i] - r[0]) % self.c for r in rotations])
            mask = (rotations[:, i] - rotations[:, 0]) % self.c == min_diff

            if np.array_equal(rotations, rotations[mask]):
                return PitchClassSet(rotations[0, :])
            elif rotations.shape[0] > 1:
                rotations = rotations[mask]
                pass
            else:
                return PitchClassSet(rotations.flatten())

    def prime_form(self):

        t = self.normal_form()
        t = t.transpose(-t.pcs[0])

        i = t.invert().normal_form()
        i = i.transpose(-i.pcs[0])

        if np.array_equal(i.pcs, t.pcs):
            return t
        elif np.less_equal((t.pcs - i.pcs).all(), (i.pcs - t.pcs).all()):
            return i
        else:
            return t

        # The following special cases were taken from https://ianring.com/
        # TODO: Implement special cases!
        # // Special set classes:
        # // Forte  Prime form packed    Prime form packed
        # // name   from the right       to the left
        # // ----------------------------------------------
        # // 5-20      (01568)           (01378)
        # // 6-Z29     (023679)          (013689)
        # // 6-31      (014579)          (013589)
        # // 7-20      (0125679)         (0124789)
        # // 8-26      (0134578T)        (0124579T)

    def interval_vector(self):
        half = int(np.ceil(self.c / 2))
        intervals = [(b - a) % 12 for a, b in list(combinations(self.pcs, r=2))]
        interval_classes = [i if i <= half else self.c - i for i in intervals]

        iv = np.zeros(half, dtype=int)
        for i in interval_classes:
            iv[i - 1] += 1

        return iv

    def sum(self) -> int:
        return sum(self.pcs)

    def retrograde(self):
        return PitchClassSet(np.flip(self.pcs))

    def inversion(self):
        """This is different from `self.invert` !!"""
        return self.invert(self.pcs[0]).transpose(self.pcs[0])

    def matrix(self):
        return np.asarray([self.transpose(-i).pcs for i in self.pcs])

    def info(self):
        print("=" * len(repr(pcset)))
        print(repr(pcset))
        print("=" * len(repr(pcset)))
        print()
        print("Set Theory")
        print("==========")
        print("complement\t:", pcset.complement())
        print("transposed\t:", pcset.transpose(2))
        print("inverted\t:", pcset.invert())
        print("T2I\t\t:", pcset.invert(2))
        print("normal form\t:", pcset.normal_form())
        print("prime form\t:", pcset.prime_form())
        print("interval vector\t:", pcset.interval_vector())
        print()
        print("Serialism")
        print("=========")
        print("original\t:", pcset)
        print("retrograde\t:", pcset.retrograde())
        print("inversion\t:", pcset.inversion())
        print("retro.-inv.\t:", pcset.inversion().retrograde())
        print("matrix\t\t:", str(pcset.matrix()).replace("\n", "\n\t\t"))


if __name__ == "__main__":

    # test cases from https://musictheory.pugetsound.edu/mt21c/PrimeForm.html
    s = {3, 11, 2}
    # s = {11,2,3,7}
    # s = {8,0,9}
    s = {0, 2, 4, 5, 7, 9, 11}
    # s = {0,1,2}
    # s = {0,4,7}
    s = {7, 10, 1, 5}
    s = [0, 1, 6, 7, 5, 2, 4, 3, 10, 9, 11, 8]  # 12-tone row
    pcset = PitchClassSet(s)

    pcset.info()
