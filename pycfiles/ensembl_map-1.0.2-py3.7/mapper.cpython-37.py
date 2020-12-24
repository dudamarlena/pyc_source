# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ensembl_map/mapper.py
# Compiled at: 2020-04-01 16:07:17
# Size of source mod 2**32: 9373 bytes
import logging
from .ensembl import Ensembl
from .convert import get_convert_func
from .features import get_load_function
from .transcript import get_transcripts
from .util import assert_valid_position

def cds_to_exon(feature, start, end=None, raise_error=True):
    """Map CDS coordinates to exon coordinates."""
    result = []
    for pos in cds_to_transcript(feature, start, end, raise_error=False):
        result.extend(transcript_to_exon(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map CDS {feature} to an exon")
    return result


def cds_to_gene(feature, start, end=None, raise_error=True):
    """Map CDS coordinates to gene coordinates."""
    result = []
    for pos in cds_to_transcript(feature, start, end, raise_error=False):
        result.extend(transcript_to_gene(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map CDS {feature} to a gene")
    return result


def cds_to_protein(feature, start, end=None, raise_error=True):
    """Map CDS coordinates to protein coordinates."""
    result = _map(feature, start, end, 'cds', 'protein')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map CDS {feature} to a protein")
    return result


def cds_to_transcript(feature, start, end=None, raise_error=True):
    """Map CDS coordinates to transcript coordinates."""
    result = _map(feature, start, end, 'cds', 'transcript')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map CDS {feature} to a transcript")
    return result


def exon_to_cds(feature, raise_error=True):
    """Map an exon to CDS coordinates."""
    try:
        exon = Ensembl().data.exon_by_id(feature)
    except TypeError:
        logging.error(f"No exon '{feature}' found")
        return []
    else:
        result = _map(feature, exon.start, exon.end, 'exon', 'cds')
        if not result:
            if raise_error:
                raise ValueError(f"Could not map exon {feature} to a CDS")
        return result


def exon_to_gene(feature, raise_error=True):
    """Map an exon to gene coordinates."""
    result = []
    for pos in exon_to_transcript(feature, raise_error=False):
        result.extend(transcript_to_gene(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map exon {feature} to a gene")
    return result


def exon_to_protein(feature, raise_error=True):
    """Map an exon to gene coordinates."""
    result = []
    for pos in exon_to_cds(feature, raise_error=False):
        result.extend(cds_to_protein(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map exon {feature} to a protein")
    return result


def exon_to_transcript(feature, raise_error=True):
    """Map an exon to transcript coordinates."""
    result = []
    try:
        exon = Ensembl().data.exon_by_id(feature)
    except TypeError:
        logging.error(f"No exon '{feature}' found")
        return result
    else:
        valid_transcripts = [i.transcript_id for i in get_transcripts(feature, 'exon')]
        for pos in gene_to_transcript((exon.gene_id), (exon.start), (exon.end), raise_error=False):
            if pos.transcript_id in valid_transcripts:
                result.append(pos)
            else:
                logging.debug(f"{pos.transcript_id} does not contain exon {exon.exon_id}")

        if not result:
            if raise_error:
                raise ValueError(f"Could not map exon {feature} to a transcript")
        return result


def gene_to_cds(feature, start, end=None, raise_error=True):
    """Map gene coordinates to CDS coordinates."""
    result = []
    for pos in gene_to_transcript(feature, start, end, raise_error=False):
        result.extend(transcript_to_cds(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map gene {feature} to a CDS")
    return result


def gene_to_exon(feature, start, end=None, raise_error=True):
    """Map gene coordinates to exon coordinates."""
    result = _map(feature, start, end, 'gene', 'exon')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map gene {feature} to an exon")
    return result


def gene_to_protein(feature, start, end=None, raise_error=True):
    """Map gene coordinates to protein coordinates."""
    result = []
    for pos in gene_to_cds(feature, start, end, raise_error=False):
        result.extend(cds_to_protein(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map gene {feature} to a protein")
    return result


def gene_to_transcript(feature, start, end=None, raise_error=True):
    """Map gene coordinates to transcript coordinates."""
    result = _map(feature, start, end, 'gene', 'transcript')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map gene {feature} to a transcript")
    return result


def protein_to_cds(feature, start, end=None, raise_error=True):
    """Map protein coordinates to CDS coordinates."""
    result = _map(feature, start, end, 'protein', 'cds')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map protein {feature} to a CDS")
    return result


def protein_to_exon(feature, start, end=None, raise_error=True):
    """Map protein coordinates to exon coordinates."""
    result = []
    for pos in protein_to_transcript(feature, start, end, raise_error=False):
        result.extend(transcript_to_exon(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map protein {feature} to an exon")
    return result


def protein_to_gene(feature, start, end=None, raise_error=True):
    """Map protein coordinates to gene coordinates."""
    result = []
    for pos in protein_to_transcript(feature, start, end, raise_error=False):
        result.extend(transcript_to_gene(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map protein {feature} to a gene")
    return result


def protein_to_transcript(feature, start, end=None, raise_error=True):
    """Map protein coordinates to transcript coordinates."""
    result = []
    for pos in protein_to_cds(feature, start, end, raise_error=False):
        result.extend(cds_to_transcript(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map protein {feature} to a transcript")
    return result


def transcript_to_cds(feature, start, end=None, raise_error=True):
    """Map transcript coordinates to CDS coordinates."""
    result = _map(feature, start, end, 'transcript', 'cds')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map transcript {feature} to a CDS")
    return result


def transcript_to_exon(feature, start, end=None, raise_error=True):
    """Map transcript coordinates to exon coordinates."""
    result = []
    for pos in transcript_to_gene(feature, start, end, raise_error=False):
        result.extend(gene_to_exon(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map transcript {feature} to an exon")
    return result


def transcript_to_gene(feature, start, end=None, raise_error=True):
    """Map transcript coordinates to gene coordinates."""
    result = _map(feature, start, end, 'transcript', 'gene')
    if not result:
        if raise_error:
            raise ValueError(f"Could not map transcript {feature} to a gene")
    return result


def transcript_to_protein(feature, start, end=None, raise_error=True):
    """Map transcript coordinates to protein coordinates."""
    result = []
    for pos in transcript_to_cds(feature, start, end, raise_error=False):
        result.extend(cds_to_protein(*(pos.to_tuple)(), **{'raise_error': False}))

    if not result:
        if raise_error:
            raise ValueError(f"Could not map transcript {feature} to a protein")
    return result


def _map(feature, start, end, from_type, to_type):
    """
    Template function for mapping a feature to the associated transcript(s), then 
    converting the given coordinates.

    Args:
        feature (str): feature name or Ensembl ID
        start (int): first position relative to `feature`
        end (int or None): second position relative to `feature`
        from_type (str): coordinates relative to this type of feature (e.g. 'gene')
        to_type (str): map coordinates to this type of feature (e.g 'transcript')
        
    Returns:
        list: of converted coordinates, mapped to a `features` instance
    """
    result = []
    logging.debug(f"Map {from_type} ({feature}, {start}, {end}) to {to_type}")
    assert_valid_position(start, end)
    map_func = get_convert_func(from_type, to_type)
    load_func = get_load_function(to_type)
    for transcript in get_transcripts(feature, from_type):
        retval = None
        try:
            retval = map_func(transcript, start, end)
            logging.debug(f"Got: {retval}")
        except ValueError as exc:
            try:
                logging.debug(exc)
                continue
            finally:
                exc = None
                del exc

        ret_obj = load_func(transcript, *retval)
        logging.debug(f"Parsed {(transcript, retval)} to {ret_obj}")
        result.append(ret_obj)

    return result