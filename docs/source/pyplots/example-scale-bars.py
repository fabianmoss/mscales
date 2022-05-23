from mscales import Scales
from mscales.plots import plot_bars
import matplotlib.pyplot as plt

scales = Scales(c=12, d=7).all()
scale = scales[500]

plot_bars(scale)
plt.show()
