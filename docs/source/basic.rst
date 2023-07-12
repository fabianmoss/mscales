Basic objects
=============

.. note::
    Apart from the ``scales`` module discussed
    in Quickstart, ``mscales`` also contains the ``pcsets`` module.
    At the moment, they are alternatives with partially overlapping
    functionalities but they will be merged in the futured.
    
    As a rule of thumb, use the ``scales`` module whenever possible
    and only revert to ``pcsets`` when you need very specific things.

The ``pcsets`` module implements classic definitions of
and transformations on pitch-class sets known from
`Set Theory <https://en.wikipedia.org/wiki/Set_theory_(music)>`_.

Pitch classes
-------------

The fundamental objects of set theory are `pitch classes`.
Pitch classes incorporate two fundamental assumptions about how
pitches relate to one another:

#. Octave equivalence: pitches that are related by (multiples of)
   octaves are considered equivalent.
#. Enharmonic equivalence: pitches that are mapped to the same key on a piano
   (irrespective of the octave) are considered equivalent.

In ``mscales``, pitch classes are instantiated by passing an integer
to the PitchClass class::

    >>> from mscales import PitchClass
    >>> p = PitchClass(3) # E-flat

For now, this is the only instantiation method.
One can see that ``PitchClass`` instances incorporate enharmonic equivalence::

    >>> PitchClass(3) == PitchClass(15)
    True

Pitch-class intervals
---------------------

Pitch classes can be transposed by adding a ``PitchClassInterval``::

    >>> from mscales import PitchClassInterval
    >>> i = PitchClassInterval(7) # perfect fifth
    >>> p + i
    PitchClass(10)

Intervals are here understood as ascending.
For descending intervals, we can either initialize it 
with ``PitchClassInterval(-j)`` for some integer ``j``, 
or simply subtract an ascending interval from a pitch class::

    >>> p - i
    PitchClass(5)

Pitch-class sets
----------------

Pitch-class sets (from now on pcsets) can be instantiated as follows:

>>> from mscales import PitchClassSet
>>> s = PitchClassSet({0,4,1,6})
[0  4  1  6]

We can also look at the vector representation of a pitch-class set::

    >>> v = s.to_vector()
    >>> v
    array([1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0])

.. This representation allows us to use the plotting functions
.. from the ``plots`` module:

    .. .. plot::
    ..     :align: center

    ..     from .mscales import PitchClassSet
    ..     from .mscales.plots import plot_radar

    ..     v = PitchClassSet({0,4,1,6}).to_vector()
    ..     plot_radar(v)

The ``PitchClassSet`` class has lots of transformations implemented,
and their results are stored in the ``.info()`` method.

.. code-block:: python

   >>> s.info()
   """
    ========================
    PitchClassSet([0 1 4 6])
    ========================

    Set Theory
    ==========
    cardin. (d, c)  : 4 12
    pc vector       : [1 1 0 0 1 0 1 0 0 0 0 0]
    complement      : [ 2  3  5  7  8  9 10 11]
    transposed      : [2 3 6 8]
    inverted        : [ 0 11  8  6]
    T2I             : [ 2  1 10  8]
    normal form     : [0 1 4 6]
    prime form      : [0 1 7 9]
    interval vector : [1 1 1 1 1 1]

    Serialism
    =========
    original        : [0 1 4 6]
    retrograde      : [6 4 1 0]
    inversion       : [ 0 11  8  6]
    retro.-inv.     : [ 6  8 11  0]
    matrix          : [[ 0  1  4  6]
                    [11  0  3  5]
                    [ 8  9  0  2]
                    [ 6  7 10  0]]
    """


.. rubric:: API

All methods currently implemented are:

.. automodule:: pcsets
    :members:
    :undoc-members:
