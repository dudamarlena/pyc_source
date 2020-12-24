# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/input.py
# Compiled at: 2014-07-01 10:29:06
from tffstub import tff

class InputHandler(tff.DefaultHandler):
    """ <F6> toggle trace state
        <F7> toggle break state
        <F8> step to next char or seq
        <F9> step to next ESC or CSI seq
    """

    def __init__(self, controller, tracer):
        self._controller = controller
        self._tracer = tracer

    def handle_esc(self, context, intermediate, final):
        self._tracer.set_input()
        return self._tracer.handle_esc(context, intermediate, final)

    def handle_csi(self, context, parameter, intermediate, final):
        self._tracer.set_input()
        return self._tracer.handle_csi(context, parameter, intermediate, final)

    def handle_ss2(self, context, final):
        self._tracer.set_input()
        return self._tracer.handle_ss2(context, final)

    def handle_ss3(self, context, final):
        self._tracer.set_input()
        return self._tracer.handle_ss3(context, final)

    def handle_control_string(self, context, prefix, value):
        self._tracer.set_input()
        return self._tracer.handle_control_string(context, prefix, value)

    def handle_char(self, context, final):
        self._tracer.set_input()
        return self._tracer.handle_char(context, final)

    def handle_invalid(self, context, seq):
        self._tracer.set_input()
        return self._tracer.handle_invalid(context, seq)

    def handle_draw(self, context):
        self._controller.tick()


if __name__ == '__main__':
    import doctest
    doctest.testmod()