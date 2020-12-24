# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/rpc/interfaces.py
# Compiled at: 2011-08-30 23:33:15
"""interfaces.py
Created on Aug 12, 2011
Copyright (c) 2011, Sean D. True
"""
demo = '\ninterface demo {\n    kernel sum(in float *a, in float *b, outlike a);\n    };\n'
convolve = '\n    interface convolve {\n        kernel ${name}(sizeof a, in float* a, outlike a);\n    };\n'
convolves = '\n    interface convolves {\n%for name,conv in convs:\n        kernel ${name}(sizeof a, in float* a, outlike a);\n%endfor \n    };\n'
median3x3 = '\n    interface median3x3 {\n        kernel median3x3(sizeof int a, heightof int a, in float* a, outlike a );\n        alias first as median3x3(sizeof int a, heightof int a, in float* a, in float* ret );\n        alias step as median3x3(sizeof int a, heightof int a, resident float* a, resident float* ret );\n        alias last as median3x3(sizeof int a, heightof int a, resident float* a, out float* ret );\n    };\n'
hsi = '\n    interface hsi {\n        kernel rgb2hsi(in float *r, in float *g, in float *b, outlike r, outlike r, outlike r, outlike r);\n        kernel hsi2rgb(in float *h, in float *s, in float *i, outlike h, outlike h, outlike h);\n    };\n'
mandelbrot = '\n    interface mandelbrot {\n        kernel mandelbrot(in complex64 *q, outlike short *q, in int maxiter);\n};\n'
gradient = '\n    interface gradient {\n        kernel gradient(sizeof int a, heightof int a, in float* a, in int reach, outlike a, outlike a );\n    };\n'