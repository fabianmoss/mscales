.. Packaging Scientific Python documentation master file, created by
   sphinx-quickstart on Thu Jun 28 12:35:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mscales Quickstart
==================

Installation
------------

Install `mscales` by entering the following into your terminal::

   pip install mscales

Generation
----------

In `mscales`, musical scales are conceived as binary vectors.
You can generate all scales with chromatic cardinality `c` as follows:

.. code-block:: python

    from mscales.scales import generate_scales
    scales = generate_scales(c=12)

The variable `s` will then contain a numpy array with all possible scales
in 12-tone equal temperament, including the empty scale,
stored in a :math:`2^c \times c` numpy array:

>>> scales.shape
(4096, 12)

.. warning::
   Be careful with your choice for `c`!
   Since scales are binary vectors, there are :math:`2^c` scales,
   a number that can `grow very quickly <https://en.wikipedia.org/wiki/Power_of_two>`_
   and seriously slow down your computer.

One can access a specific scale through its row index:

>>> s = scales[3000,:]
>>> s
array([1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0])

Plotting
--------

Scales from this collection can then be accessed and plotted:

.. code-block:: python

   import matplotlib.pyplot as plt
   from mscales.plots import plot_scale

   plot_scale(s)
   plt.show()

.. image:: img/example-scale.png
   :alt: Example scale.

Sonification
------------

Sonification, the mapping of generated scales to sound,
is achieved with the `sound` module.

.. code-block:: python

   from mscales.sound import tone_cloud

   t = tone_cloud(s, save_as="example-scale.wav")

.. raw:: html

    <audio controls="controls">
      <source src="_static/example-scale.wav" type="audio/wav">
      Your browser does not support the <code>audio</code> element.
    </audio>

There are lots of parameters to change the sound. They will be documented
in more detail in future releases.

History
-------

.. toctree::
   :maxdepth: 2

   release-history
   min_versions
