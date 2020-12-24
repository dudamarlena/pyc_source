# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/gff3.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 2518 bytes
import csv, sys

class Gff3Parser(object):
    __doc__ = '\n    A format description can be found at:\n    http://genome.ucsc.edu/FAQ/FAQformat.html#format3\n    http://www.sequenceontology.org/gff3.shtml\n\n    a validator can be found here:\n    http://modencode.oicr.on.ca/cgi-bin/validate_gff3_online\n    '

    def entries(self, input_gff_fh):
        """
        """
        for entry_dict in csv.DictReader(input_gff_fh,
          delimiter='\t', fieldnames=[
         'seq_id', 'source', 'feature', 'start',
         'end', 'score', 'strand', 'phase', 'attributes']):
            if entry_dict['seq_id'].startswith('#'):
                continue
            try:
                yield self._dict_to_entry(entry_dict)
            except:
                sys.stderr.write('Error! Please make sure that you use GFF3 formated annotation files. GTF2/GTF is not valid and the usage of that format is not recommended anymore (see http://www.sequenceontology.org/gff3.shtml for more information).\n')
                sys.exit(0)

    def _dict_to_entry(self, entry_dict):
        return Gff3Entry(entry_dict)


class Gff3Entry(object):

    def __init__(self, entry_dict):
        self.seq_id = entry_dict['seq_id']
        self.source = entry_dict['source']
        self.feature = entry_dict['feature']
        start, end = sorted([int(entry_dict['start']), int(entry_dict['end'])])
        self.start = start
        self.end = end
        self.score = entry_dict['score']
        self.strand = entry_dict['strand']
        self.phase = entry_dict['phase']
        self.attributes = self._attributes(entry_dict['attributes'])
        self.attribute_string = entry_dict['attributes']

    def _attributes(self, attributes_string):
        """Translate the attribute string to dictionary"""
        if attributes_string is None:
            return {}
        if attributes_string.endswith(';'):
            attributes_string = attributes_string[:-1]
        return dict([key_value_pair.split('=') for key_value_pair in attributes_string.split(';')])

    def __str__(self):
        return '\t'.join([str(field) for field in [
         self.seq_id, self.source, self.feature, self.start,
         self.end, self.score, self.strand, self.phase,
         self.attribute_string]])