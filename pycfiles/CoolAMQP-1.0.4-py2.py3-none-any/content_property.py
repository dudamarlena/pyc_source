# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/framing/compilation/content_property.py
# Compiled at: 2020-04-03 16:00:47
from __future__ import absolute_import, division, print_function
import six, struct, logging
from coolamqp.framing.compilation.textcode_fields import get_counter, get_from_buffer, get_serializer
logger = logging.getLogger(__name__)
INIT_I = '\n    def __init__(self, %s):\n'
SLOTS_I = '\n    __slots__ = (%s)\n'
FROM_BUFFER_1 = '    def from_buffer(cls, buf, start_offset):\n        offset = start_offset + %s\n'
ASSIGN_A = '        self.%s = %s\n'
STARTER = 'from coolamqp.framing.base import AMQPContentPropertyList\n\nclass ParticularContentTypeList(AMQPContentPropertyList):\n    """\n    For fields:\n'
ZPF_S = '\n    # A value for property flags that is used, assuming all bit fields are FALSE (0)\n    ZERO_PROPERTY_FLAGS = %s\n'
NB = "raise NotImplementedError('I don't support bits in properties')"
INTER_X = '    * %s::%s'
BUF_WRITE_A = '\n    def write_to(self, buf):\n        buf.write('
RESERVED = ' (reserved)'
UNICO = "u'%s'"
SPACER = '\n    """\n'
GET_SIZE_HEADER = '\n    def get_size(self):\n'

def _compile_particular_content_property_list_class(zpf, fields):
    """
    Compile a particular content property list.

    Particularity stems from
    :param zpf: zero property list, as bytearray
    :param fields: list of all possible fields in this content property
    """
    from coolamqp.framing.compilation.utilities import format_field_name
    structers = {}
    if any(field.basic_type == 'bit' for field in fields):
        return NB
    even = True
    zpf_bits = []
    for q in bytearray(zpf):
        p = bin(q)[2:]
        p = '0' * (8 - len(p)) + p
        if not even:
            p = p[:7]
        for x in p:
            zpf_bits.append(bool(int(x)))

    zpf_length = len(zpf)
    zpf_bits = [ zpf_bit or field.type == 'bit' for zpf_bit, field in zip(zpf_bits, fields)
               ]
    mod = [
     STARTER]
    for field in fields:
        mod.append(INTER_X % (format_field_name(field.name), field.type))
        if field.reserved:
            mod.append(RESERVED)
        mod.append('\n')

    x = repr(six.binary_type(zpf))
    if not x.startswith('b'):
        x = 'b' + x
    present_fields = [ field for field, present in zip(fields, zpf_bits) if present
                     ]
    mod.append(SPACER)
    if len(present_fields) == 0:
        slots = ''
    else:
        slots = (', ').join(UNICO % format_field_name(field.name) for field in present_fields) + ', '
    mod.append(SLOTS_I % slots)
    mod.append(ZPF_S % (x,))
    FFN = (', ').join(format_field_name(field.name) for field in present_fields)
    if len(present_fields) > 0:
        mod.append(INIT_I % (FFN,))
    for field in present_fields:
        mod.append(ASSIGN_A.replace('%s', format_field_name(field.name)))

    mod.append(BUF_WRITE_A)
    repred_zpf = repr(zpf)
    if not repred_zpf.startswith('b'):
        repred_zpf = 'b' + repred_zpf
    mod.append(repred_zpf)
    mod.append(')\n')
    line, new_structers = get_serializer(present_fields, prefix='self.', indent_level=2)
    structers.update(new_structers)
    mod.append(line)
    mod.append('    @classmethod\n')
    mod.append(FROM_BUFFER_1 % (
     zpf_length,))
    line, new_structers = get_from_buffer(present_fields, prefix='', indent_level=2)
    structers.update(new_structers)
    mod.append(line)
    mod.append('        return cls(%s)\n' % (FFN,))
    mod.append(GET_SIZE_HEADER)
    mod.append(get_counter(present_fields, prefix='self.', indent_level=2)[:-1])
    mod.append(' + %s\n' % (zpf_length,))
    return (
     ('').join(mod), structers)


STRUCTERS_FOR_NOW = {}

def compile_particular_content_property_list_class(zpf, fields):
    global STRUCTERS_FOR_NOW
    from coolamqp.framing.base import AMQPContentPropertyList
    q, structers = _compile_particular_content_property_list_class(zpf, fields)
    locals_ = {'AMQPContentPropertyList': AMQPContentPropertyList}
    for structer in structers:
        if structer not in STRUCTERS_FOR_NOW:
            STRUCTERS_FOR_NOW[structer] = struct.Struct('!%s' % (structer,))
        locals_['STRUCT_%s' % (structer,)] = STRUCTERS_FOR_NOW[structer]

    loc = dict(globals(), **locals_)
    exec q in loc
    return loc['ParticularContentTypeList']