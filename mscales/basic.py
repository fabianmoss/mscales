import numpy as np
from itertools import combinations
from collections.abc import Iterable
import matplotlib.pyplot as plt


class PitchClass:
    """
    Basic pitch-class representation as integers.
    """

    def __init__(self, p, c: int = 12):
        self.c = c
        self.p = p % self.c

    def __repr__(self):
        return f"PitchClass({self.p})"

    def __str__(self):
        return str(self.p)

    def __neg__(self):
        return -self.p % self.c

    def __add__(self, other):
        if isinstance(other, PitchClassInterval):
            return PitchClass((self.p + other.i) % self.c)
        else:
            raise TypeError(f"Can't add type {type(other)} to pitch class {self.p}.")

    def __sub__(self, other):
        if isinstance(other, PitchClassInterval):
            return PitchClass((self.p - other.i) % self.c)
        else:
            raise TypeError(f"Can't subtract type {type(other)} from pitch class {self.p}.")

    def __eq__(self, other):
        return self.p == other.p


class PitchClassInterval:
    """
    Interval between two pitch classes.
    """

    def __init__(self, i: int, c: int = 12):
        self.c = c
        self.i = i

    def __repr__(self):
        return f"PitchClassInterval({self.i})"

    def __str__(self):
        return str(self.i)

    def __add__(self, other):
        if isinstance(other, PitchClassInterval):
            return PitchClassInterval((self.i + other.i) % self.c)
        elif isinstance(other, PitchClass):
            return PitchClass((self.i + other.p) % self.c)
        else:
            raise TypeError(f"Can't add type {type(other)} to interval {self.i}.")

    def __sub__(self, other):
        if isinstance(other, PitchClassInterval):
            return self.i - other.i % self.c
        else:
            raise TypeError(f"Can't subtract type {type(other)} from interval {self.i}.")

    def __eq__(self, other):
        return self.i == other.i


class PitchClassSet:
    """
    Set of pitch classes.
    """

    def __init__(self, pcset, c: int = 12):
        self.c = c
        self.d = len(pcset)

        if isinstance(pcset, str):
            assert all(
                x in [str(i) for i in range(10)] + ["T"] + ["E"] for x in list(pcset)
            ), "Some pitch classes are not valid."
            self.pcs = np.array([10 if p == "T" else 11 if p == "E" else int(p) for p in list(pcset)])
        elif isinstance(pcset, (Iterable, PitchClassSet)):
            self.pcs = np.array([int(p) for p in pcset])
        else:
            raise TypeError(f"I don't recognize the pitch-class input {type(pcset)}.")

    def __repr__(self):
        return f"PitchClassSet({self.pcs})"

    def __str__(self):
        return str(set(self.pcs))

    def __len__(self):
        return len(self.pcs)

    def __eq__(self, other) -> bool:
        if isinstance(other, PitchClassSet):
            return np.array_equal(self.pcs, other.pcs)

    def sort(self):
        return PitchClassSet(np.sort(self.pcs))

    def to_vector(self):
        v = np.zeros(self.c, dtype=int)
        v[self.pcs] += 1
        return v

    def transpose(self, n: int):
        return PitchClassSet((self.pcs + n) % self.c)

    def invert(self, n: int = 0):
        return PitchClassSet((n - self.pcs) % self.c)

    def complement(self):
        return PitchClassSet(np.setdiff1d(np.arange(self.c), self.pcs))

    def normal_form(self):
        """
        Bring pitch-class set in normal form according to description at:
        https://musictheory.pugetsound.edu/mt21c/NormalForm.html
        """

        self = self.sort()

        if len(self.pcs) == 0:
            raise "PitchClassSet is empty!"
        elif len(self.pcs) == 1:
            return self
        else:
            rotations = np.array([np.roll(self.pcs, i) for i in range(self.pcs.shape[0])])
            for length in range(self.d - 1, 0, -1):
                spans = [(r[-1] - r[0]) % self.c for r in rotations[:, : length + 1]]
                mask = spans == min(spans)
                min_span_rotations = rotations[mask]

                # if there is a tie in the first step and we want to obtain all candidates
                # if there is only one candidate left
                if min_span_rotations.shape[0] == 1:
                    return PitchClassSet(min_span_rotations.flatten())
                # (if there are more than one)
                elif min_span_rotations.shape[0] > 1:  # (length == self.d - 1) and
                    rotations = min_span_rotations
                else:
                    raise "Something went wrong!"

                # if there is an absolute tie, chose the one with smaller first element
            if min_span_rotations.shape[0] > 1:
                min_idx = np.argmin(min_span_rotations, axis=0)[0]
                return PitchClassSet(min_span_rotations[min_idx])

    def prime_form(self):
        """Prime form of the pitch-class set, after Rahn.
        See also: https://ianring.com/musictheory/scales/#primeform
        """

        if len(self.pcs) == 0:
            return "PitchClassSet is empty!"
        elif len(self.pcs) == 1:
            # TODO: transoposition should know whether it operates
            # on Pitches, PitchSets, or PitchClass sets, and take the modulo
            # from the Class
            return self.transpose(-self.pcs[0] % self.c)

        normal = self.normal_form()
        transposed = normal.transpose(-normal.pcs[0])
        candidate1 = transposed

        inverted = transposed.invert()
        sorted = inverted.sort()

        candidate2 = sorted.normal_form().transpose(-sorted.normal_form().pcs[0])

        try:
            if np.less_equal(candidate1.pcs, candidate2.pcs).all():
                return candidate1
            elif np.less_equal(candidate2.pcs, candidate1.pcs).all():
                return candidate2
        except Exception as e:
            return e

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
        intervals = [(b - a) % self.c for a, b in list(combinations(self.pcs, r=2))]
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

    def plot(self, kind="lollipop", save=False):

        if kind == "lollipop":
            # c = s.shape[0]

            # figure and axis settings
            _, ax = plt.subplots(subplot_kw={"projection": "polar", "clip_on": False})
            ax.set_theta_direction(-1)
            ax.set_theta_zero_location("N")
            ax.set_yticklabels([])
            ax.set_ylim(0, 1)
            plt.thetagrids(np.linspace(0, 360, self.c, endpoint=False), np.arange(self.c))

            # data
            thetas = [k / self.c * 2 * np.pi for k in np.flatnonzero(self.to_vector())]
            radii = np.ones(len(thetas))

            stems = ax.stem(thetas, radii, linefmt="k", markerfmt="ok")
            for st in stems:
                st.set_clip_on(False)
            plt.setp(stems, "linewidth", 3)
            plt.setp(stems[0], "markersize", 10)
        if kind == "area":
            # c = s.shape[0]

            # figure and axis settings
            _, ax = plt.subplots(subplot_kw={"projection": "polar", "clip_on": False})
            ax.set_theta_direction(-1)
            ax.set_theta_zero_location("N")
            ax.set_yticklabels([])
            ax.set_ylim(0, 1)
            plt.thetagrids(np.linspace(0, 360, self.c, endpoint=False), np.arange(self.c))

            # data
            thetas = [k / self.c * 2 * np.pi for k in np.flatnonzero(self.to_vector())]
            radii = [1 for _ in range(len(thetas))]

            thetas += thetas[:1]
            radii += radii[:1]

            ax.plot(thetas, radii, c="k", zorder=5)
            ax.fill(thetas, radii, alpha=0.75, zorder=4)

        elif kind == "bar":
            _, ax = plt.subplots()
            ax.bar(np.arange(self.c), self.to_vector(), color="k")
            ax.set(xlabel="Pitch class", yticks=[], ylim=(0, 1))

        else:
            print("I don't recognize the plot kind." "Valid values are 'polar' and 'bar'.")

        if save:
            plt.savefig(save)
        plt.show()

    def info(self):
        print("=" * len(repr(self)))
        print(repr(self))
        print("=" * len(repr(self)))
        print()
        print("Set Theory")
        print("==========")
        print("cardin. (d, c)\t:", self.d, self.c)
        print("pc vector\t:", self.to_vector())
        print("complement\t:", self.complement())
        print("transposed\t:", self.transpose(2))
        print("inverted\t:", self.invert())
        print("T2I\t\t:", self.invert(2))
        print("normal form\t:", self.normal_form())
        print("prime form\t:", self.prime_form())
        print("interval vector\t:", self.interval_vector())
        print()
        print("Serialism")
        print("=========")
        print("original\t:", self)
        print("retrograde\t:", self.retrograde())
        print("inversion\t:", self.inversion())
        print("retro.-inv.\t:", self.inversion().retrograde())
        print("matrix\t\t:", str(self.matrix()).replace("\n", "\n\t\t"))


if __name__ == "__main__":

    # test cases from https://musictheory.pugetsound.edu/mt21c/PrimeForm.html
    s = {3, 11, 2}
    s = {8, 0, 9}
    s = "123E"
    s = "17TE"
    s = "941"
    # s = {11,2,3,7,2}
    # s = {2,3,8,9}
    # s = {0, 2, 4}
    # s = {0, 1, 4, 6}  # all-interval tetrachord
    # s = {1,5,6,7} # from Straus, p. 58
    # s = {0, 2, 4, 5, 7, 9, 11}
    # s = {0,1,2}
    # s = {6,9,2}
    # s = {7, 10, 1, 5}
    # s = [0, 1, 6, 7, 5, 2, 4, 3, 10, 9, 11, 8]  # 12-tone row

    pcset = PitchClassSet(s)
    pcset.info()

    print(pcset)
