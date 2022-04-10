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
You can generate all scales with chromatic `cardinality` as follows:

.. code-block:: python

    from mscales.scales import Scales
    s = Scales(cardinality=12)

The variable `scales` has initialized all potential scales with cardinality 12.
In order to access these scales, call the `.all()` method:

>>> scales = s.all()
>>> scales
array([[0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 1],
       [0, 0, 0, ..., 0, 1, 0],
       ...,
       [1, 1, 1, ..., 1, 0, 1],
       [1, 1, 1, ..., 1, 1, 0],
       [1, 1, 1, ..., 1, 1, 1]])

This will return a :math:`2^c \times c` numpy array:

>>> scales.shape
(4096, 12)

.. warning::
   Be careful with your choice for `cardinality`!
   Since scales are binary vectors, there are :math:`2^c` scales,
   a number that can `grow very quickly <https://en.wikipedia.org/wiki/Power_of_two>`_
   and seriously slow down your computer.

One can access a specific scale through its row index:

>>> scale = scales[3000,:]
>>> scale
array([1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0])

Plotting
--------

Scales from this collection can then be accessed and plotted:

.. code-block:: python

   import matplotlib.pyplot as plt
   from mscales.plots import plot_scale

   plot_scale(scale)
   plt.show()

.. image:: img/example-scale.png
   :alt: Example scale.

Sonification
------------

.. note::
   Currently, we can only synthesize scales with a cardinality of 12
   because `mscales` relies on the `tones` library.

Sonification, the mapping of generated scales to sound,
is achieved with the `sound` module.

.. code-block:: python

   from mscales.sound import tone_cloud

   t = tone_cloud(scale, save_as="example-scale.wav")

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
