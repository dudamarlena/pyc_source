# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/__init__.py
# Compiled at: 2010-10-16 14:03:44
__doc__ = "The pyncomb (PYthoN COMBinatorics) library is a collection of\nfunctions to work with basic combinatorial objects (e.g. permutations,\nsubsets, tuples), and provides algorithms for ranking, unranking, and\niterating over all objects in a specified class.\n\n* combfuncs\n     General functions independent of any other module, including a number\n     of convenience routines to simplify working with the other modules.\n\n\nALL SUBSETS:\n-----------\n* subsetgc\n     Operations over all subsets of a base set, using a minimal change\n     order based on a binary-reflected Gray code.\n\n* subsetlex\n     Operations over all subsets of a base set, using lexicographic order.\n\n\nK-SUBSETS:\n---------\n* ksubsetcolex\n     Operations for k-subsets over a base set, using colex order.\n\n* ksubsetlex\n     Operations for k-subsets over a base set, using lexicographic order.\n\n* ksubsetrevdoor\n     Operations for k-subsets over a base set, using a minimal change\n     revolving door order.\n\n\nPERMUTATIONS:\n------------\n* permlex\n     Operations for permutations over Sn, using lexicographic order.\n\n* permtj\n     Operations for permutations over Sn, using a minimal change order\n     as per the Trotter-Johnson algorithm.\n\n\nTUPLES:\n------\n* mbtuplelex\n     Operations for tuples over mixed bases, using lexicographic order.\n     Example: generate all tuples in [0,1,2]X['a','b']X[11,22,33,44].\n\n* tuplelex\n     Operations for tuples over a fixed base, using lexicographic order.\n     Example: generate all 4-tuples over [0,1,2].\n\nBy Sebastian Raaphorst, 2009.\n\nThe algorithms herein are from:\n\nKreher, Donald and Stinson, Douglas. Combinatorial Algorithms: Generation,\n   Enumeration, and Search. CRC Press, 1999.\n\nI have tried to Pythonize them, but there is likely still considerable room\nfor improvement. Please e-mail all suggestions to srcoding@gmail.com, and they\nwill be incorporated in the next version of pyncomb."
from . import combfuncs
from . import ksubsetcolex
from . import ksubsetlex
from . import ksubsetrevdoor
from . import mbtuplelex
from . import permlex
from . import permtj
from . import subsetgc
from . import subsetlex