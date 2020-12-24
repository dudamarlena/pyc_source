# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/program/java.py
# Compiled at: 2009-09-07 17:44:28
"""
Compiled Java classes parser.

Author: Thomas de Grenier de Latour (TGL) <degrenier@easyconnect.fr>
Creation: 2006/11/01
Last-update: 2006/11/06

Introduction:
 * This parser is for compiled Java classes, aka .class files.  What is nice
   with this format is that it is well documented in the official Java VM specs.
 * Some fields, and most field sets, have dynamic sizes, and there is no offset
   to directly jump from an header to a given section, or anything like that.
   It means that accessing a field at the end of the file requires that you've
   already parsed almost the whole file.  That's not very efficient, but it's
   okay given the usual size of .class files (usually a few KB).
 * Most fields are just indexes of some "constant pool" entries, which holds
   most constant datas of the class.  And constant pool entries reference other
   constant pool entries, etc.  Hence, a raw display of this fields only shows
   integers and is not really understandable.  Because of that, this parser
   comes with two important custom field classes:
    - CPInfo are constant pool entries.  They have a type ("Utf8", "Methodref",
      etc.), and some contents fields depending on this type.  They also have a
      "__str__()" method, which returns a syntetic view of this contents.
    - CPIndex are constant pool indexes (UInt16).  It is possible to specify
      what type of CPInfo they are allowed to points to.  They also have a
      custom display method, usually printing something like "->  foo", where
      foo is the str() of their target CPInfo.

References:
 * The Java Virtual Machine Specification, 2nd edition, chapter 4, in HTML:
   http://java.sun.com/docs/books/vmspec/2nd-edition/html/ClassFile.doc.html
    => That's the spec i've been implementing so far. I think it is format
       version 46.0 (JDK 1.2).
 * The Java Virtual Machine Specification, 2nd edition, chapter 4, in PDF:
   http://java.sun.com/docs/books/vmspec/2nd-edition/ClassFileFormat.pdf
    => don't trust the URL, this PDF version is more recent than the HTML one.
       It highligths some recent additions to the format (i don't know the
       exact version though), which are not yet implemented in this parser.
 * The Java Virtual Machine Specification, chapter 4:
   http://java.sun.com/docs/books/vmspec/html/ClassFile.doc.html
    => describes an older format, probably version 45.3 (JDK 1.1).

TODO/FIXME:
 * Google for some existing free .class files parsers, to get more infos on
   the various formats differences, etc.
 * Write/compile some good tests cases.
 * Rework pretty-printing of CPIndex fields.  This str() thing sinks.
 * Add support of formats other than 46.0 (45.3 seems to already be ok, but
   there are things to add for later formats).
 * Make parsing robust: currently, the parser will die on asserts as soon as
   something seems wrong.  It should rather be tolerant, print errors/warnings,
   and try its best to continue.  Check how error-handling is done in other
   parsers.
 * Gettextize the whole thing.
 * Check whether Float32/64 are really the same as Java floats/double. PEP-0754
   says that handling of +/-infinity and NaN is very implementation-dependent.
   Also check how this values are displayed.
 * Make the parser edition-proof.  For instance, editing a constant-pool string
   should update the length field of it's entry, etc.  Sounds like a huge work.
"""
from hachoir_parser import Parser
from hachoir_core.field import ParserError, FieldSet, StaticFieldSet, Enum, RawBytes, PascalString16, Float32, Float64, Int8, UInt8, Int16, UInt16, Int32, UInt32, Int64, Bit, NullBits
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_core.tools import paddingSize

def parse_flags(flags, flags_dict, show_unknown_flags=True, separator=' '):
    """
    Parses an integer representing a set of flags.  The known flags are
    stored with their bit-mask in a dictionnary.  Returns a string.
    """
    flags_list = []
    mask = 1
    while mask <= flags:
        if flags & mask:
            if mask in flags_dict:
                flags_list.append(flags_dict[mask])
            elif show_unknown_flags:
                flags_list.append('???')
        mask = mask << 1

    return separator.join(flags_list)


code_to_type_name = {'B': 'byte', 'C': 'char', 'D': 'double', 'F': 'float', 'I': 'int', 'J': 'long', 'S': 'short', 'Z': 'boolean', 'V': 'void'}

def eat_descriptor(descr):
    """
    Read head of a field/method descriptor.  Returns a pair of strings, where
    the first one is a human-readable string representation of the first found
    type, and the second one is the tail of the parameter.
    """
    global code_to_type_name
    array_dim = 0
    while descr[0] == '[':
        array_dim += 1
        descr = descr[1:]

    if descr[0] == 'L':
        try:
            end = descr.find(';')
        except:
            raise ParserError('Not a valid descriptor string: ' + descr)
        else:
            type = descr[1:end]
            descr = descr[end:]
    else:
        try:
            type = code_to_type_name[descr[0]]
        except KeyError:
            raise ParserError('Not a valid descriptor string: %s' % descr)

    return (
     type.replace('/', '.') + array_dim * '[]', descr[1:])


def parse_field_descriptor(descr, name=None):
    """
    Parse a field descriptor (single type), and returns it as human-readable
    string representation.
    """
    assert descr
    (type, tail) = eat_descriptor(descr)
    assert not tail
    if name:
        return type + ' ' + name
    else:
        return type


def parse_method_descriptor(descr, name=None):
    """
    Parse a method descriptor (params type and return type), and returns it
    as human-readable string representation.
    """
    assert descr and descr[0] == '('
    descr = descr[1:]
    params_list = []
    while descr[0] != ')':
        (param, descr) = eat_descriptor(descr)
        params_list.append(param)

    (type, tail) = eat_descriptor(descr[1:])
    assert not tail
    params = (', ').join(params_list)
    if name:
        return '%s %s(%s)' % (type, name, params)
    else:
        return '%s (%s)' % (type, params)


def parse_any_descriptor(descr, name=None):
    """
    Parse either a field or method descriptor, and returns it as human-
    readable string representation.
    """
    assert descr
    if descr[0] == '(':
        return parse_method_descriptor(descr, name)
    else:
        return parse_field_descriptor(descr, name)


class FieldArray(FieldSet):
    """
    Holds a fixed length array of fields which all have the same type.  This
    type may be variable-length.  Each field will be named "foo[x]" (with x
    starting at 0).
    """
    __module__ = __name__

    def __init__(self, parent, name, elements_class, length, **elements_extra_args):
        """Create a FieldArray of <length> fields of class <elements_class>,
        named "<name>[x]".  The **elements_extra_args will be passed to the
        constructor of each field when yielded."""
        FieldSet.__init__(self, parent, name)
        self.array_elements_class = elements_class
        self.array_length = length
        self.array_elements_extra_args = elements_extra_args

    def createFields(self):
        for i in range(0, self.array_length):
            yield self.array_elements_class(self, ('%s[%d]' % (self.name, i)), **self.array_elements_extra_args)


class ConstantPool(FieldSet):
    """
    ConstantPool is similar to a FieldArray of CPInfo fields, but:
    - numbering starts at 1 instead of zero
    - some indexes are skipped (after Long or Double entries)
    """
    __module__ = __name__

    def __init__(self, parent, name, length):
        FieldSet.__init__(self, parent, name)
        self.constant_pool_length = length

    def createFields(self):
        i = 1
        while i < self.constant_pool_length:
            name = '%s[%d]' % (self.name, i)
            yield CPInfo(self, name)
            i += 1
            if self[name].constant_type in ('Long', 'Double'):
                i += 1


class CPIndex(UInt16):
    """
    Holds index of a constant pool entry.
    """
    __module__ = __name__

    def __init__(self, parent, name, description=None, target_types=None, target_text_handler=lambda x: x, allow_zero=False):
        """
        Initialize a CPIndex.
        - target_type is the tuple of expected type for the target CPInfo
          (if None, then there will be no type check)
        - target_text_handler is a string transformation function used for
          pretty printing the target str() result
        - allow_zero states whether null index is allowed (sometimes, constant
          pool index is optionnal)
        """
        UInt16.__init__(self, parent, name, description)
        if isinstance(target_types, str):
            self.target_types = (
             target_types,)
        else:
            self.target_types = target_types
        self.allow_zero = allow_zero
        self.target_text_handler = target_text_handler
        self.getOriginalDisplay = lambda : self.value

    def createDisplay(self):
        cp_entry = self.get_cp_entry()
        if self.allow_zero and not cp_entry:
            return 'ZERO'
        assert cp_entry
        return '-> ' + self.target_text_handler(str(cp_entry))

    def get_cp_entry(self):
        """
        Returns the target CPInfo field.
        """
        assert self.value < self['/constant_pool_count'].value
        if self.allow_zero and not self.value:
            return
        cp_entry = self[('/constant_pool/constant_pool[%d]' % self.value)]
        assert isinstance(cp_entry, CPInfo)
        if self.target_types:
            assert cp_entry.constant_type in self.target_types
        return cp_entry


class JavaOpcode(FieldSet):
    __module__ = __name__
    OPSIZE = 0

    def __init__(self, parent, name, op, desc):
        FieldSet.__init__(self, parent, name)
        if self.OPSIZE != 0:
            self._size = self.OPSIZE * 8
        self.op = op
        self.desc = desc

    def createDisplay(self):
        return self.op

    def createDescription(self):
        return self.desc

    def createValue(self):
        return self.createDisplay()


class OpcodeNoArgs(JavaOpcode):
    __module__ = __name__
    OPSIZE = 1

    def createFields(self):
        yield UInt8(self, 'opcode')


class OpcodeCPIndex(JavaOpcode):
    __module__ = __name__
    OPSIZE = 3

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield CPIndex(self, 'index')

    def createDisplay(self):
        return '%s(%i)' % (self.op, self['index'].value)


class OpcodeCPIndexShort(JavaOpcode):
    __module__ = __name__
    OPSIZE = 2

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield UInt8(self, 'index')

    def createDisplay(self):
        return '%s(%i)' % (self.op, self['index'].value)


class OpcodeIndex(JavaOpcode):
    __module__ = __name__
    OPSIZE = 2

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield UInt8(self, 'index')

    def createDisplay(self):
        return '%s(%i)' % (self.op, self['index'].value)


class OpcodeShortJump(JavaOpcode):
    __module__ = __name__
    OPSIZE = 3

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield Int16(self, 'offset')

    def createDisplay(self):
        return '%s(%s)' % (self.op, self['offset'].value)


class OpcodeLongJump(JavaOpcode):
    __module__ = __name__
    OPSIZE = 5

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield Int32(self, 'offset')

    def createDisplay(self):
        return '%s(%s)' % (self.op, self['offset'].value)


class OpcodeSpecial_bipush(JavaOpcode):
    __module__ = __name__
    OPSIZE = 2

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield Int8(self, 'value')

    def createDisplay(self):
        return '%s(%s)' % (self.op, self['value'].value)


class OpcodeSpecial_sipush(JavaOpcode):
    __module__ = __name__
    OPSIZE = 3

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield Int16(self, 'value')

    def createDisplay(self):
        return '%s(%s)' % (self.op, self['value'].value)


class OpcodeSpecial_iinc(JavaOpcode):
    __module__ = __name__
    OPSIZE = 3

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield UInt8(self, 'index')
        yield Int8(self, 'value')

    def createDisplay(self):
        return '%s(%i,%i)' % (self.op, self['index'].value, self['value'].value)


class OpcodeSpecial_wide(JavaOpcode):
    __module__ = __name__

    def createFields(self):
        yield UInt8(self, 'opcode')
        new_op = UInt8(self, 'new_opcode')
        yield new_op
        op = new_op._description = JavaBytecode.OPCODE_TABLE.get(new_op.value, ['reserved', None, 'Reserved'])[0]
        yield UInt16(self, 'index')
        if op == 'iinc':
            yield Int16(self, 'value')
            self.createDisplay = lambda self: '%s(%i,%i)' % (self.op, self['index'].value, self['value'].value)
        else:
            self.createDisplay = lambda self: '%s(%i)' % (self.op, self['index'].value)
        return


class OpcodeSpecial_invokeinterface(JavaOpcode):
    __module__ = __name__
    OPSIZE = 5

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield CPIndex(self, 'index')
        yield UInt8(self, 'count')
        yield UInt8(self, 'zero', 'Must be zero.')

    def createDisplay(self):
        return '%s(%i,%i,%i)' % (self.op, self['index'].value, self['count'].value, self['zero'].value)


class OpcodeSpecial_newarray(JavaOpcode):
    __module__ = __name__
    OPSIZE = 2

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield Enum(UInt8(self, 'atype'), {4: 'boolean', 5: 'char', 6: 'float', 7: 'double', 8: 'byte', 9: 'short', 10: 'int', 11: 'long'})

    def createDisplay(self):
        return '%s(%s)' % (self.op, self['atype'].createDisplay())


class OpcodeSpecial_multianewarray(JavaOpcode):
    __module__ = __name__
    OPSIZE = 4

    def createFields(self):
        yield UInt8(self, 'opcode')
        yield CPIndex(self, 'index')
        yield UInt8(self, 'dimensions')

    def createDisplay(self):
        return '%s(%i,%i)' % (self.op, self['index'].value, self['dimensions'].value)


class OpcodeSpecial_tableswitch(JavaOpcode):
    __module__ = __name__

    def createFields(self):
        yield UInt8(self, 'opcode')
        pad = paddingSize(self.address + 8, 32)
        if pad:
            yield NullBits(self, 'padding', pad)
        yield Int32(self, 'default')
        low = Int32(self, 'low')
        yield low
        high = Int32(self, 'high')
        yield high
        for i in range(high.value - low.value + 1):
            yield Int32(self, 'offset[]')

    def createDisplay(self):
        return '%s(%i,%i,%i,...)' % (self.op, self['default'].value, self['low'].value, self['high'].value)


class OpcodeSpecial_lookupswitch(JavaOpcode):
    __module__ = __name__

    def createFields(self):
        yield UInt8(self, 'opcode')
        pad = paddingSize(self.address + 8, 32)
        if pad:
            yield NullBits(self, 'padding', pad)
        yield Int32(self, 'default')
        n = Int32(self, 'npairs')
        yield n
        for i in range(n.value):
            yield Int32(self, 'match[]')
            yield Int32(self, 'offset[]')

    def createDisplay(self):
        return '%s(%i,%i,...)' % (self.op, self['default'].value, self['npairs'].value)


class JavaBytecode(FieldSet):
    __module__ = __name__
    OPCODE_TABLE = {0: ('nop', OpcodeNoArgs, 'performs no operation. Stack: [No change]'), 1: ('aconst_null', OpcodeNoArgs, "pushes a 'null' reference onto the stack. Stack: -> null"), 2: ('iconst_m1', OpcodeNoArgs, 'loads the int value -1 onto the stack. Stack: -> -1'), 3: ('iconst_0', OpcodeNoArgs, 'loads the int value 0 onto the stack. Stack: -> 0'), 4: ('iconst_1', OpcodeNoArgs, 'loads the int value 1 onto the stack. Stack: -> 1'), 5: ('iconst_2', OpcodeNoArgs, 'loads the int value 2 onto the stack. Stack: -> 2'), 6: ('iconst_3', OpcodeNoArgs, 'loads the int value 3 onto the stack. Stack: -> 3'), 7: ('iconst_4', OpcodeNoArgs, 'loads the int value 4 onto the stack. Stack: -> 4'), 8: ('iconst_5', OpcodeNoArgs, 'loads the int value 5 onto the stack. Stack: -> 5'), 9: ('lconst_0', OpcodeNoArgs, 'pushes the long 0 onto the stack. Stack: -> 0L'), 10: ('lconst_1', OpcodeNoArgs, 'pushes the long 1 onto the stack. Stack: -> 1L'), 11: ('fconst_0', OpcodeNoArgs, "pushes '0.0f' onto the stack. Stack: -> 0.0f"), 12: ('fconst_1', OpcodeNoArgs, "pushes '1.0f' onto the stack. Stack: -> 1.0f"), 13: ('fconst_2', OpcodeNoArgs, "pushes '2.0f' onto the stack. Stack: -> 2.0f"), 14: ('dconst_0', OpcodeNoArgs, "pushes the constant '0.0' onto the stack. Stack: -> 0.0"), 15: ('dconst_1', OpcodeNoArgs, "pushes the constant '1.0' onto the stack. Stack: -> 1.0"), 16: ('bipush', OpcodeSpecial_bipush, 'pushes the signed 8-bit integer argument onto the stack. Stack: -> value'), 17: ('sipush', OpcodeSpecial_sipush, 'pushes the signed 16-bit integer argument onto the stack. Stack: -> value'), 18: ('ldc', OpcodeCPIndexShort, 'pushes a constant from a constant pool (String, int, float or class type) onto the stack. Stack: -> value'), 19: ('ldc_w', OpcodeCPIndex, 'pushes a constant from a constant pool (String, int, float or class type) onto the stack. Stack: -> value'), 20: ('ldc2_w', OpcodeCPIndex, 'pushes a constant from a constant pool (double or long) onto the stack. Stack: -> value'), 21: ('iload', OpcodeIndex, "loads an int 'value' from a local variable '#index'. Stack: -> value"), 22: ('lload', OpcodeIndex, "loads a long value from a local variable '#index'. Stack: -> value"), 23: ('fload', OpcodeIndex, "loads a float 'value' from a local variable '#index'. Stack: -> value"), 24: ('dload', OpcodeIndex, "loads a double 'value' from a local variable '#index'. Stack: -> value"), 25: ('aload', OpcodeIndex, "loads a reference onto the stack from a local variable '#index'. Stack: -> objectref"), 26: ('iload_0', OpcodeNoArgs, "loads an int 'value' from variable 0. Stack: -> value"), 27: ('iload_1', OpcodeNoArgs, "loads an int 'value' from variable 1. Stack: -> value"), 28: ('iload_2', OpcodeNoArgs, "loads an int 'value' from variable 2. Stack: -> value"), 29: ('iload_3', OpcodeNoArgs, "loads an int 'value' from variable 3. Stack: -> value"), 30: ('lload_0', OpcodeNoArgs, 'load a long value from a local variable 0. Stack: -> value'), 31: ('lload_1', OpcodeNoArgs, 'load a long value from a local variable 1. Stack: -> value'), 32: ('lload_2', OpcodeNoArgs, 'load a long value from a local variable 2. Stack: -> value'), 33: ('lload_3', OpcodeNoArgs, 'load a long value from a local variable 3. Stack: -> value'), 34: ('fload_0', OpcodeNoArgs, "loads a float 'value' from local variable 0. Stack: -> value"), 35: ('fload_1', OpcodeNoArgs, "loads a float 'value' from local variable 1. Stack: -> value"), 36: ('fload_2', OpcodeNoArgs, "loads a float 'value' from local variable 2. Stack: -> value"), 37: ('fload_3', OpcodeNoArgs, "loads a float 'value' from local variable 3. Stack: -> value"), 38: ('dload_0', OpcodeNoArgs, 'loads a double from local variable 0. Stack: -> value'), 39: ('dload_1', OpcodeNoArgs, 'loads a double from local variable 1. Stack: -> value'), 40: ('dload_2', OpcodeNoArgs, 'loads a double from local variable 2. Stack: -> value'), 41: ('dload_3', OpcodeNoArgs, 'loads a double from local variable 3. Stack: -> value'), 42: ('aload_0', OpcodeNoArgs, 'loads a reference onto the stack from local variable 0. Stack: -> objectref'), 43: ('aload_1', OpcodeNoArgs, 'loads a reference onto the stack from local variable 1. Stack: -> objectref'), 44: ('aload_2', OpcodeNoArgs, 'loads a reference onto the stack from local variable 2. Stack: -> objectref'), 45: ('aload_3', OpcodeNoArgs, 'loads a reference onto the stack from local variable 3. Stack: -> objectref'), 46: ('iaload', OpcodeNoArgs, 'loads an int from an array. Stack: arrayref, index -> value'), 47: ('laload', OpcodeNoArgs, 'load a long from an array. Stack: arrayref, index -> value'), 48: ('faload', OpcodeNoArgs, 'loads a float from an array. Stack: arrayref, index -> value'), 49: ('daload', OpcodeNoArgs, 'loads a double from an array. Stack: arrayref, index -> value'), 50: ('aaload', OpcodeNoArgs, 'loads onto the stack a reference from an array. Stack: arrayref, index -> value'), 51: ('baload', OpcodeNoArgs, 'loads a byte or Boolean value from an array. Stack: arrayref, index -> value'), 52: ('caload', OpcodeNoArgs, 'loads a char from an array. Stack: arrayref, index -> value'), 53: ('saload', OpcodeNoArgs, 'load short from array. Stack: arrayref, index -> value'), 54: ('istore', OpcodeIndex, "store int 'value' into variable '#index'. Stack: value ->"), 55: ('lstore', OpcodeIndex, "store a long 'value' in a local variable '#index'. Stack: value ->"), 56: ('fstore', OpcodeIndex, "stores a float 'value' into a local variable '#index'. Stack: value ->"), 57: ('dstore', OpcodeIndex, "stores a double 'value' into a local variable '#index'. Stack: value ->"), 58: ('astore', OpcodeIndex, "stores a reference into a local variable '#index'. Stack: objectref ->"), 59: ('istore_0', OpcodeNoArgs, "store int 'value' into variable 0. Stack: value ->"), 60: ('istore_1', OpcodeNoArgs, "store int 'value' into variable 1. Stack: value ->"), 61: ('istore_2', OpcodeNoArgs, "store int 'value' into variable 2. Stack: value ->"), 62: ('istore_3', OpcodeNoArgs, "store int 'value' into variable 3. Stack: value ->"), 63: ('lstore_0', OpcodeNoArgs, "store a long 'value' in a local variable 0. Stack: value ->"), 64: ('lstore_1', OpcodeNoArgs, "store a long 'value' in a local variable 1. Stack: value ->"), 65: ('lstore_2', OpcodeNoArgs, "store a long 'value' in a local variable 2. Stack: value ->"), 66: ('lstore_3', OpcodeNoArgs, "store a long 'value' in a local variable 3. Stack: value ->"), 67: ('fstore_0', OpcodeNoArgs, "stores a float 'value' into local variable 0. Stack: value ->"), 68: ('fstore_1', OpcodeNoArgs, "stores a float 'value' into local variable 1. Stack: value ->"), 69: ('fstore_2', OpcodeNoArgs, "stores a float 'value' into local variable 2. Stack: value ->"), 70: ('fstore_3', OpcodeNoArgs, "stores a float 'value' into local variable 3. Stack: value ->"), 71: ('dstore_0', OpcodeNoArgs, 'stores a double into local variable 0. Stack: value ->'), 72: ('dstore_1', OpcodeNoArgs, 'stores a double into local variable 1. Stack: value ->'), 73: ('dstore_2', OpcodeNoArgs, 'stores a double into local variable 2. Stack: value ->'), 74: ('dstore_3', OpcodeNoArgs, 'stores a double into local variable 3. Stack: value ->'), 75: ('astore_0', OpcodeNoArgs, 'stores a reference into local variable 0. Stack: objectref ->'), 76: ('astore_1', OpcodeNoArgs, 'stores a reference into local variable 1. Stack: objectref ->'), 77: ('astore_2', OpcodeNoArgs, 'stores a reference into local variable 2. Stack: objectref ->'), 78: ('astore_3', OpcodeNoArgs, 'stores a reference into local variable 3. Stack: objectref ->'), 79: ('iastore', OpcodeNoArgs, 'stores an int into an array. Stack: arrayref, index, value ->'), 80: ('lastore', OpcodeNoArgs, 'store a long to an array. Stack: arrayref, index, value ->'), 81: ('fastore', OpcodeNoArgs, 'stores a float in an array. Stack: arreyref, index, value ->'), 82: ('dastore', OpcodeNoArgs, 'stores a double into an array. Stack: arrayref, index, value ->'), 83: ('aastore', OpcodeNoArgs, 'stores into a reference to an array. Stack: arrayref, index, value ->'), 84: ('bastore', OpcodeNoArgs, 'stores a byte or Boolean value into an array. Stack: arrayref, index, value ->'), 85: ('castore', OpcodeNoArgs, 'stores a char into an array. Stack: arrayref, index, value ->'), 86: ('sastore', OpcodeNoArgs, 'store short to array. Stack: arrayref, index, value ->'), 87: ('pop', OpcodeNoArgs, 'discards the top value on the stack. Stack: value ->'), 88: ('pop2', OpcodeNoArgs, 'discards the top two values on the stack (or one value, if it is a double or long). Stack: {value2, value1} ->'), 89: ('dup', OpcodeNoArgs, 'duplicates the value on top of the stack. Stack: value -> value, value'), 90: ('dup_x1', OpcodeNoArgs, 'inserts a copy of the top value into the stack two values from the top. Stack: value2, value1 -> value1, value2, value1'), 91: ('dup_x2', OpcodeNoArgs, 'inserts a copy of the top value into the stack two (if value2 is double or long it takes up the entry of value3, too) or three values (if value2 is neither double nor long) from the top. Stack: value3, value2, value1 -> value1, value3, value2, value1'), 92: ('dup2', OpcodeNoArgs, 'duplicate top two stack words (two values, if value1 is not double nor long; a single value, if value1 is double or long). Stack: {value2, value1} -> {value2, value1}, {value2, value1}'), 93: ('dup2_x1', OpcodeNoArgs, 'duplicate two words and insert beneath third word. Stack: value3, {value2, value1} -> {value2, value1}, value3, {value2, value1}'), 94: ('dup2_x2', OpcodeNoArgs, 'duplicate two words and insert beneath fourth word. Stack: {value4, value3}, {value2, value1} -> {value2, value1}, {value4, value3}, {value2, value1}'), 95: ('swap', OpcodeNoArgs, 'swaps two top words on the stack (note that value1 and value2 must not be double or long). Stack: value2, value1 -> value1, value2'), 96: ('iadd', OpcodeNoArgs, 'adds two ints together. Stack: value1, value2 -> result'), 97: ('ladd', OpcodeNoArgs, 'add two longs. Stack: value1, value2 -> result'), 98: ('fadd', OpcodeNoArgs, 'adds two floats. Stack: value1, value2 -> result'), 99: ('dadd', OpcodeNoArgs, 'adds two doubles. Stack: value1, value2 -> result'), 100: ('isub', OpcodeNoArgs, 'int subtract. Stack: value1, value2 -> result'), 101: ('lsub', OpcodeNoArgs, 'subtract two longs. Stack: value1, value2 -> result'), 102: ('fsub', OpcodeNoArgs, 'subtracts two floats. Stack: value1, value2 -> result'), 103: ('dsub', OpcodeNoArgs, 'subtracts a double from another. Stack: value1, value2 -> result'), 104: ('imul', OpcodeNoArgs, 'multiply two integers. Stack: value1, value2 -> result'), 105: ('lmul', OpcodeNoArgs, 'multiplies two longs. Stack: value1, value2 -> result'), 106: ('fmul', OpcodeNoArgs, 'multiplies two floats. Stack: value1, value2 -> result'), 107: ('dmul', OpcodeNoArgs, 'multiplies two doubles. Stack: value1, value2 -> result'), 108: ('idiv', OpcodeNoArgs, 'divides two integers. Stack: value1, value2 -> result'), 109: ('ldiv', OpcodeNoArgs, 'divide two longs. Stack: value1, value2 -> result'), 110: ('fdiv', OpcodeNoArgs, 'divides two floats. Stack: value1, value2 -> result'), 111: ('ddiv', OpcodeNoArgs, 'divides two doubles. Stack: value1, value2 -> result'), 112: ('irem', OpcodeNoArgs, 'logical int remainder. Stack: value1, value2 -> result'), 113: ('lrem', OpcodeNoArgs, 'remainder of division of two longs. Stack: value1, value2 -> result'), 114: ('frem', OpcodeNoArgs, 'gets the remainder from a division between two floats. Stack: value1, value2 -> result'), 115: ('drem', OpcodeNoArgs, 'gets the remainder from a division between two doubles. Stack: value1, value2 -> result'), 116: ('ineg', OpcodeNoArgs, 'negate int. Stack: value -> result'), 117: ('lneg', OpcodeNoArgs, 'negates a long. Stack: value -> result'), 118: ('fneg', OpcodeNoArgs, 'negates a float. Stack: value -> result'), 119: ('dneg', OpcodeNoArgs, 'negates a double. Stack: value -> result'), 120: ('ishl', OpcodeNoArgs, 'int shift left. Stack: value1, value2 -> result'), 121: ('lshl', OpcodeNoArgs, "bitwise shift left of a long 'value1' by 'value2' positions. Stack: value1, value2 -> result"), 122: ('ishr', OpcodeNoArgs, 'int shift right. Stack: value1, value2 -> result'), 123: ('lshr', OpcodeNoArgs, "bitwise shift right of a long 'value1' by 'value2' positions. Stack: value1, value2 -> result"), 124: ('iushr', OpcodeNoArgs, 'int shift right. Stack: value1, value2 -> result'), 125: ('lushr', OpcodeNoArgs, "bitwise shift right of a long 'value1' by 'value2' positions, unsigned. Stack: value1, value2 -> result"), 126: ('iand', OpcodeNoArgs, 'performs a logical and on two integers. Stack: value1, value2 -> result'), 127: ('land', OpcodeNoArgs, 'bitwise and of two longs. Stack: value1, value2 -> result'), 128: ('ior', OpcodeNoArgs, 'logical int or. Stack: value1, value2 -> result'), 129: ('lor', OpcodeNoArgs, 'bitwise or of two longs. Stack: value1, value2 -> result'), 130: ('ixor', OpcodeNoArgs, 'int xor. Stack: value1, value2 -> result'), 131: ('lxor', OpcodeNoArgs, 'bitwise exclusive or of two longs. Stack: value1, value2 -> result'), 132: ('iinc', OpcodeSpecial_iinc, "increment local variable '#index' by signed byte 'const'. Stack: [No change]"), 133: ('i2l', OpcodeNoArgs, 'converts an int into a long. Stack: value -> result'), 134: ('i2f', OpcodeNoArgs, 'converts an int into a float. Stack: value -> result'), 135: ('i2d', OpcodeNoArgs, 'converts an int into a double. Stack: value -> result'), 136: ('l2i', OpcodeNoArgs, 'converts a long to an int. Stack: value -> result'), 137: ('l2f', OpcodeNoArgs, 'converts a long to a float. Stack: value -> result'), 138: ('l2d', OpcodeNoArgs, 'converts a long to a double. Stack: value -> result'), 139: ('f2i', OpcodeNoArgs, 'converts a float to an int. Stack: value -> result'), 140: ('f2l', OpcodeNoArgs, 'converts a float to a long. Stack: value -> result'), 141: ('f2d', OpcodeNoArgs, 'converts a float to a double. Stack: value -> result'), 142: ('d2i', OpcodeNoArgs, 'converts a double to an int. Stack: value -> result'), 143: ('d2l', OpcodeNoArgs, 'converts a double to a long. Stack: value -> result'), 144: ('d2f', OpcodeNoArgs, 'converts a double to a float. Stack: value -> result'), 145: ('i2b', OpcodeNoArgs, 'converts an int into a byte. Stack: value -> result'), 146: ('i2c', OpcodeNoArgs, 'converts an int into a character. Stack: value -> result'), 147: ('i2s', OpcodeNoArgs, 'converts an int into a short. Stack: value -> result'), 148: ('lcmp', OpcodeNoArgs, 'compares two longs values. Stack: value1, value2 -> result'), 149: ('fcmpl', OpcodeNoArgs, 'compares two floats. Stack: value1, value2 -> result'), 150: ('fcmpg', OpcodeNoArgs, 'compares two floats. Stack: value1, value2 -> result'), 151: ('dcmpl', OpcodeNoArgs, 'compares two doubles. Stack: value1, value2 -> result'), 152: ('dcmpg', OpcodeNoArgs, 'compares two doubles. Stack: value1, value2 -> result'), 153: ('ifeq', OpcodeShortJump, "if 'value' is 0, branch to the 16-bit instruction offset argument. Stack: value ->"), 154: ('ifne', OpcodeShortJump, "if 'value' is not 0, branch to the 16-bit instruction offset argument. Stack: value ->"), 156: ('ifge', OpcodeShortJump, "if 'value' is greater than or equal to 0, branch to the 16-bit instruction offset argument. Stack: value ->"), 157: ('ifgt', OpcodeShortJump, "if 'value' is greater than 0, branch to the 16-bit instruction offset argument. Stack: value ->"), 158: ('ifle', OpcodeShortJump, "if 'value' is less than or equal to 0, branch to the 16-bit instruction offset argument. Stack: value ->"), 159: ('if_icmpeq', OpcodeShortJump, 'if ints are equal, branch to the 16-bit instruction offset argument. Stack: value1, value2 ->'), 160: ('if_icmpne', OpcodeShortJump, 'if ints are not equal, branch to the 16-bit instruction offset argument. Stack: value1, value2 ->'), 161: ('if_icmplt', OpcodeShortJump, "if 'value1' is less than 'value2', branch to the 16-bit instruction offset argument. Stack: value1, value2 ->"), 162: ('if_icmpge', OpcodeShortJump, "if 'value1' is greater than or equal to 'value2', branch to the 16-bit instruction offset argument. Stack: value1, value2 ->"), 163: ('if_icmpgt', OpcodeShortJump, "if 'value1' is greater than 'value2', branch to the 16-bit instruction offset argument. Stack: value1, value2 ->"), 164: ('if_icmple', OpcodeShortJump, "if 'value1' is less than or equal to 'value2', branch to the 16-bit instruction offset argument. Stack: value1, value2 ->"), 165: ('if_acmpeq', OpcodeShortJump, 'if references are equal, branch to the 16-bit instruction offset argument. Stack: value1, value2 ->'), 166: ('if_acmpne', OpcodeShortJump, 'if references are not equal, branch to the 16-bit instruction offset argument. Stack: value1, value2 ->'), 167: ('goto', OpcodeShortJump, 'goes to the 16-bit instruction offset argument. Stack: [no change]'), 168: ('jsr', OpcodeShortJump, 'jump to subroutine at the 16-bit instruction offset argument and place the return address on the stack. Stack: -> address'), 169: ('ret', OpcodeIndex, "continue execution from address taken from a local variable '#index'. Stack: [No change]"), 170: ('tableswitch', OpcodeSpecial_tableswitch, "continue execution from an address in the table at offset 'index'. Stack: index ->"), 171: ('lookupswitch', OpcodeSpecial_lookupswitch, 'a target address is looked up from a table using a key and execution continues from the instruction at that address. Stack: key ->'), 172: ('ireturn', OpcodeNoArgs, 'returns an integer from a method. Stack: value -> [empty]'), 173: ('lreturn', OpcodeNoArgs, 'returns a long value. Stack: value -> [empty]'), 174: ('freturn', OpcodeNoArgs, 'returns a float. Stack: value -> [empty]'), 175: ('dreturn', OpcodeNoArgs, 'returns a double from a method. Stack: value -> [empty]'), 176: ('areturn', OpcodeNoArgs, 'returns a reference from a method. Stack: objectref -> [empty]'), 177: ('return', OpcodeNoArgs, 'return void from method. Stack: -> [empty]'), 178: ('getstatic', OpcodeCPIndex, "gets a static field 'value' of a class, where the field is identified by field reference in the constant pool. Stack: -> value"), 179: ('putstatic', OpcodeCPIndex, "set static field to 'value' in a class, where the field is identified by a field reference in constant pool. Stack: value ->"), 180: ('getfield', OpcodeCPIndex, "gets a field 'value' of an object 'objectref', where the field is identified by field reference <argument> in the constant pool. Stack: objectref -> value"), 181: ('putfield', OpcodeCPIndex, "set field to 'value' in an object 'objectref', where the field is identified by a field reference <argument> in constant pool. Stack: objectref, value ->"), 182: ('invokevirtual', OpcodeCPIndex, "invoke virtual method on object 'objectref', where the method is identified by method reference <argument> in constant pool. Stack: objectref, [arg1, arg2, ...] ->"), 183: ('invokespecial', OpcodeCPIndex, "invoke instance method on object 'objectref', where the method is identified by method reference <argument> in constant pool. Stack: objectref, [arg1, arg2, ...] ->"), 184: ('invokestatic', OpcodeCPIndex, 'invoke a static method, where the method is identified by method reference <argument> in the constant pool. Stack: [arg1, arg2, ...] ->'), 185: ('invokeinterface', OpcodeSpecial_invokeinterface, "invokes an interface method on object 'objectref', where the interface method is identified by method reference <argument> in constant pool. Stack: objectref, [arg1, arg2, ...] ->"), 186: ('xxxunusedxxx', OpcodeNoArgs, 'this opcode is reserved for historical reasons. Stack: '), 187: ('new', OpcodeCPIndex, 'creates new object of type identified by class reference <argument> in constant pool. Stack: -> objectref'), 188: ('newarray', OpcodeSpecial_newarray, "creates new array with 'count' elements of primitive type given in the argument. Stack: count -> arrayref"), 189: ('anewarray', OpcodeCPIndex, "creates a new array of references of length 'count' and component type identified by the class reference <argument> in the constant pool. Stack: count -> arrayref"), 190: ('arraylength', OpcodeNoArgs, 'gets the length of an array. Stack: arrayref -> length'), 191: ('athrow', OpcodeNoArgs, 'throws an error or exception (notice that the rest of the stack is cleared, leaving only a reference to the Throwable). Stack: objectref -> [empty], objectref'), 192: ('checkcast', OpcodeCPIndex, "checks whether an 'objectref' is of a certain type, the class reference of which is in the constant pool. Stack: objectref -> objectref"), 193: ('instanceof', OpcodeCPIndex, "determines if an object 'objectref' is of a given type, identified by class reference <argument> in constant pool. Stack: objectref -> result"), 194: ('monitorenter', OpcodeNoArgs, 'enter monitor for object ("grab the lock" - start of synchronized() section). Stack: objectref -> '), 195: ('monitorexit', OpcodeNoArgs, 'exit monitor for object ("release the lock" - end of synchronized() section). Stack: objectref -> '), 196: ('wide', OpcodeSpecial_wide, "execute 'opcode', where 'opcode' is either iload, fload, aload, lload, dload, istore, fstore, astore, lstore, dstore, or ret, but assume the 'index' is 16 bit; or execute iinc, where the 'index' is 16 bits and the constant to increment by is a signed 16 bit short. Stack: [same as for corresponding instructions]"), 197: ('multianewarray', OpcodeSpecial_multianewarray, "create a new array of 'dimensions' dimensions with elements of type identified by class reference in constant pool; the sizes of each dimension is identified by 'count1', ['count2', etc]. Stack: count1, [count2,...] -> arrayref"), 198: ('ifnull', OpcodeShortJump, "if 'value' is null, branch to the 16-bit instruction offset argument. Stack: value ->"), 199: ('ifnonnull', OpcodeShortJump, "if 'value' is not null, branch to the 16-bit instruction offset argument. Stack: value ->"), 200: ('goto_w', OpcodeLongJump, 'goes to another instruction at the 32-bit branch offset argument. Stack: [no change]'), 201: ('jsr_w', OpcodeLongJump, 'jump to subroutine at the 32-bit branch offset argument and place the return address on the stack. Stack: -> address'), 202: ('breakpoint', OpcodeNoArgs, 'reserved for breakpoints in Java debuggers; should not appear in any class file.'), 254: ('impdep1', OpcodeNoArgs, 'reserved for implementation-dependent operations within debuggers; should not appear in any class file.'), 255: ('impdep2', OpcodeNoArgs, 'reserved for implementation-dependent operations within debuggers; should not appear in any class file.')}

    def __init__(self, parent, name, length):
        FieldSet.__init__(self, parent, name)
        self._size = length * 8

    def createFields(self):
        while self.current_size < self.size:
            bytecode = ord(self.parent.stream.readBytes(self.absolute_address + self.current_size, 1))
            (op, cls, desc) = self.OPCODE_TABLE.get(bytecode, ['<reserved_opcode>', OpcodeNoArgs, 'Reserved opcode.'])
            yield cls(self, 'bytecode[]', op, desc)


class CPInfo(FieldSet):
    """
    Holds a constant pool entry.  Entries all have a type, and various contents
    fields depending on their type.
    """
    __module__ = __name__

    def createFields(self):
        yield Enum(UInt8(self, 'tag'), self.root.CONSTANT_TYPES)
        if self['tag'].value not in self.root.CONSTANT_TYPES:
            raise ParserError('Java: unknown constant type (%s)' % self['tag'].value)
        self.constant_type = self.root.CONSTANT_TYPES[self['tag'].value]
        if self.constant_type == 'Utf8':
            yield PascalString16(self, 'bytes', charset='UTF-8')
        elif self.constant_type == 'Integer':
            yield Int32(self, 'bytes')
        elif self.constant_type == 'Float':
            yield Float32(self, 'bytes')
        elif self.constant_type == 'Long':
            yield Int64(self, 'bytes')
        elif self.constant_type == 'Double':
            yield Float64(self, 'bytes')
        elif self.constant_type == 'Class':
            yield CPIndex(self, 'name_index', 'Class or interface name', target_types='Utf8')
        elif self.constant_type == 'String':
            yield CPIndex(self, 'string_index', target_types='Utf8')
        elif self.constant_type == 'Fieldref':
            yield CPIndex(self, 'class_index', 'Field class or interface name', target_types='Class')
            yield CPIndex(self, 'name_and_type_index', target_types='NameAndType')
        elif self.constant_type == 'Methodref':
            yield CPIndex(self, 'class_index', 'Method class name', target_types='Class')
            yield CPIndex(self, 'name_and_type_index', target_types='NameAndType')
        elif self.constant_type == 'InterfaceMethodref':
            yield CPIndex(self, 'class_index', 'Method interface name', target_types='Class')
            yield CPIndex(self, 'name_and_type_index', target_types='NameAndType')
        elif self.constant_type == 'NameAndType':
            yield CPIndex(self, 'name_index', target_types='Utf8')
            yield CPIndex(self, 'descriptor_index', target_types='Utf8')
        else:
            raise ParserError('Not a valid constant pool element type: ' + self['tag'].value)

    def __str__(self):
        """
        Returns a human-readable string representation of the constant pool
        entry.  It is used for pretty-printing of the CPIndex fields pointing
        to it.
        """
        if self.constant_type == 'Utf8':
            return self['bytes'].value
        elif self.constant_type in ('Integer', 'Float', 'Long', 'Double'):
            return self['bytes'].display
        elif self.constant_type == 'Class':
            class_name = str(self['name_index'].get_cp_entry())
            return class_name.replace('/', '.')
        elif self.constant_type == 'String':
            return str(self['string_index'].get_cp_entry())
        elif self.constant_type == 'Fieldref':
            return '%s (from %s)' % (self['name_and_type_index'], self['class_index'])
        elif self.constant_type == 'Methodref':
            return '%s (from %s)' % (self['name_and_type_index'], self['class_index'])
        elif self.constant_type == 'InterfaceMethodref':
            return '%s (from %s)' % (self['name_and_type_index'], self['class_index'])
        elif self.constant_type == 'NameAndType':
            return parse_any_descriptor(str(self['descriptor_index'].get_cp_entry()), name=str(self['name_index'].get_cp_entry()))
        else:
            raise ParserError('Not a valid constant pool element type: ' + self['tag'].value)


class FieldInfo(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield NullBits(self, 'reserved[]', 8)
        yield Bit(self, 'transient')
        yield Bit(self, 'volatile')
        yield NullBits(self, 'reserved[]', 1)
        yield Bit(self, 'final')
        yield Bit(self, 'static')
        yield Bit(self, 'protected')
        yield Bit(self, 'private')
        yield Bit(self, 'public')
        yield CPIndex(self, 'name_index', 'Field name', target_types='Utf8')
        yield CPIndex(self, 'descriptor_index', 'Field descriptor', target_types='Utf8', target_text_handler=parse_field_descriptor)
        yield UInt16(self, 'attributes_count', 'Number of field attributes')
        if self['attributes_count'].value > 0:
            yield FieldArray(self, 'attributes', AttributeInfo, self['attributes_count'].value)


class MethodInfo(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield NullBits(self, 'reserved[]', 4)
        yield Bit(self, 'strict')
        yield Bit(self, 'abstract')
        yield NullBits(self, 'reserved[]', 1)
        yield Bit(self, 'native')
        yield NullBits(self, 'reserved[]', 2)
        yield Bit(self, 'synchronized')
        yield Bit(self, 'final')
        yield Bit(self, 'static')
        yield Bit(self, 'protected')
        yield Bit(self, 'private')
        yield Bit(self, 'public')
        yield CPIndex(self, 'name_index', 'Method name', target_types='Utf8')
        yield CPIndex(self, 'descriptor_index', 'Method descriptor', target_types='Utf8', target_text_handler=parse_method_descriptor)
        yield UInt16(self, 'attributes_count', 'Number of method attributes')
        if self['attributes_count'].value > 0:
            yield FieldArray(self, 'attributes', AttributeInfo, self['attributes_count'].value)


class AttributeInfo(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._size = (self['attribute_length'].value + 6) * 8

    def createFields(self):
        yield CPIndex(self, 'attribute_name_index', 'Attribute name', target_types='Utf8')
        yield UInt32(self, 'attribute_length', 'Length of the attribute')
        attr_name = str(self['attribute_name_index'].get_cp_entry())
        if attr_name == 'ConstantValue':
            if self['attribute_length'].value != 2:
                raise ParserError('Java: Invalid attribute %s length (%s)' % (self.path, self['attribute_length'].value))
            yield CPIndex(self, 'constantvalue_index', target_types=('Long', 'Float',
                                                                     'Double', 'Integer',
                                                                     'String'))
        elif attr_name == 'Code':
            yield UInt16(self, 'max_stack')
            yield UInt16(self, 'max_locals')
            yield UInt32(self, 'code_length')
            if self['code_length'].value > 0:
                yield JavaBytecode(self, 'code', self['code_length'].value)
            yield UInt16(self, 'exception_table_length')
            if self['exception_table_length'].value > 0:
                yield FieldArray(self, 'exception_table', ExceptionTableEntry, self['exception_table_length'].value)
            yield UInt16(self, 'attributes_count')
            if self['attributes_count'].value > 0:
                yield FieldArray(self, 'attributes', AttributeInfo, self['attributes_count'].value)
        elif attr_name == 'Exceptions':
            yield UInt16(self, 'number_of_exceptions')
            yield FieldArray(self, 'exception_index_table', CPIndex, self['number_of_exceptions'].value, target_types='Class')
            assert self['attribute_length'].value == 2 + self['number_of_exceptions'].value * 2
        elif attr_name == 'InnerClasses':
            yield UInt16(self, 'number_of_classes')
            if self['number_of_classes'].value > 0:
                yield FieldArray(self, 'classes', InnerClassesEntry, self['number_of_classes'].value)
            assert self['attribute_length'].value == 2 + self['number_of_classes'].value * 8
        elif attr_name == 'Synthetic':
            assert self['attribute_length'].value == 0
        elif attr_name == 'SourceFile':
            assert self['attribute_length'].value == 2
            yield CPIndex(self, 'sourcefile_index', target_types='Utf8')
        elif attr_name == 'LineNumberTable':
            yield UInt16(self, 'line_number_table_length')
            if self['line_number_table_length'].value > 0:
                yield FieldArray(self, 'line_number_table', LineNumberTableEntry, self['line_number_table_length'].value)
            assert self['attribute_length'].value == 2 + self['line_number_table_length'].value * 4
        elif attr_name == 'LocalVariableTable':
            yield UInt16(self, 'local_variable_table_length')
            if self['local_variable_table_length'].value > 0:
                yield FieldArray(self, 'local_variable_table', LocalVariableTableEntry, self['local_variable_table_length'].value)
            assert self['attribute_length'].value == 2 + self['local_variable_table_length'].value * 10
        elif attr_name == 'Deprecated':
            assert self['attribute_length'].value == 0
        elif self['attribute_length'].value > 0:
            yield RawBytes(self, 'info', self['attribute_length'].value)


class ExceptionTableEntry(FieldSet):
    __module__ = __name__
    static_size = 48 + CPIndex.static_size

    def createFields(self):
        yield textHandler(UInt16(self, 'start_pc'), hexadecimal)
        yield textHandler(UInt16(self, 'end_pc'), hexadecimal)
        yield textHandler(UInt16(self, 'handler_pc'), hexadecimal)
        yield CPIndex(self, 'catch_type', target_types='Class')


class InnerClassesEntry(StaticFieldSet):
    __module__ = __name__
    format = ((CPIndex, 'inner_class_info_index', {'target_types': 'Class', 'allow_zero': True}), (CPIndex, 'outer_class_info_index', {'target_types': 'Class', 'allow_zero': True}), (CPIndex, 'inner_name_index', {'target_types': 'Utf8', 'allow_zero': True}), (NullBits, 'reserved[]', 5), (Bit, 'abstract'), (Bit, 'interface'), (NullBits, 'reserved[]', 3), (Bit, 'super'), (Bit, 'final'), (Bit, 'static'), (Bit, 'protected'), (Bit, 'private'), (Bit, 'public'))


class LineNumberTableEntry(StaticFieldSet):
    __module__ = __name__
    format = ((UInt16, 'start_pc'), (UInt16, 'line_number'))


class LocalVariableTableEntry(StaticFieldSet):
    __module__ = __name__
    format = ((UInt16, 'start_pc'), (UInt16, 'length'), (CPIndex, 'name_index', {'target_types': 'Utf8'}), (CPIndex, 'descriptor_index', {'target_types': 'Utf8', 'target_text_handler': parse_field_descriptor}), (UInt16, 'index'))


class JavaCompiledClassFile(Parser):
    """
    Root of the .class parser.
    """
    __module__ = __name__
    endian = BIG_ENDIAN
    PARSER_TAGS = {'id': 'java_class', 'category': 'program', 'file_ext': ('class', ), 'mime': ('application/java-vm', ), 'min_size': 32 + 3 * 16, 'description': 'Compiled Java class'}
    MAGIC = 3405691582
    KNOWN_VERSIONS = {'45.3': 'JDK 1.1', '46.0': 'JDK 1.2', '47.0': 'JDK 1.3', '48.0': 'JDK 1.4', '49.0': 'JDK 1.5', '50.0': 'JDK 1.6'}
    CONSTANT_TYPES = {1: 'Utf8', 3: 'Integer', 4: 'Float', 5: 'Long', 6: 'Double', 7: 'Class', 8: 'String', 9: 'Fieldref', 10: 'Methodref', 11: 'InterfaceMethodref', 12: 'NameAndType'}

    def validate(self):
        if self['magic'].value != self.MAGIC:
            return 'Wrong magic signature!'
        version = '%d.%d' % (self['major_version'].value, self['minor_version'].value)
        if version not in self.KNOWN_VERSIONS:
            return 'Unknown version (%s)' % version
        return True

    def createDescription(self):
        version = '%d.%d' % (self['major_version'].value, self['minor_version'].value)
        if version in self.KNOWN_VERSIONS:
            return 'Compiled Java class, %s' % self.KNOWN_VERSIONS[version]
        else:
            return 'Compiled Java class, version %s' % version

    def createFields(self):
        yield textHandler(UInt32(self, 'magic', 'Java compiled class signature'), hexadecimal)
        yield UInt16(self, 'minor_version', 'Class format minor version')
        yield UInt16(self, 'major_version', 'Class format major version')
        yield UInt16(self, 'constant_pool_count', 'Size of the constant pool')
        if self['constant_pool_count'].value > 1:
            yield ConstantPool(self, 'constant_pool', self['constant_pool_count'].value)
        yield NullBits(self, 'reserved[]', 5)
        yield Bit(self, 'abstract')
        yield Bit(self, 'interface')
        yield NullBits(self, 'reserved[]', 3)
        yield Bit(self, 'super')
        yield Bit(self, 'final')
        yield Bit(self, 'static')
        yield Bit(self, 'protected')
        yield Bit(self, 'private')
        yield Bit(self, 'public')
        yield CPIndex(self, 'this_class', 'Class name', target_types='Class')
        yield CPIndex(self, 'super_class', 'Super class name', target_types='Class')
        yield UInt16(self, 'interfaces_count', 'Number of implemented interfaces')
        if self['interfaces_count'].value > 0:
            yield FieldArray(self, 'interfaces', CPIndex, self['interfaces_count'].value, target_types='Class')
        yield UInt16(self, 'fields_count', 'Number of fields')
        if self['fields_count'].value > 0:
            yield FieldArray(self, 'fields', FieldInfo, self['fields_count'].value)
        yield UInt16(self, 'methods_count', 'Number of methods')
        if self['methods_count'].value > 0:
            yield FieldArray(self, 'methods', MethodInfo, self['methods_count'].value)
        yield UInt16(self, 'attributes_count', 'Number of attributes')
        if self['attributes_count'].value > 0:
            yield FieldArray(self, 'attributes', AttributeInfo, self['attributes_count'].value)