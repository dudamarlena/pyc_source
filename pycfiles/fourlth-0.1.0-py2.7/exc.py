# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/fourlth/exc.py
# Compiled at: 2013-07-11 03:41:55
"""FoURLth Exception classes.
"""

class FourlthRootFactory(object):

    def __init__(self, request):
        self._req = request

    def __call__(self, *args, **kwargs):
        return FourlthInterpreter()


class FourlthSyntaxError(Exception):

    def __init__(self, *args, **kwargs):
        super(FourlthSyntaxError, self).__init__(*args, **kwargs)


class FourlthRuntimeError(Exception):

    def __init__(self, *args, **kwargs):
        super(FourlthRuntimeError, self).__init__(*args, **kwargs)


class FourlthBreak(Exception):

    def __init__(self, *args, **kwargs):
        super(FourlthBreak, self).__init__(*args, **kwargs)


class FourlthAbort(Exception):

    def __init__(self, *args, **kwargs):
        super(FourlthAbort, self).__init__(*args, **kwargs)


def stackTrace(frame):
    while frame is not None:
        print ('\t\t -> line {0.tb_lineno} in {0.tb_frame.f_code.co_filename}').format(frame)
        frame = frame.tb_next

    return