# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/python_prefork/__init__.py
# Compiled at: 2009-12-13 07:40:53
"""
   This module is inspired by Parallel::Prefork in CPAN.
   As Parallel::Prefork, this module is intended to be
   some operations done in parallel.

   Simple example of usage is followings

       >>> from python_prefork import PythonPrefork
       >>> pp = PythonPrefork()
       >>> while not pp.signal_received:
       >>>     if pp.start(): continue
       >>>
       >>>     run() # do some task in child process
       >>> 
       >>>     pp.finish()
       >>> pp.wait_all_children()

   Some options can be set in constructor
       [ max_workers ]
       maximum number of child processes to fork
       
       [trap_signals]
       arrays of signals to be trapped.
       parent process will send these signals to all children

       [on_reap_cb]
       function to be called when a child is end.
       This function must have two parameters, child pid and exit status.
"""
__author__ = 'Matsumoto Taichi (taichino@gmail.com)'
__version__ = '0.1.2'
__license__ = 'MIT License'
from python_prefork import PythonPrefork