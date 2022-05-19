import numpy as np


class PitchClassSet:
    def __init__(self, pcset: set = {}, c: int = 12):

        self.c = c
        self.pcset = {p % self.c for p in pcset}

    def sum(self) -> int:
        return sum(self.pcset)

    def transpose(self, n: int) -> set:
        return {(p + n) % self.c for p in self.pcset}

    def invert(self, n: int = 0) -> set:
        return {(n - p) % self.c for p in self.pcset}

    def complement(self) -> set:
        return {p for p in range(self.c)}.difference(self.pcset)

    def normal_form(self):

        s = sorted(self.pcset)

        rotations = np.asarray([s[i : len(s)] + s[0:i] for i in range(len(s))])

        for i in range(rotations.shape[1] - 1, 0, -1):
            min_diff = min([(r[i] - r[0]) % self.c for r in rotations])
            mask = (rotations[:, i] - rotations[:, 0]) % self.c == min_diff

            if np.array_equal(rotations, rotations[mask]):
                return rotations[0, :]
            elif rotations.shape[0] > 1:
                rotations = rotations[mask]
                pass
            else:
                return rotations.flatten()

    def prime_form(self):
        # can't use `self.transpose` and `self.invert` here, because it operates on sets
        # but `self.normal_form`` returns array. Those functions need to be updated to work
        # on arrays as well.

        normal = self.normal_form()
        normal -= normal[0] % self.c

        normal_inverted = -normal % self.c
        normal_inverted -= normal_inverted[0] % self.c

        return self.normal_form()

        if sum(normal) < sum(normal_inverted):
            prime = np.sort(normal % self.c)
        else:
            prime = np.sort(normal_inverted % self.c)

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

        return tuple(prime)

    def interval_vector(self):
        raise NotImplementedError

    def info(self):
        print("pc set\t:", pcset.pcset)
        print("compl.\t:", pcset.complement())
        print("sum\t:", pcset.sum())
        print("transp.\t:", pcset.transpose(2))
        print("inv.\t:", pcset.invert())
        print("T2I\t:", pcset.invert(2))
        print("NF\t:", pcset.normal_form())


#        print("PF\t:", pcset.prime_form())


if __name__ == "__main__":

    s = {2, 3, 11}
    # s = {2,3,8,9}
    pcset = PitchClassSet(s)
    pcset.info()
