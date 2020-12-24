# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/__init__.py
# Compiled at: 2014-12-16 17:37:19
import string, types, xml.etree.cElementTree as ElementTree
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation

class ImmuneChain(SeqRecord):
    """Data structure to represent an immune chain.
    
    It extends a biopython SeqRecord object with some simpler interface for
    common analyses.
    """

    def __init__(self, *args, **kw):
        """Initialize ImmuneChain
        
        This is performed either with a prebuilt SeqRecord object or as a
        native SeqRecord object.
        """
        if len(args) > 0 and isinstance(args[0], SeqRecord):
            self._init_with_SeqRecord(args[0])
        elif kw.has_key('record'):
            self._init_with_SeqRecord(kw['record'])
        else:
            SeqRecord.__init__(self, *args, **kw)
        self._update_feature_dict()
        self._process_source_feature()
        self._tags = set(self.annotations.setdefault('tags', []))

    def _init_with_SeqRecord(self, record):
        if 'phred_quality' in record.letter_annotations and isinstance(record.letter_annotations['phred_quality'], types.ListType):
            qual = ('').join([ chr(q + 33) for q in record.letter_annotations['phred_quality'] ])
            record.letter_annotations['phred_quality'] = qual
        SeqRecord.__init__(self, seq=record.seq, id=record.id, name=record.name, description=record.description, dbxrefs=record.dbxrefs, features=record.features, annotations=record.annotations, letter_annotations=record.letter_annotations)

    def _update_feature_dict(self):
        self._features = {}
        for i, feature in enumerate(self.features):
            self._features.setdefault(feature.type, []).append(i)

    def _process_source_feature(self):
        if 'source' in self._features:
            if len(self._features['source']) > 1:
                raise ValueError, 'Found more than one `source` feature in %s' % self.id
            for k, v in self.features[self._features['source'][0]].qualifiers.iteritems():
                if k.startswith('__letter_annotations__'):
                    self.letter_annotations[('.').join(k.split('.')[1:])] = ('').join(v[0].split())
                    continue
                if k != 'tags' and isinstance(v, types.ListType) and len(v) == 1:
                    v = v[0]
                if k == 'gapped_reference' or k == 'gapped_query':
                    self.annotations[k] = v.translate(None, string.whitespace)
                    continue
                self.annotations[k] = v

            self.features.pop(self._features['source'][0])
            self._features.pop('source')
        return

    def __getattribute__(self, name):
        """Look for attributes in annotations and features."""
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass

        try:
            return self.annotations[name]
        except KeyError:
            pass

        try:
            if len(self._features[name]) > 1:
                raise AttributeError, '%s is not a unique feature' % name
            return self.features[self._features[name][0]]
        except KeyError:
            pass

        raise AttributeError, "couldn't find %s" % name

    def add_tags(self, tags):
        if isinstance(tags, types.StringTypes):
            tags = [
             tags]
        elif isinstance(tags, types.ListType):
            tags = list(tags)
        else:
            raise TypeError, 'value must be string type or list type'
        tags = set(tags)
        self._tags.update(tags)
        self.annotations['tags'] = list(self._tags)
        return self

    def add_tag(self, tag):
        return self.add_tags(tag)

    def has_tags(self, tags):
        if isinstance(tags, types.StringTypes):
            tags = [
             tags]
        elif isinstance(tags, types.ListType):
            tags = list(tags)
        else:
            raise TypeError, 'value must be string type or list type'
        return set(tags) <= self._tags

    def has_tag(self, tag):
        return self.has_tags(tag)

    def del_tags(self, tags):
        if isinstance(tags, types.StringTypes):
            tags = [
             tags]
        else:
            if isinstance(tags, types.ListType):
                tags = list(tags)
            else:
                raise TypeError, 'value must be string type or list type'
            for tag in tags:
                self._tags.remove(tag)

        self.annotations['tags'] = list(self._tags)
        return self

    def del_tag(self, tag):
        return self.del_tags(tag)

    @property
    def junction(self):
        return self.junction_nt

    @property
    def junction_nt(self):
        return self.__getattribute__('CDR3-IMGT').extract(self.seq.tostring())

    @property
    def junction_aa(self):
        return self.__getattribute__('CDR3-IMGT').qualifiers['translation']

    @property
    def full_chain(self):
        start = self.__getattribute__('V-REGION').location.nofuzzy_start
        end = self.__getattribute__('J-REGION').location.nofuzzy_end
        return self[start:end]

    @property
    def cdr3(self):
        return len(self.junction)

    @property
    def v(self):
        return self.__getattribute__('V-REGION').qualifiers['allele'][0]

    @property
    def v_seq(self):
        return self.__getattribute__('V-REGION').extract(self.seq.tostring())

    @property
    def d(self):
        return self.annotations['D-REGION']

    @property
    def j(self):
        return self.__getattribute__('J-REGION').qualifiers['allele'][0]

    @property
    def j_seq(self):
        return self.__getattribute__('J-REGION').extract(self.seq.tostring())

    @property
    def vj(self):
        return ('|').join([self.v, self.j])

    @property
    def vdj(self):
        return ('|').join([self.v, self.d, self.j])

    @property
    def num_mutations(self):
        aln = self.letter_annotations['alignment']
        return aln.count('S') + aln.count('I')

    @property
    def num_substitutions(self):
        return self.letter_annotations['alignment'].count('S')

    @property
    def num_germline(self):
        aln = self.letter_annotations['alignment']
        return len(aln) - aln.count('3') - aln.count('_') - aln.count('I')

    def format(self, *args, **kw):
        """Format SeqRecord using any supported format.
        
        The only reason for redefining this is the hack related to storing
        user-defined annotations in a source feature.
        """
        self._update_feature_dict()
        if 'source' in self._features:
            raise ValueError, 'I should never get here'
            assert len(self._features['source']) == 1
            feature = self.features[self._features['source'][0]]
            feature.qualifiers.update(self.annotations)
            for k, v in self.letter_annotations.iteritems():
                feature.qualifiers['__letter_annotations__.' + k] = v

        else:
            feature = SeqFeature(type='source', location=FeatureLocation(0, len(self)), qualifiers=self.annotations)
            for k, v in self.letter_annotations.iteritems():
                feature.qualifiers['__letter_annotations__.' + k] = v

            self.features.append(feature)
        output = SeqRecord.format(self, *args, **kw)
        self.features.pop()
        return output

    def __len__(self):
        return len(self.seq)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.format('imgt')


def seq2chain(*args):
    """Convert raw sequence into ImmuneChain object"""
    if len(args) == 1:
        name = 'seq'
        seq = args[0]
    elif len(args) == 2:
        name = args[0]
        seq = args[1]
    else:
        raise ValueError('Give either name,seq or just seq')
    return ImmuneChain(seq=Seq(seq, generic_dna), id=name)


def parse_imgt(inputfile):
    """Parser for VDJXML
    
    Really just a wrapper around SeqIO that upgrades SeqRecord to ImmuneChain
    """
    for record in SeqIO.parse(inputfile, 'imgt'):
        yield ImmuneChain(record)


def filter_parse_imgt(inputfile, predicate):
    """Parser that takes a predicate function"""
    for record in SeqIO.parse(inputfile, 'imgt'):
        chain = ImmuneChain(record)
        if predicate(chain):
            yield chain


class ImmuneChainXML(object):
    """Data structure to represent an immune chain."""

    def __init__(self, **kw):
        """Initialize ImmuneChain
        
        seq is 5'->3'
        """

        def kw_init(attrib):
            if kw.has_key(attrib):
                self.__setattr__(attrib, kw[attrib])

        kw_init('seq')
        kw_init('descr')
        kw_init('locus')
        kw_init('v')
        kw_init('d')
        kw_init('j')
        kw_init('c')
        kw_init('junction')
        if kw.has_key('tags'):
            tags = kw['tags']
            if isinstance(tags, types.StringTypes):
                tags = [tags]
            self.tags = set(tags)
        else:
            self.tags = set([])

    def get_cdr3(self):
        return len(self.junction)

    def set_cdr3(self, value):
        pass

    cdr3 = property(fget=get_cdr3, fset=set_cdr3)

    def get_vj(self):
        return ('|').join([self.v, self.j])

    def set_vj(self):
        pass

    vj = property(fget=get_vj, fset=set_vj)

    def get_vdj(self):
        return ('|').join([self.v, self.d, self.j])

    def set_vdj(self):
        pass

    vdj = property(fget=get_vdj, fset=set_vdj)

    def add_tags(self, tagset):
        if isinstance(tagset, types.StringTypes):
            tagset = [tagset]
        self.tags.update(tagset)

    def add_tag(self, tag):
        self.add_tags(tag)

    def remove_tags(self, tagset):
        if isinstance(tagset, types.StringTypes):
            tagset = [tagset]
        for tag in tagset:
            self.tags.remove(tag)

    def remove_tag(self, tag):
        self.remove_tags(tag)

    def has_tag(self, tag):
        if tag in self.tags:
            return True
        else:
            return False

    def __len__(self):
        return len(self.seq)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.get_XML()

    def get_XML(self):
        format_xml = lambda attrib, value: '\t<%(attrib)s>%(value)s</%(attrib)s>\n' % {'attrib': attrib, 'value': value}
        xmlstring = '<ImmuneChain>\n'
        for attrib, value in self.__dict__.iteritems():
            if attrib == 'tags':
                for tag in self.tags:
                    xmlstring += format_xml('tag', tag)

            else:
                xmlstring += format_xml(attrib, value)

        xmlstring += '</ImmuneChain>\n'
        return xmlstring


class ParserVDJXML(object):
    """Parser for VDJXML"""

    def __init__(self):
        self.chain = None
        return

    def start_handler(self, elem):
        if elem.tag == 'ImmuneChain':
            self.chain = ImmuneChainXML()

    def end_handler(self, elem):
        if elem.tag == 'tag':
            self.chain.add_tags(elem.text)
        elif elem.tag == 'v_end_idx' or elem.tag == 'j_start_idx':
            self.chain.__setattr__(elem.tag, int(elem.text))
        else:
            self.chain.__setattr__(elem.tag, elem.text)

    def parse(self, inputfile):
        for event, elem in ElementTree.iterparse(inputfile, events=('start', 'end')):
            if event == 'start':
                if elem.tag == 'root':
                    pass
                else:
                    self.start_handler(elem)
            elif event == 'end':
                if elem.tag == 'ImmuneChain':
                    yield self.chain
                elif elem.tag == 'root':
                    pass
                else:
                    self.end_handler(elem)


class PredicateParserVDJXML(ParserVDJXML):
    """VDJXML Parser that takes a predicate function"""

    def __init__(self, predicate):
        ParserVDJXML.__init__(self)
        self.predicate = predicate

    def parse(self, inputfile):
        for event, elem in ElementTree.iterparse(inputfile, events=('start', 'end')):
            if event == 'start':
                self.start_handler(elem)
            elif event == 'end':
                if elem.tag == 'ImmuneChain':
                    if self.predicate(self.chain) == True:
                        yield self.chain
                else:
                    self.end_handler(elem)


def parse_VDJXML(inputfile):
    vdjxmlparser = ParserVDJXML()
    return vdjxmlparser.parse(inputfile)


def filter_parse_VDJXML(inputfile, predicate):
    vdjxmlparser = PredicateParserVDJXML(predicate)
    return vdjxmlparser.parse(inputfile)


def xml2imgt(chainXML):
    seq = Seq(chainXML.seq, generic_dna)
    chain = ImmuneChain(seq=seq, id=chainXML.descr, name=chainXML.descr, description=chainXML.descr)
    chain.annotations['barcode'] = chainXML.barcode
    chain.add_tags(list(chainXML.tags))
    chain.annotations['clone'] = chainXML.clone
    if 'coding' not in chain.tags:
        raise ValueError, 'I want coding chains only.'
    vfeature = SeqFeature(location=FeatureLocation(0, chainXML.v_end_idx), type='V-REGION', strand=1, qualifiers={'allele': [chainXML.v]})
    jfeature = SeqFeature(location=FeatureLocation(chainXML.j_start_idx, len(seq)), type='J-REGION', strand=1, qualifiers={'allele': [chainXML.j]})
    cdr3feature = SeqFeature(location=FeatureLocation(chainXML.v_end_idx + 3, chainXML.j_start_idx - 3), type='CDR3-IMGT', strand=1)
    chain.features.append(vfeature)
    chain.features.append(jfeature)
    chain.features.append(cdr3feature)
    chain._update_feature_dict()
    chain._process_source_feature()
    return chain