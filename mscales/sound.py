import numpy as np
from numpy.random import default_rng
import pretty_midi as pm


rng = default_rng(123)


def tone_cloud(
    scale,
    n_notes: int = 100,
    note_duration: float = 0.15,
    velocity: int = 100,
    instrument_name: str = "Acoustic Grand Piano",
    save_as: str = None,
):
    starts = np.arange(n_notes) * note_duration  # onsets
    ends = starts + note_duration  # offsets

    # binary = "".join([str(x) for x in scale])

    pitches = [x for x in rng.choice(np.nonzero(scale)[0], size=n_notes)]
    octaves = rng.choice(np.arange(3, 7), size=n_notes)
    midi_pitches = [(p + 12 * o) for p, o in list(zip(pitches, octaves))]

    # Create a PrettyMIDI object
    midi = pm.PrettyMIDI()

    # Create an Instrument instance for an instrument
    assert instrument_name in pm.constants.INSTRUMENT_MAP, f"Instrument must be in {pm.constants.INSTRUMENT_MAP}"
    # instrument_code = pm.constants.INSTRUMENT_MAP.index(instrument_name)

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
        # filename = f'mid_i{instrument_code}_p{binary}_d{int(note_duration * 1000)}.mid'
        midi.write(save_as)
    else:
        return midi
