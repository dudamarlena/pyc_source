# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/assemble.py
# Compiled at: 2000-03-15 16:55:42
import types, string, new
from bytecodehacks import opbases, code_editor
from bytecodehacks.ops import *

def getops(module):
    ret = {}
    mod = __import__(module, globals(), locals(), '.' in module and [[]] or [])
    for k, v in mod.__dict__.items():
        if type(v) is types.ClassType and issubclass(v, opbases.ByteCode):
            ret[k] = v

    return ret


import StringIO

class Assembler:

    def __init__(self):
        self.superior = self.sub = None
        self.filename = '<assembled code>'
        self.lineno = 0
        self.opcodes = getops('bytecodehacks.ops')
        return

    def process_line(self, line):
        self.lineno = self.lineno + 1
        if self.sub is not None:
            self.sub.process_line(line)
        else:
            p = string.find(line, ';')
            if p >= 0:
                line = line[:p]
            line = string.strip(line)
            if not line:
                return
            command = string.split(line, None, 1)
            if len(command) > 1:
                command, rest = command
            else:
                command, = command
                rest = ''
            if self.opcodes.has_key(command):
                self.opcode(command, rest)
            else:
                getattr(self, command)(rest)
        return

    def subordinate_done(self):
        self.sub = None
        return

    def opcode(self, opname, arg):
        opclass = self.opcodes[opname]
        if arg != '':
            if arg[0] == '#':
                arg = int(arg[1:])
            elif arg[0] == '@' or arg[0] == '!':
                if arg[0] == '@':
                    const = self.code.co_code.consts[arg[1:]]
                else:
                    const = eval(arg[1:])
                if const in self.code.co_consts:
                    arg = self.code.co_consts.index(const)
                else:
                    arg = len(self.code.co_consts)
                    self.code.co_consts.append(const)
            self.code.co_code.append(opclass(arg))
        else:
            self.code.co_code.append(opclass())

    def top(self):
        n = self
        while n is not None:
            n, p = n.superior, n

        return p

    def function(self, args):
        print 'hello', args
        self.sub = FunctionAssembler(args, self)

    def load(self, args):
        self.opcodes.update(getops(args))

    def make(self):
        return self.code.make_code()


class ModuleAssembler(Assembler):

    def __init__(self, filename):
        Assembler.__init__(self)
        self.code = code_editor.EditableCode()
        self.filename = filename

    def subordinate_done(self):
        cindex = len(self.code.co_consts)
        code = self.sub.make()
        self.code.co_consts.append(code)
        self.code.co_code.extend([
         LOAD_CONST(cindex),
         MAKE_FUNCTION(0),
         STORE_NAME(code.co_name)])
        self.sub = None
        return

    def make_module(self, modulename):
        code = self.make()
        module = new.module(modulename)
        exec code in module.__dict__
        module.__file__ = self.filename
        return module


class FunctionAssembler(Assembler):

    def __init__(self, args, superior):
        Assembler.__init__(self)
        self.superior = superior
        args = string.split(args)
        self.code = code_editor.EditableCode()
        self.code.co_varnames.extend(args[1:])
        self.code.co_name = args[0]
        self.code.co_filename = self.top().filename
        self.code.co_firstlineno = self.top().lineno
        self.code.co_argcount = len(args) - 1

    def subordinate_done(self):
        cindex = len(self.code.co_consts)
        code = self.sub.make()
        self.code.co_consts.append(code)
        self.code.co_code.extend([
         LOAD_CONST(cindex),
         MAKE_FUNCTION(0),
         STORE_FAST(code.co_name)])
        self.sub = None
        return

    def end(self, _):
        self.superior.subordinate_done()


def assemble(file, filename='<assembled module>'):
    if type(file) is types.StringType:
        file = StringIO.StringIO(file)
    assembler = ModuleAssembler(filename)
    for line in file.readlines():
        assembler.process_line(line)

    return assembler.make_module(filename)


def compile(file):
    """compile the Python Assembler file `file' into a code object"""
    pass