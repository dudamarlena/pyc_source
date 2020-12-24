# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pysvtools/utils.py
# Compiled at: 2015-11-16 18:31:33
import datetime, re, vcf.model
from pysvtools import __version__
from pysvtools.models.exclusionregion import ExclusionRegion

def extractTXmate(record):
    """
    :param record: pyVCF.vcf.model._Record
    :return: [ chrB, chrBpos ]: Returning mate chromosome if possible, otherwise [None, None]
    """
    chrB = None
    chrBpos = None
    try:
        alt = record.ALT.pop()
    except:
        alt = ''

    if type(alt) == vcf.model._SV:
        chrB = record.INFO.get('CHR2', None)
        chrBpos = record.sv_end
    elif type(alt) == vcf.model._Breakend:
        chrB = alt.chr
        chrBpos = alt.pos
    return [
     chrB, chrBpos]


def vcfHeader():
    ts_now = datetime.datetime.now()
    vcf_header = ('##fileformat=VCFv4.1\n##fileDate={filedate}\n##source=pysvtools-{version}\n##ALT=<ID=DEL,Description="Deletion">\n##ALT=<ID=DUP,Description="Duplication">\n##ALT=<ID=INS,Description="Insertion">\n##ALT=<ID=INV,Description="Inversion">\n##ALT=<ID=TRA,Description="Translocation">\n##FILTER=<ID=LowQual,Description="PE support below 3 or mapping quality below 20.">\n##FORMAT=<ID=DR,Number=1,Type=Integer,Description="# high-quality reference pairs">\n##FORMAT=<ID=DV,Number=1,Type=Integer,Description="# high-quality variant pairs">\n##FORMAT=<ID=FT,Number=1,Type=String,Description="Per-sample genotype filter">\n##FORMAT=<ID=GL,Number=G,Type=Float,Description="Log10-scaled genotype likelihoods for RR,RA,AA genotypes">\n##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n##FORMAT=<ID=PL,Number=G,Type=Integer,Description="Normalized, Phred-scaled likelihoods for genotypes as defined in the VCF specification">\n##FORMAT=<ID=RC,Number=1,Type=Integer,Description="Normalized high-quality read count for the SV">\n##FORMAT=<ID=RR,Number=1,Type=Integer,Description="# high-quality reference junction reads">\n##FORMAT=<ID=RV,Number=1,Type=Integer,Description="# high-quality variant junction reads">\n##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">\n##INFO=<ID=CHR2,Number=1,Type=String,Description="Chromosome for END coordinate in case of a translocation">\n##INFO=<ID=CIEND,Number=2,Type=Integer,Description="PE confidence interval around END">\n##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="PE confidence interval around POS">\n##INFO=<ID=CONSENSUS,Number=1,Type=String,Description="Split-read consensus sequence">\n##INFO=<ID=CT,Number=1,Type=String,Description="Paired-end signature induced connection type">\n##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the structural variant">\n##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">\n##INFO=<ID=MAPQ,Number=1,Type=Integer,Description="Median mapping quality of paired-ends">\n##INFO=<ID=PE,Number=1,Type=Integer,Description="Paired-end support of the structural variant">\n##INFO=<ID=PRECISE,Number=0,Type=Flag,Description="Precise structural variation">\n##INFO=<ID=SR,Number=1,Type=Integer,Description="Split-read support">\n##INFO=<ID=SRQ,Number=1,Type=Float,Description="Split-read consensus alignment quality">\n##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length of the SV">\n##INFO=<ID=SVMETHOD,Number=1,Type=String,Description="Type of approach used to detect SV">\n##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">\n##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">').format(filedate=ts_now.strftime('%Y%m%d'), version=__version__)
    return vcf_header + '\n' + '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tdefault'


def extractTXmateINFOFIELD(breakpoints):
    if breakpoints == []:
        return ('0', 1)
    if type(breakpoints) == type(list()):
        try:
            breakpoints = breakpoints[1]
        except:
            print breakpoints

    breakpoints = breakpoints.replace('"', '')
    try:
        return re.findall('([\\d\\w\\_]+)\\:([\\d]+)', breakpoints, re.I | re.M)[0]
    except:
        raise IndexError


def extractDPFromRecord(record):
    if 'DP' in record.INFO.keys():
        if type(record.INFO['DP']) == type(list):
            return record.INFO['DP'][0]
        return record.INFO['DP']
    if len(record.samples):
        return getattr(record.samples[0].data, 'DP', 0)
    return 0


def firstFromList(arr):
    if type(arr) == type([]):
        return arr[0]
    return arr


def getSVType(record):
    if type(record.INFO['SVTYPE']) == type([]):
        SVTYPE = record.INFO['SVTYPE'][0]
    else:
        SVTYPE = record.INFO['SVTYPE']
    return SVTYPE


def getSVLEN(record):
    SVLEN = 0
    if 'SVLEN' in record.INFO.keys():
        if type(record.INFO['SVLEN']) == type([]):
            SVLEN = record.INFO['SVLEN'][0]
        elif type(record.INFO['SVLEN']) == type(0):
            SVLEN = record.INFO['SVLEN']
    return SVLEN


def formatBedTrack(mergedHit):
    formatted_bed = ''
    if mergedHit.sv_type in ('INS', 'DEL', 'ITX'):
        formatted_bed = ('{chrom}\t{start}\t{end}\t{annot}\n').format(chrom=mergedHit.chrA, start=mergedHit.chrApos, end=mergedHit.chrBpos, annot=('SVTYPE={svtype};DP={dp};SIZE={size}').format(svtype=mergedHit.sv_type, dp=mergedHit.dp, size=mergedHit.size))
    else:
        formatted_bed = ('{chrom}\t{start}\t{end}\t{annot}\n').format(chrom=mergedHit.chrA, start=mergedHit.chrApos > 50 and mergedHit.chrApos - 50 or mergedHit.chrApos, end=mergedHit.chrApos + 50, annot=('SVTYPE={svtype};DP={dp};SIZE={size};MATE={chrb}:{chrbpos}').format(svtype=mergedHit.sv_type, dp=mergedHit.dp, size=mergedHit.size, chrb=mergedHit.chrB, chrbpos=mergedHit.chrBpos))
        formatted_bed += ('{chrom}\t{start}\t{end}\t{annot}\n').format(chrom=mergedHit.chrB, start=mergedHit.chrBpos - 50, end=mergedHit.chrBpos + 50, annot=('SVTYPE={svtype};DP={dp};SIZE={size};MATE={chrb}:{chrbpos}').format(svtype=mergedHit.sv_type, dp=mergedHit.dp, size=mergedHit.size, chrb=mergedHit.chrA, chrbpos=mergedHit.chrApos))
    return formatted_bed


def formatVCFRecord(mergedHit):
    INFOFIELDS = ('IMPRECISE;SVTYPE={};CHR2={};END={};SVMETHOD={svmethod}').format(mergedHit.sv_type, mergedHit.chrB, mergedHit.chrBpos, svmethod=mergedHit.svmethod)
    FORMATFIELDS = (':').join(map(str, [
     '1/.',
     mergedHit.dp]))
    formattedVCFRecord = ('{chrA}\t{pos}\t{id}\t{ref}\t<{alt}>\t{qual}\t{filter}\t{info}\tGT:DP\t{format}').format(chrA=mergedHit.chrA, pos=mergedHit.chrApos, id='.', ref='N', alt=mergedHit.sv_type, qual='100', filter='PASS', info=INFOFIELDS, format=FORMATFIELDS)
    return formattedVCFRecord


def build_exclusion(bed_exclude=None):
    exclusiondb = []
    with open(bed_exclude, 'r') as (fd):
        for r in fd:
            row = r.strip().split('\t')
            cols = dict(zip(['chromosome', 'start', 'end', 'band', 'color'], row))
            exclusion = ExclusionRegion(**cols)
            exclusiondb.append(exclusion)

    return exclusiondb