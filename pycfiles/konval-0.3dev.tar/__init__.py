# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Py-konval/konval/konval/__init__.py
# Compiled at: 2011-08-02 10:02:25
"""
Validation and conversion of data.

The problem of sanitizing data (checking correctness and transforming to a
useful form) is widespread throughout programming:

* How do I verify user input is correct?
* How do I munge data from a spreadsheet into dates and numbers?
* How do I convert raw database fields into an object?

Ian Bicking produced a sensible approach to this, embodied in his Formencode
library: data validation and conversion are one and the same thing, and can be
handled by passing raw data through a chain of validators. In this spirit,
*konval* is a package

* a rich library of validation objects
* base classes for easily producing custom validators
* functions for easily using validators on objects

"""
__version__ = '0.3'
__author__ = 'Paul-Michael Agapow'
__email__ = 'pma@agapow.net'
from fxn import *
from basevalidator import *
from typeval import *
from containerval import *
from defs import *
from sizeval import *
from containerval import *
from vocabval import *
from stringval import *
from logicval import *