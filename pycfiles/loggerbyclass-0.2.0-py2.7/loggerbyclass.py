# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/loggerbyclass.py
# Compiled at: 2015-02-16 05:52:15
"""
Provides a single helper function to simplify the common idiom
of getting one logger object from python standard logging per
class.

@author: languitar
"""
import logging

def get_logger_by_class(klass, instance=None):
    """Gets a python logger instance based on a class instance. The logger name
    will be a dotted string containing python module and class name, hence
    being the full path to the class.

    @param klass: class instance
    @return: logger instance
    """
    return logging.getLogger(klass.__module__ + '.' + klass.__name__ + (('.__{}__').format(instance.replace('.', '_')) if instance else ''))