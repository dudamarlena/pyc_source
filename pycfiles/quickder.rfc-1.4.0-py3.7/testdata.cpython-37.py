# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arpa2/quickder_tools/generators/testdata.py
# Compiled at: 2020-03-04 06:22:47
# Size of source mod 2**32: 16634 bytes
from asn1ate.sema import DefinedType, SimpleType, BitStringType, ValueListType, NamedType, TaggedType, ChoiceType, SequenceType, SetType, SequenceOfType, SetOfType, dependency_sort, TypeAssignment, TagImplicitness, ExtensionMarker, ComponentType
import arpa2.quickder_tools as api
from arpa2.quickder_tools.generators import QuickDERgeneric

class QuickDER2testdata(QuickDERgeneric):
    __doc__ = 'This builds a network of generators that exhibits the structure\n       of the data, generating test variations for each of the parts.\n       For each named type, an entry point for the network is setup in\n       a dictionary, from which any number of test cases can be retrieved.\n\n       The search structure for the generators is width-first, meaning\n       that structures first seek out variations at the outer levels,\n       using already-found cases for end points, and only later start\n       to vary deeper down.  This way, test cases can be enumerated\n       in a consistent manner and tests become reproducable, even when\n       the total work load for testing is rediculously high.  The\n       width-first approach was chosen because often a type includes\n       other named types, which may be tested independently.\n\n       The deliverable of the type-processing routines is a tuple\n       (casecount,casegenerator) where the casecount gives the total\n       number of tests available (usually much larger than deemed\n       interesting for a test) and where the casegenerator can be\n       asked to generate one numbered test case.  This allows us to\n       both generate "the first 100 tests" and any specific test or\n       range of tests that we might be interested in (perhaps we\n       got an error report on case 1234567 and would like to make\n       it a standard test).\n\n       The reason we speak of a network of generators is that the\n       various definitions are connected, often in a cyclical\n       manner, and to that end they lookup values in the dictionary\n       that maps type names to (casecount,casegenerator) tuples.\n       These are not generators in the Python3 sense however, as\n       these would not allow us to request arbitrary entries such\n       as the aforementioned test case 1234567.  It is closer to\n       a functional programming concept with closures standing by\n       to operate on a given index in a (virtual) output list.\n\n       The efficiency might be poor if we generated each case for\n       each type name freshly, because there will be a lot of\n       repeated uses.  To make the case generators operate more\n       smoothly, they may employ a cache, perhaps based on weak\n       references.\n\n       This class can hold the network of generators as well as\n       their cache structures, and supports output of test data\n       in individual files.  As an alternative use case, one may\n       consider delivering test cases over a stream, such as an\n       HTTP API.\n    '

    def __init__(self, semamod, outfn, refmods, outdir):
        self.semamod = semamod
        self.refmods = refmods
        super(QuickDER2testdata, self).__init__(outdir, outfn, '.testdata')
        self.type2tdgen = {}
        self.funmap_tdgen = {DefinedType: self.tdgenDefinedType, 
         SimpleType: self.tdgenSimple, 
         BitStringType: self.tdgenSimple, 
         ValueListType: self.tdgenSimple, 
         NamedType: self.tdgenNamedType, 
         TaggedType: self.tdgenTagged, 
         ChoiceType: self.tdgenChoice, 
         SequenceType: self.tdgenConstructed, 
         SetType: self.tdgenConstructed, 
         SequenceOfType: self.tdgenRepeated, 
         SetOfType: self.tdgenRepeated}

    def fetch_one(self, typename, casenr):
        max_, fun = self.type2tdgen[typename]
        if casenr >= max_:
            return
        assert casenr < max_, 'Case number out of range for ' + typename
        return fun(casenr)

    def fetch_multi(self, typename, testcases):
        return [(i, self.fetch_one(typename, i)) for s, e in testcases for i in range(s, e + 1)]

    def all_typenames(self):
        return self.type2tdgen.keys()

    def generate_testdata(self):
        for assigncompos in dependency_sort(self.semamod.assignments):
            for assign in assigncompos:
                if type(assign) != TypeAssignment:
                    continue
                self.process_TypeAssignment(assign)

    def process_TypeAssignment(self, node):
        self.type2tdgen[node.type_name] = self.generate_tdgen(node.type_decl)

    def generate_tdgen(self, node, **subarg):
        tnm = type(node)
        if tnm not in self.funmap_tdgen.keys():
            raise Exception('Failure to generate a python type for ' + str(tnm))
        return (self.funmap_tdgen[tnm])(node, **subarg)

    def tdgenDefinedType(self, node, **subarg):
        modnm = node.module_ref
        if modnm is None:
            syms = self.semamod.imports.imports
            for mod in syms.keys():
                if node.type_name in syms[mod]:
                    modnm = str(mod).lower()
                    break

        if modnm is None:
            modnm = self.unit.lower()
        if modnm not in self.refmods:
            raise Exception('Module name "%s" not found' % modnm)
        thetype = self.refmods[modnm].user_types()[node.type_name]
        return (self.generate_tdgen)(thetype, **subarg)

    def der_prefixhead(self, tag, body):
        blen = len(body)
        if blen == 0:
            lenh = chr(0)
        else:
            if blen <= 127:
                lenh = chr(blen)
            else:
                lenh = ''
                while blen > 0:
                    lenh = chr(blen % 256) + lenh
                    blen >>= 8

                lenh = chr(128 + len(lenh)) + lenh
        return chr(tag) + lenh + body

    simple_cases = {'BOOLEAN':[
      '\x01\x01\x00', '\x01\x01ÿ'], 
     'INTEGER':[
      '\x02\x00', '\x02\x01\x80', '\x02\x01\x01',
      '\x02\x01À', '\x02\x04\x80\x00\x00\x00',
      '\x02\x04À\x00\x00\x00'], 
     'BITSTRING':[
      '\x03\x01\x00', '\x03\x02\x00\x01',
      '\x03\x02\x00ÿ', '\x03\x02\x00ÿ',
      '\x03\x02\x01~', '\x03\x02\x07\x80'], 
     'OCTETSTRING':[
      '\x04\x00', '\x04\x04ABCD', '\x04\x04A\x00CD',
      '\x04\x05ABCD\x00'], 
     'NULL':[
      '\x05\x00', '\x05\x04ABCD'], 
     'OBJECTIDENTIFIER':[
      '\x06\x03U\x04\x06', '\x06\x03))'], 
     'REAL':[
      '\t\x00', '\t\x04ABCD'], 
     'ENUMERATED':[
      '\n\x00', '\n\x01\x01', '\n\x03\x124V'], 
     'UTF8STRING':[
      '\x0c\x00', '\x0c\x01\x7f',
      '\x0c\x02ÀÀ', '\x0c\x02ßÿ',
      '\x0c\x03à\x80\x80', '\x0c\x03ï¿¿',
      '\x0c\x04ð\x00\x00\x00',
      '\x0c\x04÷¿¿¿'], 
     'SEQUENCE':[
      '0\x00'], 
     'SET':[
      '1\x00'], 
     'IA5STRING':[
      '\x16\x00', '\x16\x04ABCD'], 
     'UTCTIME':[
      '\x17\r200207235959Z'], 
     'GENERALIZEDTIME':[
      '\x18\x0e20001231235959',
      '\x18\x1220001231235959.999',
      '\x18\x1320001231205959.999Z'], 
     'GENERALSTRING':[
      '\x1b\x00'], 
     'UNIVERSALSTRING':[
      '\x1c\x00']}

    def tdgenSimple(self, node):
        cases = self.simple_cases[node.type_name.replace(' ', '').upper()]

        def do_gen(casenr):
            assert casenr < len(cases), 'Simple type case number out of range'
            return cases[casenr]

        return (
         len(cases), do_gen)

    def tdgenNamedType(self, node, **subarg):
        return (self.generate_tdgen)((node.type_decl), **subarg)

    nodeclass2basaltag = {'APPLICATION':api.DER_PACK_ENTER | api.DER_TAG_APPLICATION(0), 
     'CONTEXT':api.DER_PACK_ENTER | api.DER_TAG_CONTEXT(0), 
     'PRIVATE':api.DER_PACK_ENTER | api.DER_TAG_PRIVATE(0)}

    def tdgenTagged(self, node, implicit_tag=None):
        subcnt, subgen = self.generate_tdgen(node.type_decl)
        am_implicit = self.semamod.resolve_tag_implicitness(node.implicitness, node.type_decl) == TagImplicitness.IMPLICIT
        tag = self.nodeclass2basaltag[(node.class_name or 'CONTEXT')]
        tag |= int(node.class_number)

        def do_gen(casenr):
            if am_implicit:
                retval = subgen(casenr, implicit_tag=tag)
            else:
                retval = subgen(casenr)
                retval = self.der_prefixhead(tag, retval)
            if implicit_tag is not None:
                retval = self.der_prefixhead(implicit_tag, retval)
            return retval

        return (
         subcnt, do_gen)

    def tdgenChoice(self, node, implicit_tag=None):
        """CHOICE test cases are generated by enabling each of the
           choices in turn.  Initially, this yields the (0) choice.
           On further rounds, alternatives within each of the
           choices are addressed.  This implements the width-first
           approach, by iterating over the choices first, and only
           within that allow for iteration within the choices.
        """
        elcnts = []
        elgens = []
        for comp in node.components:
            if isinstance(comp, ExtensionMarker):
                continue
            if isinstance(comp, ComponentType):
                if comp.components_of_type is not None:
                    continue
            c, g = self.generate_tdgen(comp.type_decl)
            elcnts.append(c)
            elgens.append(g)

        round2flips = []
        for e in range(max(elcnts)):
            round2flips.append(len([e for e in elcnts if e > len(round2flips)]))

        totcnt = sum(elcnts)

        def do_gen(casenr):
            round_ = 0
            while casenr >= round2flips[round_]:
                casenr -= round2flips[round_]
                round_ += 1

            eltidx = 0
            while True:
                if elcnts[eltidx] > round_:
                    if casenr == 0:
                        break
                    casenr -= 1
                eltidx += 1

            retval = elgens[eltidx](round_)
            if implicit_tag is not None:
                retval = self.der_prefixhead(implicit_tag, retval)
            return retval

        return (
         totcnt, do_gen)

    def tdgenConstructed(self, node, implicit_tag=None):
        """SEQUENCE and SET test cases are generated assuming
           that the fields are orthogonal.  This means that not all
           combinations of all fields are formed.  The search is
           however width-first, meaning that it does not pass through
           all values of the first field before continuing to the
           next, but instead it will cycle over the fields.  While
           experimenting with a field, the other fields are set to
           their 0 value, for simplicity's sake.

           TODO: Missing support for OPTIONAL / DEFAULT cases
        """
        elcnts = []
        elgens = []
        for comp in node.components:
            if isinstance(comp, ExtensionMarker):
                continue
            if isinstance(comp, ComponentType):
                if comp.components_of_type is not None:
                    continue
            c, g = self.generate_tdgen(comp.type_decl)
            elcnts.append(c)
            elgens.append(g)

        round2flips = []
        for e in range(max(elcnts)):
            round2flips.append(len([e for e in elcnts if e > len(round2flips)]))

        totcnt = 1 + sum(elcnts) - len(elcnts)
        comp = [
         None] * len(elgens)
        if implicit_tag is not None:
            tag = implicit_tag
        else:
            if type(node) == SetType:
                tag = 49
            else:
                tag = 48

        def do_gen(casenr):
            if None in comp:
                for idx2 in range(len(elgens)):
                    comp[idx2] = elgens[idx2](0)

            round_ = 0
            while casenr >= round2flips[round_]:
                casenr -= round2flips[round_]
                round_ += 1

            eltidx = 0
            while True:
                if elcnts[eltidx] > round_:
                    if casenr == 0:
                        break
                    casenr -= 1
                eltidx += 1

            retval = comp[:eltidx]
            if round_ > 0:
                retval += elgens[eltidx](round_)
                eltidx += 1
            retval += comp[eltidx:]
            retval = ''.join(retval)
            retval = self.der_prefixhead(tag, retval)
            return retval

        return (
         totcnt, do_gen)

    def tdgenRepeated(self, node, **subarg):
        subcnt, subgen = (self.generate_tdgen)((node.type_decl), **subarg)
        totcnt = 1 + subcnt + subcnt * subcnt
        tag = 49 if type(node) == SetOfType else 48

        def do_gen(casenr):
            if casenr == 0:
                retval = ''
            else:
                casenr -= 1
                retval = subgen(casenr % subcnt)
                if casenr >= subcnt:
                    casenr -= subcnt
                    retval = retval + subgen(casenr / subcnt)
            retval = self.der_prefixhead(tag, retval)
            return retval

        return (
         totcnt, do_gen)