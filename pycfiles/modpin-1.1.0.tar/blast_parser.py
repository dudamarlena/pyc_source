# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/external/blast/blast_parser.py
# Compiled at: 2018-02-02 06:38:56
import BlastResult as BR, BlastHit as BH
from SBI.error import BlastError as BE
from SBI import SBIglobals
from xml.dom.minidom import parseString
import sys

def parse_blast(query_sequence, blast_output_file, selfHit, hitIDformat):
    """
        2. We retrieve the file as a Dom Object
    """
    file_fd = open(blast_output_file, 'r')
    domObj = parseString(file_fd.read())
    file_fd.close()
    error_bool = False
    error_str = ''
    SBIglobals.alert('debug', 'blast_parser', 'DEBUG: File %s opened and read correctly\n' % blast_output_file)
    queryname = domObj.getElementsByTagName('BlastOutput_query-def')[0].childNodes[0].nodeValue.strip().split()[0].strip()
    querylength = domObj.getElementsByTagName('BlastOutput_query-len')[0].childNodes[0].nodeValue
    blastversion = domObj.getElementsByTagName('BlastOutput_version')[0].childNodes[0].nodeValue
    matrix = domObj.getElementsByTagName('Parameters_matrix')[0].childNodes[0].nodeValue
    gap_open = domObj.getElementsByTagName('Parameters_gap-open')[0].childNodes[0].nodeValue
    gap_extend = domObj.getElementsByTagName('Parameters_gap-extend')[0].childNodes[0].nodeValue
    db = domObj.getElementsByTagName('BlastOutput_db')[0].childNodes[0].nodeValue
    SBIglobals.alert('debug', 'blast_parser', 'DEBUG: Query is %s with length %s\n' % (queryname, querylength))
    BlastOutput = BR.BlastResult(queryname=queryname, querylength=querylength, blastversion=blastversion, blastmatrix=matrix, gap_open=int(gap_open), gap_extend=int(gap_extend), blastdb=db, queryseq=query_sequence)
    SBIglobals.alert('debug', 'blast_parser', BlastOutput.str_blast_details() + '\n')
    for iteration in domObj.getElementsByTagName('Iteration'):
        iteration_number = int(iteration.getElementsByTagName('Iteration_iter-num')[0].childNodes[0].nodeValue)
        SBIglobals.alert('debug', 'blast_parser', 'Parsing iteration %d\n' % iteration_number)
        for hit in iteration.getElementsByTagName('Hit'):
            hitname = hit.getElementsByTagName('Hit_def')[0].childNodes[0].nodeValue.strip()
            if hitIDformat == 'single':
                hitname = hitname.split()[0].strip()
            elif hitIDformat == 'double':
                hitname = (' ').join(hitname.split()[:2]).strip()
            hitlength = int(hit.getElementsByTagName('Hit_len')[0].childNodes[0].nodeValue)
            SBIglobals.alert('debug', 'blast_parser', '\tParsing hit sequence %s of length %d\n' % (hitname, hitlength))
            if not same_query_hit_names(query=queryname, hit=hitname, selfHit=selfHit):
                for subhitlist in hit.getElementsByTagName('Hit_hsps'):
                    SBIglobals.alert('debug', 'blast_parser', '\t\tParsing subhit alignment...\n')
                    for subhit in subhitlist.getElementsByTagName('Hsp'):
                        data = parse_subhit(subhit=subhit)
                        OutputHit = BH.BlastHit(name=hitname, length=hitlength, iteration=iteration_number, e_value=data['ev'], align_length=data['al'], identities=data['hi'], positives=data['hp'], gaps=data['hg'], qseq=data['qs'], hseq=data['hs'], qpos=data['qpi'], hpos=data['hpi'], score_seq=data['scs'])
                        BlastOutput._hits.append(OutputHit)
                        SBIglobals.alert('debug', 'blast_parser', '\t\tHit added to BlastResult List\n')
                        if not OutputHit.are_segments_ok:
                            error_bool = True
                            error_str += 'WARNING: Some error has occurred on the fragmentation of the alignment for the query %s with %s\nERROR: PLEASE CHECK THE ALIGNMENT:\nERROR: ' % (
                             queryname, hitname)
                            error_str += '%s\n' % OutputHit
                        SBIglobals.alert('debug', 'blast_parser', '\t\tNext Sub-hit\n')

                SBIglobals.alert('debug', 'blast_parser', '\tNext Hit\n')
            else:
                SBIglobals.alert('debug', 'blast_parser', '\tHit %s is skipped as it corresponds to the query sequence\n' % hitname.split()[0].strip())

    BlastOutput.set_last_iteration()
    if error_bool:
        raise BE(code=1, value=error_str)
    return BlastOutput


def parse_subhit(subhit):
    """
    Returns the required data from the given subhit 
    """
    data = {}
    if len(subhit.getElementsByTagName('Hsp_gaps')) != 0:
        data['hg'] = int(subhit.getElementsByTagName('Hsp_gaps')[0].childNodes[0].nodeValue)
    else:
        data['hg'] = 0
    if len(subhit.getElementsByTagName('Hsp_identity')) != 0:
        data['hi'] = int(subhit.getElementsByTagName('Hsp_identity')[0].childNodes[0].nodeValue)
    else:
        data['hi'] = 0
    if len(subhit.getElementsByTagName('Hsp_positive')) != 0:
        data['hp'] = int(subhit.getElementsByTagName('Hsp_positive')[0].childNodes[0].nodeValue)
    else:
        data['hp'] = 0
    SBIglobals.alert('debug', 'blast_parser', '\t\tGaps: %d\n\t\tIdentities: %d\n\t\tSimilarities: %d\n' % (data['hg'], data['hi'], data['hp']))
    data['ev'] = float(subhit.getElementsByTagName('Hsp_evalue')[0].childNodes[0].nodeValue)
    data['al'] = int(subhit.getElementsByTagName('Hsp_align-len')[0].childNodes[0].nodeValue)
    data['qs'] = str(subhit.getElementsByTagName('Hsp_qseq')[0].childNodes[0].nodeValue).strip()
    data['hs'] = str(subhit.getElementsByTagName('Hsp_hseq')[0].childNodes[0].nodeValue).strip()
    data['qpi'] = int(subhit.getElementsByTagName('Hsp_query-from')[0].childNodes[0].nodeValue)
    data['qpe'] = int(subhit.getElementsByTagName('Hsp_query-to')[0].childNodes[0].nodeValue)
    data['hpi'] = int(subhit.getElementsByTagName('Hsp_hit-from')[0].childNodes[0].nodeValue)
    data['hpe'] = int(subhit.getElementsByTagName('Hsp_hit-to')[0].childNodes[0].nodeValue)
    data['scs'] = str(subhit.getElementsByTagName('Hsp_midline')[0].childNodes[0].nodeValue).strip()
    return data


def same_query_hit_names(query, hit, selfHit):
    """
    Returns True if both names are the same (*based on the first word)
    Returns False if the names are different or skip is True
    """
    if selfHit:
        return False
    return query.split()[0].strip() == hit.split()[0].strip()