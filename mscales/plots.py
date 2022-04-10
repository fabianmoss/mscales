import matplotlib.pyplot as plt
import numpy as np


def plot_scale(s, save=False):
    """
    Bar plot of a scale.

    Parameters
    ----------
    s : np.array
        Numpy array of ones and zeroes.
    """

    _, ax = plt.subplots()
    ax.bar(np.arange(s.shape[0]), s)

    ax.set(xlabel="Pitch class", ylabel="Frequency")

    if save:
        plt.savefig(save)
    plt.show()
