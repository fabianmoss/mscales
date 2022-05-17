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


def plot_polar(s, save=False):

    _, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2.0)
    # ax.set_xticks(np.arange(s.shape[0]))
    # ax.set_xticklabels(np.arange(s.shape[0]))
    # ax.set_xticks(np.linspace(0, 2* np.pi* 12, 12, endpoint=False))
    lines, labels = plt.thetagrids(np.linspace(0, 360, 12, endpoint=False), np.arange(12))

    for i, k in enumerate(s):
        ax.plot([0, i], [0, k], marker="o", c="k", markersize=8)

    if save:
        plt.savefig(save)
    plt.show()
