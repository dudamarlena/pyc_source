# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/tangle/m_event.py
# Compiled at: 2017-08-24 10:00:25
# Size of source mod 2**32: 651 bytes
from tangle.m_aspect import Aspect

class ApplicationContextPostProcessor(object):

    def post_process(self, application_context):
        pass


class BeanPostProcessor(object):

    def post_initialize(self, application_context, bean):
        pass

    def post_process(self, application_context, bean):
        pass


class AspectBeanPostProcessor(BeanPostProcessor):

    def post_initialize(self, application_context, bean):
        beans = application_context.get_all_singleton_beans().values()
        for aspect in filter(lambda asp: isinstance(asp, Aspect), beans):
            print(aspect)