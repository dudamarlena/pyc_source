# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/container/action_script.py
# Compiled at: 2010-01-20 18:00:26
"""
SWF (Macromedia/Adobe Flash) file parser.

Documentation:

 - Alexis' SWF Reference:
   http://www.m2osw.com/swf_alexref.html

Author: Sebastien Ponce
Creation date: 26 April 2008
"""
from hachoir_core.field import FieldSet, ParserError, Bit, Bits, UInt8, UInt32, Int16, UInt16, Float32, CString, RawBytes
from hachoir_core.field.float import FloatExponent
from struct import unpack

class FlashFloat64(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield Bits(self, 'mantisa_high', 20)
        yield FloatExponent(self, 'exponent', 11)
        yield Bit(self, 'negative')
        yield Bits(self, 'mantisa_low', 32)

    def createValue(self):
        bytes = self.parent.stream.readBytes(self.absolute_address, self.size // 8)
        bytes = bytes[4:8] + bytes[0:4]
        return unpack('<d', bytes)[0]


TYPE_INFO = {0: (CString, 'Cstring[]'), 1: (Float32, 'Float[]'), 2: (None, 'Null[]'), 3: (None, 'Undefined[]'), 4: (UInt8, 'Register[]'), 5: (UInt8, 'Boolean[]'), 6: (FlashFloat64, 'Double[]'), 7: (UInt32, 'Integer[]'), 8: (UInt8, 'Dictionnary_Lookup_Index[]'), 9: (UInt16, 'Large_Dictionnary_Lookup_Index[]')}

def parseBranch(parent, size):
    yield Int16(parent, 'offset')


def parseDeclareFunction(parent, size):
    yield CString(parent, 'name')
    argCount = UInt16(parent, 'arg_count')
    yield argCount
    for i in range(argCount.value):
        yield CString(parent, 'arg[]')

    yield UInt16(parent, 'function_length')


def parseDeclareFunctionV7(parent, size):
    yield CString(parent, 'name')
    argCount = UInt16(parent, 'arg_count')
    yield argCount
    yield UInt8(parent, 'reg_count')
    yield Bits(parent, 'reserved', 7)
    yield Bit(parent, 'preload_global')
    yield Bit(parent, 'preload_parent')
    yield Bit(parent, 'preload_root')
    yield Bit(parent, 'suppress_super')
    yield Bit(parent, 'preload_super')
    yield Bit(parent, 'suppress_arguments')
    yield Bit(parent, 'preload_arguments')
    yield Bit(parent, 'suppress_this')
    yield Bit(parent, 'preload_this')
    for i in range(argCount.value):
        yield UInt8(parent, 'register[]')
        yield CString(parent, 'arg[]')

    yield UInt16(parent, 'function_length')


def parseTry(parent, size):
    yield Bits(parent, 'reserved', 5)
    catchInReg = Bit(parent, 'catch_in_register')
    yield catchInReg
    yield Bit(parent, 'finally')
    yield Bit(parent, 'catch')
    yield UInt8(parent, 'try_size')
    yield UInt8(parent, 'catch_size')
    yield UInt8(parent, 'finally_size')
    if catchInReg.value:
        yield CString(parent, 'name')
    else:
        yield UInt8(parent, 'register')


def parsePushData(parent, size):
    while not parent.eof:
        codeobj = UInt8(parent, 'data_type[]')
        yield codeobj
        code = codeobj.value
        if code not in TYPE_INFO:
            raise ParserError('Unknown type in Push_Data : ' + hex(code))
        (parser, name) = TYPE_INFO[code]
        if parser:
            yield parser(parent, name)


def parseSetTarget(parent, size):
    yield CString(parent, 'target')


def parseWith(parent, size):
    yield UInt16(parent, 'size')


def parseGetURL(parent, size):
    yield CString(parent, 'url')
    yield CString(parent, 'target')


def parseGetURL2(parent, size):
    yield UInt8(parent, 'method')


def parseGotoExpression(parent, size):
    yield UInt8(parent, 'play')


def parseGotoFrame(parent, size):
    yield UInt16(parent, 'frame_no')


def parseGotoLabel(parent, size):
    yield CString(parent, 'label')


def parseWaitForFrame(parent, size):
    yield UInt16(parent, 'frame')
    yield UInt8(parent, 'skip')


def parseWaitForFrameDyn(parent, size):
    yield UInt8(parent, 'skip')


def parseDeclareDictionnary(parent, size):
    count = UInt16(parent, 'count')
    yield count
    for i in range(count.value):
        yield CString(parent, 'dictionnary[]')


def parseStoreRegister(parent, size):
    yield UInt8(parent, 'register')


def parseStrictMode(parent, size):
    yield UInt8(parent, 'strict')


class Instruction(FieldSet):
    __module__ = __name__
    ACTION_INFO = {0: ('end[]', 'End', None), 153: ('Branch_Always[]', 'Branch Always', parseBranch), 157: ('Branch_If_True[]', 'Branch If True', parseBranch), 61: ('Call_Function[]', 'Call Function', None), 82: ('Call_Method[]', 'Call Method', None), 155: ('Declare_Function[]', 'Declare Function', parseDeclareFunction), 142: ('Declare_Function_V7[]', 'Declare Function (V7)', parseDeclareFunctionV7), 62: ('Return[]', 'Return', None), 42: ('Throw[]', 'Throw', None), 143: ('Try[]', 'Try', parseTry), 76: ('Duplicate[]', 'Duplicate', None), 150: ('Push_Data[]', 'Push Data', parsePushData), 77: ('Swap[]', 'Swap', None), 139: ('Set_Target[]', 'Set Target', parseSetTarget), 32: ('Set_Target_dynamic[]', 'Set Target (dynamic)', None), 148: ('With[]', 'With', parseWith), 158: ('Call_Frame[]', 'Call Frame', None), 131: ('Get_URL[]', 'Get URL', parseGetURL), 154: ('Get_URL2[]', 'Get URL2', parseGetURL2), 159: ('Goto_Expression[]', 'Goto Expression', parseGotoExpression), 129: ('Goto_Frame[]', 'Goto Frame', parseGotoFrame), 140: ('Goto_Label[]', 'Goto Label', parseGotoLabel), 4: ('Next_Frame[]', 'Next Frame', None), 6: ('Play[]', 'Play', None), 5: ('Previous_Frame[]', 'Previous Frame', None), 7: ('Stop[]', 'Stop', None), 8: ('Toggle_Quality[]', 'Toggle Quality', None), 138: ('Wait_For_Frame[]', 'Wait For Frame', parseWaitForFrame), 141: ('Wait_For_Frame_dynamic[]', 'Wait For Frame (dynamic)', parseWaitForFrameDyn), 9: ('Stop_Sound[]', 'Stop Sound', None), 10: ('Add[]', 'Add', None), 71: ('Add_typed[]', 'Add (typed)', None), 81: ('Decrement[]', 'Decrement', None), 13: ('Divide[]', 'Divide', None), 80: ('Increment[]', 'Increment', None), 24: ('Integral_Part[]', 'Integral Part', None), 63: ('Modulo[]', 'Modulo', None), 12: ('Multiply[]', 'Multiply', None), 74: ('Number[]', 'Number', None), 11: ('Subtract[]', 'Subtract', None), 14: ('Equal[]', 'Equal', None), 73: ('Equal_typed[]', 'Equal (typed)', None), 102: ('Strict_Equal[]', 'Strict Equal', None), 103: ('Greater_Than_typed[]', 'Greater Than (typed)', None), 15: ('Less_Than[]', 'Less Than', None), 72: ('Less_Than_typed[]', 'Less Than (typed)', None), 19: ('String_Equal[]', 'String Equal', None), 104: ('String_Greater_Than[]', 'String Greater Than', None), 41: ('String_Less_Than[]', 'String Less Than', None), 96: ('And[]', 'And', None), 16: ('Logical_And[]', 'Logical And', None), 18: ('Logical_Not[]', 'Logical Not', None), 17: ('Logical_Or[]', 'Logical Or', None), 97: ('Or[]', 'Or', None), 99: ('Shift_Left[]', 'Shift Left', None), 100: ('Shift_Right[]', 'Shift Right', None), 101: ('Shift_Right_Unsigned[]', 'Shift Right Unsigned', None), 98: ('Xor[]', 'Xor', None), 51: ('Chr[]', 'Chr', None), 55: ('Chr_multi-bytes[]', 'Chr (multi-bytes)', None), 33: ('Concatenate_Strings[]', 'Concatenate Strings', None), 50: ('Ord[]', 'Ord', None), 54: ('Ord_multi-bytes[]', 'Ord (multi-bytes)', None), 75: ('String[]', 'String', None), 20: ('String_Length[]', 'String Length', None), 49: ('String_Length_multi-bytes[]', 'String Length (multi-bytes)', None), 21: ('SubString[]', 'SubString', None), 53: ('SubString_multi-bytes[]', 'SubString (multi-bytes)', None), 34: ('Get_Property[]', 'Get Property', None), 35: ('Set_Property[]', 'Set Property', None), 43: ('Cast_Object[]', 'Cast Object', None), 66: ('Declare_Array[]', 'Declare Array', None), 136: ('Declare_Dictionary[]', 'Declare Dictionary', parseDeclareDictionnary), 67: ('Declare_Object[]', 'Declare Object', None), 58: ('Delete[]', 'Delete', None), 59: ('Delete_All[]', 'Delete All', None), 36: ('Duplicate_Sprite[]', 'Duplicate Sprite', None), 70: ('Enumerate[]', 'Enumerate', None), 85: ('Enumerate_Object[]', 'Enumerate Object', None), 105: ('Extends[]', 'Extends', None), 78: ('Get_Member[]', 'Get Member', None), 69: ('Get_Target[]', 'Get Target', None), 44: ('Implements[]', 'Implements', None), 84: ('Instance_Of[]', 'Instance Of', None), 64: ('New[]', 'New', None), 83: ('New_Method[]', 'New Method', None), 37: ('Remove_Sprite[]', 'Remove Sprite', None), 79: ('Set_Member[]', 'Set Member', None), 68: ('Type_Of[]', 'Type Of', None), 65: ('Declare_Local_Variable[]', 'Declare Local Variable', None), 28: ('Get_Variable[]', 'Get Variable', None), 60: ('Set_Local_Variable[]', 'Set Local Variable', None), 29: ('Set_Variable[]', 'Set Variable', None), 45: ('FSCommand2[]', 'FSCommand2', None), 52: ('Get_Timer[]', 'Get Timer', None), 48: ('Random[]', 'Random', None), 39: ('Start_Drag[]', 'Start Drag', None), 40: ('Stop_Drag[]', 'Stop Drag', None), 135: ('Store_Register[]', 'Store Register', parseStoreRegister), 137: ('Strict_Mode[]', 'Strict Mode', parseStrictMode), 38: ('Trace[]', 'Trace', None)}

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        code = self['action_id'].value
        if code & 128:
            self._size = (3 + self['action_length'].value) * 8
        else:
            self._size = 8
        if code in self.ACTION_INFO:
            (self._name, self._description, self.parser) = self.ACTION_INFO[code]
        else:
            self.parser = None
        return

    def createFields(self):
        yield Bits(self, 'action_id', 8)
        if not self['action_id'].value & 128:
            return
        yield UInt16(self, 'action_length')
        size = self['action_length'].value
        if not size:
            return
        if self.parser:
            for field in self.parser(self, size):
                yield field

        else:
            yield RawBytes(self, 'action_data', size)

    def createDescription(self):
        return self._description

    def __str__(self):
        r = str(self._description)
        for f in self:
            if f.name not in ('action_id', 'action_length', 'count') and not f.name.startswith('data_type'):
                r = r + '\n   ' + str((self.address + f.address) / 8) + ' ' + str(f.name) + '=' + str(f.value)

        return r


class ActionScript(FieldSet):
    __module__ = __name__

    def createFields(self):
        while not self.eof:
            yield Instruction(self, 'instr[]')

    def __str__(self):
        r = ''
        for f in self:
            r = r + str(f.address / 8) + ' ' + str(f) + '\n'

        return r


def parseActionScript(parent, size):
    yield ActionScript(parent, 'action', size=size * 8)