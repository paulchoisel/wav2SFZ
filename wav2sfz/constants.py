from enum import Enum

MIDI_MAX_NOTES = 128
SEMI_TONES_NUMBER = 12
SECONDS_PER_MINUTE = 60


class Pitches(Enum):

    C = "c"
    Cs = "c#"
    D = "d"
    Ds = "d#"
    E = "e"
    F = "f"
    Fs = "f#"
    G = "g"
    Gs = "g#"
    A = "a"
    As = "a#"
    B = "b"
