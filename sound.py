import numpy as np
from numpy.random import default_rng

# Use the tones library to synthesize scales: https://pypi.org/project/tones/
from tones import SINE_WAVE, SAWTOOTH_WAVE, SQUARE_WAVE
from tones.mixer import Mixer


rng = default_rng()

# Specific pitch-class spellings
NOTES = ["c", "c#", "d", "eb", "e", "f", "f#", "g", "ab", "a", "bb", "b"]


def pc2note(pc):
    """Converts a pitch class to a spelled note name.

    Parameters
    ----------
    pc : int
        Pitch class (integer between 0 and 11, inclusively)

    Returns
    -------
    str
        Note name (spelling) of pitch class
    """

    assert pc in range(0, 12)

    d = {p: n for p, n in zip(np.arange(12), NOTES)}

    return d[pc]


def scale2notelist(s):
    """Converts a scale to a list of pitch classes.

    Parameters
    ----------
    s : np.array
        Scale with non-negative entries

    Returns
    -------
    list
        List of note names
    """

    assert s.shape[0] == 12

    pcs = np.nonzero(s)

    return [pc2note(pc) for pc in pcs]


def tone_cloud(
    note_list,
    tracks=1,
    n_samples=100,
    duration=0.15,
    waveform=SINE_WAVE,
    sample_rate=44100,
    amplitude=0.5,
    attack=0.01,
    decay=0.1,
    save_as=None,
):
    """Generate a tone cloud from a note list (specific spellings of pitch classes).
    NOTE: Currently only works with 12-tet vectors because the `tones` libray only accepts Western note names.

    Parameters
    ----------
    pc_list : list
        List of pitch classes (e.g. ["g", "a", "b", "c", "d", "e", "f#"] for the G-major scale)
    tracks : int, optional
        Number of tracks that play simultaneously, by default 1
    n_samples : int, optional
        Number of samples, by default 100
    duration : float, optional
        Duration of each sample in seconds, by default .15
    waveform:
        Waveform from `tones` library, by detault `SINE_WAVE`
    sample_rate : int, optional
        Sample rate, by default 44100
    amplitude : float, optional
        Amplitude, by default .5
    attack : float, optional
        Attack, by default 0.01
    decay : float, optional
        Decay, by default 0.1
    save_as : str, optional
        File path to save the wave file, by default None

    Returns
    -------
    _type_
        _description_
    """

    # initialize mixer
    mixer = Mixer(sample_rate, amplitude)

    # add tracks
    for i in range(tracks):
        mixer.create_track(i, waveform=waveform, attack=attack, decay=decay)

        assert waveform in [SINE_WAVE, SQUARE_WAVE, SAWTOOTH_WAVE]

        # sample tones from list and add to mixer
        tones = [np.random.choice(note_list) for _ in range(n_samples)]
        for t in tones:
            if duration == "random":
                mixer.add_note(
                    i, note=t, octave=np.random.randint(3, 6), duration=rng.exponential(scale=0.25) + 0.0001
                )
            else:
                mixer.add_note(i, note=t, octave=np.random.randint(3, 6), duration=duration)

    # create samples
    samples = mixer.mix()

    # save
    if save_as is not None:
        mixer.write_wav(save_as)

    # return samples
    return samples  # ipd.Audio(samples, rate=sample_rate)
