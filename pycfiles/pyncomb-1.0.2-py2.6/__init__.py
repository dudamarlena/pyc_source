# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/__init__.py
# Compiled at: 2010-10-16 14:03:44
"""The pyncomb (PYthoN COMBinatorics) library is a collection of
functions to work with basic combinatorial objects (e.g. permutations,
subsets, tuples), and provides algorithms for ranking, unranking, and
iterating over all objects in a specified class.

* combfuncs
     General functions independent of any other module, including a number
     of convenience routines to simplify working with the other modules.

ALL SUBSETS:
-----------
* subsetgc
     Operations over all subsets of a base set, using a minimal change
     order based on a binary-reflected Gray code.

* subsetlex
     Operations over all subsets of a base set, using lexicographic order.

K-SUBSETS:
---------
* ksubsetcolex
     Operations for k-subsets over a base set, using colex order.

* ksubsetlex
     Operations for k-subsets over a base set, using lexicographic order.

* ksubsetrevdoor
     Operations for k-subsets over a base set, using a minimal change
     revolving door order.

PERMUTATIONS:
------------
* permlex
     Operations for permutations over Sn, using lexicographic order.

* permtj
     Operations for permutations over Sn, using a minimal change order
     as per the Trotter-Johnson algorithm.

TUPLES:
------
* mbtuplelex
     Operations for tuples over mixed bases, using lexicographic order.
     Example: generate all tuples in [0,1,2]X['a','b']X[11,22,33,44].

* tuplelex
     Operations for tuples over a fixed base, using lexicographic order.
     Example: generate all 4-tuples over [0,1,2].

By Sebastian Raaphorst, 2009.

The algorithms herein are from:

Kreher, Donald and Stinson, Douglas. Combinatorial Algorithms: Generation,
   Enumeration, and Search. CRC Press, 1999.

I have tried to Pythonize them, but there is likely still considerable room
for improvement. Please e-mail all suggestions to srcoding@gmail.com, and they
will be incorporated in the next version of pyncomb."""
from . import combfuncs
from . import ksubsetcolex
from . import ksubsetlex
from . import ksubsetrevdoor
from . import mbtuplelex
from . import permlex
from . import permtj
from . import subsetgc
from . import subsetlex