import numpy as np
from numpy.random import default_rng
import pretty_midi as pm
from mscales.scales import Scale


rng = default_rng(123)


def tone_cloud(
    scale: Scale,
    n_notes: int = 100,
    note_duration: float = 0.15,
    velocity: int = 100,
    instrument_name: str = "Acoustic Grand Piano",
    save_as: str = None,
    shepard=True,
    octave_range: list[int] = [4, 7],
) -> pm.PrettyMIDI:
    """Generate a tone cloud from an input scale.

    Returns
    -------
    pretty_midi.PrettyMidi()
        Returns a PrettyMidi() object.
    """
    starts = np.arange(n_notes) * note_duration  # onsets
    ends = starts + note_duration  # offsets

    # binary = "".join([str(x) for x in scale])

    pitches = [x for x in rng.choice(np.nonzero(scale)[0], size=n_notes)]

    if shepard:
        seq = []
        for p in pitches:
            freq = pitch2freq(p)
            Fs = 44100
            s, t = generate_shepard_tone(freq=freq, dur=note_duration, Fs=Fs, amp=0.5)
            seq = np.concatenate((seq, s))

            return seq

    else:

        octaves = rng.choice(np.arange(*octave_range), size=n_notes)
        midi_pitches = [(p + 12 * o) for p, o in list(zip(pitches, octaves))]

        # Create a PrettyMIDI object
        midi = pm.PrettyMIDI()

        # Create an Instrument instance for an instrument
        assert (
            instrument_name in pm.constants.INSTRUMENT_MAP
        ), f"Instrument must be in {pm.constants.INSTRUMENT_MAP}"

        program = pm.instrument_name_to_program(instrument_name)
        instrument = pm.Instrument(program=program)

        for mp, s, e in zip(midi_pitches, starts, ends):
            # Create a Note instance for this note, starting at `s` and ending at `e`.
            note = pm.Note(pitch=mp, velocity=velocity, start=s, end=e)
            # Add it to instrument
            instrument.notes.append(note)

        # Add the instrument to the PrettyMIDI object
        midi.instruments.append(instrument)

        if save_as is not None:
            midi.write(save_as)

        return midi


def generate_shepard_tone(freq=440, dur=0.5, Fs=44100, amp=1):
    """Generate Shepard tone

    Adapted from: https://www.audiolabs-erlangen.de/resources/MIR/FMP/C1/C1S1_ChromaShepard.html

    Notebook: C1/C1S1_ChromaShepard.ipynb

    Args:
        freq (float): Frequency of Shepard tone (Default value = 440)
        dur (float): Duration (in seconds) (Default value = 0.5)
        Fs (scalar): Sampling rate (Default value = 44100)
        amp (float): Amplitude of generated signal (Default value = 1)

    Returns:
        x (np.ndarray): Shepard tone
        t (np.ndarray): Time axis (in seconds)
    """

    N = int(dur * Fs)
    t = np.arange(N) / Fs
    num_sin = 1
    x = np.sin(2 * np.pi * freq * t)
    freq_lower = freq / 2
    while freq_lower > 20:
        num_sin += 1
        x = x + np.sin(2 * np.pi * freq_lower * t)
        freq_lower = freq_lower / 2
    freq_upper = freq * 2
    while freq_upper < 20_000:
        num_sin += 1
        x = x + np.sin(2 * np.pi * freq_upper * t)
        freq_upper = freq_upper * 2
    x = x / num_sin
    x = amp * x / np.max(x)
    return x, t


def pitch2freq(p):
    F_A4 = 440
    return F_A4 * 2 ** ((p - 69) / 12)


# Fs = 44100
# dur = 0.5

# pitch_start = 48
# pitch_end = 72
# scale = []
# for p in range(pitch_start, pitch_end + 1):
#     freq = f_pitch(p)
#     s, t = generate_shepard_tone(freq=freq, dur=dur, Fs=Fs, amp = 0.5)
#     scale = np.concatenate((scale, s))

# ipd.display(ipd.Audio(scale, rate=Fs))
