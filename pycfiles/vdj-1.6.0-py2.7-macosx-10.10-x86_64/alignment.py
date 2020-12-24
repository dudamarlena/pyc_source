# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/alignment.py
# Compiled at: 2014-12-19 17:13:26
import warnings, copy, numpy as np
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
import seqtools, vdj
from vdj import refseq, alignmentcore
warnings.simplefilter('always')

class vdj_aligner(object):

    def __init__(self, **kw):
        self.numCrudeVCandidates = 5
        self.numCrudeDCandidates = 10
        self.numCrudeJCandidates = 2
        self.minVscore = 100
        self.minDscore = 4
        self.minJscore = 13
        if kw.has_key('rigorous') and kw['rigorous'] == True:
            self.numCrudeVCandidates = 10000
            self.numCrudeDCandidates = 10000
            self.numCrudeJCandidates = 10000
            self.minVscore = 20
            self.minDscore = 1
            self.minJscore = 5
        patternA = '111011001011010111'
        patternB = '1111000100010011010111'
        patternC = '111111111111'
        patternD = '110100001100010101111'
        patternE = '1110111010001111'
        self.seedpatterns = [patternA, patternB, patternC, patternD, patternE]
        self.miniseedpatterns = ['111011', '110111']
        self.patternPos = '111111111111'
        self.locus = kw['locus']
        self.refV = refseq.__getattribute__(self.locus + 'V')
        refV_seqs = dict([ (allele, record.seq.tostring()) for allele, record in self.refV.iteritems() ])
        self.Vseqlistkeys = vdj_aligner.seqdict2kmers(refV_seqs, self.seedpatterns)
        self.refJ = refseq.__getattribute__(self.locus + 'J')
        refJ_seqs = dict([ (allele, record.seq.tostring()) for allele, record in self.refJ.iteritems() ])
        self.Jseqlistkeys = vdj_aligner.seqdict2kmers(refJ_seqs, self.seedpatterns)
        try:
            self.refD = refseq.__getattribute__(self.locus + 'D')
            refD_seqs = dict([ (allele, record.seq.tostring()) for allele, record in self.refD.iteritems() ])
            self.Dseqlistkeysmini = vdj_aligner.seqdict2kmers(refD_seqs, self.miniseedpatterns)
        except AttributeError:
            pass

        posVseqlistkeys = vdj_aligner.seqdict2kmers(refV_seqs, [self.patternPos])
        posJseqlistkeys = vdj_aligner.seqdict2kmers(refJ_seqs, [self.patternPos])
        negVseqlistkeys = vdj_aligner.seqdict2kmers(vdj_aligner.seqdict2revcompseqdict(refV_seqs), [self.patternPos])
        negJseqlistkeys = vdj_aligner.seqdict2kmers(vdj_aligner.seqdict2revcompseqdict(refJ_seqs), [self.patternPos])
        posset = set([])
        for key in posVseqlistkeys.keys():
            posset.update(posVseqlistkeys[key][self.patternPos])

        for key in posJseqlistkeys.keys():
            posset.update(posJseqlistkeys[key][self.patternPos])

        negset = set([])
        for key in negVseqlistkeys.keys():
            negset.update(negVseqlistkeys[key][self.patternPos])

        for key in negJseqlistkeys.keys():
            negset.update(negJseqlistkeys[key][self.patternPos])

        possetnew = posset - negset
        negsetnew = negset - posset
        self.posset = possetnew
        self.negset = negsetnew

    def Valign_chain(self, chain, verbose=False):
        querykeys = vdj_aligner.seq2kmers(chain.seq.tostring(), self.seedpatterns)
        Vscores_hash = vdj_aligner.hashscore(self.Vseqlistkeys, querykeys)
        goodVseglist = sorted(self.refV.keys(), key=lambda k: Vscores_hash[k], reverse=True)[0:self.numCrudeVCandidates]
        goodVsegdict = dict([ (seg, self.refV[seg].seq.tostring()) for seg in goodVseglist ])
        bestVseg, bestVscore, bestVscoremat, bestVtracemat = vdj_aligner.bestalignNW(goodVsegdict, chain.seq.tostring(), self.minVscore)
        if bestVseg is not None:
            Vrefaln, Vqueryaln = vdj_aligner.construct_alignment(self.refV[bestVseg].seq.tostring(), chain.seq.tostring(), bestVscoremat, bestVtracemat)
            coord_mapping = vdj_aligner.ungapped_coord_mapping(Vrefaln, Vqueryaln)
            seqtools.copy_features(self.refV[bestVseg], chain, coord_mapping, erase=['translation'], replace=False)
            chain.annotations['gapped_query'] = Vqueryaln
            chain.annotations['gapped_reference'] = Vrefaln
            curr_annot = chain.letter_annotations['alignment']
            aln_annot = vdj_aligner.alignment_annotation(Vrefaln, Vqueryaln)
            aln_annot = aln_annot.translate(None, 'D')
            lNER = len(aln_annot) - len(aln_annot.lstrip('I'))
            rNER = len(aln_annot.rstrip('I'))
            chain.letter_annotations['alignment'] = curr_annot[:lNER] + aln_annot[lNER:rNER] + curr_annot[rNER:]
            chain._update_feature_dict()
            try:
                chain.features.pop(chain._features['CDR3-IMGT'][0])
                chain._features.pop('CDR3-IMGT')
                chain._update_feature_dict()
            except KeyError:
                pass

            cys = chain.features[chain._features['2nd-CYS'][0]]
            v_reg = chain.features[chain._features['V-REGION'][0]]
            v_reg.qualifiers['codon_start'] = [cys.location.start.position % 3 + 1]
        return bestVscore

    def Jalign_chain(self, chain, verbose=False):
        try:
            second_cys = chain.__getattribute__('2nd-CYS')
            second_cys_offset = second_cys.location.end.position
            query = chain.seq.tostring()[second_cys_offset:]
        except AttributeError:
            query = chain.seq.tostring()
            second_cys_offset = 0

        querykeys = vdj_aligner.seq2kmers(query, self.seedpatterns)
        Jscores_hash = vdj_aligner.hashscore(self.Jseqlistkeys, querykeys)
        goodJseglist = sorted(self.refJ.keys(), key=lambda k: Jscores_hash[k], reverse=True)[0:self.numCrudeJCandidates]
        goodJsegdict = dict([ (seg, self.refJ[seg].seq.tostring()) for seg in goodJseglist ])
        bestJseg, bestJscore, bestJscoremat, bestJtracemat = vdj_aligner.bestalignNW(goodJsegdict, query, self.minJscore)
        if bestJseg is not None:
            Jrefaln, Jqueryaln = vdj_aligner.construct_alignment(self.refJ[bestJseg].seq.tostring(), query, bestJscoremat, bestJtracemat)
            coord_mapping = vdj_aligner.ungapped_coord_mapping(Jrefaln, Jqueryaln)
            seqtools.copy_features(self.refJ[bestJseg], chain, coord_mapping, offset=second_cys_offset, erase=['translation'], replace=False)
            chain._update_feature_dict()
            gapped_query = chain.annotations.get('gapped_query', '')
            gapped_reference = chain.annotations.get('gapped_reference', '')
            gapped_CDR3_offset = vdj_aligner.ungapped2gapped_coord(chain.seq.tostring(), gapped_query, second_cys_offset)
            gapped_Vref_aln_end = len(gapped_reference.rstrip('-'))
            chain.annotations['gapped_query'] = gapped_query[:gapped_Vref_aln_end] + Jqueryaln[gapped_Vref_aln_end - gapped_CDR3_offset:]
            chain.annotations['gapped_reference'] = gapped_reference[:gapped_Vref_aln_end] + Jrefaln[gapped_Vref_aln_end - gapped_CDR3_offset:]
            curr_annot = chain.letter_annotations['alignment']
            aln_annot = vdj_aligner.alignment_annotation(Jrefaln, Jqueryaln)
            aln_annot = aln_annot.translate(None, 'D')
            lNER = len(aln_annot) - len(aln_annot.lstrip('I'))
            rNER = len(aln_annot.rstrip('I'))
            chain.letter_annotations['alignment'] = curr_annot[:second_cys_offset + lNER] + aln_annot[lNER:rNER] + curr_annot[second_cys_offset + rNER:]
        return bestJscore

    def Dalign_chain(self, chain, verbose=False):
        query = chain.junction
        querykeys = vdj_aligner.seq2kmers(query, self.miniseedpatterns)
        Dscores_hash = vdj_aligner.hashscore(self.Dseqlistkeysmini, querykeys)
        goodDseglist = sorted(self.refD.keys(), key=lambda k: Dscores_hash[k], reverse=True)[0:self.numCrudeDCandidates]
        goodDsegdict = dict([ (seg, self.refD[seg].seq.tostring()) for seg in goodDseglist ])
        bestDseg, bestDscore, bestDscoremat, bestDtracemat = vdj_aligner.bestalignSW(goodDsegdict, query, self.minDscore)
        if bestDseg is not None:
            chain.annotations['D-REGION'] = bestDseg
        return bestDscore

    def align_chain(self, chain, verbose=False, debug=False):
        if debug:
            import pdb
            pdb.set_trace()
        if chain.seq.tostring() != chain.seq.tostring().upper():
            raise ValueError, 'aligner requires all uppercase alphabet.'
        if not chain.has_tag('positive') and not chain.has_tag('coding'):
            warnings.warn('chain %s may not be the correct strand' % chain.id)
        chain.letter_annotations['alignment'] = '_' * len(chain)
        scores = {}
        scores['v'] = self.Valign_chain(chain, verbose)
        scores['j'] = self.Jalign_chain(chain, verbose)
        try:
            if chain.v and chain.j:
                cdr3_start = chain.__getattribute__('2nd-CYS').location.end.position
                try:
                    cdr3_end = chain.__getattribute__('J-PHE').location.start.position
                except AttributeError:
                    cdr3_end = chain.__getattribute__('J-TRP').location.start.position

                cdr3_feature = SeqFeature(location=FeatureLocation(cdr3_start, cdr3_end), type='CDR3-IMGT', strand=1)
                chain.features.append(cdr3_feature)
                chain._update_feature_dict()
                curr_annot = chain.letter_annotations['alignment']
                chain.letter_annotations['alignment'] = curr_annot[:cdr3_start] + '3' * (cdr3_end - cdr3_start) + curr_annot[cdr3_end:]
                if self.locus in ('IGH', 'TRB', 'TRD'):
                    scores['d'] = self.Dalign_chain(chain, verbose)
        except AttributeError:
            pass

        return scores

    def coding_chain(self, chain, verbose=False):
        strand = self.seq2coding(chain.seq.tostring())
        if strand == -1:
            chain.seq = chain.seq.reverse_complement()
            chain.add_tag('revcomp')
        chain.add_tag('coding')

    def seq2coding(self, seq):
        seqkeys = vdj_aligner.seq2kmers(seq, [self.patternPos])
        seqwords = seqkeys[self.patternPos]
        strandid = 1
        if len(self.negset & seqwords) > len(self.posset & seqwords):
            strandid = -1
        return strandid

    @staticmethod
    def seq2kmers(seq, patterns):
        """Given sequence and patterns, for each pattern, compute all corresponding k-mers from sequence.
        
        The result is seqannot[pattern][key]=[pos1,pos2,...,posN] in seq
                      seqkeys[pattern] = set([kmers])
        
        """
        seqkeys = {}
        patlens = []
        for pattern in patterns:
            patlens.append(len(pattern))
            seqkeys[pattern] = set()

        maxpatlen = max(patlens)
        for i in xrange(len(seq)):
            word = seq[i:i + maxpatlen]
            for pattern in patterns:
                patlen = len(pattern)
                if len(word) >= patlen:
                    key = ''
                    for j in xrange(patlen):
                        if pattern[j] == '1':
                            key += word[j]

                    seqkeys[pattern].add(key)

        return seqkeys

    @staticmethod
    def seqdict2kmers(seqdict, patterns):
        seqlistkeys = {}
        for seq in seqdict.iteritems():
            seqlistkeys[seq[0]] = vdj_aligner.seq2kmers(seq[1], patterns)

        return seqlistkeys

    @staticmethod
    def hashscore(refkeys, querykeys):
        """Compute number of common keys for each reference sequence.
    
        querykeys is dict of sets, where dict keys are patterns
        reference keys is dict of ref seqs, where each elt is a
        dict of patterns with sets as values.  the patterns must be
        the same
        """
        scores = {}
        for seg in refkeys.iterkeys():
            score = 0
            for pattern in querykeys.iterkeys():
                score += len(refkeys[seg][pattern] & querykeys[pattern])

            scores[seg] = score

        return scores

    @staticmethod
    def bestalignNW(candidatedict, query, minscore):
        bestseg = None
        bestscore = minscore
        bestscoremat = None
        besttracemat = None
        seq2 = query
        for seg, seq1 in candidatedict.iteritems():
            scores = np.zeros([len(seq1) + 1, len(seq2) + 1])
            Ix = np.zeros([len(seq1) + 1, len(seq2) + 1])
            Iy = np.zeros([len(seq1) + 1, len(seq2) + 1])
            trace = np.zeros([len(seq1) + 1, len(seq2) + 1], dtype=np.int)
            alignmentcore.alignNW(scores, Ix, Iy, trace, seq1, seq2)
            currscore = vdj_aligner.scoreVJalign(scores)
            if currscore > bestscore:
                bestscore = currscore
                bestseg = seg
                bestscoremat = scores
                besttracemat = trace

        return (
         bestseg, bestscore, bestscoremat, besttracemat)

    @staticmethod
    def bestalignSW(candidatedict, query, minscore):
        bestseg = None
        bestscore = minscore
        bestscoremat = None
        besttracemat = None
        seq2 = query
        for seg, seq1 in candidatedict.iteritems():
            scores = np.zeros([len(seq1) + 1, len(seq2) + 1])
            trace = np.zeros([len(seq1) + 1, len(seq2) + 1], dtype=np.int)
            alignmentcore.alignSW(scores, trace, seq1, seq2)
            currscore = vdj_aligner.scoreDalign(scores)
            if currscore > bestscore:
                bestscore = currscore
                bestseg = seg
                bestscoremat = scores
                besttracemat = trace

        return (
         bestseg, bestscore, bestscoremat, besttracemat)

    @staticmethod
    def alignment_annotation(aln_ref, aln_query):
        assert len(aln_query) == len(aln_ref)
        annot = ''
        for ref_letter, query_letter in zip(aln_ref, aln_query):
            if query_letter == '-':
                annot += 'D'
            elif ref_letter == '-':
                annot += 'I'
            elif query_letter == ref_letter:
                annot += '.'
            else:
                annot += 'S'

        return annot

    @staticmethod
    def gapped_alignment_masked_annotation(chain, debug=False):
        """Returns full-chain/CDR3 masked annotation of fully gapped aln, including insertions and deletions."""
        gapped_ref = chain.annotations['gapped_reference']
        gapped_query = chain.annotations['gapped_query']
        gapped_annot = vdj_aligner.alignment_annotation(gapped_ref, gapped_query)
        ungapped_v_start = chain.__getattribute__('V-REGION').location.nofuzzy_start
        ungapped_j_end = chain.__getattribute__('J-REGION').location.nofuzzy_end
        ungapped_cdr3_start = chain.__getattribute__('2nd-CYS').location.end.position
        try:
            ungapped_cdr3_end = chain.__getattribute__('J-PHE').location.start.position
        except AttributeError:
            ungapped_cdr3_end = chain.__getattribute__('J-TRP').location.start.position

        gapped_v_start = vdj.alignment.vdj_aligner.ungapped2gapped_coord(chain.seq.tostring(), gapped_query, ungapped_v_start)
        gapped_j_end = vdj.alignment.vdj_aligner.ungapped2gapped_coord(chain.seq.tostring(), gapped_query, ungapped_j_end)
        gapped_cdr3_start = vdj.alignment.vdj_aligner.ungapped2gapped_coord(chain.seq.tostring(), gapped_query, ungapped_cdr3_start)
        gapped_cdr3_end = vdj.alignment.vdj_aligner.ungapped2gapped_coord(chain.seq.tostring(), gapped_query, ungapped_cdr3_end)
        masked_annot = '_' * gapped_v_start + gapped_annot[gapped_v_start:gapped_cdr3_start] + '3' * (gapped_cdr3_end - gapped_cdr3_start) + gapped_annot[gapped_cdr3_end:gapped_j_end] + '_' * (len(gapped_annot) - gapped_j_end)
        if debug:
            s = []
            s.append(('').join([ '/%-9i' % i for i in range(0, 500, 10) ]))
            s.append('%s    %s' % (gapped_ref, 'gapped_ref'))
            s.append('%s    %s' % (gapped_query, 'gapped_query'))
            s.append('%s    %s' % (gapped_annot, 'gapped_annot'))
            s.append('%s    %s' % (masked_annot, 'masked_annot'))
            s.append(' ' * (gapped_v_start - 1) + '/' + ' ' * (gapped_cdr3_start - gapped_v_start - 1) + '/' + ' ' * (gapped_cdr3_end - gapped_cdr3_start - 1) + '/' + ' ' * (gapped_j_end - gapped_cdr3_end - 1) + '/')
            s.append('')
            s.append(chain.seq.tostring())
            s.append(chain.letter_annotations['alignment'])
            print ('\n').join(s)
        return masked_annot

    @staticmethod
    def ungapped_coord_mapping(aln_from, aln_to):
        if len(aln_from) != len(aln_to):
            raise ValueError, 'from and to strings must be same length'
        coord_from = 0
        coord_to = 0
        mapping = {}
        for coord_gapped in range(len(aln_from)):
            if aln_from[coord_gapped - 1:coord_gapped + 1] == '--':
                coord_to += 1
                continue
            mapping.setdefault(coord_from, []).append(coord_to)
            if aln_from[coord_gapped] != '-':
                coord_from += 1
            if aln_to[coord_gapped] != '-':
                coord_to += 1

        mapping.setdefault(coord_from, []).append(coord_to)
        return mapping

    @staticmethod
    def ungapped2gapped_coord(ungapped, gapped, ungapped_coord):
        left_gaps = len(gapped) - len(gapped.lstrip('-'))
        gapped_coord = ungapped_coord + left_gaps
        gaps = gapped.count('-', 0, gapped_coord)
        while gapped_coord - gaps < ungapped_coord:
            gapped_coord += gaps
            gaps = gapped.count('-', 0, gapped_coord)

        return gapped_coord

    @staticmethod
    def construct_alignment(seq1, seq2, scoremat, tracemat):
        """Construct alignment of ref segment to query from score and trace
        matrices.
        """
        nrows, ncols = scoremat.shape
        if len(seq1) + 1 != nrows or len(seq2) + 1 != ncols:
            raise Exception, 'nrows and ncols must be equal to len(seq1)+1 and len(seq2)+1'
        deltas = {0: (1, 1), 
           1: (1, 0), 
           2: (0, 1), 
           3: (0, 0)}
        col = np.argmax(scoremat[nrows - 1, :])
        row = nrows - 1
        aln1 = seq1[row - 1:] + '-' * (ncols - col - 1)
        aln2 = seq2[col - 1:] + '-' * (nrows - row - 1)
        while row - 1 > 0 and col - 1 > 0:
            rowchange, colchange = deltas[tracemat[(row, col)]]
            if rowchange == 1:
                row -= 1
                aln1 = seq1[(row - 1)] + aln1
            elif rowchange == 0:
                aln1 = '-' + aln1
            else:
                raise Exception, 'Trace matrix contained jump of greater than one row/col.'
            if colchange == 1:
                col -= 1
                aln2 = seq2[(col - 1)] + aln2
            elif colchange == 0:
                aln2 = '-' + aln2
            else:
                raise Exception, 'Trace matrix contained jump of greater than one row/col.'

        aln1 = seq1[:row - 1] + '-' * (col - 1) + aln1
        aln2 = seq2[:col - 1] + '-' * (row - 1) + aln2
        return (
         aln1, aln2)

    @staticmethod
    def scoreVJalign(scorematrix):
        """Computes score of V alignment given Needleman-Wunsch score matrix
        
        ASSUMES num rows < num cols, i.e., refseq V seg is on vertical axis
        
        """
        nrows, ncols = scorematrix.shape
        return np.max(scorematrix[nrows - 1, :])

    @staticmethod
    def scoreDalign(scorematrix):
        """Computes score of D alignment given Smith-Waterman score matrix
        
        """
        return np.max(scorematrix)

    @staticmethod
    def seqdict2revcompseqdict(seqdict):
        revcompdict = {}
        for item in seqdict.iteritems():
            revcompdict[item[0]] = seqtools.reverse_complement(item[1])

        return revcompdict


class vdj_aligner_combined(object):
    """vdj aligner for multiple loci
    
    this class will perform alignment for all specified loci, e.g., IGK and IGL
    and pick the one with the better V score
    """

    def __init__(self, **kw):
        self.loci = kw['loci']
        self.aligners = [ vdj_aligner(locus=locus, **kw) for locus in self.loci ]
        self.patternPos = '111111111111'
        self.posset = set()
        self.negset = set()
        for aligner in self.aligners:
            self.posset.update(aligner.posset)
            self.negset.update(aligner.negset)

    def align_chain(self, chain, verbose=False, debug=False):
        alignments = []
        for aligner in self.aligners:
            curr_chain = copy.deepcopy(chain)
            curr_score = aligner.align_chain(curr_chain, debug=debug)
            alignments.append((curr_chain, curr_score))

        alignments = sorted(filter(lambda a: hasattr(a[0], 'v'), alignments), key=lambda a: a[1]['v'], reverse=True)
        if len(alignments) > 0:
            bestchain = alignments[0][0]
            chain.__init__(bestchain)
            return alignments[0][1]

    def coding_chain(self, chain, verbose=False):
        strand = self.seq2coding(chain.seq.tostring())
        if strand == -1:
            chain.seq = chain.seq.reverse_complement()
            chain.add_tag('revcomp')
        chain.add_tag('coding')

    def seq2coding(self, seq):
        seqkeys = vdj_aligner.seq2kmers(seq, [self.patternPos])
        seqwords = seqkeys[self.patternPos]
        strandid = 1
        if len(self.negset & seqwords) > len(self.posset & seqwords):
            strandid = -1
        return strandid


def igh_aligner(**kw):
    return vdj_aligner(locus='IGH', **kw)


def igk_aligner(**kw):
    return vdj_aligner(locus='IGK', **kw)


def igl_aligner(**kw):
    return vdj_aligner(locus='IGL', **kw)


def igkl_aligner(**kw):
    return vdj_aligner_combined(loci=['IGK', 'IGL'], **kw)


def ighkl_aligner(**kw):
    return vdj_aligner_combined(loci=['IGH', 'IGK', 'IGL'], **kw)


def trb_aligner(**kw):
    return vdj_aligner(locus='TRB', **kw)


def tra_aligner(**kw):
    return vdj_aligner(locus='TRA', **kw)


def trd_aligner(**kw):
    return vdj_aligner(locus='TRD', **kw)


def trg_aligner(**kw):
    return vdj_aligner(locus='TRG', **kw)


def align_with_gaps(query, allele):
    pass