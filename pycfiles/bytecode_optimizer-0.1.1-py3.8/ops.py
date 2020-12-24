# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/ops.py
# Compiled at: 2000-04-01 07:02:52
from bytecodehacks import opbases
from bytecodehacks.label import Label
_opbases = opbases
_Label = Label
del Label
del opbases
_bytecodes = {}

class STOP_CODE(_opbases.GenericOneByteCode):
    op = 0
    opc = '\x00'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[STOP_CODE.opc] = STOP_CODE

class POP_TOP(_opbases.GenericOneByteCode):
    op = 1
    opc = '\x01'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[POP_TOP.opc] = POP_TOP

class ROT_TWO(_opbases.GenericOneByteCode):
    op = 2
    opc = '\x02'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         stack[(-1)], stack[(-2)]]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[ROT_TWO.opc] = ROT_TWO

class ROT_THREE(_opbases.GenericOneByteCode):
    op = 3
    opc = '\x03'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-3):] = [stack[(-1)],
         stack[(-3)],
         stack[(-2)]]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[ROT_THREE.opc] = ROT_THREE

class DUP_TOP(_opbases.GenericOneByteCode):
    op = 4
    opc = '\x04'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack.append(stack[(-1)])

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[DUP_TOP.opc] = DUP_TOP

class UNARY_POSITIVE(_opbases.GenericOneByteCode):
    op = 10
    opc = '\n'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[UNARY_POSITIVE.opc] = UNARY_POSITIVE

class UNARY_NEGATIVE(_opbases.GenericOneByteCode):
    op = 11
    opc = '\x0b'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[UNARY_NEGATIVE.opc] = UNARY_NEGATIVE

class UNARY_NOT(_opbases.GenericOneByteCode):
    op = 12
    opc = '\x0c'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[UNARY_NOT.opc] = UNARY_NOT

class UNARY_CONVERT(_opbases.GenericOneByteCode):
    op = 13
    opc = '\r'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[UNARY_CONVERT.opc] = UNARY_CONVERT

class UNARY_INVERT(_opbases.GenericOneByteCode):
    op = 15
    opc = '\x0f'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[UNARY_INVERT.opc] = UNARY_INVERT

class BINARY_POWER(_opbases.GenericOneByteCode):
    op = 19
    opc = '\x13'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_POWER.opc] = BINARY_POWER

class BINARY_MULTIPLY(_opbases.GenericOneByteCode):
    op = 20
    opc = '\x14'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_MULTIPLY.opc] = BINARY_MULTIPLY

class BINARY_DIVIDE(_opbases.GenericOneByteCode):
    op = 21
    opc = '\x15'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_DIVIDE.opc] = BINARY_DIVIDE

class BINARY_MODULO(_opbases.GenericOneByteCode):
    op = 22
    opc = '\x16'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_MODULO.opc] = BINARY_MODULO

class BINARY_ADD(_opbases.GenericOneByteCode):
    op = 23
    opc = '\x17'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_ADD.opc] = BINARY_ADD

class BINARY_SUBTRACT(_opbases.GenericOneByteCode):
    op = 24
    opc = '\x18'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_SUBTRACT.opc] = BINARY_SUBTRACT

class BINARY_SUBSCR(_opbases.GenericOneByteCode):
    op = 25
    opc = '\x19'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_SUBSCR.opc] = BINARY_SUBSCR

class SLICE_0(_opbases.GenericOneByteCode):
    op = 30
    opc = '\x1e'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[SLICE_0.opc] = SLICE_0

class SLICE_1(_opbases.GenericOneByteCode):
    op = 31
    opc = '\x1f'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[SLICE_1.opc] = SLICE_1

class SLICE_2(_opbases.GenericOneByteCode):
    op = 32
    opc = ' '

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[SLICE_2.opc] = SLICE_2

class SLICE_3(_opbases.GenericOneByteCode):
    op = 33
    opc = '!'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-3):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(2)


_bytecodes[SLICE_3.opc] = SLICE_3

class STORE_SLICE_0(_opbases.GenericOneByteCode):
    op = 40
    opc = '('

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-2:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(2)


_bytecodes[STORE_SLICE_0.opc] = STORE_SLICE_0

class STORE_SLICE_1(_opbases.GenericOneByteCode):
    op = 41
    opc = ')'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-3:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(3)


_bytecodes[STORE_SLICE_1.opc] = STORE_SLICE_1

class STORE_SLICE_2(_opbases.GenericOneByteCode):
    op = 42
    opc = '*'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-3:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(3)


_bytecodes[STORE_SLICE_2.opc] = STORE_SLICE_2

class STORE_SLICE_3(_opbases.GenericOneByteCode):
    op = 43
    opc = '+'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-4:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(4)


_bytecodes[STORE_SLICE_3.opc] = STORE_SLICE_3

class DELETE_SLICE_0(_opbases.GenericOneByteCode):
    op = 50
    opc = '2'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-1:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[DELETE_SLICE_0.opc] = DELETE_SLICE_0

class DELETE_SLICE_1(_opbases.GenericOneByteCode):
    op = 51
    opc = '3'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-2:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(2)


_bytecodes[DELETE_SLICE_1.opc] = DELETE_SLICE_1

class DELETE_SLICE_2(_opbases.GenericOneByteCode):
    op = 52
    opc = '4'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-2:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(2)


_bytecodes[DELETE_SLICE_2.opc] = DELETE_SLICE_2

class DELETE_SLICE_3(_opbases.GenericOneByteCode):
    op = 53
    opc = '5'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-3:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(3)


_bytecodes[DELETE_SLICE_3.opc] = DELETE_SLICE_3

class STORE_SUBSCR(_opbases.GenericOneByteCode):
    op = 60
    opc = '<'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-3:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(3)


_bytecodes[STORE_SUBSCR.opc] = STORE_SUBSCR

class DELETE_SUBSCR(_opbases.GenericOneByteCode):
    op = 61
    opc = '='

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        del stack[-2:]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(2)


_bytecodes[DELETE_SUBSCR.opc] = DELETE_SUBSCR

class BINARY_LSHIFT(_opbases.GenericOneByteCode):
    op = 62
    opc = '>'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_LSHIFT.opc] = BINARY_LSHIFT

class BINARY_RSHIFT(_opbases.GenericOneByteCode):
    op = 63
    opc = '?'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_RSHIFT.opc] = BINARY_RSHIFT

class BINARY_AND(_opbases.GenericOneByteCode):
    op = 64
    opc = '@'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_AND.opc] = BINARY_AND

class BINARY_XOR(_opbases.GenericOneByteCode):
    op = 65
    opc = 'A'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_XOR.opc] = BINARY_XOR

class BINARY_OR(_opbases.GenericOneByteCode):
    op = 66
    opc = 'B'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[BINARY_OR.opc] = BINARY_OR

class PRINT_EXPR(_opbases.GenericOneByteCode):
    op = 70
    opc = 'F'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[PRINT_EXPR.opc] = PRINT_EXPR

class PRINT_ITEM(_opbases.GenericOneByteCode):
    op = 71
    opc = 'G'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[PRINT_ITEM.opc] = PRINT_ITEM

class PRINT_NEWLINE(_opbases.GenericOneByteCode):
    op = 72
    opc = 'H'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[PRINT_NEWLINE.opc] = PRINT_NEWLINE

class BREAK_LOOP(_opbases.GenericOneByteCode):
    op = 80
    opc = 'P'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        raise 'No jumps here!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[BREAK_LOOP.opc] = BREAK_LOOP

class LOAD_LOCALS(_opbases.GenericOneByteCode):
    op = 82
    opc = 'R'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[LOAD_LOCALS.opc] = LOAD_LOCALS

class RETURN_VALUE(_opbases.GenericOneByteCode):
    op = 83
    opc = 'S'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[:] = []

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[RETURN_VALUE.opc] = RETURN_VALUE

class EXEC_STMT(_opbases.GenericOneByteCode):
    op = 85
    opc = 'U'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(3)


_bytecodes[EXEC_STMT.opc] = EXEC_STMT

class POP_BLOCK(_opbases.GenericOneByteCode):
    op = 87
    opc = 'W'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        block_pop()


_bytecodes[POP_BLOCK.opc] = POP_BLOCK

class END_FINALLY(_opbases.GenericOneByteCode):
    op = 88
    opc = 'X'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        tracker.handle_end_finally()


_bytecodes[END_FINALLY.opc] = END_FINALLY

class BUILD_CLASS(_opbases.GenericOneByteCode):
    op = 89
    opc = 'Y'

    def __init__(self, cs=None, code=None):
        if cs is not None:
            _opbases.GenericOneByteCode.__init__(self, cs, code)
        return

    def execute(self, stack):
        stack[(-3):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(3)


_bytecodes[BUILD_CLASS.opc] = BUILD_CLASS

class STORE_NAME(_opbases.NameOpcode):
    op = 90
    opc = 'Z'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[STORE_NAME.opc] = STORE_NAME

class DELETE_NAME(_opbases.NameOpcode):
    op = 91
    opc = '['

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[DELETE_NAME.opc] = DELETE_NAME

class UNPACK_TUPLE(_opbases.GenericThreeByteCode):
    op = 92
    opc = '\\'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append([self] * self.arg)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(self.arg)


_bytecodes[UNPACK_TUPLE.opc] = UNPACK_TUPLE

class UNPACK_LIST(_opbases.GenericThreeByteCode):
    op = 93
    opc = ']'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append([self] * self.arg)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(self.arg)


_bytecodes[UNPACK_LIST.opc] = UNPACK_LIST

class STORE_ATTR(_opbases.NameOpcode):
    op = 95
    opc = '_'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[STORE_ATTR.opc] = STORE_ATTR

class DELETE_ATTR(_opbases.NameOpcode):
    op = 96
    opc = '`'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[DELETE_ATTR.opc] = DELETE_ATTR

class STORE_GLOBAL(_opbases.NameOpcode):
    op = 97
    opc = 'a'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[STORE_GLOBAL.opc] = STORE_GLOBAL

class DELETE_GLOBAL(_opbases.NameOpcode):
    op = 98
    opc = 'b'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[DELETE_GLOBAL.opc] = DELETE_GLOBAL

class LOAD_CONST(_opbases.GenericThreeByteCode):
    op = 100
    opc = 'd'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[LOAD_CONST.opc] = LOAD_CONST

class LOAD_NAME(_opbases.NameOpcode):
    op = 101
    opc = 'e'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[LOAD_NAME.opc] = LOAD_NAME

class BUILD_TUPLE(_opbases.GenericThreeByteCode):
    op = 102
    opc = 'f'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        if self.arg > 0:
            stack[(-self.arg):] = [
             self]
        else:
            stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(self.arg - 1)


_bytecodes[BUILD_TUPLE.opc] = BUILD_TUPLE

class BUILD_LIST(_opbases.GenericThreeByteCode):
    op = 103
    opc = 'g'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        if self.arg > 0:
            stack[(-self.arg):] = [
             self]
        else:
            stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(self.arg - 1)


_bytecodes[BUILD_LIST.opc] = BUILD_LIST

class BUILD_MAP(_opbases.GenericThreeByteCode):
    op = 104
    opc = 'h'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[BUILD_MAP.opc] = BUILD_MAP

class LOAD_ATTR(_opbases.NameOpcode):
    op = 105
    opc = 'i'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack[-1] = self

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[LOAD_ATTR.opc] = LOAD_ATTR

class COMPARE_OP(_opbases.GenericThreeByteCode):
    op = 106
    opc = 'j'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack[(-2):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[COMPARE_OP.opc] = COMPARE_OP

class IMPORT_NAME(_opbases.NameOpcode):
    op = 107
    opc = 'k'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[IMPORT_NAME.opc] = IMPORT_NAME

class IMPORT_FROM(_opbases.NameOpcode):
    op = 108
    opc = 'l'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[IMPORT_FROM.opc] = IMPORT_FROM

class JUMP_FORWARD(_opbases.JRel):
    op = 110
    opc = 'n'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        raise 'jumps not handled here!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[JUMP_FORWARD.opc] = JUMP_FORWARD

class JUMP_IF_FALSE(_opbases.JRel):
    op = 111
    opc = 'o'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        raise 'jumps not handled here!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[JUMP_IF_FALSE.opc] = JUMP_IF_FALSE

class JUMP_IF_TRUE(_opbases.JRel):
    op = 112
    opc = 'p'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        raise 'jumps not handled here!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[JUMP_IF_TRUE.opc] = JUMP_IF_TRUE

class JUMP_ABSOLUTE(_opbases.JAbs):
    op = 113
    opc = 'q'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JAbs.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        raise 'jumps not handled here!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[JUMP_ABSOLUTE.opc] = JUMP_ABSOLUTE

class FOR_LOOP(_opbases.JRel):
    op = 114
    opc = 'r'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        raise 'loop alert'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[FOR_LOOP.opc] = FOR_LOOP

class LOAD_GLOBAL(_opbases.NameOpcode):
    op = 116
    opc = 't'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.NameOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[LOAD_GLOBAL.opc] = LOAD_GLOBAL

class SETUP_LOOP(_opbases.JRel):
    op = 120
    opc = 'x'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        raise 'loop alert!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        block_push()


_bytecodes[SETUP_LOOP.opc] = SETUP_LOOP

class SETUP_EXCEPT(_opbases.JRel):
    op = 121
    opc = 'y'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        block_push(3)


_bytecodes[SETUP_EXCEPT.opc] = SETUP_EXCEPT

class SETUP_FINALLY(_opbases.JRel):
    op = 122
    opc = 'z'

    def __init__(self, csorarg=None, code=None):
        if csorarg is not None:
            if code is not None:
                _opbases.JRel.__init__(self, csorarg, code)
            else:
                self.label = _Label()
                self.user_init(csorarg)
        else:
            self.label = _Label()
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        block_push(2)


_bytecodes[SETUP_FINALLY.opc] = SETUP_FINALLY

class LOAD_FAST(_opbases.LocalOpcode):
    op = 124
    opc = '|'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.LocalOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.append(self)

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        push()


_bytecodes[LOAD_FAST.opc] = LOAD_FAST

class STORE_FAST(_opbases.LocalOpcode):
    op = 125
    opc = '}'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.LocalOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop()


_bytecodes[STORE_FAST.opc] = STORE_FAST

class DELETE_FAST(_opbases.LocalOpcode):
    op = 126
    opc = '~'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.LocalOpcode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack.pop()

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[DELETE_FAST.opc] = DELETE_FAST

class SET_LINENO(_opbases.GenericThreeByteCode):
    op = 127
    opc = '\x7f'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        pass

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pass


_bytecodes[SET_LINENO.opc] = SET_LINENO

class RAISE_VARARGS(_opbases.GenericThreeByteCode):
    op = 130
    opc = b'\x82'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        raise 'Exception!'

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(self.arg)


_bytecodes[RAISE_VARARGS.opc] = RAISE_VARARGS

class CALL_FUNCTION(_opbases.GenericThreeByteCode):
    op = 131
    opc = b'\x83'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        num_keyword_args = self.arg >> 8
        num_regular_args = self.arg & 255
        stack[(-2 * num_keyword_args - num_regular_args - 1):] = [self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        num_keyword_args = (self.arg & 65280) >> 8
        num_regular_args = self.arg & 255
        pop(2 * num_keyword_args + num_regular_args)


_bytecodes[CALL_FUNCTION.opc] = CALL_FUNCTION

class MAKE_FUNCTION(_opbases.GenericThreeByteCode):
    op = 132
    opc = b'\x84'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack[(-self.arg - 1):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(1 + self.arg)


_bytecodes[MAKE_FUNCTION.opc] = MAKE_FUNCTION

class BUILD_SLICE(_opbases.GenericThreeByteCode):
    op = 133
    opc = b'\x85'

    def __init__(self, csorarg, code=None):
        if code is not None:
            _opbases.GenericThreeByteCode.__init__(self, csorarg, code)
        else:
            self.user_init(csorarg)
        return

    def execute(self, stack):
        stack[(-self.arg):] = [
         self]

    def stack_manipulate(self, push, pop, block_push, block_pop, tracker):
        pop(self.arg - 1)


_bytecodes[BUILD_SLICE.opc] = BUILD_SLICE