# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/callback/base_callback.py
# Compiled at: 2016-10-26 09:22:48


class BaseCallback(object):

    def before_gpi_start(self, domain, value_function):
        pass

    def before_update(self, iteration_count, domain, value_function):
        pass

    def after_update(self, iteration_count, domain, value_function):
        pass

    def after_gpi_finish(self, domain, value_function):
        pass

    def interrupt_gpi(self, iteration_count, domain, value_function):
        return False

    def define_log_tag(self):
        return self.__class__.__name__

    def log(self, message):
        if message and len(message) != 0:
            print '[%s] %s' % (self.define_log_tag(), message)