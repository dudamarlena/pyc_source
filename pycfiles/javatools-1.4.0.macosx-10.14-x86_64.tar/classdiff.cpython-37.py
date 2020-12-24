# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/classdiff.py
# Compiled at: 2019-06-21 15:26:13
# Size of source mod 2**32: 27239 bytes
"""
Utility script for comparing the internals of two Java class files
for differences in structure and data. Has options to specify changes
which may be immaterial or unimportant, such as re-ordering of the
constant pool, line number changes (either absolute or relative),
added fields or methods, deprecation changes, etc.

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: LGPL
"""
import sys
from abc import ABCMeta
from argparse import ArgumentParser, Action
from six import add_metaclass
from . import unpack_classfile
from .change import GenericChange, SuperChange
from .change import Addition, Removal
from .change import yield_sorted_by_type
from .opcodes import get_opname_by_code, has_const_arg
from .report import quick_report, Reporter
from .report import JSONReportFormat, TextReportFormat
from .report import add_general_report_optgroup
from .report import add_json_report_optgroup, add_html_report_optgroup
__all__ = ('JavaClassChange', 'ClassInfoChange', 'ClassAnnotationsChange', 'ClassInvisibleAnnotationsChange',
           'ClassConstantPoolChange', 'ClassFieldsChange', 'ClassMethodsChange',
           'ClassMembersChange', 'MemberSuperChange', 'MemberAdded', 'MemberRemoved',
           'FieldChange', 'FieldAdded', 'FieldRemoved', 'FieldNameChange', 'FieldTypeChange',
           'FieldSignatureChange', 'FieldAnnotationsChange', 'FieldInvisibleAnnotationsChange',
           'FieldAccessflagsChange', 'FieldConstvalueChange', 'FieldDeprecationChange',
           'MethodChange', 'MethodAdded', 'MethodRemoved', 'MethodNameChange', 'MethodTypeChange',
           'MethodSignatureChange', 'MethodAnnotationsChange', 'MethodInvisibleAnnotationsChange',
           'MethodParametersChange', 'MethodAccessflagsChange', 'MethodExceptionsChange',
           'MethodAbstractChange', 'MethodCodeChange', 'MethodDeprecationChange',
           'CodeAbsoluteLinesChange', 'CodeRelativeLinesChange', 'CodeStackChange',
           'CodeLocalsChange', 'CodeExceptionChange', 'CodeConstantsChange', 'CodeBodyChange',
           'JavaClassReport', 'pretty_merge_constants', 'merge_code', 'cli', 'main',
           'cli_classes_diff', 'add_classdiff_optgroup', 'default_classdiff_options',
           'add_general_optgroup')

class ClassNameChange(GenericChange):
    label = 'Class name'

    def fn_data(self, c):
        return c.get_this()

    def fn_pretty(self, c):
        return c.pretty_this()


class ClassVersionChange(GenericChange):
    label = 'Java class verison'

    def fn_data(self, c):
        return c.version

    def is_ignored(self, o):
        lver = self.ldata.version
        rver = self.rdata.version
        return o.ignore_version_up and lver < rver or o.ignore_version_down and lver > rver


class ClassPlatformChange(GenericChange):
    label = 'Java platform'

    def fn_data(self, c):
        return c.get_platform()

    def is_ignored(self, o):
        lver = self.ldata.version
        rver = self.rdata.version
        return o.ignore_version_up and lver < rver or o.ignore_version_down and lver > rver


class ClassSuperclassChange(GenericChange):
    label = 'Superclass'

    def fn_data(self, c):
        return c.get_super()

    def fn_pretty(self, c):
        return c.pretty_super()


class ClassInterfacesChange(GenericChange):
    label = 'Interfaces'

    def fn_data(self, c):
        return set(c.get_interfaces())

    def fn_pretty(self, c):
        return tuple(c.pretty_interfaces())


class ClassAccessflagsChange(GenericChange):
    label = 'Access flags'

    def fn_data(self, c):
        return c.access_flags

    def fn_pretty(self, c):
        return tuple(c.pretty_access_flags())


class ClassDeprecationChange(GenericChange):
    label = 'Deprecation'

    def fn_data(self, c):
        return c.is_deprecated()

    def is_ignored(self, o):
        return o.ignore_deprecated


class ClassSignatureChange(GenericChange):
    label = 'Generics Signature'

    def fn_data(self, c):
        return c.get_signature()

    def fn_pretty(self, c):
        return c.pretty_signature()


@add_metaclass(ABCMeta)
class AnnotationsChange(GenericChange):
    label = 'Runtime annotations'

    def fn_data(self, c):
        return c.get_annotations() or tuple()

    def fn_pretty(self, c):
        annos = self.fn_data(c)
        return [anno.pretty_annotation() for anno in annos]


@add_metaclass(ABCMeta)
class InvisibleAnnotationsChange(AnnotationsChange):
    label = 'Runtime Invisible annotations'

    def fn_data(self, c):
        return c.get_invisible_annotations() or tuple()


class ClassAnnotationsChange(AnnotationsChange):
    label = 'Class runtime annotations'


class ClassInvisibleAnnotationsChange(InvisibleAnnotationsChange):
    label = 'Class runtime invisible annotations'


class ClassInfoChange(SuperChange):
    label = 'Class information'
    change_types = (
     ClassNameChange,
     ClassVersionChange,
     ClassPlatformChange,
     ClassSuperclassChange,
     ClassInterfacesChange,
     ClassAccessflagsChange,
     ClassDeprecationChange,
     ClassSignatureChange)


@add_metaclass(ABCMeta)
class MemberSuperChange(SuperChange):
    __doc__ = '\n    basis for FieldChange and MethodChange\n    '
    label = 'Member'

    def get_description(self):
        return '%s: %s' % (self.label, self.ldata.pretty_descriptor())


@add_metaclass(ABCMeta)
class MemberAdded(Addition):
    __doc__ = '\n    basis for FieldAdded and MethodAdded\n    '
    label = 'Member added'

    def get_description(self):
        return '%s: %s' % (self.label, self.rdata.pretty_descriptor())


@add_metaclass(ABCMeta)
class MemberRemoved(Removal):
    __doc__ = '\n    basis for FieldChange and MethodChange\n    '
    label = 'Member removed'

    def get_description(self):
        return '%s: %s' % (self.label, self.ldata.pretty_descriptor())


@add_metaclass(ABCMeta)
class ClassMembersChange(SuperChange):
    __doc__ = '\n    basis for ClassFieldsChange and ClassMethodsChange\n    '
    label = 'Members'
    member_added = MemberAdded
    member_removed = MemberRemoved
    member_changed = MemberSuperChange

    def collect_impl(self):
        li = {}
        for member in self.ldata:
            li[member.get_identifier()] = member

        for member in self.rdata:
            key = member.get_identifier()
            lf = li.get(key, None)
            if lf:
                del li[key]
                yield self.member_changed(lf, member)
            else:
                yield self.member_added(None, member)

        for member in li.values():
            yield self.member_removed(member, None)


class CodeAbsoluteLinesChange(GenericChange):
    label = 'Absolute line numbers'

    def fn_data(self, c):
        return c and c.get_linenumbertable() or tuple()

    def is_ignored(self, options):
        return options.ignore_absolute_lines


class CodeRelativeLinesChange(GenericChange):
    label = 'Relative line numbers'

    def fn_data(self, c):
        return c and c.get_relativelinenumbertable() or tuple()

    def is_ignored(self, options):
        return options.ignore_relative_lines


class CodeStackChange(GenericChange):
    label = 'Stack size'

    def fn_data(self, c):
        return c and c.max_stack or 0


class CodeLocalsChange(GenericChange):
    label = 'Locals'

    def fn_data(self, c):
        return c and c.max_locals or 0


class CodeExceptionChange(GenericChange):
    label = 'Exception table'

    def fn_data(self, c):
        return c and c.exceptions or tuple()

    def fn_pretty(self, c):
        a = list()
        for e in self.fn_data(c):
            p = (
             e.start_pc, e.end_pc,
             e.handler_pc, e.pretty_catch_type())
            a.append(p)

        return repr(a)


class CodeConstantsChange(GenericChange):
    __doc__ = "\n    This is a test to find instances where the individual opcodes and\n    arguments for a method's code may all be identical except that ops\n    which load from the constant pool may use a different index. We\n    will deref the constant index for both sides, and if all of the\n    constant values match then we can consider the code to be equal.\n\n    The purpose of such a check is to find other-wise meaningless\n    constant pool reordering. If all uses of the pool result in the\n    same values, we don't really care if the pool is in a different\n    order between the old and new versions of a class.\n    "
    label = 'Code constants'

    def __init__(self, lcode, rcode):
        super(CodeConstantsChange, self).__init__(lcode, rcode)
        self.offsets = None

    def fn_pretty(self, c):
        if not self.offsets:
            return
        pr = list()
        for offset, code, args in c.disassemble():
            if offset in self.offsets and has_const_arg(code):
                name = get_opname_by_code(code)
                data = c.cpool.pretty_deref_const(args[0])
                pr.append((offset, name, data))

        return pr

    def check_impl(self):
        left = self.ldata
        right = self.rdata
        offsets = list()
        if left is None or right is None:
            return (True, None)
        if len(left.code) != len(right.code):
            return (True, None)
        for l, r in zip(left.disassemble(), right.disassemble()):
            if l[0] == r[0]:
                if not l[1] == r[1]:
                    return (True, None)
                largs = l[2]
                rargs = r[2]
                if has_const_arg(l[1]):
                    largs, rargs = list(largs), list(rargs)
                    largs[0] = left.cpool.deref_const(largs[0])
                    rargs[0] = right.cpool.deref_const(rargs[0])
                if largs != rargs:
                    offsets.append(l[0])

        self.offsets = offsets
        return (bool(self.offsets), None)


class CodeBodyChange(GenericChange):
    __doc__ = '\n    The length or the opcodes or the arguments of the opcodes has\n    changed, signalling that the method body is different\n    '
    label = 'Code body'

    def fn_data(self, c):
        return c and c.disassemble() or tuple()

    def fn_pretty(self, c):
        pr = list()
        for offset, code, args in self.fn_data(c):
            name = get_opname_by_code(code)
            pr.append((offset, name, args))

        return pr

    def check_impl(self):
        left = self.ldata
        right = self.rdata
        if left is None or right is None:
            return (True, None)
        if len(left.code) != len(right.code):
            desc = 'Code length changed from %r to %r' % (
             len(left.code), len(right.code))
            return (True, desc)
        for l, r in zip(left.disassemble(), right.disassemble()):
            if l[0] == r[0]:
                return l[1] == r[1] or (True, None)

        return (False, None)


class MethodNameChange(GenericChange):
    label = 'Method name'

    def fn_data(self, c):
        return c.get_name()


class MethodTypeChange(GenericChange):
    label = 'Method type'

    def fn_data(self, c):
        return c.get_type_descriptor()

    def fn_pretty(self, c):
        return c.pretty_type()


class MethodSignatureChange(GenericChange):
    label = 'Method generic signature'

    def fn_data(self, c):
        return c.get_signature()

    def fn_pretty(self, c):
        return c.pretty_signature()


class MethodParametersChange(GenericChange):
    label = 'Method parameters'

    def fn_data(self, c):
        return c.get_arg_type_descriptors()

    def fn_pretty(self, c):
        return tuple(c.pretty_arg_types())


class MethodAccessflagsChange(GenericChange):
    label = 'Method accessflags'

    def fn_data(self, c):
        return c.access_flags

    def fn_pretty(self, c):
        return tuple(c.pretty_access_flags())


class MethodAbstractChange(GenericChange):
    label = 'Method abstract'

    def fn_data(self, c):
        return not c.get_code()

    def fn_pretty_desc(self, c):
        if self.fn_data(c):
            return 'Method is abstract'
        return 'Method is concrete'


class MethodExceptionsChange(GenericChange):
    label = 'Method exceptions'

    def fn_data(self, c):
        return c.get_exceptions()

    def fn_pretty(self, c):
        return tuple(c.pretty_exceptions())


class MethodCodeChange(SuperChange):
    label = 'Method Code'
    change_types = (
     CodeAbsoluteLinesChange,
     CodeRelativeLinesChange,
     CodeStackChange,
     CodeLocalsChange,
     CodeExceptionChange,
     CodeConstantsChange,
     CodeBodyChange)

    def __init__(self, l, r):
        super(MethodCodeChange, self).__init__(l.get_code(), r.get_code())

    def collect_impl(self):
        if self.ldata is self.rdata is None:
            return tuple()
        return super(MethodCodeChange, self).collect_impl()

    def check_impl(self):
        if None in (self.ldata, self.rdata):
            return (
             self.ldata != self.rdata, None)
        return super(MethodCodeChange, self).check_impl()


class MethodDeprecationChange(GenericChange):
    label = 'Method deprecation'

    def fn_data(self, c):
        return c.is_deprecated()

    def is_ignored(self, o):
        return o.ignore_deprecated


class MethodAnnotationsChange(AnnotationsChange):
    label = 'Method runtime annotations'


class MethodInvisibleAnnotationsChange(InvisibleAnnotationsChange):
    label = 'Method runtime invisible annotations'


class MethodChange(MemberSuperChange):
    label = 'Method'
    change_types = (
     MethodNameChange,
     MethodTypeChange,
     MethodSignatureChange,
     MethodAnnotationsChange,
     MethodInvisibleAnnotationsChange,
     MethodParametersChange,
     MethodAccessflagsChange,
     MethodExceptionsChange,
     MethodAbstractChange,
     MethodDeprecationChange,
     MethodCodeChange)


class FieldNameChange(GenericChange):
    label = 'Field name'

    def fn_data(self, c):
        return c.get_name()


class FieldTypeChange(GenericChange):
    label = 'Field type'

    def fn_data(self, c):
        return c.get_descriptor()

    def fn_pretty(self, c):
        return c.pretty_type()


class FieldSignatureChange(GenericChange):
    label = 'Field Generic Signature'

    def fn_data(self, c):
        return c.get_signature()

    def fn_pretty(self, c):
        return c.pretty_signature()


class FieldAccessflagsChange(GenericChange):
    label = 'Field accessflags'

    def fn_data(self, c):
        return c.access_flags

    def fn_pretty(self, c):
        return tuple(c.pretty_access_flags())

    def fn_pretty_desc(self, c):
        return ','.join(c.pretty_access_flags())


class FieldConstvalueChange(GenericChange):
    label = 'Field constvalue'

    def fn_data(self, c):
        return c.deref_constantvalue()

    def fn_pretty(self, c):
        return repr(c.deref_constantvalue())


class FieldDeprecationChange(GenericChange):
    label = 'Field deprecation'

    def fn_data(self, c):
        return c.is_deprecated()

    def is_ignored(self, o):
        return o.ignore_deprecated


class FieldAnnotationsChange(AnnotationsChange):
    label = 'Field runtime annotations'


class FieldInvisibleAnnotationsChange(InvisibleAnnotationsChange):
    label = 'Field runtime invisible annotations'


class FieldChange(MemberSuperChange):
    label = 'Field'
    change_types = (
     FieldNameChange,
     FieldTypeChange,
     FieldSignatureChange,
     FieldAnnotationsChange,
     FieldInvisibleAnnotationsChange,
     FieldAccessflagsChange,
     FieldConstvalueChange,
     FieldDeprecationChange)


class FieldAdded(MemberAdded):
    label = 'Field added'


class FieldRemoved(MemberRemoved):
    label = 'Field removed'


class ClassFieldsChange(ClassMembersChange):
    label = 'Fields'
    member_added = FieldAdded
    member_removed = FieldRemoved
    member_changed = FieldChange

    @yield_sorted_by_type(FieldAdded, FieldRemoved, FieldChange)
    def collect_impl(self):
        return super(ClassFieldsChange, self).collect_impl()

    def __init__(self, lclass, rclass):
        super(ClassFieldsChange, self).__init__(lclass.fields, rclass.fields)


class MethodAdded(MemberAdded):
    label = 'Method added'


class MethodRemoved(MemberRemoved):
    label = 'Method removed'


class ClassMethodsChange(ClassMembersChange):
    label = 'Methods'
    member_added = MethodAdded
    member_removed = MethodRemoved
    member_changed = MethodChange

    @yield_sorted_by_type(MethodAdded, MethodRemoved, MethodChange)
    def collect_impl(self):
        return super(ClassMethodsChange, self).collect_impl()

    def __init__(self, lclass, rclass):
        super(ClassMethodsChange, self).__init__(lclass.methods, rclass.methods)


class ClassConstantPoolChange(GenericChange):
    label = 'Constant pool'

    def fn_data(self, c):
        return c.cpool

    def fn_pretty(self, c):
        return tuple(c.cpool.pretty_constants())

    def is_ignored(self, options):
        return options.ignore_pool

    def get_description(self):
        return self.label + (' unaltered', ' altered')[self.is_change()]


class JavaClassChange(SuperChange):
    label = 'Java Class'
    change_types = (
     ClassInfoChange,
     ClassAnnotationsChange,
     ClassInvisibleAnnotationsChange,
     ClassConstantPoolChange,
     ClassFieldsChange,
     ClassMethodsChange)

    def get_description(self):
        return '%s %s' % (self.label, self.ldata.pretty_this())


class JavaClassReport(JavaClassChange):
    __doc__ = '\n    a JavaClassChange with the side-effect of writing reports\n    '

    def __init__(self, l, r, reporter):
        super(JavaClassReport, self).__init__(l, r)
        self.reporter = reporter

    def check(self):
        super(JavaClassReport, self).check()
        self.reporter.run(self)


def pretty_merge_constants--- This code section failed: ---

 L. 897         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'left_cpool'
                4  LOAD_ATTR                consts
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  STORE_FAST               'lsize'

 L. 898        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'right_cpool'
               14  LOAD_ATTR                consts
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  STORE_FAST               'rsize'

 L. 900        20  LOAD_CONST               1
               22  STORE_FAST               'index'

 L. 901        24  SETUP_LOOP           94  'to 94'
               26  LOAD_GLOBAL              range
               28  LOAD_CONST               1
               30  LOAD_GLOBAL              min
               32  LOAD_FAST                'lsize'
               34  LOAD_FAST                'rsize'
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  CALL_FUNCTION_2       2  '2 positional arguments'
               40  GET_ITER         
               42  FOR_ITER             92  'to 92'
               44  STORE_FAST               'index'

 L. 902        46  LOAD_FAST                'left_cpool'
               48  LOAD_METHOD              pretty_const
               50  LOAD_FAST                'index'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'lt'
               58  STORE_FAST               'lv'

 L. 903        60  LOAD_FAST                'right_cpool'
               62  LOAD_METHOD              pretty_const
               64  LOAD_FAST                'index'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'rt'
               72  STORE_FAST               'rv'

 L. 904        74  LOAD_FAST                'index'
               76  LOAD_FAST                'lt'
               78  LOAD_FAST                'lv'
               80  LOAD_FAST                'rt'
               82  LOAD_FAST                'rv'
               84  BUILD_TUPLE_5         5 
               86  YIELD_VALUE      
               88  POP_TOP          
               90  JUMP_BACK            42  'to 42'
               92  POP_BLOCK        
             94_0  COME_FROM_LOOP       24  '24'

 L. 906        94  LOAD_FAST                'lsize'
               96  LOAD_FAST                'rsize'
               98  COMPARE_OP               >
              100  POP_JUMP_IF_FALSE   154  'to 154'

 L. 907       102  SETUP_LOOP          212  'to 212'
              104  LOAD_GLOBAL              range
              106  LOAD_FAST                'index'
              108  LOAD_FAST                'lsize'
              110  CALL_FUNCTION_2       2  '2 positional arguments'
              112  GET_ITER         
              114  FOR_ITER            150  'to 150'
              116  STORE_FAST               'index'

 L. 908       118  LOAD_FAST                'left_cpool'
              120  LOAD_METHOD              pretty_const
              122  LOAD_FAST                'index'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'lt'
              130  STORE_FAST               'lv'

 L. 909       132  LOAD_FAST                'index'
              134  LOAD_FAST                'lt'
              136  LOAD_FAST                'lv'
              138  LOAD_CONST               None
              140  LOAD_CONST               None
              142  BUILD_TUPLE_5         5 
              144  YIELD_VALUE      
              146  POP_TOP          
              148  JUMP_BACK           114  'to 114'
              150  POP_BLOCK        
              152  JUMP_FORWARD        212  'to 212'
            154_0  COME_FROM           100  '100'

 L. 911       154  LOAD_FAST                'rsize'
              156  LOAD_FAST                'lsize'
              158  COMPARE_OP               >
              160  POP_JUMP_IF_FALSE   212  'to 212'

 L. 912       162  SETUP_LOOP          212  'to 212'
              164  LOAD_GLOBAL              range
              166  LOAD_FAST                'index'
              168  LOAD_FAST                'rsize'
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  GET_ITER         
              174  FOR_ITER            210  'to 210'
              176  STORE_FAST               'index'

 L. 913       178  LOAD_FAST                'right_cpool'
              180  LOAD_METHOD              pretty_const
              182  LOAD_FAST                'index'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'rt'
              190  STORE_FAST               'rv'

 L. 914       192  LOAD_FAST                'index'
              194  LOAD_CONST               None
              196  LOAD_CONST               None
              198  LOAD_FAST                'rt'
              200  LOAD_FAST                'rv'
              202  BUILD_TUPLE_5         5 
              204  YIELD_VALUE      
              206  POP_TOP          
              208  JUMP_BACK           174  'to 174'
              210  POP_BLOCK        
            212_0  COME_FROM_LOOP      162  '162'
            212_1  COME_FROM           160  '160'
            212_2  COME_FROM           152  '152'
            212_3  COME_FROM_LOOP      102  '102'

Parse error at or near `COME_FROM' instruction at offset 212_2


def merge_code(left_code, right_code):
    """
    { relative_line:
      ((left_abs_line, ((offset, op, args), ...)),
       (right_abs_line, ((offset, op, args), ...))),
      ... }
    """
    data = dict()
    code_lines = left_code and left_code.iter_code_by_lines() or tuple()
    for abs_line, rel_line, dis in code_lines:
        assert rel_line is not None
        data[rel_line] = [(abs_line, dis), None]

    code_lines = right_code and right_code.iter_code_by_lines() or tuple()
    for abs_line, rel_line, dis in code_lines:
        assert rel_line is not None
        found = data.get(rel_line, None)
        if found is None:
            found = [
             None, (abs_line, dis)]
            data[rel_line] = found
        else:
            found[1] = (
             abs_line, dis)

    return data


def cli_classes_diff(options, left, right):
    reports = getattr(options, 'reports', tuple())
    if reports:
        rdir = options.report_dir or './'
        rpt = Reporter(rdir, 'JavaClassReport', options)
        rpt.add_formats_by_name(reports)
        delta = JavaClassReport(left, right, rpt)
    else:
        delta = JavaClassChange(left, right)
    delta.check()
    if not options.silent:
        if options.json:
            quick_report(JSONReportFormat, delta, options)
        else:
            quick_report(TextReportFormat, delta, options)
    if not delta.is_change() or delta.is_ignored(options):
        return 0
    return 1


def cli(options):
    left = unpack_classfile(options.classfile[0])
    right = unpack_classfile(options.classfile[1])
    return cli_classes_diff(options, left, right)


def add_classdiff_optgroup(parser):
    """
    option group specific to class checking
    """
    g = parser.add_argument_group('Class Checking Options')
    g.add_argument('--ignore-version-up', action='store_true', default=False)
    g.add_argument('--ignore-version-down', action='store_true', default=False)
    g.add_argument('--ignore-platform-up', action='store_true', default=False)
    g.add_argument('--ignore-platform-down', action='store_true', default=False)
    g.add_argument('--ignore-absolute-lines', action='store_true', default=False)
    g.add_argument('--ignore-relative-lines', action='store_true', default=False)
    g.add_argument('--ignore-deprecated', action='store_true', default=False)
    g.add_argument('--ignore-added', action='store_true', default=False)
    g.add_argument('--ignore-pool', action='store_true', default=False)
    g.add_argument('--ignore-lines', nargs=0, help='ignore relative and absolute line-number changes',
      action=_opt_cb_ign_lines)
    g.add_argument('--ignore-platform', nargs=0, help='ignore platform changes',
      action=_opt_cb_ign_platform)
    g.add_argument('--ignore-version', nargs=0, help='ignore version changes',
      action=_opt_cb_ign_version)


class _opt_cb_ignore(Action):
    __doc__ = '\n    handle the --ignore option, which trigges other options\n    '

    def __call__(self, parser, options, values, option_string=None):
        if not values:
            return
        ignore = getattr(options, 'ignore', None)
        if ignore is None:
            options.ignore = ignore = list()
        ign = (i.strip() for i in values.split(','))
        ign = (i for i in ign if i)
        for i in ign:
            ignore.append(i)
            setattr(options, 'ignore_' + i.replace('-', '_'), True)


class _opt_cb_ign_lines(Action):
    __doc__ = '\n    handle the --ignore-lines option\n    '

    def __call__(self, parser, options, values, option_string=None):
        options.ignore_lines = True
        options.ignore_absolute_lines = True
        options.ignore_relative_lines = True


class _opt_cb_ign_version(Action):
    __doc__ = '\n    handle the --ignore-version option\n    '

    def __call__(self, parser, options, values, option_string=None):
        options.ignore_version = True
        options.ignore_version_up = True
        options.ignore_version_down = True


class _opt_cb_ign_platform(Action):
    __doc__ = '\n    handle the --ignore-platform option\n    '

    def __call__(self, parser, options, values, option_string=None):
        options.ignore_platform = True
        options.ignore_platform_up = True
        options.ignore_platform_down = True


class _opt_cb_verbose(Action):
    __doc__ = '\n    handle the --verbose option\n    '

    def __call__(self, parser, options, values, option_string=None):
        options.verbose = True
        options.show_unchanged = True
        options.show_ignored = True


def add_general_optgroup(parser):
    """
    option group for general-use features of all javatool CLIs
    """
    g = parser.add_argument_group('General Options')
    g.add_argument('-q', '--quiet', dest='silent', action='store_true',
      default=False)
    g.add_argument('-v', '--verbose', nargs=0, action=_opt_cb_verbose)
    g.add_argument('-o', '--output', dest='output', default=None)
    g.add_argument('-j', '--json', dest='json', action='store_true',
      default=False)
    g.add_argument('--show-ignored', action='store_true', default=False)
    g.add_argument('--show-unchanged', action='store_true', default=False)
    g.add_argument('--ignore', action=_opt_cb_ignore, help='comma-separated list of ignores')


def create_optparser(progname=None):
    """
    an OptionParser instance with the appropriate options and groups
    for the classdiff utility
    """
    parser = ArgumentParser(prog=progname)
    parser.add_argument('classfile', nargs=2, help='class files to compare')
    add_general_optgroup(parser)
    add_classdiff_optgroup(parser)
    add_general_report_optgroup(parser)
    add_json_report_optgroup(parser)
    add_html_report_optgroup(parser)
    return parser


def default_classdiff_options(updates=None):
    """
    generate an options object with the appropriate default values in
    place for API usage of classdiff features. overrides is an
    optional dictionary which will be used to update fields on the
    options object.
    """
    parser = create_optparser()
    options, _args = parser.parse_args(list())
    if updates:
        options._update_careful(updates)
    return options


def main(args=sys.argv):
    """
    Main entry point for the classdiff CLI
    """
    parser = create_optparser(args[0])
    return cli(parser.parse_args(args[1:]))