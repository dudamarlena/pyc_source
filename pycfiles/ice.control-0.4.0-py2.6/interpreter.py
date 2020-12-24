# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/repl/interpreter.py
# Compiled at: 2010-08-27 06:32:04
import code, sys, StringIO

class Interpreter(code.InteractiveInterpreter):
    output = []

    def write(self, data):
        self.output.append(data.rstrip())

    def get_output(self):
        r = self.output[:]
        self.output = []
        return r

    def runcode(self, code):
        stdout = sys.stdout
        trap = StringIO.StringIO()
        sys.stdout = trap
        try:
            exec code in self.locals
            self.write(trap.getvalue())
        except SystemExit:
            sys.stdout = stdout
            trap.close()
            del trap
            raise
        except:
            self.showtraceback()

        sys.stdout = stdout
        del trap