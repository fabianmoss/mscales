import numpy as np
from numpy.random import default_rng

# Use the tones library to synthesize scales: https://pypi.org/project/tones/
from tones import SINE_WAVE, SAWTOOTH_WAVE, SQUARE_WAVE
from tones.mixer import Mixer


rng = default_rng()

# Specific pitch-class spellings
NOTES = ["c", "c#", "d", "eb", "e", "f", "f#", "g", "ab", "a", "bb", "b"]

wave_dict = {"SINE_WAVE": SINE_WAVE, "SAWTOOTH_WAVE": SAWTOOTH_WAVE, "SQUARE_WAVE": SQUARE_WAVE}


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

    (pcs,) = np.nonzero(s)

    return [pc2note(pc) for pc in pcs]


def tone_cloud(
    scale,
    tracks=1,
    duration=10,
    rate=5,
    waveform="SINE_WAVE",
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
    scale : numpy.array
        Binary numpy array
    tracks : int, optional
        Number of tracks that play simultaneously, by default 1
    duration : float, optional
        Duration of the synthesized tone cloud in seconds, by default 10
    rate : int, optional
        Tones per second, by default 5
    waveform: str, optional
        Waveform from `tones` library (one of `SINE_WAVE`, `SQUARE_WAVE`, `SAWTOOTH_WAVE`), by detault `SINE_WAVE`
    sample_rate : int, optional
        Sample rate, by default 44100
        NOTE: This is the sample rate for the audio to be synthesizes, _not_ the
        sampling rate for the tone cloud
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
    tones.tone.Sample
        Array of samples
    """

    assert wave_dict[waveform] in [SINE_WAVE, SQUARE_WAVE, SAWTOOTH_WAVE]

    note_list = scale2notelist(scale)

    # initialize mixer
    mixer = Mixer(sample_rate, amplitude)

    # add tracks
    for i in range(tracks):
        mixer.create_track(i, wave_dict[waveform], attack=attack, decay=decay)

        # sample tones from list and add to mixer
        tones = [np.random.choice(note_list) for _ in range(duration * rate)]
        for t in tones:
            # TODO: add non-uniform durations
            # if duration == "random":
            #     mixer.add_note(
            #         i, note=t, octave=np.random.randint(3, 6), duration=rng.exponential(scale=0.25) + 0.0001
            #     )
            mixer.add_note(i, note=t, octave=np.random.randint(3, 6), duration=1 / rate)

    # create samples
    samples = mixer.mix()

    # save
    if save_as is not None:
        mixer.write_wav(save_as)

    # return samples
    return samples  # ipd.Audio(samples, rate=sample_rate)


# MINGUS TEST
# from mingus.containers import Note, NoteContainer
# from mingus.midi import fluidsynth
# from mingus.midi.midi_file_out import write_NoteContainer

# # sf = "/home/fmoss/Downloads/FluidR3_GM/FluidR3_GM.sf2"
# sf = "/home/fmoss/Downloads/nintendo_soundfont.sf2"  # from musical-artifacts.com
# fluidsynth.init(sf, "alsa")
# fluidsynth.set_instrument(1, 35, 0)

# if __name__ == "__main__":
#     m = Note("C#")
#     m.channel = 1
#     nc = NoteContainer(m)
#     write_NoteContainer("test.mid", nc)
