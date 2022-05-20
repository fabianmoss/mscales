import numpy as np

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
            self.pcs = np.array([p for p in pcset])
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
        s = sorted(self.pcs)
        rotations = np.asarray([s[i : len(s)] + s[0:i] for i in range(len(s))])

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
        raise NotImplementedError

    def sum(self) -> int:
        return sum(self.pcs)

    def info(self):
        print("=" * len(repr(pcset)))
        print(repr(pcset))
        print("=" * len(repr(pcset)))
        print("compl.\t:", pcset.complement())
        print("transp.\t:", pcset.transpose(2))
        print("inv.\t:", pcset.invert())
        print("T2I\t:", pcset.invert(2))
        print("NF\t:", pcset.normal_form())
        print("PF\t:", pcset.prime_form())


if __name__ == "__main__":

    # test cases from https://musictheory.pugetsound.edu/mt21c/PrimeForm.html
    s = {3, 11, 2}
    # s = {11,2,3,7}
    # s = {8,0,9}
    s = {0, 2, 4, 5, 7, 9, 11}
    pcset = PitchClassSet(s)

    pcset.info()
