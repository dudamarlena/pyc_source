# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ensembl_map/symbol.py
# Compiled at: 2020-04-30 13:00:36
# Size of source mod 2**32: 6345 bytes
from .ensembl import Ensembl
from .util import is_ensembl_id

def get_exons(feature, feature_type):
    exons = []
    for exon_id in get_exon_ids(feature, feature_type):
        exons.append(_query(exon_id, 'exon', Ensembl().data.exon_by_id))

    return exons


def get_exon_ids(feature, feature_type):
    if is_ensembl_id(feature):
        exon_ids = _get_exon_ids_by_id(feature, feature_type)
    else:
        exon_ids = _get_exon_ids_by_name(feature, feature_type)
    if exon_ids:
        if not isinstance(exon_ids, list):
            exon_ids = [
             exon_ids]
    return sorted(exon_ids)


def _get_exon_ids_by_id(feature, feature_type):
    if feature_type == 'cds' or feature_type == 'transcript':
        return _query(feature, feature_type, Ensembl().data.exon_ids_of_transcript_id)
    if feature_type == 'exon':
        return feature
    if feature_type == 'gene':
        return _query(feature, feature_type, Ensembl().data.exon_ids_of_gene_id)
    if feature_type == 'protein':
        exon_ids = []
        for transcript_id in get_transcript_ids(feature, 'protein'):
            exon_ids.extend(_get_exon_ids_by_id(transcript_id, 'transcript'))

        return exon_ids
    raise TypeError(f"Cannot get exon IDs from (ID={feature}, type={feature_type})")


def _get_exon_ids_by_name(feature, feature_type):
    if feature_type == 'cds' or feature_type == 'transcript':
        return _query(feature, 'transcript', Ensembl().data.exon_ids_of_transcript_name)
    if feature_type == 'gene':
        return _query(feature, feature_type, Ensembl().data.exon_ids_of_gene_name)
    raise TypeError(f"Cannot get exon IDs from (name={feature}, type={feature_type})")


def get_genes(feature, feature_type):
    genes = []
    for gene_id in get_gene_ids(feature, feature_type):
        genes.append(_query(gene_id, 'gene', Ensembl().data.gene_by_id))

    return genes


def get_gene_ids(feature, feature_type):
    if is_ensembl_id(feature):
        gene_ids = _get_gene_ids_by_id(feature, feature_type)
    else:
        gene_ids = _get_gene_ids_by_name(feature, feature_type)
    if gene_ids:
        if not isinstance(gene_ids, list):
            gene_ids = [
             gene_ids]
    return sorted(gene_ids)


def _get_gene_ids_by_id(feature, feature_type):
    if feature_type == 'cds' or feature_type == 'transcript':
        gene_name = _query(feature, feature_type, Ensembl().data.gene_name_of_transcript_id)
        return _gene_name_to_id(gene_name)
    if feature_type == 'exon':
        gene_name = _query(feature, feature_type, Ensembl().data.gene_name_of_exon_id)
        return _gene_name_to_id(gene_name)
    if feature_type == 'gene':
        return feature
    if feature_type == 'protein':
        return _query(feature, feature_type, Ensembl().data.gene_id_of_protein_id)
    raise TypeError(f"Cannot get gene IDs from (ID={feature}, type={feature_type})")


def _get_gene_ids_by_name(feature, feature_type):
    if feature_type == 'cds' or feature_type == 'transcript':
        gene_name = _query(feature, 'transcript', Ensembl().data.gene_name_of_transcript_name)
        return _gene_name_to_id(gene_name)
    if feature_type == 'gene':
        return _query(feature, feature_type, Ensembl().data.gene_ids_of_gene_name)
    raise TypeError(f"Cannot get gene IDs from (name={feature}, type={feature_type})")


def _gene_name_to_id(gene_name):
    return Ensembl().data.gene_ids_of_gene_name(gene_name)


def get_protein_ids(feature, feature_type):
    protein_ids = []
    for transcript in get_transcripts(feature, feature_type):
        if transcript.protein_id:
            protein_ids.append(transcript.protein_id)

    return sorted(protein_ids)


def get_transcripts(feature, feature_type):
    transcripts = []
    for transcript_id in get_transcript_ids(feature, feature_type):
        transcripts.append(_query(transcript_id, 'transcript', Ensembl().data.transcript_by_id))

    return transcripts


def get_transcript_ids(feature, feature_type):
    if is_ensembl_id(feature):
        transcript_ids = _get_transcript_ids_by_id(feature, feature_type)
    else:
        transcript_ids = _get_transcript_ids_by_name(feature, feature_type)
    if transcript_ids:
        if not isinstance(transcript_ids, list):
            transcript_ids = [
             transcript_ids]
    return sorted(transcript_ids)


def _get_transcript_ids_with_exon(feature):
    transcript_ids = []
    exon = _query(feature, 'exon', Ensembl().data.exon_by_id)
    for transcript in get_transcripts(exon.gene_id, 'gene'):
        if feature in [i.exon_id for i in transcript.exons]:
            transcript_ids.append(transcript.transcript_id)

    return transcript_ids


def _get_transcript_ids_by_id(feature, feature_type):
    if feature_type == 'cds' or feature_type == 'transcript':
        return feature
    if feature_type == 'exon':
        return _get_transcript_ids_with_exon(feature)
    if feature_type == 'gene':
        return _query(feature, feature_type, Ensembl().data.transcript_ids_of_gene_id)
    if feature_type == 'protein':
        return _query(feature, feature_type, Ensembl().data.transcript_id_of_protein_id)
    raise TypeError(f"Cannot get transcript IDs from (ID={feature}, type={feature_type})")


def _get_transcript_ids_by_name(feature, feature_type):
    if feature_type == 'cds' or feature_type == 'transcript':
        return _query(feature, 'transcript', Ensembl().data.transcript_ids_of_transcript_name)
    if feature_type == 'gene':
        return _query(feature, feature_type, Ensembl().data.transcript_ids_of_gene_name)
    raise TypeError(f"Cannot get transcript IDs from (name={feature}, type={feature_type})")


def _query(feature, feature_type, func):
    try:
        return func(feature)
    except ValueError:
        raise ValueError(f"No match for {feature_type} '{feature}'")