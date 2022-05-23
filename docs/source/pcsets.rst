Pitch-Class Sets
================

Apart from the ``scales`` module discussed
in Quickstart, ``mscales`` also contains the ``pcsets`` module.
At the moment, they are alternatives with partially overlapping
functionalities but they will be merged in the futured.

.. note::
    As a rule of thumb, use the ``scales`` module whenever possible
    and only revert to ``pcsets`` when you need very specific things.

The ``pcsets`` module implements classic definitions of
and transformations on pitch-class sets known from Set Theory.
Pitch-class sets (from now on pcsets) can be instantiated as follows:

>>> from mscales import PitchClassSet
>>> s = PitchClassSet({11,2,3})
[11  2  3]

pcsets have lots of transformations impmented, and their results
are stored in the ``.info()`` method.

.. code-block:: python

   >>> s.info()
   """
    =========================
    PitchClassSet([11  2  3])
    =========================

    Set Theory
    ==========
    complement      : [ 0  1  4  5  6  7  8  9 10]
    transposed      : [1 4 5]
    inverted        : [ 1 10  9]
    T2I             : [ 3  0 11]
    normal form     : [11  2  3]
    prime form      : [0 4 1]
    interval vector : [1 0 1 1 0 0]

    Serialism
    =========
    original        :  [11  2  3]
    retrograde      :  [ 3  2 11]
    inversion       :  [11  8  7]
    retro.-inv.     :  [ 7  8 11]
    matrix          : [[ 0  3  4]
                       [ 9  0  1]
                       [ 8 11  0]]
    """

The methods currently implemented are:

.. automodule:: pcsets
    :members:
    :undoc-members:
