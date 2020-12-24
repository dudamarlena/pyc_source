# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/crossalignfilter.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 3874 bytes
import pysam, sys

class CrossAlignFilter(object):

    def __init__(self, input_bam, output_bam, output_crossmapped_reads, orgs_and_replicon_ids):
        self._input_bam = input_bam
        self._output_bam = output_bam
        self._output_crossmapped_reads = output_crossmapped_reads
        self._orgs_and_replicon_ids = orgs_and_replicon_ids
        self._crossmapped_reads = set()
        self.no_of_crossmapped_reads = None

    def determine_crossmapped_reads(self):
        """Find reads that are mapped to sequences of different species.

        The comparison is performed replicon wise in order to reduce
        the memory footprint.
        """
        self._check_replicon_existance()
        done_replicon_comparison = []
        with pysam.Samfile(self._input_bam) as (bam):
            for org, replicon_ids in self._orgs_and_replicon_ids.items():
                for replicon_id in replicon_ids:
                    self._read_ids = set()
                    for alignment in bam.fetch(reference=replicon_id):
                        self._read_ids.add(alignment.qname)

                    for comp_org, comp_replicon_ids in self._orgs_and_replicon_ids.items():
                        if org == comp_org:
                            continue
                        for comp_replicon_id in comp_replicon_ids:
                            comparison = sorted([replicon_id,
                             comp_replicon_id])
                            if comparison in done_replicon_comparison:
                                continue
                            done_replicon_comparison.append(comparison)
                            for alignment in bam.fetch(reference=comp_replicon_id):
                                if alignment.qname in self._read_ids:
                                    self._crossmapped_reads.add(alignment.qname)

        self.no_of_crossmapped_reads = len(self._crossmapped_reads)
        with open(self._output_crossmapped_reads, 'w') as (output_list_fh):
            output_list_fh.write('\n'.join(self._crossmapped_reads) + '\n')

    def _check_replicon_existance(self):
        found_all = True
        with pysam.Samfile(self._input_bam) as (bam):
            for replicon_ids in self._orgs_and_replicon_ids.values():
                for replicon_id in replicon_ids:
                    if replicon_id not in bam.references:
                        sys.stderr.write('"%s" not found in BAM header.\n' % replicon_id)
                        found_all = False

        if not found_all:
            raise RepliconIdNotInBam

    def write_crossmapping_free_bam(self):
        with pysam.Samfile(self._input_bam) as (input_bam):
            with pysam.Samfile((self._output_bam), 'wb', header=(input_bam.header)) as (output_bam):
                for alignment in input_bam.fetch():
                    if alignment.qname not in self._crossmapped_reads:
                        output_bam.write(alignment)

        pysam.index(self._output_bam)


class RepliconIdNotInBam(BaseException):
    pass