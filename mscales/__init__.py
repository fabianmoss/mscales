from ._version import get_versions
from .scales import Scales
from .pcsets import PitchClass, PitchClassInterval, PitchClassSet
from .plots import plot_barcode, plot_polar

__version__ = get_versions()["version"]
del get_versions
