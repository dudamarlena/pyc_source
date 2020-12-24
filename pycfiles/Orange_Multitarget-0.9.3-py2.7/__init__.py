# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/_multitarget/__init__.py
# Compiled at: 2012-11-23 17:14:54
"""
Examples
========

The following example uses a simple multi-target data set (generated with
:download:`generate_multitarget.py <code/generate_multitarget.py>`) to show
some basic functionalities (part of
:download:`multitarget.py <code/multitarget.py>`).

.. literalinclude:: code/multitarget.py
    :lines: 1-6

Multi-target learners can build prediction models (classifiers)
which then predict (multiple) class values for a new instance (continuation of
:download:`multitarget.py <code/multitarget.py>`):

.. literalinclude:: code/multitarget.py
    :lines: 8-

"""
from pkg_resources import resource_filename

def datasets():
    yield (
     'multitarget', resource_filename(__name__, 'datasets'))


import Orange
from Orange.regression import earth
import tree, chain, binary, neural, scoring, pls