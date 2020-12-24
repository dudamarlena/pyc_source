# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zzeng/Documents/GitHub/IRTools/IRTools/annotation_cmd.py
# Compiled at: 2017-04-10 18:42:35
"""Description

Setup script for IRTools -- a powerful toolset for intron retention detection

Copyright (c) 2015 Zhouhao Zeng <zzhlbj23@gwmail.gwu.edu>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file COPYING included with
the distribution).

@status:  beta
@version: $Revision$
@author:  Zhouhao Zeng
@contact: zzhlbj23@gwmail.gwu.edu
"""
import sys, os, logging, re, collections, HTSeq

def find_bad_genes(gtffile):
    exon_dict = {}
    bad_gene_list = []
    for feature in gtffile:
        if feature.type == 'exon' and feature.attr['gene_id'] not in bad_gene_list:
            gene_id = feature.attr['gene_id']
            gene_chrom = feature.iv.chrom
            gene_strand = feature.iv.strand
            if gene_id not in exon_dict.keys():
                exon_dict[gene_id] = (
                 gene_chrom, gene_strand)
            elif gene_chrom != exon_dict[gene_id][0] or gene_strand != exon_dict[gene_id][1]:
                bad_gene_list.append(gene_id)

    return bad_gene_list


def extend_transcript_region(feature, transcript_region):
    gene_id = feature.attr['gene_id']
    transcript_id = feature.attr['transcript_id']
    if gene_id not in transcript_region.keys() or transcript_id not in transcript_region[gene_id].keys():
        transcript_region[gene_id][transcript_id] = feature.iv.copy()
    else:
        transcript_iv = transcript_region[gene_id][transcript_id]
        assert transcript_iv.chrom == feature.iv.chrom
        assert transcript_iv.strand == feature.iv.strand
        transcript_region[gene_id][transcript_id].start = min(transcript_region[gene_id][transcript_id].start, feature.iv.start)
        transcript_region[gene_id][transcript_id].end = max(transcript_region[gene_id][transcript_id].end, feature.iv.end)


def find_gene_region(transcript_region):
    gene_region = {}
    for gene_id in transcript_region.keys():
        for transcript_id in transcript_region[gene_id].keys():
            if gene_id not in gene_region.keys():
                gene_region[gene_id] = transcript_region[gene_id][transcript_id].copy()
            else:
                gene_region[gene_id].start = min(gene_region[gene_id].start, transcript_region[gene_id][transcript_id].start)
                gene_region[gene_id].end = max(gene_region[gene_id].end, transcript_region[gene_id][transcript_id].end)

    return gene_region


def find_gene_region_length(gene_region, transcript_region):
    gene_region_length = collections.Counter()
    for gene_id in transcript_region.keys():
        transcripts = HTSeq.GenomicArrayOfSets('auto', stranded=True)
        for transcript_id in transcript_region[gene_id].keys():
            transcripts[transcript_region[gene_id][transcript_id]] += gene_id

        for iv, step_set in transcripts[gene_region[gene_id]].steps():
            if len(step_set) != 0:
                gene_region_length[gene_id] += iv.length

    return gene_region_length


def overlap(iv, exon_iv_list):
    for exon_iv in exon_iv_list:
        if iv.overlaps(exon_iv):
            return True

    return False


def find_UTR_region_iv(start_codon_region_iv, stop_codon_region_iv, transcript_region_iv):
    UTR_region_chrom = transcript_region_iv.chrom
    UTR_region_strand = transcript_region_iv.strand
    if UTR_region_strand == '+':
        five_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, transcript_region_iv.start, start_codon_region_iv.start, UTR_region_strand)
        three_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, stop_codon_region_iv.end, transcript_region_iv.end, UTR_region_strand)
    elif UTR_region_strand == '-':
        five_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, start_codon_region_iv.end, transcript_region_iv.end, UTR_region_strand)
        three_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, transcript_region_iv.start, stop_codon_region_iv.start, UTR_region_strand)
    return (
     five_UTR_region_iv, three_UTR_region_iv)


def find_CDS_and_UTR_region_iv(start_codon_region_iv, stop_codon_region_iv, transcript_region_iv):
    UTR_region_chrom = transcript_region_iv.chrom
    UTR_region_strand = transcript_region_iv.strand
    if UTR_region_strand == '+':
        CDS_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, start_codon_region_iv.start, stop_codon_region_iv.start, UTR_region_strand)
        five_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, transcript_region_iv.start, start_codon_region_iv.start, UTR_region_strand)
        three_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, stop_codon_region_iv.end, transcript_region_iv.end, UTR_region_strand)
    elif UTR_region_strand == '-':
        CDS_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, stop_codon_region_iv.end, start_codon_region_iv.end, UTR_region_strand)
        five_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, start_codon_region_iv.end, transcript_region_iv.end, UTR_region_strand)
        three_UTR_region_iv = HTSeq.GenomicInterval(UTR_region_chrom, transcript_region_iv.start, stop_codon_region_iv.start, UTR_region_strand)
    return (
     CDS_region_iv, five_UTR_region_iv, three_UTR_region_iv)


def find_CDS_and_UTR_region(start_codon_region, stop_codon_region, transcript_region):
    CDS_region = collections.defaultdict(lambda : dict())
    five_UTR_region = collections.defaultdict(lambda : dict())
    three_UTR_region = collections.defaultdict(lambda : dict())
    for gene_id in start_codon_region.keys():
        for transcript_id in start_codon_region[gene_id].keys():
            start_codon_region_iv = start_codon_region[gene_id][transcript_id]
            stop_codon_region_iv = stop_codon_region[gene_id][transcript_id]
            transcript_region_iv = transcript_region[gene_id][transcript_id]
            CDS_region_iv, five_UTR_region_iv, three_UTR_region_iv = find_CDS_and_UTR_region_iv(start_codon_region_iv, stop_codon_region_iv, transcript_region_iv)
            CDS_region[gene_id][transcript_id] = CDS_region_iv
            five_UTR_region[gene_id][transcript_id] = five_UTR_region_iv
            three_UTR_region[gene_id][transcript_id] = three_UTR_region_iv

    return (
     CDS_region, five_UTR_region, three_UTR_region)


def find_region_number(pos, feature_list, start_d_or_end_d_as_pos):
    for feature in feature_list:
        if pos == getattr(feature.iv, start_d_or_end_d_as_pos):
            region_number_attr_name = feature.type + '_number'
            return feature.attr[region_number_attr_name]


def find_region_number_and_index(pos, feature_list, start_d_or_end_d_as_pos):
    for index in range(len(feature_list)):
        feature = feature_list[index]
        if pos == getattr(feature.iv, start_d_or_end_d_as_pos):
            region_number_attr_name = feature.type + '_number'
            return (
             feature.attr[region_number_attr_name], index)


def run(args):
    exons = collections.defaultdict(lambda : HTSeq.GenomicArrayOfSets('auto', stranded=True))
    gene_region = {}
    gene_region_length = collections.Counter()
    transcript_region = collections.defaultdict(lambda : dict())
    start_codon_region = collections.defaultdict(lambda : dict())
    stop_codon_region = collections.defaultdict(lambda : dict())
    CDS_region = collections.defaultdict(lambda : dict())
    five_UTR_region = collections.defaultdict(lambda : dict())
    three_UTR_region = collections.defaultdict(lambda : dict())
    gtffile = HTSeq.GFF_Reader(args.inputfile, end_included=True)
    bad_gene_list = find_bad_genes(gtffile)
    logging.info('Removing genes with exons in different chromosomes or strands (%i discarded)' % len(bad_gene_list))
    gtffile = filter(lambda feature: feature.attr['gene_id'] not in bad_gene_list, gtffile)
    for feature in gtffile:
        if feature.type == 'exon':
            gene_id = feature.attr['gene_id']
            exons[gene_id][feature.iv] += feature.attr['transcript_id']
            extend_transcript_region(feature, transcript_region)
        elif feature.type == 'start_codon':
            gene_id = feature.attr['gene_id']
            transcript_id = feature.attr['transcript_id']
            start_codon_region[gene_id][transcript_id] = feature.iv
        elif feature.type == 'stop_codon':
            gene_id = feature.attr['gene_id']
            transcript_id = feature.attr['transcript_id']
            stop_codon_region[gene_id][transcript_id] = feature.iv

    gene_region = find_gene_region(transcript_region)
    gene_region_length = find_gene_region_length(gene_region, transcript_region)
    CDS_region, five_UTR_region, three_UTR_region = find_CDS_and_UTR_region(start_codon_region, stop_codon_region, transcript_region)
    introns = collections.defaultdict(lambda : HTSeq.GenomicArrayOfSets('auto', stranded=True))
    for gene_id in transcript_region.keys():
        for transcript_id in transcript_region[gene_id].keys():
            transcript_iv = transcript_region[gene_id][transcript_id]
            for iv, step_set in exons[gene_id][transcript_iv].steps():
                if transcript_id not in step_set:
                    introns[gene_id][iv] += transcript_id

    gene_exons_bins = collections.defaultdict(lambda : list())
    for gene_id in gene_region.keys():
        gene_iv = gene_region[gene_id]
        for iv, step_set in exons[gene_id][gene_iv].steps():
            transcript_list = list(step_set)
            if len(transcript_list) != 0:
                feature = HTSeq.GenomicFeature(gene_id, 'exonic_region', iv)
                feature.source = 'IR_annotation'
                feature.attr = {}
                feature.attr['gene_id'] = gene_id
                feature.attr['transcripts'] = ('+').join(transcript_list)
                gene_exons_bins[gene_id].append(feature)

        if gene_iv.strand == '-':
            gene_exons_bins[gene_id] = gene_exons_bins[gene_id][::-1]

    for exons_bins_list in gene_exons_bins.values():
        for i in xrange(len(exons_bins_list)):
            exons_bins_list[i].attr['exonic_region_number'] = '%03d' % (i + 1)

    gene_introns_bins = collections.defaultdict(lambda : list())
    for gene_id in gene_region.keys():
        gene_iv = gene_region[gene_id]
        for iv, step_set in introns[gene_id][gene_iv].steps():
            transcript_list = list(step_set)
            if len(transcript_list) != 0:
                feature = HTSeq.GenomicFeature(gene_id, 'intronic_region', iv)
                feature.source = 'IR_annotation'
                feature.attr = {}
                feature.attr['gene_id'] = gene_id
                feature.attr['transcripts'] = ('+').join(transcript_list)
                gene_introns_bins[gene_id].append(feature)

        if gene_iv.strand == '-':
            gene_introns_bins[gene_id] = gene_introns_bins[gene_id][::-1]

    for introns_bins_list in gene_introns_bins.values():
        for i in xrange(len(introns_bins_list)):
            introns_bins_list[i].attr['intronic_region_number'] = '%03d' % (i + 1)

    logging.info('Generating constitutive exonic region (CER) annotation')
    gene_constitutive_exons_bins = collections.defaultdict(lambda : list())
    gene_constitutive_exons_start_d = collections.defaultdict(lambda : set())
    gene_constitutive_exons_end_d = collections.defaultdict(lambda : set())
    gene_constitutive_exons_length = collections.Counter()
    gene_constitutive_exons_number = collections.Counter()
    for gene_id in gene_region.keys():
        transcripts_in_gene = len(transcript_region[gene_id])
        gene_iv = gene_region[gene_id]
        for iv, step_set in exons[gene_id][gene_iv].steps():
            transcript_list = list(step_set)
            if len(transcript_list) == transcripts_in_gene:
                feature = HTSeq.GenomicFeature(gene_id, 'constitutive_exonic_region', iv)
                feature.source = 'IR_annotation'
                feature.attr = {}
                feature.attr['gene_id'] = gene_id
                gene_constitutive_exons_bins[gene_id].append(feature)
                gene_constitutive_exons_start_d[gene_id].add(feature.iv.start_d_as_pos)
                gene_constitutive_exons_end_d[gene_id].add(feature.iv.end_d_as_pos)
                gene_constitutive_exons_length[gene_id] += feature.iv.length
                gene_constitutive_exons_number[gene_id] += 1

        if gene_iv.strand == '-':
            gene_constitutive_exons_bins[gene_id] = gene_constitutive_exons_bins[gene_id][::-1]

    for constitutive_exons_bins_list in gene_constitutive_exons_bins.values():
        for i in xrange(len(constitutive_exons_bins_list)):
            constitutive_exons_bins_list[i].attr['constitutive_exonic_region_number'] = '%03d' % (i + 1)

    logging.info('Generating constitutive intronic region (CIR) annotation')
    gene_constitutive_introns_bins = collections.defaultdict(lambda : list())
    gene_constitutive_introns_start_d = collections.defaultdict(lambda : set())
    gene_constitutive_introns_end_d = collections.defaultdict(lambda : set())
    gene_constitutive_introns_length = collections.Counter()
    gene_constitutive_introns_number = collections.Counter()
    for gene_id in gene_region.keys():
        transcripts_in_gene = len(transcript_region[gene_id])
        gene_iv = gene_region[gene_id]
        exist_UTR_regions = False
        if not (transcripts_in_gene == 1 and gene_id in start_codon_region.keys() and len(start_codon_region[gene_id]) == len(stop_codon_region[gene_id]) == 1):
            raise AssertionError
            transcript_id = start_codon_region[gene_id].keys()[0]
            start_codon_region_iv = start_codon_region[gene_id].values()[0]
            stop_codon_region_iv = stop_codon_region[gene_id].values()[0]
            five_UTR_region_iv, three_UTR_region_iv = find_UTR_region_iv(start_codon_region_iv, stop_codon_region_iv, transcript_region[gene_id][transcript_id])
            exist_UTR_regions = True
        for iv, step_set in introns[gene_id][gene_iv].steps():
            transcript_list = list(step_set)
            if len(transcript_list) == transcripts_in_gene:
                feature = HTSeq.GenomicFeature(gene_id, 'constitutive_intronic_region', iv)
                feature.source = 'IR_annotation'
                feature.attr = {}
                feature.attr['gene_id'] = gene_id
                if exist_UTR_regions == True:
                    if feature.iv.is_contained_in(five_UTR_region_iv):
                        feature.attr['five_UTR_constitutive_intron'] = 'five_UTR_constitutive_intron'
                    elif feature.iv.is_contained_in(three_UTR_region_iv):
                        feature.attr['three_UTR_constitutive_intron'] = 'three_UTR_constitutive_intron'
                gene_constitutive_introns_bins[gene_id].append(feature)
                gene_constitutive_introns_start_d[gene_id].add(feature.iv.start_d_as_pos)
                gene_constitutive_introns_end_d[gene_id].add(feature.iv.end_d_as_pos)
                gene_constitutive_introns_length[gene_id] += feature.iv.length
                gene_constitutive_introns_number[gene_id] += 1

        if gene_iv.strand == '-':
            gene_constitutive_introns_bins[gene_id] = gene_constitutive_introns_bins[gene_id][::-1]

    five_UTR_constitutive_introns = collections.defaultdict(lambda : list())
    three_UTR_constitutive_introns = collections.defaultdict(lambda : list())
    for constitutive_introns_bins_list in gene_constitutive_introns_bins.values():
        for i in xrange(len(constitutive_introns_bins_list)):
            gene_id = constitutive_introns_bins_list[i].attr['gene_id']
            constitutive_intronic_region_number = constitutive_introns_bins_list[i].attr['constitutive_intronic_region_number'] = '%03d' % (i + 1)
            if 'five_UTR_constitutive_intron' in constitutive_introns_bins_list[i].attr.keys():
                five_UTR_constitutive_introns[gene_id].append(constitutive_intronic_region_number)
            elif 'three_UTR_constitutive_intron' in constitutive_introns_bins_list[i].attr.keys():
                three_UTR_constitutive_introns[gene_id].append(constitutive_intronic_region_number)

    logging.info('Generating constitutive junctions (CJ) annotation')
    gene_constitutive_junction = collections.defaultdict(lambda : list())
    for gene_id in gene_constitutive_exons_start_d.keys():
        if gene_id in gene_constitutive_introns_start_d.keys():
            gene_constitutive_junction_from_exon_to_intron_set = gene_constitutive_exons_end_d[gene_id] & gene_constitutive_introns_start_d[gene_id]
            for gene_constitutive_junction_pos in gene_constitutive_junction_from_exon_to_intron_set:
                feature = HTSeq.GenomicFeature(gene_id, 'constitutive_junction', gene_constitutive_junction_pos)
                feature.source = 'IR_annotation'
                feature.attr = {}
                feature.attr['gene_id'] = gene_id
                from_region_number = find_region_number(gene_constitutive_junction_pos, gene_constitutive_exons_bins[gene_id], 'end_d_as_pos')
                feature.attr['upstream'] = 'constitutive_exonic_region_number ' + from_region_number
                to_region_number, index = find_region_number_and_index(gene_constitutive_junction_pos, gene_constitutive_introns_bins[gene_id], 'start_d_as_pos')
                feature.attr['downstream'] = 'constitutive_intronic_region_number ' + to_region_number
                feature.attr['constitutive_junction_type'] = "5'_splice_junction"
                gene_constitutive_junction[gene_id].append((feature, index))

            gene_constitutive_junction_from_intron_to_exon_set = gene_constitutive_exons_start_d[gene_id] & gene_constitutive_introns_end_d[gene_id]
            for gene_constitutive_junction_pos in gene_constitutive_junction_from_intron_to_exon_set:
                feature = HTSeq.GenomicFeature(gene_id, 'constitutive_junction', gene_constitutive_junction_pos)
                feature.source = 'IR_annotation'
                feature.attr = {}
                feature.attr['gene_id'] = gene_id
                from_region_number, index = find_region_number_and_index(gene_constitutive_junction_pos, gene_constitutive_introns_bins[gene_id], 'end_d_as_pos')
                feature.attr['upstream'] = 'constitutive_intronic_region_number ' + from_region_number
                to_region_number = find_region_number(gene_constitutive_junction_pos, gene_constitutive_exons_bins[gene_id], 'start_d_as_pos')
                feature.attr['downstream'] = 'constitutive_exonic_region_number ' + to_region_number
                feature.attr['constitutive_junction_type'] = "3'_splice_junction"
                gene_constitutive_junction[gene_id].append((feature, index))

        if len(gene_constitutive_junction[gene_id]) > 0:
            gene_strand = gene_constitutive_junction[gene_id][0][0].iv.strand
            if gene_strand == '+':
                gene_constitutive_junction[gene_id].sort(key=lambda f: (f[0].iv.chrom, f[0].iv.start))
            else:
                gene_constitutive_junction[gene_id].sort(key=lambda f: (f[0].iv.chrom, -f[0].iv.start))

    for gene_constitutive_junction_list in gene_constitutive_junction.values():
        for i in xrange(len(gene_constitutive_junction_list)):
            gene_constitutive_junction_list[i][0].attr['constitutive_junction_number'] = '%03d' % (i + 1)
            feature = gene_constitutive_junction_list[i][0]
            gene_id = feature.attr['gene_id']
            constitutive_junction_type = feature.attr['constitutive_junction_type']
            if constitutive_junction_type == "5'_splice_junction":
                index = gene_constitutive_junction_list[i][1]
                gene_constitutive_introns_bins[gene_id][index].attr['upstream_constitutive_junction_number'] = '%03d' % (i + 1)
            elif constitutive_junction_type == "3'_splice_junction":
                index = gene_constitutive_junction_list[i][1]
                gene_constitutive_introns_bins[gene_id][index].attr['downstream_constitutive_junction_number'] = '%03d' % (i + 1)

    gene_region_features = []
    for gene_id in gene_region.keys():
        iv = gene_region[gene_id]
        feature = HTSeq.GenomicFeature(gene_id, 'gene_region', iv)
        feature.source = 'IR_annotation'
        feature.attr = {}
        feature.attr['gene_id'] = gene_id
        feature.attr['transcripts_in_gene'] = len(transcript_region[gene_id])
        feature.attr['gene_region_length'] = gene_region_length[gene_id]
        feature.attr['constitutive_exonic_region_length'] = gene_constitutive_exons_length[gene_id]
        feature.attr['constitutive_intronic_region_length'] = gene_constitutive_introns_length[gene_id]
        feature.attr['constitutive_exonic_region_number'] = gene_constitutive_exons_number[gene_id]
        feature.attr['constitutive_intronic_region_number'] = gene_constitutive_introns_number[gene_id]
        if gene_id in five_UTR_constitutive_introns.keys():
            feature.attr['five_UTR_constitutive_introns'] = (',').join(five_UTR_constitutive_introns[gene_id])
        if gene_id in three_UTR_constitutive_introns.keys():
            feature.attr['three_UTR_constitutive_introns'] = (',').join(three_UTR_constitutive_introns[gene_id])
        gene_region_features.append(feature)

    gene_region_features.sort(key=lambda f: (f.iv.chrom, f.iv.start))
    transcript_region_features = collections.defaultdict(lambda : list())
    for gene_id in transcript_region.keys():
        for transcript_id in transcript_region[gene_id].keys():
            iv = transcript_region[gene_id][transcript_id]
            feature = HTSeq.GenomicFeature(gene_id, 'transcript_region', iv)
            feature.source = 'IR_annotation'
            feature.attr = {}
            feature.attr['gene_id'] = gene_id
            feature.attr['transcript_id'] = transcript_id
            transcript_region_features[gene_id].append(feature)

    CDS_region_features = collections.defaultdict(lambda : list())
    for gene_id in CDS_region.keys():
        for transcript_id in CDS_region[gene_id].keys():
            iv = CDS_region[gene_id][transcript_id]
            feature = HTSeq.GenomicFeature(gene_id, 'CDS_region', iv)
            feature.source = 'IR_annotation'
            feature.attr = {}
            feature.attr['gene_id'] = gene_id
            feature.attr['transcript_id'] = transcript_id
            CDS_region_features[gene_id].append(feature)

    five_UTR_region_features = collections.defaultdict(lambda : list())
    for gene_id in five_UTR_region.keys():
        for transcript_id in five_UTR_region[gene_id].keys():
            iv = five_UTR_region[gene_id][transcript_id]
            feature = HTSeq.GenomicFeature(gene_id, 'five_UTR_region', iv)
            feature.source = 'IR_annotation'
            feature.attr = {}
            feature.attr['gene_id'] = gene_id
            feature.attr['transcript_id'] = transcript_id
            five_UTR_region_features[gene_id].append(feature)

    three_UTR_region_features = collections.defaultdict(lambda : list())
    for gene_id in three_UTR_region.keys():
        for transcript_id in three_UTR_region[gene_id].keys():
            iv = three_UTR_region[gene_id][transcript_id]
            feature = HTSeq.GenomicFeature(gene_id, 'three_UTR_region', iv)
            feature.source = 'IR_annotation'
            feature.attr = {}
            feature.attr['gene_id'] = gene_id
            feature.attr['transcript_id'] = transcript_id
            three_UTR_region_features[gene_id].append(feature)

    logging.info('Writing annotation to file: %s' % os.path.join(args.outdir, args.annofile))
    f = open(os.path.join(args.outdir, args.annofile), 'w')
    for gene_region_feature in gene_region_features:
        f.write(gene_region_feature.get_gff_line())
        gene_id = gene_region_feature.attr['gene_id']
        for feature in transcript_region_features[gene_id]:
            f.write(feature.get_gff_line())

        for feature in CDS_region_features[gene_id]:
            f.write(feature.get_gff_line())

        for feature in five_UTR_region_features[gene_id]:
            f.write(feature.get_gff_line())

        for feature in three_UTR_region_features[gene_id]:
            f.write(feature.get_gff_line())

        for feature in gene_exons_bins[gene_id]:
            f.write(feature.get_gff_line())

        for feature in gene_introns_bins[gene_id]:
            f.write(feature.get_gff_line())

        for feature in gene_constitutive_exons_bins[gene_id]:
            f.write(feature.get_gff_line())

        for feature in gene_constitutive_introns_bins[gene_id]:
            f.write(feature.get_gff_line())

        for feature in [ item[0] for item in gene_constitutive_junction[gene_id] ]:
            f.write(feature.get_gff_line())

    f.close()