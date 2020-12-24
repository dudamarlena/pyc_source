# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/disk9/cfse/dettmann/code/airinnova/pytornado/src/lib/pytornado/aero/__init__.py
# Compiled at: 2019-08-05 06:01:38
# Size of source mod 2**32: 975 bytes
"""
The aero package contains the Python modules and C/C++ libraries used in
the calculation of aerodynamic loads using the Vortex-Lattice Method.

The aero.vlm module contains the Python functions that prepare and pre-allocate
the aircraft, state and lattice data for the C wrapper functions contained in
aero.c_vlm.

The aero.c_vlm file contains the wrapper functions required to interpret and
operate on incoming data from Python and NumPy, using the native APIs. From
here, calls are made to the pure-C subroutines for the Vortex-Lattice Method
calculations. These are contained in separate files:

    * :aero.c_lattice: lattice generation
    * :aero.c_downwash: calculation of the downwash coefficients
    * :aero.c_boundary: calculation of the right-hand side terms
    * :aero.c_results: calculation of velocities, forces, coefficients

The .cpp and .h files must be compiled to a dynamic library c_vlm.so or
c_vlm.dll, manually or using the provided Makefile.
"""