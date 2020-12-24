# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/pipeline.py
# Compiled at: 2014-12-16 17:37:19
import warnings
from Bio.Seq import Seq
from Bio.Alphabet import DNAAlphabet
import vdj, alignment, seqtools

def parse_jobfile(filename):
    parameters = {}
    ip = open(filename, 'r')
    for line in ip:
        data = line.split('#')[0].strip()
        if data == '':
            continue
        data = data.split('\t')
        name = data[0].strip()
        value = data[1].strip()
        if value == '':
            continue
        if name == 'locus':
            parameters.setdefault(name, []).append(value)
            continue
        if name == 'rigorous':
            parameters[name] = bool(value)
            continue
        parameters[name] = value

    ip.close()
    return parameters


def iterator2parts(iterator, basename, packetsize, prefix='', suffix=''):
    """Split data from iterator into multiple files"""
    parts = []
    num_processed = 0
    file_num = 1
    curr_outname = basename + '.' + str(file_num)
    for obj in iterator:
        if num_processed == 0:
            op = open(curr_outname, 'w')
            print >> op, prefix
            parts.append(curr_outname)
        print >> op, obj
        num_processed += 1
        if num_processed == packetsize:
            print >> op, suffix
            op.close()
            num_processed = 0
            file_num += 1
            curr_outname = basename + '.' + str(file_num)

    if not op.closed:
        print >> op, suffix
        op.close()
    return parts


def load_barcodes(barcode_file):
    bcip = open(barcode_file, 'r')
    barcodes = {}
    for descr, seq in seqtools.FastaIterator(bcip):
        barcodes[seq.upper()] = descr

    bcip.close()
    barcode_len = len(barcodes.keys()[0])
    for bc in barcodes.keys():
        if len(bc) != barcode_len:
            raise Exception, 'ERROR: All barcode lengths must be equal.'

    return barcodes


def id_barcode(chain, barcodes):
    barcode_len = len(barcodes.keys()[0])
    try:
        curr_barcode = barcodes[chain.seq.tostring()[:barcode_len].upper()]
    except KeyError:
        return

    chain.__init__(chain[barcode_len:])
    chain.annotations['barcode'] = curr_barcode


def load_isotypes(isotype_file):
    ighcip = open(isotype_file, 'r')
    isotypes = {}
    for descr, seq in seqtools.FastaIterator(ighcip):
        isotypes[seq.upper()] = descr

    ighcip.close()
    return isotypes


def id_isotype(chain, isotypes):
    if not chain.has_tag('positive') and not chain.has_tag('coding'):
        warnings.warn('chain %s may not be the correct strand' % chain.descr)
    for iso in isotypes.iteritems():
        if iso[0] in chain.seq[-50:]:
            chain.annotations['c'] = iso[1]


def fasta2imgt(inhandle, outhandle):
    for seq in SeqIO.parse(inhandle, 'fasta'):
        chain = vdj.ImmuneChain(seq)
        print >> outhandle, chain


def imgt2fasta(inhandle, outhandle):
    for chain in vdj.parse_imgt(inhandle):
        outhandle.write(chain.format('fasta'))


def partition_VJ(inhandle, basename):

    def vj_id_no_allele(chain):
        return seqtools.cleanup_id(chain.v.split('*')[0]) + '_' + seqtools.cleanup_id(chain.j.split('*')[0])

    def outname(basename, vj_id):
        return '%s.%s.imgt' % (basename, vj_id)

    outhandles = {}
    for chain in vdj.parse_imgt(inhandle):
        curr_vj_id = vj_id_no_allele(chain)
        try:
            print >> outhandles[curr_vj_id], chain
        except KeyError:
            outhandles[curr_vj_id] = open(outname(basename, curr_vj_id), 'w')
            print >> outhandles[curr_vj_id], chain

    for outhandle in outhandles.itervalues():
        outhandle.close()

    return [ outname(basename, vj_id) for vj_id in outhandles.iterkeys() ]


def translate_chain(chain):
    chain.annotations['translation'] = chain.seq.translate().tostring()
    for feature in chain.features:
        offset = int(feature.qualifiers.get('codon_start', [1])[0]) - 1
        feature.qualifiers['translation'] = feature.extract(chain.seq)[offset:].translate().tostring()


def sequence_force_in_frame(chain, replace=False):
    nt = ''
    cdr3_start = alignment.vdj_aligner.ungapped2gapped_coord(chain.seq.tostring(), chain.annotations['gapped_query'], chain.__getattribute__('CDR3-IMGT').location.nofuzzy_start)
    cdr3_len = len(chain.junction_nt)
    extra_junction = cdr3_len % 3
    for i, (r, q) in enumerate(zip(chain.annotations['gapped_reference'], chain.annotations['gapped_query'])):
        if i >= cdr3_start and i < cdr3_start + cdr3_len:
            in_cdr3 = True
        elif i == cdr3_start + cdr3_len:
            in_cdr3 = False
            nt += '-' * ((3 - cdr3_len % 3) % 3)
        else:
            in_cdr3 = False
        if r == '-':
            nt += '' if not in_cdr3 else q.upper()
        elif q == '-':
            nt += r.lower() if replace else q
        else:
            nt += q.upper()

    return nt


def translate_chain_force_in_frame(chain):
    nt = sequence_force_in_frame(chain, replace=False)
    return Seq(nt.replace('-', 'N'), DNAAlphabet()).translate().tostring()