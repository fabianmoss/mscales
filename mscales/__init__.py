from ._version import get_versions
from .scales import Scales  # pyflakes.ignore
from .pcsets import PitchClassSet  # pyflakes.ignore

__version__ = get_versions()["version"]
del get_versions
