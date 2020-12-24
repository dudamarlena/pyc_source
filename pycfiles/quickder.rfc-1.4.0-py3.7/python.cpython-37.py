# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arpa2/quickder_tools/generators/python.py
# Compiled at: 2020-03-04 06:22:47
# Size of source mod 2**32: 17932 bytes
from asn1ate.sema import DefinedType, SimpleType, BitStringType, ValueListType, NamedType, TaggedType, ChoiceType, SequenceType, SetType, SequenceOfType, SetOfType, dependency_sort, ValueAssignment, NameForm, NumberForm, NameAndNumberForm, TypeAssignment, TagImplicitness, ExtensionMarker, ComponentType
import arpa2.quickder_tools as api
from arpa2.quickder_tools.util import api_prefix, dertag2atomsubclass
from arpa2.quickder_tools.generators import QuickDERgeneric
from arpa2.quickder_tools.util import tosym

class QuickDER2py(QuickDERgeneric):
    __doc__ = 'Generate Python modules with Quick DER definitions, based on\n       generic definitions in the arpa2.quickder module.  The main task of\n       this generator is to provide class definitions that subclass\n       ASN1Object (usually through an intermediate subclass such as\n       ASN1StructuredType) and can be invoked with a binary string\n       holding DER-encoded data, or without any argument to create\n       an empty structure.  The resulting classes support both the\n       der_pack() and der_unpack() operations.  See PYTHON.MD!\n\n       The recursion model strives for two, overlapping, goals and\n       must therefore be stopped explicitly.  First, it constructs\n       packer code up to a SEQUENCE OF or SET OF or ANY and cannot\n       support recursion (yet).  This form of recursion can stop as\n       soon as any of the packer-terminal codes is reached, but it\n       needs to follow type references via DefinedType elements.\n       The second reason for recursion is to produce class code,\n       and this passes through SEQUENCE OF and SET OF (but not ANY)\n       to complete the class definition.  It does not need to\n       traverse to other classes by following DefinedType elements,\n       however.  Each of these discards certain information from\n       their continued explorations, and when both kinds of\n       traversal were crossed, the data would only be collected to\n       be discarded.  This can be avoided by knowing whether both\n       forms have been crossed, and stopping the further traversal\n       if this is indeed the case.  In terms of code, once the\n       execution reaches a point where it would set one flag, it\n       would check the other flag and return trivially if this\n       is already/also set.  Flags are only raised for the\n       duration of the recursive traversal, and they may be set\n       multiple times before the other flag is set, so they are\n       subjected to a stack-based regimen -- or, even simpler,\n       to nesting counters.  The first form is managed with\n       nested_typecuts, the second with nested_typerefs.\n    '

    def __init__(self, semamod, outfn, refmods, outdir):
        self.cursor_offset = None
        self.nested_typerefs = None
        self.nested_typecuts = None
        self.semamod = semamod
        self.refmods = refmods
        super(QuickDER2py, self).__init__(outdir, outfn, '.py')
        self.funmap_pytype = {DefinedType: self.pytypeDefinedType, 
         SimpleType: self.pytypeSimple, 
         BitStringType: self.pytypeSimple, 
         ValueListType: self.pytypeSimple, 
         NamedType: self.pytypeNamedType, 
         TaggedType: self.pytypeTagged, 
         ChoiceType: self.pytypeChoice, 
         SequenceType: self.pytypeSequence, 
         SetType: self.pytypeSet, 
         SequenceOfType: self.pytypeSequenceOf, 
         SetOfType: self.pytypeSetOf}

    def comment(self, text):
        for ln in str(text).split('\n'):
            self.writeln('# ' + ln)

    def generate_head(self):
        self.writeln('#')
        self.writeln('# asn2quickder output for ' + self.semamod.name + ' -- automatically generated')
        self.writeln('#')
        self.writeln("# Read more about Quick `n' Easy DER on https://gitlab.com/arpa2/quick-der")
        self.writeln('#')
        self.writeln()
        self.writeln()
        self.writeln('#')
        self.writeln('# Import general definitions and package dependencies')
        self.writeln('#')
        self.writeln()
        self.writeln('from arpa2.quickder import api as ' + api_prefix)
        self.writeln()
        if not self.semamod.imports:
            return
        imports = self.semamod.imports.imports
        for rm in imports.keys():
            pymod = tosym(str(rm).rsplit('.', 1)[0]).lower()
            self.write('from ' + pymod + ' import ')
            self.writeln(', '.join(map(tosym, imports[rm])))

        self.writeln()
        self.writeln()

    def generate_tail(self):
        self.writeln()
        self.writeln('# asn2quickder output for ' + self.semamod.name + ' ends here')

    def generate_values(self):
        self.writeln('#')
        self.writeln('# Variables with ASN.1 value assignments')
        self.writeln('#')
        self.writeln()
        for assigncompos in dependency_sort(self.semamod.assignments):
            for assign in assigncompos:
                if type(assign) != ValueAssignment:
                    continue
                self.pygenValueAssignment(assign)

    def pygenValueAssignment(self, node):
        cls = tosym(node.type_decl)
        var = tosym(node.value_name)
        if cls == 'INTEGER':
            val = self.pyvalInteger(node.value)
            cls = api_prefix + '.ASN1Integer'
        else:
            if cls == 'OBJECTIDENTIFIER':
                val = self.pyvalOID(node.value)
                cls = api_prefix + '.ASN1OID'
            else:
                val = 'UNDEF_MAP2DER("""' + str(node.value) + '""")'
        self.comment(str(node))
        self.writeln(var + ' = ' + cls + ' (bindata=[' + val + '], context={})')
        self.writeln()

    def pyvalInteger(self, valnode):
        return api_prefix + '.der_format_INTEGER (' + str(int(valnode)) + ')'

    def pyvalOID(self, valnode):
        retc = []
        for oidcompo in valnode.components:
            if type(oidcompo) == NameForm:
                retc.append(api_prefix + '.der_parse_OID (' + tosym(oidcompo.name) + '.get())')
            else:
                if type(oidcompo) == NumberForm:
                    retc.append("'" + str(oidcompo.value) + "'")

        retval = " + '.' + ".join(retc)
        retval = api_prefix + '.der_format_OID (' + retval.replace("' + '", '') + ')'
        return retval

    def generate_classes(self):
        self.writeln('#')
        self.writeln('# Classes for ASN.1 type assignments')
        self.writeln('#')
        self.writeln()
        for assigncompos in dependency_sort(self.semamod.assignments):
            for assign in assigncompos:
                if type(assign) != TypeAssignment:
                    continue
                self.pygenTypeAssignment(assign)

    def pygenTypeAssignment(self, node):

        def pymap_packer(pck, ln='\n        '):
            retval = '(' + ln
            pck = pck + ['DER_PACK_END']
            comma = ''
            for pcke in pck:
                pcke = pcke.replace('DER_', api_prefix + '.DER_')
                retval += comma + 'chr(' + pcke + ')'
                comma = ' +' + ln

            retval += ' )'
            return retval

        def pymap_recipe(recp, ctxofs, ln='\n    '):
            if type(recp) == int:
                retval = str(recp + ctxofs)
            else:
                if recp[0] == '_NAMED':
                    _NAMED, map_ = recp
                    ln += '    '
                    retval = "('_NAMED', {"
                    comma = False
                    for fld, fldrcp in map_.items():
                        if comma:
                            retval += ',' + ln
                        else:
                            retval += ln
                        retval += "'" + tosym(fld) + "': "
                        retval += pymap_recipe(fldrcp, ctxofs, ln)
                        comma = True

                    retval += ' } )'
                else:
                    if recp[0] in ('_SEQOF', '_SETOF'):
                        _STHOF, allidx, pck, num, inner_recp = recp
                        ln += '    '
                        retval = "('" + _STHOF + "', "
                        retval += str(allidx) + ', '
                        retval += pymap_packer(pck, ln) + ','
                        retval += str(num) + ',' + ln
                        retval += pymap_recipe(inner_recp, 0, ln) + ' )'
                    else:
                        if recp[0] == '_TYPTR':
                            _TYPTR, (clsnm,), ofs = recp
                            retval = repr(recp)
                        else:
                            assert False, 'Unexpected recipe tag ' + str(recp[0])
                            return retval

        def pygen_class(clsnm, tp, ctxofs, pck, recp, numcrs):
            supertp = tosym(tp)
            self.writeln('class ' + clsnm + ' (' + supertp + '):')
            atom = type(recp) == int
            subatom = atom and tp != 'ASN1Atom'
            said_sth = False
            if tp not in ('ASN1SequenceOf', 'ASN1SetOf'):
                if not subatom:
                    self.writeln('    _der_packer = ' + pymap_packer(pck))
                    said_sth = True
                else:
                    atom or self.writeln('    _recipe = ' + pymap_recipe(recp, ctxofs))
                    said_sth = True
                atom or self.writeln('    _context = globals ()')
                self.writeln('    _numcursori = ' + str(numcrs))
                said_sth = True
            else:
                if subatom:
                    self.writeln('    _context = ' + api_prefix + '.__dict__')
                else:
                    said_sth or self.writeln('    pass')
                self.writeln()

        self.cursor_offset = 0
        self.nested_typerefs = 0
        self.nested_typecuts = 0
        self.comment(str(node))
        pck, recp = self.generate_pytype(node.type_decl)
        ofs = 0
        tp = None
        if type(recp) == int:
            dertag = eval(pck[0], api.__dict__)
            if dertag in dertag2atomsubclass:
                tp = dertag2atomsubclass[dertag]
            else:
                tp = 'ASN1Atom'
            tp = api_prefix + '.' + tp
        else:
            if recp[0] == '_NAMED':
                tp = api_prefix + '.ASN1ConstructedType'
            else:
                if recp[0] == '_SEQOF':
                    tp = api_prefix + '.ASN1SequenceOf'
                else:
                    if recp[0] == '_SETOF':
                        tp = api_prefix + '.ASN1SetOf'
                    else:
                        if recp[0] == '_TYPTR':
                            _TYPTR, (cls,), ofs = recp
                            tp = str(cls)
                        else:
                            assert False, 'Unknown recipe tag ' + str(recp[0])
                            numcrs = self.cursor_offset
                            pygen_class(tosym(node.type_name), tp, ofs, pck, recp, numcrs)

    def generate_pytype(self, node, **subarg):
        tnm = type(node)
        if tnm not in self.funmap_pytype.keys():
            raise Exception('Failure to generate a python type for ' + str(tnm))
        return (self.funmap_pytype[tnm])(node, **subarg)

    def pytypeDefinedType(self, node, **subarg):
        modnm = node.module_ref
        if not modnm:
            if self.semamod.imports:
                syms = self.semamod.imports.imports
                for mod in syms.keys():
                    if node.type_name in syms[mod]:
                        modnm = str(mod).lower()
                        break

        if modnm is None:
            modnm = self.unit.lower()
        if modnm not in self.refmods:
            raise Exception('Module name "%s" not found' % modnm)
        popunit = self.unit
        popsema = self.semamod
        popcofs = self.cursor_offset
        self.unit = modnm
        self.semamod = self.refmods[modnm]
        if self.nested_typecuts > 0:
            self.nested_typerefs += 1
        thetype = self.refmods[modnm].user_types()[node.type_name]
        pck, recp = (self.generate_pytype)(thetype, **subarg)
        recp = (
         '_TYPTR', [node.type_name], popcofs)
        self.nested_typerefs -= 1
        self.semamod = popsema
        self.unit = popunit
        return (pck, recp)

    def pytypeSimple(self, node, implicit_tag=None):
        simptp = node.type_name.replace(' ', '').upper()
        if simptp == 'ANY':
            pck = [
             'DER_PACK_ANY']
            simptag = api.DER_PACK_ANY
            if implicit_tag:
                pck = ['DER_PACK_ENTER | ' + implicit_tag] + pck + ['DER_PACK_LEAVE']
        else:
            if not implicit_tag:
                implicit_tag = 'DER_TAG_' + simptp
            pck = [
             'DER_PACK_STORE | ' + implicit_tag]
            simptag = eval('DER_TAG_' + simptp, api.__dict__)
        recp = self.cursor_offset
        self.cursor_offset += 1
        if simptag in dertag2atomsubclass:
            recp = (
             '_TYPTR', [api_prefix + '.' + dertag2atomsubclass[simptag]], recp)
        return (
         pck, recp)

    def pytypeTagged(self, node, implicit_tag=None):
        mytag = 'DER_TAG_' + (node.class_name or 'CONTEXT') + '(' + node.class_number + ')'
        if self.semamod.resolve_tag_implicitness(node.implicitness, node.type_decl) == TagImplicitness.IMPLICIT:
            pck, recp = self.generate_pytype((node.type_decl), implicit_tag=mytag)
        else:
            pck, recp = self.generate_pytype(node.type_decl)
            pck = ['DER_PACK_ENTER | ' + mytag] + pck + ['DER_PACK_LEAVE']
        if implicit_tag:
            pck = ['DER_PACK_ENTER | ' + implicit_tag] + pck + ['DER_PACK_LEAVE']
        return (
         pck, recp)

    def pytypeNamedType(self, node, **subarg):
        return (self.generate_pytype)((node.type_decl), **subarg)

    def pyhelpConstructedType(self, node):
        pck = []
        recp = {}
        for comp in node.components:
            if isinstance(comp, ExtensionMarker):
                continue
            else:
                if isinstance(comp, ComponentType):
                    if comp.components_of_type is not None:
                        continue
                pck1, stru1 = self.generate_pytype(comp.type_decl)
                if not isinstance(comp, ComponentType) or comp.optional or comp.default_value:
                    pck1 = [
                     'DER_PACK_OPTIONAL'] + pck1
            pck = pck + pck1
            recp[tosym(comp.identifier)] = stru1

        return (
         pck, ('_NAMED', recp))

    def pytypeChoice(self, node, implicit_tag=None):
        pck, recp = self.pyhelpConstructedType(node)
        pck = ['DER_PACK_CHOICE_BEGIN'] + pck + ['DER_PACK_CHOICE_END']
        if implicit_tag:
            pck = ['DER_PACK_ENTER | ' + implicit_tag] + pck + ['DER_PACK_LEAVE']
        return (
         pck, recp)

    def pytypeSequence(self, node, implicit_tag='DER_TAG_SEQUENCE'):
        pck, recp = self.pyhelpConstructedType(node)
        pck = ['DER_PACK_ENTER | ' + implicit_tag] + pck + ['DER_PACK_LEAVE']
        return (pck, recp)

    def pytypeSet(self, node, implicit_tag='DER_TAG_SET'):
        pck, recp = self.pyhelpConstructedType(node)
        pck = ['DER_PACK_ENTER | ' + implicit_tag] + pck + ['DER_PACK_LEAVE']
        return (pck, recp)

    def pyhelpRepeatedType(self, node, dertag, recptag):
        allidx = self.cursor_offset
        self.cursor_offset += 1
        if self.nested_typerefs > 0 and self.nested_typecuts > 0:
            subpck = [
             'DER_ERROR_RECURSIVE_USE_IN' + recptag]
            subrcp = ('_ERROR', 'Recursive use in ' + recptag)
            subnum = 0
        else:
            self.nested_typecuts = self.nested_typecuts + 1
            popcofs = self.cursor_offset
            self.cursor_offset = 0
            subpck, subrcp = self.generate_pytype(node.type_decl)
            subnum = self.cursor_offset
            self.cursor_offset = popcofs
            self.nested_typecuts = self.nested_typecuts - 1
        pck = [
         'DER_PACK_STORE | ' + dertag]
        return (pck, (recptag, allidx, subpck, subnum, subrcp))

    def pytypeSequenceOf(self, node, implicit_tag='DER_TAG_SEQUENCE'):
        return self.pyhelpRepeatedType(node, implicit_tag, '_SEQOF')

    def pytypeSetOf(self, node, implicit_tag='DER_TAG_SET'):
        return self.pyhelpRepeatedType(node, implicit_tag, '_SETOF')