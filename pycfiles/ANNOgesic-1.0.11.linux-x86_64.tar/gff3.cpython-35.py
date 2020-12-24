# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/gff3.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 3417 bytes
import csv

class Gff3Parser(object):
    __doc__ = '\nA format description can be found at:\nhttp://genome.ucsc.edu/FAQ/FAQformat.html#format3\nhttp://www.sequenceontology.org/gff3.shtml\n\na validator can be found here:\nhttp://modencode.oicr.on.ca/cgi-bin/validate_gff3_online\n\nWARNING: Currently this class in not strict enough and would also\nparse file not following the standard.\n'

    def entries(self, input_gff_fh):
        """
"""
        for entry_dict in csv.DictReader(input_gff_fh, delimiter='\t', fieldnames=[
         'seq_id', 'source', 'feature', 'start',
         'end', 'score', 'strand', 'phase', 'attributes']):
            if entry_dict['seq_id'].startswith('#'):
                pass
            else:
                yield self._dict_to_entry(entry_dict)

    def _dict_to_entry(self, entry_dict):
        return Gff3Entry(entry_dict)


class Gff3Entry(object):
    __doc__ = '\n\nExample:\nstart, end = sorted([int(pos) for pos in [start, end]])\nGff3Entry({\n"seq_id" : seq_id,\n"source" : "MyLab",\n"feature" : "sRNA",\n"start" : start,\n"end" : end,\n"strand" : strand,\n"score" : ".",\n"phase" : ".",\n"attributes" : "name=%s;locus_tag=%s" % (name, locus_tag)})\n'

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
        self.info = '\t'.join([str(field) for field in [
         self.seq_id, self.source, self.feature, self.start,
         self.end, self.score, self.strand, self.phase,
         self.attribute_string]])
        self.info_without_attributes = '\t'.join([str(field) for field in [
         self.seq_id, self.source, self.feature, self.start,
         self.end, self.score, self.strand, self.phase]])

    def _attributes(self, attributes_string):
        """Translate the attribute string to dictionary"""
        attributes = {}
        if len(attributes_string) > 0:
            for attribute in attributes_string.split(';'):
                key_value_pair = attribute.split('=')
                key = key_value_pair[0]
                if len(key_value_pair) > 2:
                    value = '='.join(key_value_pair[1:])
                else:
                    if len(key_value_pair) == 2:
                        value = key_value_pair[1]
                    else:
                        value = ''
                attributes[key] = value

            return attributes
        else:
            return attributes

    def add_attribute(self, key, value):
        self.attributes[key] = value
        self.attribute_string = ';'.join(['='.join(items) for items in self.attributes.items()])

    def __str__(self):
        return '\t'.join([str(field) for field in [
         self.seq_id, self.source, self.feature, self.start,
         self.end, self.score, self.strand, self.phase,
         self.attribute_string]])