# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/refseq.py
# Compiled at: 2014-12-16 17:37:19
import os, sys, types, glob, warnings
from Bio import SeqIO
from seqtools import FastaIterator
import params

def parse_imgt_fasta_header(record):
    raw_data = record.description.strip().split('|')
    data = {}
    data['accession'] = raw_data[0]
    data['allele'] = raw_data[1]
    data['group'] = data['allele'][0:4]
    data['gene'] = data['allele'].split('*')[0]
    data['species'] = raw_data[2]
    data['functionality'] = raw_data[3]
    data['imgt_label'] = raw_data[4]
    data['frame'] = int(raw_data[7]) - 1
    data['partial'] = raw_data[13]
    raw_coords_start = int(raw_data[5].split('.')[0])
    raw_coords_end = int(raw_data[5].split('.')[(-1)])
    coords = (raw_coords_start - 1, raw_coords_end)
    data['coords'] = coords
    return data


def get_X_REGION_feature(record, X):
    for feature in record.features:
        if feature.type == '%s-REGION' % X:
            return feature


def get_any_X_REGION_feature(record):
    for feature in record.features:
        if feature.type in ('V-REGION', 'D-REGION', 'J-REGION'):
            return feature


def has_CYS(record):
    for feature in record.features:
        if feature.type == '2nd-CYS':
            return True

    return False


def has_TRP_PHE(record):
    for feature in record.features:
        if feature.type in ('J-TRP', 'J-PHE'):
            return True

    return False


ref_dir = os.path.join(params.vdj_dir, params.data_dir)
ligm_index = None
processed_dir = os.path.join(params.vdj_dir, params.processed_dir, params.organism)
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir, mode=493)
reference_files = glob.glob(os.path.join(ref_dir, '*.fasta'))
processed_files = glob.glob(os.path.join(processed_dir, '*.imgt'))
get_group = lambda f: os.path.splitext(os.path.basename(f))[0]
groups_to_process = set(map(get_group, reference_files)) - set(map(get_group, processed_files))
files_to_process = filter(lambda f: get_group(f) in groups_to_process, reference_files)
for reference_fasta in files_to_process:
    if ligm_index == None:
        ligm_index = SeqIO.index(os.path.join(params.imgt_dir, 'imgt.dat'), 'imgt')
    group = get_group(reference_fasta)
    reference_imgt = os.path.join(processed_dir, group + '.imgt')
    reference_records = []
    for record in SeqIO.parse(reference_fasta, 'fasta'):
        try:
            header_data = parse_imgt_fasta_header(record)
        except ValueError as e:
            print >> sys.stderr, 'Problem with parsing fasta header\n%s\n%s' % (record.description, e)
            continue

        imgt_record = ligm_index[header_data['accession']]
        reference_record = imgt_record[header_data['coords'][0]:header_data['coords'][1]]
        reference_feature = get_X_REGION_feature(reference_record, group[(-1)])
        if reference_feature == None:
            print >> sys.stderr, "Couldn't find a %s-REGION feature in %s when clipped to fasta coords.  Skipping." % (group[(-1)], reference_record.id)
            continue
        if not reference_feature.qualifiers.has_key('allele'):
            warnings.warn("Reference record %s's %s is missing an `allele` qualifier; it (%s) was added manually." % (reference_record.id, reference_feature.type, header_data['allele']))
            reference_feature.qualifiers['allele'] = [header_data['allele']]
        elif reference_feature.qualifiers['allele'][0] != header_data['allele']:
            warnings.warn("Reference record %s's %s is annotated %s while the corres. fasta header annotates it as %s.  I picked the LIGM version." % (reference_record.id, reference_feature.type, reference_feature.qualifiers['allele'][0], header_data['allele']))
        if group[(-1)] == 'V' and not has_CYS(reference_record):
            continue
        elif group[(-1)] == 'J' and not has_TRP_PHE(reference_record):
            continue
        reference_records.append(reference_record)

    SeqIO.write(reference_records, reference_imgt, 'imgt')

get_allele = lambda record: get_any_X_REGION_feature(record).qualifiers['allele'][0]
IGHV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGHV.imgt'), 'imgt') ])
IGHD = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGHD.imgt'), 'imgt') ])
IGHJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGHJ.imgt'), 'imgt') ])
IGKV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGKV.imgt'), 'imgt') ])
IGKJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGKJ.imgt'), 'imgt') ])
IGLV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGLV.imgt'), 'imgt') ])
IGLJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'IGLJ.imgt'), 'imgt') ])
TRBV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRBV.imgt'), 'imgt') ])
TRBD = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRBD.imgt'), 'imgt') ])
TRBJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRBJ.imgt'), 'imgt') ])
TRAV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRAV.imgt'), 'imgt') ])
TRAJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRAJ.imgt'), 'imgt') ])
TRDV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRDV.imgt'), 'imgt') ])
TRDD = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRDD.imgt'), 'imgt') ])
TRDJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRDJ.imgt'), 'imgt') ])
TRGV = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRGV.imgt'), 'imgt') ])
TRGJ = dict([ (get_allele(r), r) for r in SeqIO.parse(os.path.join(processed_dir, 'TRGJ.imgt'), 'imgt') ])
ALL = reduce(lambda a, b: dict(a.items() + b.items()), [IGHV, IGHD, IGHJ, IGKV, IGKJ, IGLV, IGLJ, TRBV, TRBD, TRBJ, TRAV, TRAJ, TRDV, TRDD, TRDJ, TRGV, TRGJ])
data_dir = os.path.join(params.vdj_dir, params.data_dir)
IGHV_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGHV.fasta'), lambda s: s.split('|')[1]))
IGHD_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGHD.fasta'), lambda s: s.split('|')[1]))
IGHJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGHJ.fasta'), lambda s: s.split('|')[1]))
IGKV_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGKV.fasta'), lambda s: s.split('|')[1]))
IGKJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGKJ.fasta'), lambda s: s.split('|')[1]))
IGLV_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGLV.fasta'), lambda s: s.split('|')[1]))
IGLJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'IGLJ.fasta'), lambda s: s.split('|')[1]))
TRBV_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRBV.fasta'), lambda s: s.split('|')[1]))
TRBD_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRBD.fasta'), lambda s: s.split('|')[1]))
TRBJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRBJ.fasta'), lambda s: s.split('|')[1]))
TRAV_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRAV.fasta'), lambda s: s.split('|')[1]))
TRAJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRAJ.fasta'), lambda s: s.split('|')[1]))
TRDV_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRDV.fasta'), lambda s: s.split('|')[1]))
TRDD_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRDD.fasta'), lambda s: s.split('|')[1]))
TRDJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRDJ.fasta'), lambda s: s.split('|')[1]))
TRGV_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRGV.fasta'), lambda s: s.split('|')[1]))
TRGJ_gapped = dict(FastaIterator(os.path.join(data_dir, 'TRGJ.fasta'), lambda s: s.split('|')[1]))
ALL_gapped = reduce(lambda a, b: dict(a.items() + b.items()), [IGHV_gapped, IGHD_gapped, IGHJ_gapped, IGKV_gapped, IGKJ_gapped, IGLV_gapped, IGLJ_gapped, TRBV_gapped, TRBD_gapped, TRBJ_gapped, TRAV_gapped, TRAJ_gapped, TRDV_gapped, TRDD_gapped, TRDJ_gapped, TRGV_gapped, TRGJ_gapped])