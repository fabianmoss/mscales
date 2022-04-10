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

    from mscales import generate_scales
    s = generate_scales(c=12)

The variable `s` will then contain a numpy array with all possible scales
in 12-tone equal temperament.

.. warning::
   Be careful with your choice for `c`!
   Since scales are binary vectors, there are :math:`2^c` scales,
   a number that can `grow very quickly <https://en.wikipedia.org/wiki/Power_of_two>`_
   and seriously slow down your computer.

Plotting
--------

Scales from this collection can then be accessed and plotted:

.. code-block:: python

   import matplotlib.pyplot as plt
   from mscales.plots import plot_scale

   plot_scale(s[4,:])
   plt.show()


Sonification
------------

Sonification, the mapping of generated scales to sound,
is achieved with the `sound` module.

History
-------

.. toctree::
   :maxdepth: 2

   release-history
   min_versions
