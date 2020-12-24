# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/vcf/model.py
# Compiled at: 2016-03-18 12:18:31
# Size of source mod 2**32: 23697 bytes
from abc import ABCMeta, abstractmethod
import collections, sys, re
try:
    from collections import Counter
except ImportError:
    from counter import Counter

allele_delimiter = re.compile('[|/]')

class _Call(object):
    __doc__ = ' A genotype call, a cell entry in a VCF file'
    __slots__ = [
     'site', 'sample', 'data', 'gt_nums', 'gt_alleles', 'called', 'ploidity']

    def __init__(self, site, sample, data):
        self.site = site
        self.sample = sample
        self.data = data
        if hasattr(self.data, 'GT'):
            self.gt_alleles = [al if al != '.' else None for al in allele_delimiter.split(self.data.GT)]
            self.ploidity = len(self.gt_alleles)
            self.called = all([al != None for al in self.gt_alleles])
            self.gt_nums = self.data.GT if self.called else None
        else:
            self.gt_alleles = None
            self.ploidity = None
            self.called = None
            self.gt_nums = None

    def __repr__(self):
        return 'Call(sample=%s, %s)' % (self.sample, str(self.data))

    def __eq__(self, other):
        """ Two _Calls are equal if their _Records are equal
            and the samples and ``gt_type``s are the same
        """
        return self.site == getattr(other, 'site', None) and self.sample == getattr(other, 'sample', None) and self.gt_type == getattr(other, 'gt_type', None)

    def __getstate__(self):
        return dict((attr, getattr(self, attr)) for attr in self.__slots__)

    def __setstate__(self, state):
        for attr in self.__slots__:
            setattr(self, attr, state.get(attr))

    def gt_phase_char(self):
        if not self.phased:
            return '/'
        return '|'

    @property
    def gt_bases(self):
        """The actual genotype alleles.
           E.g. if VCF genotype is 0/1, return A/G
        """
        if self.called:
            try:
                return self.gt_phase_char().join(str(self.site.alleles[int(X)]) for X in self.gt_alleles)
            except:
                sys.stderr.write('Allele number not found in list of alleles\n')

        else:
            return

    @property
    def gt_type(self):
        """The type of genotype.
           hom_ref  = 0
           het      = 1
           hom_alt  = 2  (we don;t track _which+ ALT)
           uncalled = None
        """
        if self.called:
            alleles = self.gt_alleles
            if all(X == alleles[0] for X in alleles[1:]):
                if alleles[0] == '0':
                    return 0
                else:
                    return 2
            else:
                return 1
        else:
            return

    @property
    def phased(self):
        """A boolean indicating whether or not
           the genotype is phased for this sample
        """
        return self.gt_nums is not None and self.gt_nums.find('|') >= 0

    def __getitem__(self, key):
        """ Lookup value, backwards compatibility """
        return getattr(self.data, key)

    @property
    def is_variant(self):
        """ Return True if not a reference call """
        if not self.called:
            return
        return self.gt_type != 0

    @property
    def is_het(self):
        """ Return True for heterozygous calls """
        if not self.called:
            return
        return self.gt_type == 1


class _Record(object):
    __doc__ = ' A set of calls at a site.  Equivalent to a row in a VCF file.\n\n        The standard VCF fields CHROM, POS, ID, REF, ALT, QUAL, FILTER,\n        INFO and FORMAT are available as properties.\n\n        The list of genotype calls is in the ``samples`` property.\n\n        Regarding the coordinates associated with each instance:\n\n        - ``POS``, per VCF specification, is the one-based index\n          (the first base of the contig has an index of 1) of the first\n          base of the ``REF`` sequence.\n        - The ``start`` and ``end`` denote the coordinates of the entire\n          ``REF`` sequence in the zero-based, half-open coordinate\n          system (see\n          http://genomewiki.ucsc.edu/index.php/Coordinate_Transforms),\n          where the first base of the contig has an index of 0, and the\n          interval runs up to, but does not include, the base at the\n          ``end`` index. This indexing scheme is analagous to Python\n          slice notation.\n        - The ``affected_start`` and ``affected_end`` coordinates are\n          also in the zero-based, half-open coordinate system. These\n          coordinates indicate the precise region of the reference\n          genome actually affected by the events denoted in ``ALT``\n          (i.e., the minimum ``affected_start`` and maximum\n          ``affected_end``).\n\n          - For SNPs and structural variants, the affected region\n            includes all bases of ``REF``, including the first base\n            (i.e., ``affected_start = start = POS - 1``).\n          - For deletions, the region includes all bases of ``REF``\n            except the first base, which flanks upstream the actual\n            deletion event, per VCF specification.\n          - For insertions, the ``affected_start`` and ``affected_end``\n            coordinates represent a 0 bp-length region between the two\n            flanking bases (i.e., ``affected_start`` =\n            ``affected_end``). This is analagous to Python slice\n            notation (see http://stackoverflow.com/a/2947881/38140).\n            Neither the upstream nor downstream flanking bases are\n            included in the region.\n    '

    def __init__(self, CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, sample_indexes, samples=None):
        self.CHROM = CHROM
        self.POS = POS
        self.ID = ID
        self.REF = REF
        self.ALT = ALT
        self.QUAL = QUAL
        self.FILTER = FILTER
        self.INFO = INFO
        self.FORMAT = FORMAT
        self.start = self.POS - 1
        self.end = self.start + len(self.REF)
        self.alleles = [
         self.REF]
        self.alleles.extend(self.ALT)
        self.samples = samples or []
        self._sample_indexes = sample_indexes
        self.affected_start = None
        self.affected_end = None
        self._set_start_and_end()

    def _set_start_and_end(self):
        self.affected_start = self.affected_end = self.POS
        for alt in self.ALT:
            if alt is None:
                start, end = self._compute_coordinates_for_none_alt()
            else:
                if alt.type == 'SNV':
                    start, end = self._compute_coordinates_for_snp()
                else:
                    if alt.type == 'MNV':
                        start, end = self._compute_coordinates_for_indel()
                    else:
                        start, end = self._compute_coordinates_for_sv()
            self.affected_start = min(self.affected_start, start)
            self.affected_end = max(self.affected_end, end)

    def _compute_coordinates_for_none_alt(self):
        start = self.POS - 1
        end = start + len(self.REF)
        return (start, end)

    def _compute_coordinates_for_snp(self):
        if len(self.REF) > 1:
            start = self.POS
            end = start + (len(self.REF) - 1)
        else:
            start = self.POS - 1
            end = self.POS
        return (
         start, end)

    def _compute_coordinates_for_indel(self):
        if len(self.REF) > 1:
            start = self.POS
            end = start + (len(self.REF) - 1)
        else:
            start = end = self.POS
        return (
         start, end)

    def _compute_coordinates_for_sv(self):
        start = self.POS - 1
        end = start + len(self.REF)
        return (start, end)

    def __cmp__(self, other):
        return cmp((self.CHROM, self.POS), (getattr(other, 'CHROM', None), getattr(other, 'POS', None)))

    def __eq__(self, other):
        """ _Records are equal if they describe the same variant (same position, alleles) """
        return self.CHROM == getattr(other, 'CHROM', None) and self.POS == getattr(other, 'POS', None) and self.REF == getattr(other, 'REF', None) and self.ALT == getattr(other, 'ALT', None)

    def __lt__(self, other):
        return (
         self.CHROM, self.POS) < (getattr(other, 'CHROM', None), getattr(other, 'POS', None))

    def __iter__(self):
        return iter(self.samples)

    def __str__(self):
        return 'Record(CHROM=%(CHROM)s, POS=%(POS)s, REF=%(REF)s, ALT=%(ALT)s)' % self.__dict__

    def add_format(self, fmt):
        self.FORMAT = self.FORMAT + ':' + fmt

    def add_filter(self, flt):
        if self.FILTER is None:
            self.FILTER = [
             flt]
        else:
            self.FILTER.append(flt)

    def add_info(self, info, value=True):
        self.INFO[info] = value

    def genotype(self, name):
        """ Lookup a ``_Call`` for the sample given in ``name`` """
        return self.samples[self._sample_indexes[name]]

    @property
    def num_called(self):
        """ The number of called samples"""
        return sum(s.called for s in self.samples)

    @property
    def call_rate(self):
        """ The fraction of genotypes that were actually called. """
        return float(self.num_called) / float(len(self.samples))

    @property
    def num_hom_ref(self):
        """ The number of homozygous for ref allele genotypes"""
        return len([s for s in self.samples if s.gt_type == 0])

    @property
    def num_hom_alt(self):
        """ The number of homozygous for alt allele genotypes"""
        return len([s for s in self.samples if s.gt_type == 2])

    @property
    def num_het(self):
        """ The number of heterozygous genotypes"""
        return len([s for s in self.samples if s.gt_type == 1])

    @property
    def num_unknown(self):
        """ The number of unknown genotypes"""
        return len([s for s in self.samples if s.gt_type is None])

    @property
    def aaf(self):
        """ A list of allele frequencies of alternate alleles.
           NOTE: Denominator calc'ed from _called_ genotypes.
        """
        num_chroms = 0.0
        allele_counts = Counter()
        for s in self.samples:
            if s.gt_type is not None:
                for a in s.gt_alleles:
                    allele_counts.update([a])
                    num_chroms += 1

        return [allele_counts[str(i)] / num_chroms for i in range(1, len(self.ALT) + 1)]

    @property
    def nucl_diversity(self):
        """
        pi_hat (estimation of nucleotide diversity) for the site.
        This metric can be summed across multiple sites to compute regional
        nucleotide diversity estimates.  For example, pi_hat for all variants
        in a given gene.

        Derived from:
        "Population Genetics: A Concise Guide, 2nd ed., p.45"
        John Gillespie.
        """
        if len(self.ALT) > 1:
            return
        p = self.aaf[0]
        q = 1.0 - p
        num_chroms = float(2.0 * self.num_called)
        return float(num_chroms / (num_chroms - 1.0)) * (2.0 * p * q)

    @property
    def heterozygosity(self):
        """
        Heterozygosity of a site. Heterozygosity gives the probability that
        two randomly chosen chromosomes from the population have different
        alleles, giving a measure of the degree of polymorphism in a population.

        If there are i alleles with frequency p_i, H=1-sum_i(p_i^2)
        """
        allele_freqs = [
         1 - sum(self.aaf)] + self.aaf
        return 1 - sum([x ** 2 for x in allele_freqs])

    def get_hom_refs(self):
        """ The list of hom ref genotypes"""
        return [s for s in self.samples if s.gt_type == 0]

    def get_hom_alts(self):
        """ The list of hom alt genotypes"""
        return [s for s in self.samples if s.gt_type == 2]

    def get_hets(self):
        """ The list of het genotypes"""
        return [s for s in self.samples if s.gt_type == 1]

    def get_unknowns(self):
        """ The list of unknown genotypes"""
        return [s for s in self.samples if s.gt_type is None]

    @property
    def is_snp(self):
        """ Return whether or not the variant is a SNP """
        if len(self.REF) > 1:
            return False
        for alt in self.ALT:
            if alt is None or alt.type != 'SNV':
                return False
            if alt not in ('A', 'C', 'G', 'T', 'N', '*'):
                return False

        return True

    @property
    def is_indel(self):
        """ Return whether or not the variant is an INDEL """
        is_sv = self.is_sv
        if len(self.REF) > 1 and not is_sv:
            return True
        for alt in self.ALT:
            if alt is None:
                return True
            if alt.type != 'SNV' and alt.type != 'MNV':
                return False
            if len(alt) != len(self.REF):
                if not is_sv:
                    return True
                else:
                    return False

        return False

    @property
    def is_sv(self):
        """ Return whether or not the variant is a structural variant """
        if self.INFO.get('SVTYPE') is None:
            return False
        return True

    @property
    def is_transition(self):
        """ Return whether or not the SNP is a transition """
        if len(self.ALT) > 1:
            return False
        if self.is_snp:
            alt_allele = self.ALT[0]
            if self.REF == 'A' and alt_allele == 'G' or self.REF == 'G' and alt_allele == 'A' or self.REF == 'C' and alt_allele == 'T' or self.REF == 'T' and alt_allele == 'C':
                return True
            else:
                return False
        else:
            return False

    @property
    def is_deletion(self):
        """ Return whether or not the INDEL is a deletion """
        if len(self.ALT) > 1:
            return False
        if self.is_indel:
            alt_allele = self.ALT[0]
            if alt_allele is None:
                return True
            else:
                if len(self.REF) > len(alt_allele):
                    return True
                return False
        else:
            return False

    @property
    def var_type(self):
        """
        Return the type of variant [snp, indel, unknown]
        TO DO: support SVs
        """
        if self.is_snp:
            return 'snp'
        else:
            if self.is_indel:
                return 'indel'
            if self.is_sv:
                return 'sv'
            return 'unknown'

    @property
    def var_subtype(self):
        """
        Return the subtype of variant.

        - For SNPs and INDELs, yeild one of: [ts, tv, ins, del]
        - For SVs yield either "complex" or the SV type defined in the ALT
          fields (removing the brackets). E.g.::

              <DEL>       -> DEL
              <INS:ME:L1> -> INS:ME:L1
              <DUP>       -> DUP

        The logic is meant to follow the rules outlined in the following
        paragraph at:

        http://www.1000genomes.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-41

        "For precisely known variants, the REF and ALT fields should contain
        the full sequences for the alleles, following the usual VCF conventions.
        For imprecise variants, the REF field may contain a single base and the
        ALT fields should contain symbolic alleles (e.g. <ID>), described in more
        detail below. Imprecise variants should also be marked by the presence
        of an IMPRECISE flag in the INFO field."
        """
        if self.is_snp:
            if self.is_transition:
                return 'ts'
            else:
                if len(self.ALT) == 1:
                    return 'tv'
                return 'unknown'
        else:
            if self.is_indel:
                if self.is_deletion:
                    return 'del'
                else:
                    if len(self.ALT) == 1:
                        return 'ins'
                    return 'unknown'
            else:
                if self.is_sv:
                    if self.INFO['SVTYPE'] == 'BND':
                        return 'complex'
                    else:
                        if self.is_sv_precise:
                            return self.INFO['SVTYPE']
                        return self.ALT[0].type
                else:
                    return 'unknown'

    @property
    def sv_end(self):
        """ Return the end position for the SV """
        if self.is_sv:
            return self.INFO['END']

    @property
    def is_sv_precise(self):
        """ Return whether the SV cordinates are mapped
            to 1 b.p. resolution.
        """
        if self.INFO.get('IMPRECISE') is None and not self.is_sv:
            return False
        if self.INFO.get('IMPRECISE') is not None and self.is_sv:
            return False
        if self.INFO.get('IMPRECISE') is None and self.is_sv:
            return True

    @property
    def is_monomorphic(self):
        """ Return True for reference calls """
        return len(self.ALT) == 1 and self.ALT[0] is None


class _AltRecord(object, metaclass=ABCMeta):
    __doc__ = 'An alternative allele record: either replacement string, SV placeholder, or breakend'

    def __init__(self, type, **kwargs):
        super(_AltRecord, self).__init__(**kwargs)
        self.type = type

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.type == getattr(other, 'type', None)


class _Substitution(_AltRecord):
    __doc__ = 'A basic ALT record, where a REF sequence is replaced by an ALT sequence'

    def __init__(self, nucleotides, **kwargs):
        if len(nucleotides) == 1:
            super(_Substitution, self).__init__(type='SNV', **kwargs)
        else:
            super(_Substitution, self).__init__(type='MNV', **kwargs)
        self.sequence = str(nucleotides)

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.sequence)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.sequence == other
        if not isinstance(other, self.__class__):
            return False
        return super(_Substitution, self).__eq__(other) and self.sequence == other.sequence


class _Breakend(_AltRecord):
    __doc__ = 'A breakend which is paired to a remote location on or off the genome'

    def __init__(self, chr, pos, orientation, remoteOrientation, connectingSequence, withinMainAssembly, **kwargs):
        super(_Breakend, self).__init__(type='BND', **kwargs)
        if chr is not None:
            self.chr = str(chr)
        else:
            self.chr = None
        if pos is not None:
            self.pos = int(pos)
        else:
            self.pos = None
        self.remoteOrientation = remoteOrientation
        self.withinMainAssembly = withinMainAssembly
        self.orientation = orientation
        self.connectingSequence = connectingSequence

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.chr is None:
            remoteTag = '.'
        else:
            if self.withinMainAssembly:
                remoteChr = self.chr
            else:
                remoteChr = '<' + self.chr + '>'
            if self.remoteOrientation:
                remoteTag = '[' + remoteChr + ':' + str(self.pos) + '['
            else:
                remoteTag = ']' + remoteChr + ':' + str(self.pos) + ']'
        if self.orientation:
            return remoteTag + self.connectingSequence
        else:
            return self.connectingSequence + remoteTag

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return super(_Breakend, self).__eq__(other) and self.chr == getattr(other, 'chr', None) and self.pos == getattr(other, 'pos', None) and self.remoteOrientation == getattr(other, 'remoteOrientation', None) and self.withinMainAssembly == getattr(other, 'withinMainAssembly', None) and self.orientation == getattr(other, 'orientation', None) and self.connectingSequence == getattr(other, 'connectingSequence', None)


class _SingleBreakend(_Breakend):
    __doc__ = 'A single breakend'

    def __init__(self, orientation, connectingSequence, **kwargs):
        super(_SingleBreakend, self).__init__(None, None, orientation, None, connectingSequence, None, **kwargs)


class _SV(_AltRecord):
    __doc__ = 'An SV placeholder'

    def __init__(self, type, **kwargs):
        super(_SV, self).__init__(type, **kwargs)

    def __str__(self):
        return '<' + self.type + '>'

    def __repr__(self):
        return str(self)


def make_calldata_tuple(fields):
    """ Return a namedtuple for a given call format """

    class CallData:
        __slots__ = ()
        _types = []
        _nums = []

        def __str__(self):
            dat = ', '.join(['%s=%s' % (x, y) for x, y in zip(self._fields, self)])
            return 'CallData(' + dat + ')'

        def __reduce__(self):
            args = super(CallData, self).__reduce__()
            return (make_calldata_tuple, (fields,))

    return CallData