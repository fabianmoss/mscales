from ._version import get_versions
from .scales import Scales
from .pcsets import PitchClassSet

__version__ = get_versions()["version"]
del get_versions
