# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/dispatcher_application_configurer.py
# Compiled at: 2018-05-31 03:57:55
__all__ = [
 'DispatcherApplicationConfigurer',
 'DefaultDispatcherApplicationConfigurer']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractproperty

class DispatcherApplicationConfigurer(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def max_redirect_count(self):
        pass


class DefaultDispatcherApplicationConfigurer(DispatcherApplicationConfigurer):

    @property
    def max_redirect_count(self):
        return 100