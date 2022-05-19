import numpy as np


class PitchClassSet:
    def __init__(self, pcset, c: int = 12):
        self.c = c

        if isinstance(pcset, set):
            self.pcs = np.array(list({p % self.c for p in pcset}))
        elif isinstance(pcset, list):
            self.pcs = np.array(pcset)
        elif isinstance(pcset, np.ndarray):
            self.pcs = pcset
        else:
            raise TypeError("I don't recognize the pitch-class input.")

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

    def most_compact(self, arr):
        for i in range(arr.shape[1] - 1, 0, -1):
            min_diff = min([(r[i] - r[0]) % self.c for r in arr])
            mask = (arr[:, i] - arr[:, 0]) % self.c == min_diff

            if np.array_equal(arr, arr[mask]):
                return PitchClassSet(arr[0, :])
            elif arr.shape[0] > 1:
                arr = arr[mask]
                pass
            else:
                return PitchClassSet(arr.flatten())

    def prime_form(self):

        t = self.normal_form()
        t = t.transpose(-t.pcs[0])

        i = t.invert().normal_form()
        i = i.transpose(-i.pcs[0])

        return t.pcs, i.pcs

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
        print("pc set\t:", pcset.pcs)
        print("compl.\t:", pcset.complement().pcs)
        print("transp.\t:", pcset.transpose(2).pcs)
        print("inv.\t:", pcset.invert().pcs)
        print("T2I\t:", pcset.invert(2).pcs)
        print("NF\t:", pcset.normal_form().pcs)
        print("PF\t:", pcset.prime_form())


if __name__ == "__main__":

    s = {3, 11, 2}
    # s = {8,0,9}
    # s = {0,2,4,5,7,9,11}
    pcset = PitchClassSet(s)
    pcset.info()
