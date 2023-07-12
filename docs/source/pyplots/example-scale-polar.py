from mscales import Scales
from mscales.plots import plot_polar

scales = Scales(c=12, d=7).all()
scale = scales[500]

plot_polar(scale)
