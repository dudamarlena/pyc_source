# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arpa2/quickder_tools/generators/source.py
# Compiled at: 2020-03-04 06:22:47
# Size of source mod 2**32: 4675 bytes
from six import StringIO
from os import path
import logging
logger = logging.getLogger(__name__)
from asn1ate.sema import DefinedType, ValueAssignment, TypeAssignment, TaggedType, SimpleType, BitStringType, ValueListType, SequenceType, SetType, ChoiceType, SequenceOfType, SetOfType, ComponentType, dependency_sort
from arpa2.quickder_tools.util import tosym
from arpa2.quickder_tools.generators import QuickDERgeneric

class QuickDER2source(QuickDERgeneric):

    def __init__(self, semamod, outfn, refmods, outdir):
        self.to_be_defined = None
        self.to_be_overlaid = None
        self.cursor_offset = None
        self.nested_typerefs = None
        self.nested_typecuts = None
        self.semamod = semamod
        self.refmods = refmods
        self.buffer = StringIO()
        self.linebuffer = StringIO()
        self.comma1 = None
        self.comma0 = None
        self.unit, curext = path.splitext(outfn)
        self.issued_typedefs = {}
        self.pack_funmap = {DefinedType: self.packDefinedType, 
         ValueAssignment: self.packValueAssignment, 
         TypeAssignment: self.packTypeAssignment, 
         TaggedType: self.packTaggedType, 
         SimpleType: self.packSimpleType, 
         BitStringType: self.packSimpleType, 
         ValueListType: self.packSimpleType, 
         SequenceType: self.packSequenceType, 
         SetType: self.packSetType, 
         ChoiceType: self.packChoiceType, 
         SequenceOfType: self.packRepeatingStructureType, 
         SetOfType: self.packRepeatingStructureType, 
         ComponentType: self.packSimpleType}

    def write(self, txt):
        self.buffer.write(txt)
        self.linebuffer.write(txt)

    def writeln(self, txt=''):
        self.buffer.write(txt + '\n')
        self.linebuffer.write(txt)
        logger.info(self.linebuffer.getvalue())
        self.linebuffer.truncate(0)
        self.linebuffer.seek(0)

    def close(self):
        pass

    def generate_head(self):
        pass

    def generate_tail(self):
        pass

    def generate_unpack(self):
        pass

    def generate_pack(self):
        for assigncompos in dependency_sort(self.semamod.assignments):
            for assign in assigncompos:
                self.generate_pack_node(assign, None, None)

    def generate_pack_node(self, node, tp, fld):
        tnm = type(node)
        if tnm in self.pack_funmap:
            self.pack_funmap[tnm](node, tp, fld)

    def packValueAssignment(self, node, tp, fld):
        pass

    def packDefinedType(self, node, tp, fld):
        pass

    def packSimpleType(self, node, tp, fld):
        pass

    def packTypeAssignment(self, node, tp, fld):
        self.to_be_defined = []
        self.to_be_overlaid = [
         (
          tosym(node.type_name), node.type_decl)]
        while len(self.to_be_overlaid) > 0:
            tname, tdecl = self.to_be_overlaid.pop(0)
            key = (self.unit, tname)
            if key not in self.issued_typedefs:
                self.issued_typedefs[key] = str(tdecl)
                self.writeln('KeehiveError')
                self.writeln('DER_PACK_{}('.format(tname))
                self.writeln('){')
                self.writeln(')}')
                self.writeln()
                self.writeln('KeehiveError')
                self.writeln('DER_UNPACK_{}('.format(tname))
                self.writeln('){')
                self.writeln(')}')
                self.writeln()
            elif self.issued_typedefs[key] != str(tdecl):
                raise TypeError('Redefinition of type %s.' % key[1])

        for tbd in self.to_be_defined:
            if tbd != 'DER_OVLY_' + self.unit + '_' + tosym(node.type_name) + '_0':
                self.writeln('typedef struct ' + tbd + ' ' + tbd + ';')

        self.writeln()

    def packSequenceType(self, node, tp, fld, naked=False):
        pass

    def packSetType(self, node, tp, fld, naked=False):
        pass

    def packChoiceType(self, node, tp, fld, naked=False):
        pass

    def packRepeatingStructureType(self, node, tp, fld):
        pass

    def packTaggedType(self, node, tp, fld):
        pass