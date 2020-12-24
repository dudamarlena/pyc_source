# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/output.py
# Compiled at: 2014-07-01 10:29:06
from tffstub import tff
import constant

class OutputHandler(tff.DefaultHandler):

    def __init__(self, controller, tracer):
        self._tracer = tracer
        self._controller = controller

    def handle_csi(self, context, parameter, intermediate, final):

        def action():
            context.put(27)
            context.put(91)
            for c in parameter:
                context.put(c)

            for c in intermediate:
                context.put(c)

            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_csi(context, parameter, intermediate, final)
            return constant.SEQ_TYPE_CSI

        self._controller.append(action)
        return True

    def handle_esc(self, context, intermediate, final):

        def action():
            context.put(27)
            for c in intermediate:
                context.put(c)

            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_esc(context, intermediate, final)
            return constant.SEQ_TYPE_ESC

        self._controller.append(action)
        return True

    def handle_ss2(self, context, final):

        def action():
            context.put(27)
            context.put(78)
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_ss2(context, final)
            return constant.SEQ_TYPE_SS2

        self._controller.append(action)
        return True

    def handle_ss3(self, context, final):

        def action():
            context.put(27)
            context.put(79)
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_ss3(context, final)
            return constant.SEQ_TYPE_SS3

        self._controller.append(action)
        return True

    def handle_control_string(self, context, prefix, value):

        def action():
            context.put(27)
            context.put(prefix)
            for c in value:
                context.put(c)

            context.put(27)
            context.put(92)
            self._tracer.set_output()
            self._tracer.handle_control_string(context, prefix, value)
            return constant.SEQ_TYPE_STR

        self._controller.append(action)
        return True

    def handle_char(self, context, final):

        def action():
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_char(context, final)
            return constant.SEQ_TYPE_CHAR

        self._controller.append(action)
        return True

    def handle_invalid(self, context, seq):

        def action():
            for c in seq:
                context.put(c)

            self._tracer.set_output()
            self._tracer.handle_invalid(context, seq)
            return constant.SEQ_TYPE_CHAR

        self._controller.append(action)
        return True

    def handle_resize(self, context, row, col):
        self._tracer.handle_resize(context, row, col)

    def handle_draw(self, context):
        self._controller.tick()
        self._tracer.handle_draw(context)


if __name__ == '__main__':
    import doctest
    doctest.testmod()