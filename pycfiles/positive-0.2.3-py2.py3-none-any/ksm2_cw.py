# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/positive//data/ksm2_cw.py
# Compiled at: 2019-03-26 15:31:05
"""
Module written by "mmrdns_write_python_freq_fit_eqns.m". Here be fitting functions for QNM frequencies for gravitational perturbations of kerr (spin weight -2).
"""
from numpy import log, exp
kappa = lambda x: (log(2.0 - x[0]) / log(3.0)) ** (1 / (2.0 + x[1] - abs(x[2])))
CW = {(2, 2, 0): lambda jf: 1.0 + kappa([jf, 2, 2]) * (1.557847 * exp(complex(0.0, 2.903124)) + 1.95097051 * exp(complex(0.0, 5.92097)) * kappa([jf, 2, 2]) + 2.09971716 * exp(complex(0.0, 2.760585)) * kappa([jf, 2, 2]) ** 2 + 1.4109466 * exp(complex(0.0, 5.91434)) * kappa([jf, 2, 2]) ** 3 + 0.41063923 * exp(complex(0.0, 2.795235)) * kappa([jf, 2, 2]) ** 4), 
   (2, -2, 0): lambda jf: -CW[(2, 2, 0)](jf).conj(), 
   (2, 2, 1): lambda jf: 1.0 + kappa([jf, 2, 2]) * (1.870939 * exp(complex(0.0, 2.511247)) + 2.71924916 * exp(complex(0.0, 5.424999)) * kappa([jf, 2, 2]) + 3.0564803 * exp(complex(0.0, 2.285698)) * kappa([jf, 2, 2]) ** 2 + 2.05309677 * exp(complex(0.0, 5.486202)) * kappa([jf, 2, 2]) ** 3 + 0.59549897 * exp(complex(0.0, 2.422525)) * kappa([jf, 2, 2]) ** 4), 
   (2, -2, 1): lambda jf: -CW[(2, 2, 1)](jf).conj(), 
   (3, 2, 0): lambda jf: 1.022464 * exp(complex(0.0, 0.00487)) + 0.24731213 * exp(complex(0.0, 0.665292)) * kappa([jf, 3, 2]) + 1.70468239 * exp(complex(0.0, 3.138283)) * kappa([jf, 3, 2]) ** 2 + 0.94604882 * exp(complex(0.0, 0.163247)) * kappa([jf, 3, 2]) ** 3 + 1.53189884 * exp(complex(0.0, 5.703573)) * kappa([jf, 3, 2]) ** 4 + 2.28052668 * exp(complex(0.0, 2.685231)) * kappa([jf, 3, 2]) ** 5 + 0.92150314 * exp(complex(0.0, 5.841704)) * kappa([jf, 3, 2]) ** 6, 
   (3, -2, 0): lambda jf: -CW[(3, 2, 0)](jf).conj(), 
   (4, 4, 0): lambda jf: 2.0 + kappa([jf, 4, 4]) * (2.658908 * exp(complex(0.0, 3.002787)) + 2.97825567 * exp(complex(0.0, 6.050955)) * kappa([jf, 4, 4]) + 3.2184235 * exp(complex(0.0, 2.877514)) * kappa([jf, 4, 4]) ** 2 + 2.12764967 * exp(complex(0.0, 5.989669)) * kappa([jf, 4, 4]) ** 3 + 0.60338186 * exp(complex(0.0, 2.830031)) * kappa([jf, 4, 4]) ** 4), 
   (4, -4, 0): lambda jf: -CW[(4, 4, 0)](jf).conj(), 
   (2, 1, 0): lambda jf: 0.589113 * exp(complex(0.0, 0.043525)) + 0.18896353 * exp(complex(0.0, 2.289868)) * kappa([jf, 2, 1]) + 1.15012965 * exp(complex(0.0, 5.810057)) * kappa([jf, 2, 1]) ** 2 + 6.04585476 * exp(complex(0.0, 2.741967)) * kappa([jf, 2, 1]) ** 3 + 11.12627777 * exp(complex(0.0, 5.84413)) * kappa([jf, 2, 1]) ** 4 + 9.34711461 * exp(complex(0.0, 2.669372)) * kappa([jf, 2, 1]) ** 5 + 3.03838318 * exp(complex(0.0, 5.791518)) * kappa([jf, 2, 1]) ** 6, 
   (2, -1, 0): lambda jf: -CW[(2, 1, 0)](jf).conj(), 
   (3, 3, 0): lambda jf: 1.5 + kappa([jf, 3, 3]) * (2.095657 * exp(complex(0.0, 2.964973)) + 2.46964352 * exp(complex(0.0, 5.996734)) * kappa([jf, 3, 3]) + 2.66552551 * exp(complex(0.0, 2.817591)) * kappa([jf, 3, 3]) ** 2 + 1.75836443 * exp(complex(0.0, 5.932693)) * kappa([jf, 3, 3]) ** 3 + 0.49905688 * exp(complex(0.0, 2.781658)) * kappa([jf, 3, 3]) ** 4), 
   (3, -3, 0): lambda jf: -CW[(3, 3, 0)](jf).conj(), 
   (3, 3, 1): lambda jf: 1.5 + kappa([jf, 3, 3]) * (2.33907 * exp(complex(0.0, 2.649692)) + 3.13988786 * exp(complex(0.0, 5.552467)) * kappa([jf, 3, 3]) + 3.59156756 * exp(complex(0.0, 2.347192)) * kappa([jf, 3, 3]) ** 2 + 2.44895997 * exp(complex(0.0, 5.443504)) * kappa([jf, 3, 3]) ** 3 + 0.70040804 * exp(complex(0.0, 2.283046)) * kappa([jf, 3, 3]) ** 4), 
   (3, -3, 1): lambda jf: -CW[(3, 3, 1)](jf).conj(), 
   (4, 3, 0): lambda jf: 1.5 + kappa([jf, 4, 3]) * (0.205046 * exp(complex(0.0, 0.595328)) + 3.10333396 * exp(complex(0.0, 3.0162)) * kappa([jf, 4, 3]) + 4.23612166 * exp(complex(0.0, 6.038842)) * kappa([jf, 4, 3]) ** 2 + 3.02890198 * exp(complex(0.0, 2.826239)) * kappa([jf, 4, 3]) ** 3 + 0.90843949 * exp(complex(0.0, 5.915164)) * kappa([jf, 4, 3]) ** 4), 
   (4, -3, 0): lambda jf: -CW[(4, 3, 0)](jf).conj(), 
   (5, 5, 0): lambda jf: 2.5 + kappa([jf, 5, 5]) * (3.240455 * exp(complex(0.0, 3.027869)) + 3.49056455 * exp(complex(0.0, 6.088814)) * kappa([jf, 5, 5]) + 3.74704093 * exp(complex(0.0, 2.921153)) * kappa([jf, 5, 5]) ** 2 + 2.4725279 * exp(complex(0.0, 6.03651)) * kappa([jf, 5, 5]) ** 3 + 0.69936568 * exp(complex(0.0, 2.876564)) * kappa([jf, 5, 5]) ** 4), 
   (5, -5, 0): lambda jf: -CW[(5, 5, 0)](jf).conj()}