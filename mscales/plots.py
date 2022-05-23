import matplotlib.pyplot as plt
import numpy as np


def plot_barcode(s, save=False):
    """
    Bar plot of a scale.

    Parameters
    ----------
    s : np.array
        Numpy array of ones and zeroes.
    """

    _, ax = plt.subplots()
    ax.bar(np.arange(s.shape[0]), s, color="k")
    ax.set(xlabel="Pitch class", yticks=[], ylim=(0, 1))

    if save:
        plt.savefig(save)
    plt.show()


def plot_polar(s, save=False):
    c = s.shape[0]

    # figure and axis settings
    _, ax = plt.subplots(subplot_kw={"projection": "polar", "clip_on": False})
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    plt.thetagrids(np.linspace(0, 360, c, endpoint=False), np.arange(c))

    # data
    thetas = [k / c * 2 * np.pi for k in np.argwhere(s > 0)]
    radii = np.ones(len(thetas))

    stems = ax.stem(thetas, radii, linefmt="k", markerfmt="ok")
    for st in stems:
        st.set_clip_on(False)
    plt.setp(stems, "linewidth", 3)
    plt.setp(stems[0], "markersize", 10)

    if save:
        plt.savefig(save)
    plt.show()
