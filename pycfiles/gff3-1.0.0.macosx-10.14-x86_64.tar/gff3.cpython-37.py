# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/gff3/gff3.py
# Compiled at: 2018-12-01 02:05:59
# Size of source mod 2**32: 76128 bytes
"""
Check a GFF3 file for errors and unwanted features, with an option to correct the errors and output a valid GFF3 file.

Count the number of Ns in each feature, remove features with N count greater than the specified threshold. (Requires FASTA)
Check and remove features with an end coordinates larger than the landmark sequence length. (Requires FASTA or ##sequence-region)
Check if the ##sequence-region matches the FASTA file. (Requires FASTA and ##sequence-region)
Add the ##sequence-region directives if missing. (Requires FASTA)
Check and correct the phase for CDS features.
"""
from __future__ import print_function
from collections import defaultdict
from itertools import groupby
from io import open
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import quote, unquote

from textwrap import wrap
import sys, re, string, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    lh = logging.StreamHandler()
    lh.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logger.addHandler(lh)
try:
    COMPLEMENT_TRANS = string.maketrans('TAGCtagc', 'ATCGATCG')
except AttributeError:
    COMPLEMENT_TRANS = str.maketrans('TAGCtagc', 'ATCGATCG')

def complement(seq):
    return seq.translate(COMPLEMENT_TRANS)


BASES = [
 't', 'c', 'a', 'g']
CODONS = [a + b + c for a in BASES for b in BASES for c in BASES]
AMINO_ACIDS = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON_TABLE = dict(zip(CODONS, AMINO_ACIDS))

def translate(seq):
    seq = seq.lower().replace('\n', '').replace(' ', '')
    peptide = ''
    for i in xrange(0, len(seq), 3):
        codon = seq[i:i + 3]
        amino_acid = CODON_TABLE.get(codon, '!')
        if amino_acid != '!':
            peptide += amino_acid

    return peptide


def fasta_file_to_dict(fasta_file, id=True, header=False, seq=False):
    """Returns a dict from a fasta file and the number of sequences as the second return value.
    fasta_file can be a string path or a file object.
    The key of fasta_dict can be set using the keyword arguments and
    results in a combination of id, header, sequence, in that order. joined with '||'. (default: id)
    Duplicate keys are checked and a warning is logged if found.
    The value of fasta_dict is a python dict with 3 keys: header, id and seq

    Changelog:
    2014/11/17:
    * Added support for url escaped id
    """
    fasta_file_f = fasta_file
    if isinstance(fasta_file, str):
        fasta_file_f = open(fasta_file, 'rb')
    fasta_dict = OrderedDict()
    keys = ['id', 'header', 'seq']
    flags = dict([('id', id), ('header', header), ('seq', seq)])
    entry = dict([('id', ''), ('header', ''), ('seq', '')])
    count = 0
    line_num = 0
    for line in fasta_file_f:
        line = line.strip()
        if line and line[0] == '>':
            count += 1
            key = '||'.join([entry[i] for i in keys if flags[i]])
            if key:
                if key in fasta_dict:
                    logger.warning('%s : Line %d : Duplicate %s [%s] : ID = [%s].', fasta_file_f.name, line_num, '||'.join([i for i in keys if flags[i]]), key[:25] + (key[25:] and '..'), entry['id'])
                entry['seq'] = ''.join(entry['seq'])
                fasta_dict[key] = entry
                if id:
                    unescaped_id = unquote(entry['id'])
                    if id != unescaped_id:
                        key = '||'.join([unescaped_id] + [entry[i] for i in keys if i != 'id' if flags[i]])
                        entry['unescaped_id'] = unescaped_id
                        fasta_dict[key] = entry
                entry = dict()
            entry['header'] = line
            entry['id'] = line.split()[0][1:]
            entry['seq'] = []
        else:
            entry['seq'].append(line.upper())
        line_num += 1

    if isinstance(fasta_file, str):
        fasta_file_f.close()
    key = '||'.join([entry[i] for i in keys if flags[i]])
    if key:
        if key in fasta_dict:
            logger.warning('%s : Line %d : Duplicate %s [%s] : ID = [%s].', fasta_file_f.name, line_num, '||'.join([i for i in keys if flags[i]]), key[:25] + (key[25:] and '..'), entry['id'])
        entry['seq'] = ''.join(entry['seq'])
        fasta_dict[key] = entry
        if id:
            unescaped_id = unquote(entry['id'])
            if id != unescaped_id:
                key = '||'.join([unescaped_id] + [entry[i] for i in keys if i != 'id' if flags[i]])
                entry['unescaped_id'] = unescaped_id
                fasta_dict[key] = entry
    return (
     fasta_dict, count)


def fasta_dict_to_file(fasta_dict, fasta_file, line_char_limit=None):
    """Write fasta_dict to fasta_file

    :param fasta_dict: returned by fasta_file_to_dict
    :param fasta_file: output file can be a string path or a file object
    :param line_char_limit: None = no limit (default)
    :return: None
    """
    fasta_fp = fasta_file
    if isinstance(fasta_file, str):
        fasta_fp = open(fasta_file, 'wb')
    for key in fasta_dict:
        seq = fasta_dict[key]['seq']
        if line_char_limit:
            seq = '\n'.join([seq[i:i + line_char_limit] for i in range(0, len(seq), line_char_limit)])
        fasta_fp.write('{0:s}\n{1:s}\n'.format(fasta_dict[key]['header'], seq))


class Gff3(object):

    def __init__(self, gff_file=None, fasta_external=None, logger=logger):
        self.logger = logger
        self.lines = []
        self.features = {}
        self.unresolved_parents = {}
        self.fasta_embedded = {}
        self.fasta_external = {}
        if gff_file:
            self.parse(gff_file)
        if fasta_external:
            self.parse_fasta_external(fasta_external)

    error_format = 'Line {current_line_num}: {error_type}: {message}\n-> {line}'

    def add_line_error(self, line_data, error_info, log_level=logging.ERROR):
        """Helper function to record and log an error message

        :param line_data: dict
        :param error_info: dict
        :param logger:
        :param log_level: int
        :return:
        """
        if not error_info:
            return
        try:
            line_data['line_errors'].append(error_info)
        except KeyError:
            line_data['line_errors'] = [
             error_info]
        except TypeError:
            pass

        try:
            self.logger.log(log_level, Gff3.error_format.format(current_line_num=(line_data['line_index'] + 1), error_type=(error_info['error_type']), message=(error_info['message']), line=(line_data['line_raw'].rstrip())))
        except AttributeError:
            pass

    def check_unresolved_parents(self):
        if len(self.unresolved_parents) > 0:
            self.logger.info('%d unresolved forward referencing parent ids, trying global lookup...' % len(self.unresolved_parents))
            globally_resolved_parents = set()
            for feature_id in self.unresolved_parents:
                if feature_id in self.features:
                    self.logger.info('  Resolved parent id: {0:s}, defined in lines: {1:s}, referenced in lines: {2:s}'.format(feature_id, ','.join([str(line_data['line_index'] + 1) for line_data in self.features[feature_id]]), ','.join([str(line_data['line_index'] + 1) for line_data in self.unresolved_parents[feature_id]])))
                    globally_resolved_parents.add(feature_id)
                    for line_data in self.unresolved_parents[feature_id]:
                        line_data['parents'].append(self.features[feature_id])
                        for ld in self.features[feature_id]:
                            ld['children'].append(line_data)

            still_unresolved_parents = sorted(list(set(self.unresolved_parents) - globally_resolved_parents))
            if len(still_unresolved_parents) > 0:
                self.logger.info('{0:d} unresolved parent ids:'.format(len(still_unresolved_parents)))
                for feature_id in still_unresolved_parents:
                    self.logger.info('  Unresolved parent id: {0:s}, referenced in lines: {1:s}'.format(feature_id, ','.join([str(line_data['line_index'] + 1) for line_data in self.unresolved_parents[feature_id]])))

    def check_parent_boundary(self):
        """
        checks whether child features are within the coordinate boundaries of parent features

        :return:
        """
        for line in self.lines:
            for parent_feature in line['parents']:
                ok = False
                for parent_line in parent_feature:
                    if parent_line['start'] <= line['start'] and line['end'] <= parent_line['end']:
                        ok = True
                        break

                if not ok:
                    self.add_line_error(line, {'message':'This feature is not contained within the feature boundaries of parent: {0:s}: {1:s}'.format(parent_feature[0]['attributes']['ID'], ','.join(['({0:s}, {1:d}, {2:d})'.format(line['seqid'], line['start'], line['end']) for line in parent_feature])), 
                     'error_type':'BOUNDS', 
                     'location':'parent_boundary'})

    def check_phase(self):
        """
        1. get a list of CDS with the same parent
        2. sort according to strand
        3. calculate and validate phase
        """
        plus_minus = set(['+', '-'])
        for k, g in groupby(sorted([line for line in self.lines if line['line_type'] == 'feature' if line['type'] == 'CDS' if 'Parent' in line['attributes']], key=(lambda x: x['attributes']['Parent'])), key=(lambda x: x['attributes']['Parent'])):
            cds_list = list(g)
            strand_set = list(set([line['strand'] for line in cds_list]))
            if len(strand_set) != 1:
                for line in cds_list:
                    self.add_line_error(line, {'message':'Inconsistent CDS strand with parent: {0:s}'.format(k),  'error_type':'STRAND'})

                continue
            if len(cds_list) == 1:
                if cds_list[0]['phase'] != 0:
                    self.add_line_error(cds_list[0], {'message':'Wrong phase {0:d}, should be {1:d}'.format(cds_list[0]['phase'], 0),  'error_type':'PHASE'})
                    continue
                strand = strand_set[0]
                if strand not in plus_minus:
                    continue
                elif strand == '-':
                    sorted_cds_list = sorted(cds_list, key=(lambda x: x['end']), reverse=True)
                else:
                    sorted_cds_list = sorted(cds_list, key=(lambda x: x['start']))
                phase = 0
                for line in sorted_cds_list:
                    if line['phase'] != phase:
                        self.add_line_error(line, {'message':'Wrong phase {0:d}, should be {1:d}'.format(line['phase'], phase),  'error_type':'PHASE'})
                    phase = (3 - (line['end'] - line['start'] + 1 - phase) % 3) % 3

    def parse_fasta_external(self, fasta_file):
        self.fasta_external, count = fasta_file_to_dict(fasta_file)

    def check_reference(self, sequence_region=False, fasta_embedded=False, fasta_external=False, check_bounds=True, check_n=True, allowed_num_of_n=0, feature_types=('CDS',)):
        """
        Check seqid, bounds and the number of Ns in each feature using one or more reference sources.

        Seqid check: check if the seqid can be found in the reference sources.

        Bounds check: check the start and end fields of each features and log error if the values aren't within the seqid sequence length, requires at least one of these sources: ##sequence-region, embedded #FASTA, or external FASTA file.

        Ns check: count the number of Ns in each feature with the type specified in *line_types (default: 'CDS') and log an error if the number is greater than allowed_num_of_n (default: 0), requires at least one of these sources: embedded #FASTA, or external FASTA file.

        When called with all source parameters set as False (default), check all available sources, and log debug message if unable to perform a check due to none of the reference sources being available.

        If any source parameter is set to True, check only those sources marked as True, log error if those sources don't exist.

        :param sequence_region: check bounds using the ##sequence-region directive (default: False)
        :param fasta_embedded: check bounds using the embedded fasta specified by the ##FASTA directive (default: False)
        :param fasta_external: check bounds using the external fasta given by the self.parse_fasta_external (default: False)
        :param check_bounds: If False, don't run the bounds check (default: True)
        :param check_n: If False, don't run the Ns check (default: True)
        :param allowed_num_of_n: only report features with a number of Ns greater than the specified value (default: 0)
        :param feature_types: only check features of these feature_types, multiple types may be specified, if none are specified, check only 'CDS'
        :return: error_lines: a set of line_index(int) with errors detected by check_reference
        """
        error_lines = set()
        if not self.lines:
            self.logger.debug('.parse(gff_file) before calling .check_bounds()')
            return error_lines
            check_n_feature_types = set(feature_types)
            if len(check_n_feature_types) == 0:
                check_n_feature_types.add('CDS')
            n_segments_finditer = re.compile('[Nn]+').finditer
            check_all_sources = True
            if not sequence_region:
                if fasta_embedded or fasta_external:
                    check_all_sources = False
                start_end_error_locations = set(('start', 'end', 'start,end'))
                valid_line_data_seqid = [[error_info for error_info in line_data['line_errors'] if 'location' in error_info if error_info['location'] in start_end_error_locations] or (line_data, unquote(line_data['seqid'])) for line_data in self.lines if line_data['line_type'] == 'feature' if line_data['seqid'] != '.' if line_data['line_errors']]
                checked_at_least_one_source = False
                valid_sequence_regions = dict([(unquote(line_data['seqid']), line_data) for line_data in self.lines if line_data['directive'] == '##sequence-region' if not line_data['line_errors']])
                unresolved_seqid = set()
                if check_all_sources or sequence_region:
                    if valid_sequence_regions:
                        checked_at_least_one_source = True
                        for line_data, seqid in valid_line_data_seqid:
                            if seqid not in valid_sequence_regions:
                                if seqid not in unresolved_seqid:
                                    unresolved_seqid.add(seqid)
                                    error_lines.add(line_data['line_index'])
                                    self.add_line_error(line_data, {'message':'Seqid not found in any ##sequence-region: {0:s}'.format(seqid), 
                                     'error_type':'BOUNDS',  'location':'sequence_region'})
                                    continue
                            if line_data['start'] < valid_sequence_regions[seqid]['start']:
                                error_lines.add(line_data['line_index'])
                                self.add_line_error(line_data, {'message':'Start is less than the ##sequence-region start: %d' % valid_sequence_regions[seqid]['start'],  'error_type':'BOUNDS',  'location':'sequence_region'})
                            if line_data['end'] > valid_sequence_regions[seqid]['end']:
                                error_lines.add(line_data['line_index'])
                                self.add_line_error(line_data, {'message':'End is greater than the ##sequence-region end: %d' % valid_sequence_regions[seqid]['end'],  'error_type':'BOUNDS',  'location':'sequence_region'})

                elif sequence_region:
                    self.logger.debug('##sequence-region not found in GFF3')
                unresolved_seqid = set()
                if check_all_sources or fasta_embedded:
                    if self.fasta_embedded:
                        checked_at_least_one_source = True
                        for line_data, seqid in valid_line_data_seqid:
                            if seqid not in self.fasta_embedded:
                                if seqid not in unresolved_seqid:
                                    unresolved_seqid.add(seqid)
                                    error_lines.add(line_data['line_index'])
                                    self.add_line_error(line_data, {'message':'Seqid not found in the embedded ##FASTA: %s' % seqid,  'error_type':'BOUNDS',  'location':'fasta_embedded'})
                                    continue
                                if line_data['end'] > len(self.fasta_embedded[seqid]['seq']):
                                    error_lines.add(line_data['line_index'])
                                    self.add_line_error(line_data, {'message':'End is greater than the embedded ##FASTA sequence length: %d' % len(self.fasta_embedded[seqid]['seq']),  'error_type':'BOUNDS',  'location':'fasta_embedded'})
                                if check_n and line_data['type'] in check_n_feature_types:
                                    n_count = self.fasta_embedded[seqid]['seq'].count('N', line_data['start'] - 1, line_data['end']) + self.fasta_embedded[seqid]['seq'].count('n', line_data['start'] - 1, line_data['end'])
                                    if n_count > allowed_num_of_n:
                                        n_segments = [(m.start(), m.end() - m.start()) for m in n_segments_finditer(self.fasta_embedded[seqid]['seq'], line_data['start'] - 1, line_data['end'])]
                                        n_segments_str = ['(%d, %d)' % (m[0], m[1]) for m in n_segments]
                                        error_lines.add(line_data['line_index'])
                                        self.add_line_error(line_data, {'message':'Found %d Ns in %s feature of length %d using the embedded ##FASTA, consists of %d segment (start, length): %s' % (n_count, line_data['type'], line_data['end'] - line_data['start'], len(n_segments), ', '.join(n_segments_str)),  'error_type':'N_COUNT',  'n_segments':n_segments,  'location':'fasta_embedded'})

            elif fasta_embedded:
                self.logger.debug('Embedded ##FASTA not found in GFF3')
            unresolved_seqid = set()
            if check_all_sources or fasta_external:
                if self.fasta_external:
                    checked_at_least_one_source = True
                    for line_data, seqid in valid_line_data_seqid:
                        if seqid not in self.fasta_external:
                            if seqid not in unresolved_seqid:
                                unresolved_seqid.add(seqid)
                                error_lines.add(line_data['line_index'])
                                self.add_line_error(line_data, {'message':'Seqid not found in the external FASTA file: %s' % seqid,  'error_type':'BOUNDS',  'location':'fasta_external'})
                                continue
                            if line_data['end'] > len(self.fasta_external[seqid]['seq']):
                                error_lines.add(line_data['line_index'])
                                self.add_line_error(line_data, {'message':'End is greater than the external FASTA sequence length: %d' % len(self.fasta_external[seqid]['seq']),  'error_type':'BOUNDS',  'location':'fasta_external'})
                            if check_n and line_data['type'] in check_n_feature_types:
                                n_count = self.fasta_external[seqid]['seq'].count('N', line_data['start'] - 1, line_data['end']) + self.fasta_external[seqid]['seq'].count('n', line_data['start'] - 1, line_data['end'])
                                if n_count > allowed_num_of_n:
                                    n_segments = [(m.start(), m.end() - m.start()) for m in n_segments_finditer(self.fasta_external[seqid]['seq'], line_data['start'] - 1, line_data['end'])]
                                    n_segments_str = ['(%d, %d)' % (m[0], m[1]) for m in n_segments]
                                    error_lines.add(line_data['line_index'])
                                    self.add_line_error(line_data, {'message':'Found %d Ns in %s feature of length %d using the external FASTA, consists of %d segment (start, length): %s' % (n_count, line_data['type'], line_data['end'] - line_data['start'], len(n_segments), ', '.join(n_segments_str)),  'error_type':'N_COUNT',  'n_segments':n_segments,  'location':'fasta_external'})

        elif fasta_external:
            self.logger.debug('External FASTA file not given')
        if check_all_sources:
            if not checked_at_least_one_source:
                self.logger.debug('Unable to perform bounds check, requires at least one of the following sources: ##sequence-region, embedded ##FASTA, or external FASTA file')
        return error_lines

    def parse--- This code section failed: ---

 L. 436         0  LOAD_GLOBAL              set
                2  LOAD_CONST               ('+', '-', '.', '?')
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'valid_strand'

 L. 437         8  LOAD_GLOBAL              set
               10  LOAD_CONST               (0, 1, 2)
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  STORE_FAST               'valid_phase'

 L. 438        16  LOAD_GLOBAL              set
               18  LOAD_CONST               ('Parent', 'Alias', 'Note', 'Dbxref', 'Ontology_term')
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  STORE_FAST               'multi_value_attributes'

 L. 439        24  LOAD_GLOBAL              set
               26  LOAD_CONST               ('+', '-', '')
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'valid_attribute_target_strand'

 L. 440        32  LOAD_GLOBAL              set
               34  LOAD_CONST               ('ID', 'Name', 'Alias', 'Parent', 'Target', 'Gap', 'Derives_from', 'Note', 'Dbxref', 'Ontology_term', 'Is_circular')
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'reserved_attributes'

 L. 451        40  LOAD_GLOBAL              re
               42  LOAD_METHOD              compile
               44  LOAD_STR                 '[^a-zA-Z0-9.:^*$@!+_?|%-]|%(?![0-9a-fA-F]{2})'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  LOAD_ATTR                search
               50  STORE_FAST               'unescaped_seqid'

 L. 452        52  LOAD_GLOBAL              re
               54  LOAD_METHOD              compile
               56  LOAD_STR                 '[\\x00-\\x1f\\x7f]|%(?![0-9a-fA-F]{2})'
               58  CALL_METHOD_1         1  '1 positional argument'
               60  LOAD_ATTR                search
               62  STORE_FAST               'unescaped_field'

 L. 454        64  LOAD_FAST                'gff_file'
               66  STORE_FAST               'gff_fp'

 L. 455        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'gff_file'
               72  LOAD_GLOBAL              str
               74  CALL_FUNCTION_2       2  '2 positional arguments'
               76  POP_JUMP_IF_FALSE    92  'to 92'

 L. 456        78  LOAD_GLOBAL              open
               80  LOAD_FAST                'gff_file'
               82  LOAD_STR                 'r'
               84  LOAD_STR                 'utf8'
               86  LOAD_CONST               ('encoding',)
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  STORE_FAST               'gff_fp'
             92_0  COME_FROM            76  '76'

 L. 458        92  BUILD_LIST_0          0 
               94  STORE_FAST               'lines'

 L. 459        96  LOAD_CONST               1
               98  STORE_FAST               'current_line_num'

 L. 460       100  LOAD_GLOBAL              defaultdict
              102  LOAD_GLOBAL              list
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  STORE_FAST               'features'

 L. 462       108  LOAD_GLOBAL              defaultdict
              110  LOAD_GLOBAL              list
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  STORE_FAST               'unresolved_parents'

 L. 464   116_118  SETUP_LOOP         4744  'to 4744'
              120  LOAD_FAST                'gff_fp'
              122  GET_ITER         
          124_126  FOR_ITER           4742  'to 4742'
              128  STORE_FAST               'line_raw'

 L. 466       130  LOAD_FAST                'current_line_num'
              132  LOAD_CONST               1
              134  BINARY_SUBTRACT  

 L. 467       136  LOAD_FAST                'line_raw'

 L. 468       138  LOAD_STR                 'normal'

 L. 469       140  BUILD_LIST_0          0 

 L. 470       142  BUILD_LIST_0          0 

 L. 471       144  LOAD_STR                 ''

 L. 472       146  LOAD_STR                 ''

 L. 473       148  BUILD_LIST_0          0 

 L. 474       150  LOAD_STR                 ''
              152  LOAD_CONST               ('line_index', 'line_raw', 'line_status', 'parents', 'children', 'line_type', 'directive', 'line_errors', 'type')
              154  BUILD_CONST_KEY_MAP_9     9 
              156  STORE_DEREF              'line_data'

 L. 476       158  LOAD_FAST                'line_raw'
              160  LOAD_METHOD              strip
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  STORE_FAST               'line_strip'

 L. 477       166  LOAD_FAST                'line_strip'
              168  LOAD_FAST                'line_raw'
              170  LOAD_CONST               None
              172  LOAD_GLOBAL              len
              174  LOAD_FAST                'line_strip'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  COMPARE_OP               !=
              184  POP_JUMP_IF_FALSE   206  'to 206'

 L. 478       186  LOAD_FAST                'self'
              188  LOAD_METHOD              add_line_error
              190  LOAD_DEREF               'line_data'
              192  LOAD_STR                 'White chars not allowed at the start of a line'
              194  LOAD_STR                 'FORMAT'
              196  LOAD_STR                 ''
              198  LOAD_CONST               ('message', 'error_type', 'location')
              200  BUILD_CONST_KEY_MAP_3     3 
              202  CALL_METHOD_2         2  '2 positional arguments'
              204  POP_TOP          
            206_0  COME_FROM           184  '184'

 L. 479       206  LOAD_FAST                'current_line_num'
              208  LOAD_CONST               1
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   244  'to 244'
              214  LOAD_FAST                'line_strip'
              216  LOAD_METHOD              startswith
              218  LOAD_STR                 '##gff-version'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_JUMP_IF_TRUE    244  'to 244'

 L. 480       224  LOAD_FAST                'self'
              226  LOAD_METHOD              add_line_error
              228  LOAD_DEREF               'line_data'
              230  LOAD_STR                 '"##gff-version" missing from the first line'
              232  LOAD_STR                 'FORMAT'
              234  LOAD_STR                 ''
              236  LOAD_CONST               ('message', 'error_type', 'location')
              238  BUILD_CONST_KEY_MAP_3     3 
              240  CALL_METHOD_2         2  '2 positional arguments'
              242  POP_TOP          
            244_0  COME_FROM           222  '222'
            244_1  COME_FROM           212  '212'

 L. 481       244  LOAD_GLOBAL              len
              246  LOAD_FAST                'line_strip'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  LOAD_CONST               0
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   268  'to 268'

 L. 482       258  LOAD_STR                 'blank'
              260  LOAD_DEREF               'line_data'
              262  LOAD_STR                 'line_type'
              264  STORE_SUBSCR     

 L. 483       266  CONTINUE            124  'to 124'
            268_0  COME_FROM           254  '254'

 L. 484       268  LOAD_FAST                'line_strip'
              270  LOAD_METHOD              startswith
              272  LOAD_STR                 '##'
              274  CALL_METHOD_1         1  '1 positional argument'
          276_278  POP_JUMP_IF_FALSE  1928  'to 1928'

 L. 485       280  LOAD_STR                 'directive'
              282  LOAD_DEREF               'line_data'
              284  LOAD_STR                 'line_type'
              286  STORE_SUBSCR     

 L. 486       288  LOAD_FAST                'line_strip'
              290  LOAD_METHOD              startswith
              292  LOAD_STR                 '##sequence-region'
              294  CALL_METHOD_1         1  '1 positional argument'
          296_298  POP_JUMP_IF_FALSE   806  'to 806'

 L. 491       300  LOAD_STR                 '##sequence-region'
              302  LOAD_DEREF               'line_data'
              304  LOAD_STR                 'directive'
              306  STORE_SUBSCR     

 L. 492       308  LOAD_GLOBAL              list
              310  LOAD_FAST                'line_strip'
              312  LOAD_METHOD              split
              314  CALL_METHOD_0         0  '0 positional arguments'
              316  LOAD_CONST               1
              318  LOAD_CONST               None
              320  BUILD_SLICE_2         2 
              322  BINARY_SUBSCR    
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               'tokens'

 L. 493       328  LOAD_GLOBAL              len
              330  LOAD_FAST                'tokens'
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  LOAD_CONST               3
              336  COMPARE_OP               !=
          338_340  POP_JUMP_IF_FALSE   390  'to 390'

 L. 494       342  LOAD_FAST                'self'
              344  LOAD_METHOD              add_line_error
              346  LOAD_DEREF               'line_data'
              348  LOAD_STR                 'Expecting 3 fields, got %d: %s'
              350  LOAD_GLOBAL              len
              352  LOAD_FAST                'tokens'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  LOAD_CONST               1
              358  BINARY_SUBTRACT  
              360  LOAD_GLOBAL              repr
              362  LOAD_FAST                'tokens'
              364  LOAD_CONST               1
              366  LOAD_CONST               None
              368  BUILD_SLICE_2         2 
              370  BINARY_SUBSCR    
              372  CALL_FUNCTION_1       1  '1 positional argument'
              374  BUILD_TUPLE_2         2 
              376  BINARY_MODULO    
              378  LOAD_STR                 'FORMAT'
              380  LOAD_STR                 ''
              382  LOAD_CONST               ('message', 'error_type', 'location')
              384  BUILD_CONST_KEY_MAP_3     3 
              386  CALL_METHOD_2         2  '2 positional arguments'
              388  POP_TOP          
            390_0  COME_FROM           338  '338'

 L. 495       390  LOAD_GLOBAL              len
              392  LOAD_FAST                'tokens'
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  LOAD_CONST               0
              398  COMPARE_OP               >
          400_402  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 496       404  LOAD_FAST                'tokens'
              406  LOAD_CONST               0
              408  BINARY_SUBSCR    
              410  LOAD_DEREF               'line_data'
              412  LOAD_STR                 'seqid'
              414  STORE_SUBSCR     

 L. 498       416  LOAD_CLOSURE             'line_data'
              418  BUILD_TUPLE_1         1 
              420  LOAD_LISTCOMP            '<code_object <listcomp>>'
              422  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
              424  MAKE_FUNCTION_8          'closure'
              426  LOAD_FAST                'lines'
              428  GET_ITER         
              430  CALL_FUNCTION_1       1  '1 positional argument'
          432_434  POP_JUMP_IF_FALSE   464  'to 464'

 L. 499       436  LOAD_FAST                'self'
              438  LOAD_METHOD              add_line_error
              440  LOAD_DEREF               'line_data'
              442  LOAD_STR                 '##sequence-region seqid: "%s" may only appear once'
              444  LOAD_DEREF               'line_data'
              446  LOAD_STR                 'seqid'
              448  BINARY_SUBSCR    
              450  BINARY_MODULO    
              452  LOAD_STR                 'FORMAT'
              454  LOAD_STR                 ''
              456  LOAD_CONST               ('message', 'error_type', 'location')
              458  BUILD_CONST_KEY_MAP_3     3 
              460  CALL_METHOD_2         2  '2 positional arguments'
              462  POP_TOP          
            464_0  COME_FROM           432  '432'

 L. 500   464_466  SETUP_EXCEPT        780  'to 780'

 L. 501       468  LOAD_CONST               True
              470  STORE_FAST               'all_good'

 L. 502       472  SETUP_EXCEPT        536  'to 536'

 L. 503       474  LOAD_GLOBAL              int
              476  LOAD_FAST                'tokens'
              478  LOAD_CONST               1
              480  BINARY_SUBSCR    
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  LOAD_DEREF               'line_data'
              486  LOAD_STR                 'start'
              488  STORE_SUBSCR     

 L. 504       490  LOAD_DEREF               'line_data'
              492  LOAD_STR                 'start'
              494  BINARY_SUBSCR    
              496  LOAD_CONST               1
              498  COMPARE_OP               <
          500_502  POP_JUMP_IF_FALSE   532  'to 532'

 L. 505       504  LOAD_FAST                'self'
              506  LOAD_METHOD              add_line_error
              508  LOAD_DEREF               'line_data'
              510  LOAD_STR                 'Start is not a valid 1-based integer coordinate: "%s"'
              512  LOAD_FAST                'tokens'
              514  LOAD_CONST               1
              516  BINARY_SUBSCR    
              518  BINARY_MODULO    
              520  LOAD_STR                 'FORMAT'
              522  LOAD_STR                 ''
              524  LOAD_CONST               ('message', 'error_type', 'location')
              526  BUILD_CONST_KEY_MAP_3     3 
              528  CALL_METHOD_2         2  '2 positional arguments'
              530  POP_TOP          
            532_0  COME_FROM           500  '500'
              532  POP_BLOCK        
              534  JUMP_FORWARD        602  'to 602'
            536_0  COME_FROM_EXCEPT    472  '472'

 L. 506       536  DUP_TOP          
              538  LOAD_GLOBAL              ValueError
              540  COMPARE_OP               exception-match
          542_544  POP_JUMP_IF_FALSE   600  'to 600'
              546  POP_TOP          
              548  POP_TOP          
              550  POP_TOP          

 L. 507       552  LOAD_CONST               False
              554  STORE_FAST               'all_good'

 L. 508       556  LOAD_FAST                'self'
              558  LOAD_METHOD              add_line_error
              560  LOAD_DEREF               'line_data'
              562  LOAD_STR                 'Start is not a valid integer: "%s"'
              564  LOAD_FAST                'tokens'
              566  LOAD_CONST               1
              568  BINARY_SUBSCR    
              570  BINARY_MODULO    
              572  LOAD_STR                 'FORMAT'
              574  LOAD_STR                 ''
              576  LOAD_CONST               ('message', 'error_type', 'location')
              578  BUILD_CONST_KEY_MAP_3     3 
              580  CALL_METHOD_2         2  '2 positional arguments'
              582  POP_TOP          

 L. 509       584  LOAD_FAST                'tokens'
              586  LOAD_CONST               1
              588  BINARY_SUBSCR    
              590  LOAD_DEREF               'line_data'
              592  LOAD_STR                 'start'
              594  STORE_SUBSCR     
              596  POP_EXCEPT       
              598  JUMP_FORWARD        602  'to 602'
            600_0  COME_FROM           542  '542'
              600  END_FINALLY      
            602_0  COME_FROM           598  '598'
            602_1  COME_FROM           534  '534'

 L. 510       602  SETUP_EXCEPT        666  'to 666'

 L. 511       604  LOAD_GLOBAL              int
              606  LOAD_FAST                'tokens'
              608  LOAD_CONST               2
              610  BINARY_SUBSCR    
              612  CALL_FUNCTION_1       1  '1 positional argument'
              614  LOAD_DEREF               'line_data'
              616  LOAD_STR                 'end'
              618  STORE_SUBSCR     

 L. 512       620  LOAD_DEREF               'line_data'
              622  LOAD_STR                 'end'
              624  BINARY_SUBSCR    
              626  LOAD_CONST               1
              628  COMPARE_OP               <
          630_632  POP_JUMP_IF_FALSE   662  'to 662'

 L. 513       634  LOAD_FAST                'self'
              636  LOAD_METHOD              add_line_error
              638  LOAD_DEREF               'line_data'
              640  LOAD_STR                 'End is not a valid 1-based integer coordinate: "%s"'
              642  LOAD_FAST                'tokens'
              644  LOAD_CONST               2
              646  BINARY_SUBSCR    
              648  BINARY_MODULO    
              650  LOAD_STR                 'FORMAT'
              652  LOAD_STR                 ''
              654  LOAD_CONST               ('message', 'error_type', 'location')
              656  BUILD_CONST_KEY_MAP_3     3 
              658  CALL_METHOD_2         2  '2 positional arguments'
              660  POP_TOP          
            662_0  COME_FROM           630  '630'
              662  POP_BLOCK        
              664  JUMP_FORWARD        732  'to 732'
            666_0  COME_FROM_EXCEPT    602  '602'

 L. 514       666  DUP_TOP          
              668  LOAD_GLOBAL              ValueError
              670  COMPARE_OP               exception-match
          672_674  POP_JUMP_IF_FALSE   730  'to 730'
              676  POP_TOP          
              678  POP_TOP          
              680  POP_TOP          

 L. 515       682  LOAD_CONST               False
              684  STORE_FAST               'all_good'

 L. 516       686  LOAD_FAST                'self'
              688  LOAD_METHOD              add_line_error
              690  LOAD_DEREF               'line_data'
              692  LOAD_STR                 'End is not a valid integer: "%s"'
              694  LOAD_FAST                'tokens'
              696  LOAD_CONST               2
              698  BINARY_SUBSCR    
              700  BINARY_MODULO    
              702  LOAD_STR                 'FORMAT'
              704  LOAD_STR                 ''
              706  LOAD_CONST               ('message', 'error_type', 'location')
              708  BUILD_CONST_KEY_MAP_3     3 
              710  CALL_METHOD_2         2  '2 positional arguments'
              712  POP_TOP          

 L. 517       714  LOAD_FAST                'tokens'
              716  LOAD_CONST               2
              718  BINARY_SUBSCR    
              720  LOAD_DEREF               'line_data'
              722  LOAD_STR                 'start'
              724  STORE_SUBSCR     
              726  POP_EXCEPT       
              728  JUMP_FORWARD        732  'to 732'
            730_0  COME_FROM           672  '672'
              730  END_FINALLY      
            732_0  COME_FROM           728  '728'
            732_1  COME_FROM           664  '664'

 L. 519       732  LOAD_FAST                'all_good'
          734_736  POP_JUMP_IF_FALSE   776  'to 776'
              738  LOAD_DEREF               'line_data'
              740  LOAD_STR                 'start'
              742  BINARY_SUBSCR    
              744  LOAD_DEREF               'line_data'
              746  LOAD_STR                 'end'
              748  BINARY_SUBSCR    
              750  COMPARE_OP               >
          752_754  POP_JUMP_IF_FALSE   776  'to 776'

 L. 520       756  LOAD_FAST                'self'
              758  LOAD_METHOD              add_line_error
              760  LOAD_DEREF               'line_data'
              762  LOAD_STR                 'Start is not less than or equal to end'
              764  LOAD_STR                 'FORMAT'
              766  LOAD_STR                 ''
              768  LOAD_CONST               ('message', 'error_type', 'location')
              770  BUILD_CONST_KEY_MAP_3     3 
              772  CALL_METHOD_2         2  '2 positional arguments'
              774  POP_TOP          
            776_0  COME_FROM           752  '752'
            776_1  COME_FROM           734  '734'
              776  POP_BLOCK        
              778  JUMP_ABSOLUTE      4722  'to 4722'
            780_0  COME_FROM_EXCEPT    464  '464'

 L. 521       780  DUP_TOP          
              782  LOAD_GLOBAL              IndexError
              784  COMPARE_OP               exception-match
          786_788  POP_JUMP_IF_FALSE   800  'to 800'
              790  POP_TOP          
              792  POP_TOP          
              794  POP_TOP          

 L. 522       796  POP_EXCEPT       
              798  JUMP_ABSOLUTE      4722  'to 4722'
            800_0  COME_FROM           786  '786'
              800  END_FINALLY      
          802_804  JUMP_ABSOLUTE      4722  'to 4722'
            806_0  COME_FROM           296  '296'

 L. 523       806  LOAD_FAST                'line_strip'
              808  LOAD_METHOD              startswith
              810  LOAD_STR                 '##gff-version'
              812  CALL_METHOD_1         1  '1 positional argument'
          814_816  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 525       818  LOAD_STR                 '##gff-version'
              820  LOAD_DEREF               'line_data'
              822  LOAD_STR                 'directive'
              824  STORE_SUBSCR     

 L. 527       826  LOAD_LISTCOMP            '<code_object <listcomp>>'
              828  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
              830  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              832  LOAD_FAST                'lines'
              834  GET_ITER         
              836  CALL_FUNCTION_1       1  '1 positional argument'
          838_840  POP_JUMP_IF_FALSE   862  'to 862'

 L. 528       842  LOAD_FAST                'self'
              844  LOAD_METHOD              add_line_error
              846  LOAD_DEREF               'line_data'
              848  LOAD_STR                 '##gff-version missing from the first line'
              850  LOAD_STR                 'FORMAT'
              852  LOAD_STR                 ''
              854  LOAD_CONST               ('message', 'error_type', 'location')
              856  BUILD_CONST_KEY_MAP_3     3 
              858  CALL_METHOD_2         2  '2 positional arguments'
              860  POP_TOP          
            862_0  COME_FROM           838  '838'

 L. 529       862  LOAD_GLOBAL              list
              864  LOAD_FAST                'line_strip'
              866  LOAD_METHOD              split
              868  CALL_METHOD_0         0  '0 positional arguments'
              870  LOAD_CONST               1
              872  LOAD_CONST               None
              874  BUILD_SLICE_2         2 
              876  BINARY_SUBSCR    
              878  CALL_FUNCTION_1       1  '1 positional argument'
              880  STORE_FAST               'tokens'

 L. 530       882  LOAD_GLOBAL              len
              884  LOAD_FAST                'tokens'
              886  CALL_FUNCTION_1       1  '1 positional argument'
              888  LOAD_CONST               1
              890  COMPARE_OP               !=
          892_894  POP_JUMP_IF_FALSE   944  'to 944'

 L. 531       896  LOAD_FAST                'self'
              898  LOAD_METHOD              add_line_error
              900  LOAD_DEREF               'line_data'
              902  LOAD_STR                 'Expecting 1 field, got %d: %s'
              904  LOAD_GLOBAL              len
              906  LOAD_FAST                'tokens'
              908  CALL_FUNCTION_1       1  '1 positional argument'
              910  LOAD_CONST               1
              912  BINARY_SUBTRACT  
              914  LOAD_GLOBAL              repr
              916  LOAD_FAST                'tokens'
              918  LOAD_CONST               1
              920  LOAD_CONST               None
              922  BUILD_SLICE_2         2 
              924  BINARY_SUBSCR    
              926  CALL_FUNCTION_1       1  '1 positional argument'
              928  BUILD_TUPLE_2         2 
              930  BINARY_MODULO    
              932  LOAD_STR                 'FORMAT'
              934  LOAD_STR                 ''
              936  LOAD_CONST               ('message', 'error_type', 'location')
              938  BUILD_CONST_KEY_MAP_3     3 
              940  CALL_METHOD_2         2  '2 positional arguments'
              942  POP_TOP          
            944_0  COME_FROM           892  '892'

 L. 532       944  LOAD_GLOBAL              len
              946  LOAD_FAST                'tokens'
              948  CALL_FUNCTION_1       1  '1 positional argument'
              950  LOAD_CONST               0
              952  COMPARE_OP               >
          954_956  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 533       958  SETUP_EXCEPT       1022  'to 1022'

 L. 534       960  LOAD_GLOBAL              int
              962  LOAD_FAST                'tokens'
              964  LOAD_CONST               0
              966  BINARY_SUBSCR    
              968  CALL_FUNCTION_1       1  '1 positional argument'
              970  LOAD_DEREF               'line_data'
              972  LOAD_STR                 'version'
              974  STORE_SUBSCR     

 L. 535       976  LOAD_DEREF               'line_data'
              978  LOAD_STR                 'version'
              980  BINARY_SUBSCR    
              982  LOAD_CONST               3
              984  COMPARE_OP               !=
          986_988  POP_JUMP_IF_FALSE  1018  'to 1018'

 L. 536       990  LOAD_FAST                'self'
              992  LOAD_METHOD              add_line_error
              994  LOAD_DEREF               'line_data'
              996  LOAD_STR                 'Version is not "3": "%s"'
              998  LOAD_FAST                'tokens'
             1000  LOAD_CONST               0
             1002  BINARY_SUBSCR    
             1004  BINARY_MODULO    
             1006  LOAD_STR                 'FORMAT'
             1008  LOAD_STR                 ''
             1010  LOAD_CONST               ('message', 'error_type', 'location')
             1012  BUILD_CONST_KEY_MAP_3     3 
             1014  CALL_METHOD_2         2  '2 positional arguments'
             1016  POP_TOP          
           1018_0  COME_FROM           986  '986'
             1018  POP_BLOCK        
             1020  JUMP_ABSOLUTE      4722  'to 4722'
           1022_0  COME_FROM_EXCEPT    958  '958'

 L. 537      1022  DUP_TOP          
             1024  LOAD_GLOBAL              ValueError
             1026  COMPARE_OP               exception-match
         1028_1030  POP_JUMP_IF_FALSE  1082  'to 1082'
             1032  POP_TOP          
             1034  POP_TOP          
             1036  POP_TOP          

 L. 538      1038  LOAD_FAST                'self'
             1040  LOAD_METHOD              add_line_error
             1042  LOAD_DEREF               'line_data'
             1044  LOAD_STR                 'Version is not a valid integer: "%s"'
             1046  LOAD_FAST                'tokens'
             1048  LOAD_CONST               0
             1050  BINARY_SUBSCR    
             1052  BINARY_MODULO    
             1054  LOAD_STR                 'FORMAT'
             1056  LOAD_STR                 ''
             1058  LOAD_CONST               ('message', 'error_type', 'location')
             1060  BUILD_CONST_KEY_MAP_3     3 
             1062  CALL_METHOD_2         2  '2 positional arguments'
             1064  POP_TOP          

 L. 539      1066  LOAD_FAST                'tokens'
             1068  LOAD_CONST               0
             1070  BINARY_SUBSCR    
             1072  LOAD_DEREF               'line_data'
             1074  LOAD_STR                 'version'
             1076  STORE_SUBSCR     
             1078  POP_EXCEPT       
             1080  JUMP_ABSOLUTE      4722  'to 4722'
           1082_0  COME_FROM          1028  '1028'
             1082  END_FINALLY      
         1084_1086  JUMP_ABSOLUTE      4722  'to 4722'
           1088_0  COME_FROM           814  '814'

 L. 540      1088  LOAD_FAST                'line_strip'
             1090  LOAD_METHOD              startswith
             1092  LOAD_STR                 '###'
             1094  CALL_METHOD_1         1  '1 positional argument'
         1096_1098  POP_JUMP_IF_FALSE  1112  'to 1112'

 L. 542      1100  LOAD_STR                 '###'
             1102  LOAD_DEREF               'line_data'
             1104  LOAD_STR                 'directive'
             1106  STORE_SUBSCR     
         1108_1110  JUMP_ABSOLUTE      4722  'to 4722'
           1112_0  COME_FROM          1096  '1096'

 L. 543      1112  LOAD_FAST                'line_strip'
             1114  LOAD_METHOD              startswith
             1116  LOAD_STR                 '##FASTA'
             1118  CALL_METHOD_1         1  '1 positional argument'
         1120_1122  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 546      1124  LOAD_STR                 '##FASTA'
             1126  LOAD_DEREF               'line_data'
             1128  LOAD_STR                 'directive'
             1130  STORE_SUBSCR     

 L. 547      1132  LOAD_FAST                'self'
             1134  LOAD_ATTR                logger
             1136  LOAD_METHOD              info
             1138  LOAD_STR                 'Reading embedded ##FASTA sequence'
             1140  CALL_METHOD_1         1  '1 positional argument'
             1142  POP_TOP          

 L. 548      1144  LOAD_GLOBAL              fasta_file_to_dict
             1146  LOAD_FAST                'gff_fp'
             1148  CALL_FUNCTION_1       1  '1 positional argument'
             1150  UNPACK_SEQUENCE_2     2 
             1152  LOAD_FAST                'self'
             1154  STORE_ATTR               fasta_embedded
             1156  STORE_FAST               'count'

 L. 549      1158  LOAD_FAST                'self'
             1160  LOAD_ATTR                logger
             1162  LOAD_METHOD              info
             1164  LOAD_STR                 '%d sequences read'
             1166  LOAD_GLOBAL              len
             1168  LOAD_FAST                'self'
             1170  LOAD_ATTR                fasta_embedded
             1172  CALL_FUNCTION_1       1  '1 positional argument'
             1174  BINARY_MODULO    
             1176  CALL_METHOD_1         1  '1 positional argument'
             1178  POP_TOP          
         1180_1182  JUMP_ABSOLUTE      4722  'to 4722'
           1184_0  COME_FROM          1120  '1120'

 L. 550      1184  LOAD_FAST                'line_strip'
             1186  LOAD_METHOD              startswith
             1188  LOAD_STR                 '##feature-ontology'
             1190  CALL_METHOD_1         1  '1 positional argument'
         1192_1194  POP_JUMP_IF_FALSE  1316  'to 1316'

 L. 553      1196  LOAD_STR                 '##feature-ontology'
             1198  LOAD_DEREF               'line_data'
             1200  LOAD_STR                 'directive'
             1202  STORE_SUBSCR     

 L. 554      1204  LOAD_GLOBAL              list
             1206  LOAD_FAST                'line_strip'
             1208  LOAD_METHOD              split
             1210  CALL_METHOD_0         0  '0 positional arguments'
             1212  LOAD_CONST               1
             1214  LOAD_CONST               None
             1216  BUILD_SLICE_2         2 
             1218  BINARY_SUBSCR    
             1220  CALL_FUNCTION_1       1  '1 positional argument'
             1222  STORE_FAST               'tokens'

 L. 555      1224  LOAD_GLOBAL              len
             1226  LOAD_FAST                'tokens'
             1228  CALL_FUNCTION_1       1  '1 positional argument'
             1230  LOAD_CONST               1
             1232  COMPARE_OP               !=
         1234_1236  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 556      1238  LOAD_FAST                'self'
             1240  LOAD_METHOD              add_line_error
             1242  LOAD_DEREF               'line_data'
             1244  LOAD_STR                 'Expecting 1 field, got %d: %s'
             1246  LOAD_GLOBAL              len
             1248  LOAD_FAST                'tokens'
             1250  CALL_FUNCTION_1       1  '1 positional argument'
             1252  LOAD_CONST               1
             1254  BINARY_SUBTRACT  
             1256  LOAD_GLOBAL              repr
             1258  LOAD_FAST                'tokens'
             1260  LOAD_CONST               1
             1262  LOAD_CONST               None
             1264  BUILD_SLICE_2         2 
             1266  BINARY_SUBSCR    
             1268  CALL_FUNCTION_1       1  '1 positional argument'
             1270  BUILD_TUPLE_2         2 
             1272  BINARY_MODULO    
             1274  LOAD_STR                 'FORMAT'
             1276  LOAD_STR                 ''
             1278  LOAD_CONST               ('message', 'error_type', 'location')
             1280  BUILD_CONST_KEY_MAP_3     3 
             1282  CALL_METHOD_2         2  '2 positional arguments'
             1284  POP_TOP          
           1286_0  COME_FROM          1234  '1234'

 L. 557      1286  LOAD_GLOBAL              len
             1288  LOAD_FAST                'tokens'
             1290  CALL_FUNCTION_1       1  '1 positional argument'
             1292  LOAD_CONST               0
             1294  COMPARE_OP               >
         1296_1298  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 558      1300  LOAD_FAST                'tokens'
             1302  LOAD_CONST               0
             1304  BINARY_SUBSCR    
             1306  LOAD_DEREF               'line_data'
             1308  LOAD_STR                 'URI'
             1310  STORE_SUBSCR     
         1312_1314  JUMP_ABSOLUTE      4722  'to 4722'
           1316_0  COME_FROM          1192  '1192'

 L. 559      1316  LOAD_FAST                'line_strip'
             1318  LOAD_METHOD              startswith
             1320  LOAD_STR                 '##attribute-ontology'
             1322  CALL_METHOD_1         1  '1 positional argument'
         1324_1326  POP_JUMP_IF_FALSE  1448  'to 1448'

 L. 562      1328  LOAD_STR                 '##attribute-ontology'
             1330  LOAD_DEREF               'line_data'
             1332  LOAD_STR                 'directive'
             1334  STORE_SUBSCR     

 L. 563      1336  LOAD_GLOBAL              list
             1338  LOAD_FAST                'line_strip'
             1340  LOAD_METHOD              split
             1342  CALL_METHOD_0         0  '0 positional arguments'
             1344  LOAD_CONST               1
             1346  LOAD_CONST               None
             1348  BUILD_SLICE_2         2 
             1350  BINARY_SUBSCR    
             1352  CALL_FUNCTION_1       1  '1 positional argument'
             1354  STORE_FAST               'tokens'

 L. 564      1356  LOAD_GLOBAL              len
             1358  LOAD_FAST                'tokens'
             1360  CALL_FUNCTION_1       1  '1 positional argument'
             1362  LOAD_CONST               1
             1364  COMPARE_OP               !=
         1366_1368  POP_JUMP_IF_FALSE  1418  'to 1418'

 L. 565      1370  LOAD_FAST                'self'
             1372  LOAD_METHOD              add_line_error
             1374  LOAD_DEREF               'line_data'
             1376  LOAD_STR                 'Expecting 1 field, got %d: %s'
             1378  LOAD_GLOBAL              len
             1380  LOAD_FAST                'tokens'
             1382  CALL_FUNCTION_1       1  '1 positional argument'
             1384  LOAD_CONST               1
             1386  BINARY_SUBTRACT  
             1388  LOAD_GLOBAL              repr
             1390  LOAD_FAST                'tokens'
             1392  LOAD_CONST               1
             1394  LOAD_CONST               None
             1396  BUILD_SLICE_2         2 
             1398  BINARY_SUBSCR    
             1400  CALL_FUNCTION_1       1  '1 positional argument'
             1402  BUILD_TUPLE_2         2 
             1404  BINARY_MODULO    
             1406  LOAD_STR                 'FORMAT'
             1408  LOAD_STR                 ''
             1410  LOAD_CONST               ('message', 'error_type', 'location')
             1412  BUILD_CONST_KEY_MAP_3     3 
             1414  CALL_METHOD_2         2  '2 positional arguments'
             1416  POP_TOP          
           1418_0  COME_FROM          1366  '1366'

 L. 566      1418  LOAD_GLOBAL              len
             1420  LOAD_FAST                'tokens'
             1422  CALL_FUNCTION_1       1  '1 positional argument'
             1424  LOAD_CONST               0
             1426  COMPARE_OP               >
         1428_1430  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 567      1432  LOAD_FAST                'tokens'
             1434  LOAD_CONST               0
             1436  BINARY_SUBSCR    
             1438  LOAD_DEREF               'line_data'
             1440  LOAD_STR                 'URI'
             1442  STORE_SUBSCR     
         1444_1446  JUMP_ABSOLUTE      4722  'to 4722'
           1448_0  COME_FROM          1324  '1324'

 L. 568      1448  LOAD_FAST                'line_strip'
             1450  LOAD_METHOD              startswith
             1452  LOAD_STR                 '##source-ontology'
             1454  CALL_METHOD_1         1  '1 positional argument'
         1456_1458  POP_JUMP_IF_FALSE  1580  'to 1580'

 L. 571      1460  LOAD_STR                 '##source-ontology'
             1462  LOAD_DEREF               'line_data'
             1464  LOAD_STR                 'directive'
             1466  STORE_SUBSCR     

 L. 572      1468  LOAD_GLOBAL              list
             1470  LOAD_FAST                'line_strip'
             1472  LOAD_METHOD              split
             1474  CALL_METHOD_0         0  '0 positional arguments'
             1476  LOAD_CONST               1
             1478  LOAD_CONST               None
             1480  BUILD_SLICE_2         2 
             1482  BINARY_SUBSCR    
             1484  CALL_FUNCTION_1       1  '1 positional argument'
             1486  STORE_FAST               'tokens'

 L. 573      1488  LOAD_GLOBAL              len
             1490  LOAD_FAST                'tokens'
             1492  CALL_FUNCTION_1       1  '1 positional argument'
             1494  LOAD_CONST               1
             1496  COMPARE_OP               !=
         1498_1500  POP_JUMP_IF_FALSE  1550  'to 1550'

 L. 574      1502  LOAD_FAST                'self'
             1504  LOAD_METHOD              add_line_error
             1506  LOAD_DEREF               'line_data'
             1508  LOAD_STR                 'Expecting 1 field, got %d: %s'
             1510  LOAD_GLOBAL              len
             1512  LOAD_FAST                'tokens'
             1514  CALL_FUNCTION_1       1  '1 positional argument'
             1516  LOAD_CONST               1
             1518  BINARY_SUBTRACT  
             1520  LOAD_GLOBAL              repr
             1522  LOAD_FAST                'tokens'
             1524  LOAD_CONST               1
             1526  LOAD_CONST               None
             1528  BUILD_SLICE_2         2 
             1530  BINARY_SUBSCR    
             1532  CALL_FUNCTION_1       1  '1 positional argument'
             1534  BUILD_TUPLE_2         2 
             1536  BINARY_MODULO    
             1538  LOAD_STR                 'FORMAT'
             1540  LOAD_STR                 ''
             1542  LOAD_CONST               ('message', 'error_type', 'location')
             1544  BUILD_CONST_KEY_MAP_3     3 
             1546  CALL_METHOD_2         2  '2 positional arguments'
             1548  POP_TOP          
           1550_0  COME_FROM          1498  '1498'

 L. 575      1550  LOAD_GLOBAL              len
             1552  LOAD_FAST                'tokens'
             1554  CALL_FUNCTION_1       1  '1 positional argument'
             1556  LOAD_CONST               0
             1558  COMPARE_OP               >
         1560_1562  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 576      1564  LOAD_FAST                'tokens'
             1566  LOAD_CONST               0
             1568  BINARY_SUBSCR    
             1570  LOAD_DEREF               'line_data'
             1572  LOAD_STR                 'URI'
             1574  STORE_SUBSCR     
         1576_1578  JUMP_ABSOLUTE      4722  'to 4722'
           1580_0  COME_FROM          1456  '1456'

 L. 577      1580  LOAD_FAST                'line_strip'
             1582  LOAD_METHOD              startswith
             1584  LOAD_STR                 '##species'
             1586  CALL_METHOD_1         1  '1 positional argument'
         1588_1590  POP_JUMP_IF_FALSE  1710  'to 1710'

 L. 580      1592  LOAD_STR                 '##species'
             1594  LOAD_DEREF               'line_data'
             1596  LOAD_STR                 'directive'
             1598  STORE_SUBSCR     

 L. 581      1600  LOAD_GLOBAL              list
             1602  LOAD_FAST                'line_strip'
             1604  LOAD_METHOD              split
             1606  CALL_METHOD_0         0  '0 positional arguments'
             1608  LOAD_CONST               1
             1610  LOAD_CONST               None
             1612  BUILD_SLICE_2         2 
             1614  BINARY_SUBSCR    
             1616  CALL_FUNCTION_1       1  '1 positional argument'
             1618  STORE_FAST               'tokens'

 L. 582      1620  LOAD_GLOBAL              len
             1622  LOAD_FAST                'tokens'
             1624  CALL_FUNCTION_1       1  '1 positional argument'
             1626  LOAD_CONST               1
             1628  COMPARE_OP               !=
         1630_1632  POP_JUMP_IF_FALSE  1682  'to 1682'

 L. 583      1634  LOAD_FAST                'self'
             1636  LOAD_METHOD              add_line_error
             1638  LOAD_DEREF               'line_data'
             1640  LOAD_STR                 'Expecting 1 field, got %d: %s'
             1642  LOAD_GLOBAL              len
             1644  LOAD_FAST                'tokens'
             1646  CALL_FUNCTION_1       1  '1 positional argument'
             1648  LOAD_CONST               1
             1650  BINARY_SUBTRACT  
             1652  LOAD_GLOBAL              repr
             1654  LOAD_FAST                'tokens'
             1656  LOAD_CONST               1
             1658  LOAD_CONST               None
             1660  BUILD_SLICE_2         2 
             1662  BINARY_SUBSCR    
             1664  CALL_FUNCTION_1       1  '1 positional argument'
             1666  BUILD_TUPLE_2         2 
             1668  BINARY_MODULO    
             1670  LOAD_STR                 'FORMAT'
             1672  LOAD_STR                 ''
             1674  LOAD_CONST               ('message', 'error_type', 'location')
             1676  BUILD_CONST_KEY_MAP_3     3 
             1678  CALL_METHOD_2         2  '2 positional arguments'
             1680  POP_TOP          
           1682_0  COME_FROM          1630  '1630'

 L. 584      1682  LOAD_GLOBAL              len
             1684  LOAD_FAST                'tokens'
             1686  CALL_FUNCTION_1       1  '1 positional argument'
             1688  LOAD_CONST               0
             1690  COMPARE_OP               >
         1692_1694  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 585      1696  LOAD_FAST                'tokens'
             1698  LOAD_CONST               0
             1700  BINARY_SUBSCR    
             1702  LOAD_DEREF               'line_data'
             1704  LOAD_STR                 'NCBI_Taxonomy_URI'
             1706  STORE_SUBSCR     
             1708  JUMP_FORWARD       4722  'to 4722'
           1710_0  COME_FROM          1588  '1588'

 L. 586      1710  LOAD_FAST                'line_strip'
             1712  LOAD_METHOD              startswith
             1714  LOAD_STR                 '##genome-build'
             1716  CALL_METHOD_1         1  '1 positional argument'
         1718_1720  POP_JUMP_IF_FALSE  1880  'to 1880'

 L. 589      1722  LOAD_STR                 '##genome-build'
             1724  LOAD_DEREF               'line_data'
             1726  LOAD_STR                 'directive'
             1728  STORE_SUBSCR     

 L. 590      1730  LOAD_GLOBAL              list
             1732  LOAD_FAST                'line_strip'
             1734  LOAD_METHOD              split
             1736  CALL_METHOD_0         0  '0 positional arguments'
             1738  LOAD_CONST               1
             1740  LOAD_CONST               None
             1742  BUILD_SLICE_2         2 
             1744  BINARY_SUBSCR    
             1746  CALL_FUNCTION_1       1  '1 positional argument'
             1748  STORE_FAST               'tokens'

 L. 591      1750  LOAD_GLOBAL              len
             1752  LOAD_FAST                'tokens'
             1754  CALL_FUNCTION_1       1  '1 positional argument'
             1756  LOAD_CONST               2
             1758  COMPARE_OP               !=
         1760_1762  POP_JUMP_IF_FALSE  1812  'to 1812'

 L. 592      1764  LOAD_FAST                'self'
             1766  LOAD_METHOD              add_line_error
             1768  LOAD_DEREF               'line_data'
             1770  LOAD_STR                 'Expecting 2 fields, got %d: %s'
             1772  LOAD_GLOBAL              len
             1774  LOAD_FAST                'tokens'
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  LOAD_CONST               1
             1780  BINARY_SUBTRACT  
             1782  LOAD_GLOBAL              repr
             1784  LOAD_FAST                'tokens'
             1786  LOAD_CONST               1
             1788  LOAD_CONST               None
             1790  BUILD_SLICE_2         2 
             1792  BINARY_SUBSCR    
             1794  CALL_FUNCTION_1       1  '1 positional argument'
             1796  BUILD_TUPLE_2         2 
             1798  BINARY_MODULO    
             1800  LOAD_STR                 'FORMAT'
             1802  LOAD_STR                 ''
             1804  LOAD_CONST               ('message', 'error_type', 'location')
             1806  BUILD_CONST_KEY_MAP_3     3 
             1808  CALL_METHOD_2         2  '2 positional arguments'
             1810  POP_TOP          
           1812_0  COME_FROM          1760  '1760'

 L. 593      1812  LOAD_GLOBAL              len
             1814  LOAD_FAST                'tokens'
             1816  CALL_FUNCTION_1       1  '1 positional argument'
             1818  LOAD_CONST               0
             1820  COMPARE_OP               >
         1822_1824  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 594      1826  LOAD_FAST                'tokens'
             1828  LOAD_CONST               0
             1830  BINARY_SUBSCR    
             1832  LOAD_DEREF               'line_data'
             1834  LOAD_STR                 'source'
             1836  STORE_SUBSCR     

 L. 595      1838  SETUP_EXCEPT       1856  'to 1856'

 L. 596      1840  LOAD_FAST                'tokens'
             1842  LOAD_CONST               1
             1844  BINARY_SUBSCR    
             1846  LOAD_DEREF               'line_data'
             1848  LOAD_STR                 'buildName'
             1850  STORE_SUBSCR     
             1852  POP_BLOCK        
             1854  JUMP_FORWARD       1878  'to 1878'
           1856_0  COME_FROM_EXCEPT   1838  '1838'

 L. 597      1856  DUP_TOP          
             1858  LOAD_GLOBAL              IndexError
             1860  COMPARE_OP               exception-match
         1862_1864  POP_JUMP_IF_FALSE  1876  'to 1876'
             1866  POP_TOP          
             1868  POP_TOP          
             1870  POP_TOP          

 L. 598      1872  POP_EXCEPT       
             1874  JUMP_FORWARD       1878  'to 1878'
           1876_0  COME_FROM          1862  '1862'
             1876  END_FINALLY      
           1878_0  COME_FROM          1874  '1874'
           1878_1  COME_FROM          1854  '1854'
             1878  JUMP_FORWARD       4722  'to 4722'
           1880_0  COME_FROM          1718  '1718'

 L. 600      1880  LOAD_FAST                'self'
             1882  LOAD_METHOD              add_line_error
             1884  LOAD_DEREF               'line_data'
             1886  LOAD_STR                 'Unknown directive'
             1888  LOAD_STR                 'FORMAT'
             1890  LOAD_STR                 ''
             1892  LOAD_CONST               ('message', 'error_type', 'location')
             1894  BUILD_CONST_KEY_MAP_3     3 
             1896  CALL_METHOD_2         2  '2 positional arguments'
             1898  POP_TOP          

 L. 601      1900  LOAD_GLOBAL              list
             1902  LOAD_FAST                'line_strip'
             1904  LOAD_METHOD              split
             1906  CALL_METHOD_0         0  '0 positional arguments'
             1908  CALL_FUNCTION_1       1  '1 positional argument'
             1910  STORE_FAST               'tokens'

 L. 602      1912  LOAD_FAST                'tokens'
             1914  LOAD_CONST               0
             1916  BINARY_SUBSCR    
             1918  LOAD_DEREF               'line_data'
             1920  LOAD_STR                 'directive'
             1922  STORE_SUBSCR     
           1924_0  COME_FROM          1822  '1822'
           1924_1  COME_FROM          1692  '1692'
           1924_2  COME_FROM          1560  '1560'
           1924_3  COME_FROM          1428  '1428'
           1924_4  COME_FROM          1296  '1296'
           1924_5  COME_FROM           954  '954'
           1924_6  COME_FROM           400  '400'
         1924_1926  JUMP_FORWARD       4722  'to 4722'
           1928_0  COME_FROM           276  '276'

 L. 603      1928  LOAD_FAST                'line_strip'
             1930  LOAD_METHOD              startswith
             1932  LOAD_STR                 '#'
             1934  CALL_METHOD_1         1  '1 positional argument'
         1936_1938  POP_JUMP_IF_FALSE  1952  'to 1952'

 L. 604      1940  LOAD_STR                 'comment'
             1942  LOAD_DEREF               'line_data'
             1944  LOAD_STR                 'line_type'
             1946  STORE_SUBSCR     
         1948_1950  JUMP_FORWARD       4722  'to 4722'
           1952_0  COME_FROM          1936  '1936'

 L. 607      1952  LOAD_STR                 'feature'
             1954  LOAD_DEREF               'line_data'
             1956  LOAD_STR                 'line_type'
             1958  STORE_SUBSCR     

 L. 608      1960  LOAD_GLOBAL              list
             1962  LOAD_GLOBAL              map
             1964  LOAD_GLOBAL              str
             1966  LOAD_ATTR                strip
             1968  LOAD_FAST                'line_raw'
             1970  LOAD_METHOD              split
             1972  LOAD_STR                 '\t'
             1974  CALL_METHOD_1         1  '1 positional argument'
             1976  CALL_FUNCTION_2       2  '2 positional arguments'
             1978  CALL_FUNCTION_1       1  '1 positional argument'
             1980  STORE_FAST               'tokens'

 L. 609      1982  LOAD_GLOBAL              len
             1984  LOAD_FAST                'tokens'
             1986  CALL_FUNCTION_1       1  '1 positional argument'
             1988  LOAD_CONST               9
             1990  COMPARE_OP               !=
         1992_1994  POP_JUMP_IF_FALSE  2044  'to 2044'

 L. 610      1996  LOAD_FAST                'self'
             1998  LOAD_METHOD              add_line_error
             2000  LOAD_DEREF               'line_data'
             2002  LOAD_STR                 'Features should contain 9 fields, got %d: %s'
             2004  LOAD_GLOBAL              len
             2006  LOAD_FAST                'tokens'
             2008  CALL_FUNCTION_1       1  '1 positional argument'
             2010  LOAD_CONST               1
             2012  BINARY_SUBTRACT  
             2014  LOAD_GLOBAL              repr
             2016  LOAD_FAST                'tokens'
             2018  LOAD_CONST               1
             2020  LOAD_CONST               None
             2022  BUILD_SLICE_2         2 
             2024  BINARY_SUBSCR    
             2026  CALL_FUNCTION_1       1  '1 positional argument'
             2028  BUILD_TUPLE_2         2 
             2030  BINARY_MODULO    
             2032  LOAD_STR                 'FORMAT'
             2034  LOAD_STR                 ''
             2036  LOAD_CONST               ('message', 'error_type', 'location')
             2038  BUILD_CONST_KEY_MAP_3     3 
             2040  CALL_METHOD_2         2  '2 positional arguments'
             2042  POP_TOP          
           2044_0  COME_FROM          1992  '1992'

 L. 611      2044  SETUP_LOOP         2102  'to 2102'
             2046  LOAD_GLOBAL              enumerate
             2048  LOAD_FAST                'tokens'
             2050  CALL_FUNCTION_1       1  '1 positional argument'
             2052  GET_ITER         
           2054_0  COME_FROM          2064  '2064'
             2054  FOR_ITER           2100  'to 2100'
             2056  UNPACK_SEQUENCE_2     2 
             2058  STORE_FAST               'i'
             2060  STORE_FAST               't'

 L. 612      2062  LOAD_FAST                't'
         2064_2066  POP_JUMP_IF_TRUE   2054  'to 2054'

 L. 613      2068  LOAD_FAST                'self'
             2070  LOAD_METHOD              add_line_error
             2072  LOAD_DEREF               'line_data'
             2074  LOAD_STR                 'Empty field: %d, must have a "."'
             2076  LOAD_FAST                'i'
             2078  LOAD_CONST               1
             2080  BINARY_ADD       
             2082  BINARY_MODULO    
             2084  LOAD_STR                 'FORMAT'
             2086  LOAD_STR                 ''
             2088  LOAD_CONST               ('message', 'error_type', 'location')
             2090  BUILD_CONST_KEY_MAP_3     3 
             2092  CALL_METHOD_2         2  '2 positional arguments'
             2094  POP_TOP          
         2096_2098  JUMP_BACK          2054  'to 2054'
             2100  POP_BLOCK        
           2102_0  COME_FROM_LOOP     2044  '2044'

 L. 614  2102_2104  SETUP_EXCEPT       4700  'to 4700'

 L. 615      2106  LOAD_FAST                'tokens'
             2108  LOAD_CONST               0
             2110  BINARY_SUBSCR    
             2112  LOAD_DEREF               'line_data'
             2114  LOAD_STR                 'seqid'
             2116  STORE_SUBSCR     

 L. 616      2118  LOAD_FAST                'unescaped_seqid'
             2120  LOAD_FAST                'tokens'
             2122  LOAD_CONST               0
             2124  BINARY_SUBSCR    
             2126  CALL_FUNCTION_1       1  '1 positional argument'
         2128_2130  POP_JUMP_IF_FALSE  2160  'to 2160'

 L. 617      2132  LOAD_FAST                'self'
             2134  LOAD_METHOD              add_line_error
             2136  LOAD_DEREF               'line_data'
             2138  LOAD_STR                 'Seqid must escape any characters not in the set [a-zA-Z0-9.:^*$@!+_?-|]: "%s"'
             2140  LOAD_FAST                'tokens'
             2142  LOAD_CONST               0
             2144  BINARY_SUBSCR    
             2146  BINARY_MODULO    
             2148  LOAD_STR                 'FORMAT'
             2150  LOAD_STR                 ''
             2152  LOAD_CONST               ('message', 'error_type', 'location')
             2154  BUILD_CONST_KEY_MAP_3     3 
             2156  CALL_METHOD_2         2  '2 positional arguments'
             2158  POP_TOP          
           2160_0  COME_FROM          2128  '2128'

 L. 618      2160  LOAD_FAST                'tokens'
             2162  LOAD_CONST               1
             2164  BINARY_SUBSCR    
             2166  LOAD_DEREF               'line_data'
             2168  LOAD_STR                 'source'
             2170  STORE_SUBSCR     

 L. 619      2172  LOAD_FAST                'unescaped_field'
             2174  LOAD_FAST                'tokens'
             2176  LOAD_CONST               1
             2178  BINARY_SUBSCR    
             2180  CALL_FUNCTION_1       1  '1 positional argument'
         2182_2184  POP_JUMP_IF_FALSE  2214  'to 2214'

 L. 620      2186  LOAD_FAST                'self'
             2188  LOAD_METHOD              add_line_error
             2190  LOAD_DEREF               'line_data'
             2192  LOAD_STR                 'Source must escape the percent (%%) sign and any control characters: "%s"'
             2194  LOAD_FAST                'tokens'
             2196  LOAD_CONST               1
             2198  BINARY_SUBSCR    
             2200  BINARY_MODULO    
             2202  LOAD_STR                 'FORMAT'
             2204  LOAD_STR                 ''
             2206  LOAD_CONST               ('message', 'error_type', 'location')
             2208  BUILD_CONST_KEY_MAP_3     3 
             2210  CALL_METHOD_2         2  '2 positional arguments'
             2212  POP_TOP          
           2214_0  COME_FROM          2182  '2182'

 L. 621      2214  LOAD_FAST                'tokens'
             2216  LOAD_CONST               2
             2218  BINARY_SUBSCR    
             2220  LOAD_DEREF               'line_data'
             2222  LOAD_STR                 'type'
             2224  STORE_SUBSCR     

 L. 622      2226  LOAD_FAST                'unescaped_field'
             2228  LOAD_FAST                'tokens'
             2230  LOAD_CONST               2
             2232  BINARY_SUBSCR    
             2234  CALL_FUNCTION_1       1  '1 positional argument'
         2236_2238  POP_JUMP_IF_FALSE  2268  'to 2268'

 L. 623      2240  LOAD_FAST                'self'
             2242  LOAD_METHOD              add_line_error
             2244  LOAD_DEREF               'line_data'
             2246  LOAD_STR                 'Type must escape the percent (%%) sign and any control characters: "%s"'
             2248  LOAD_FAST                'tokens'
             2250  LOAD_CONST               2
             2252  BINARY_SUBSCR    
             2254  BINARY_MODULO    
             2256  LOAD_STR                 'FORMAT'
             2258  LOAD_STR                 ''
             2260  LOAD_CONST               ('message', 'error_type', 'location')
             2262  BUILD_CONST_KEY_MAP_3     3 
             2264  CALL_METHOD_2         2  '2 positional arguments'
             2266  POP_TOP          
           2268_0  COME_FROM          2236  '2236'

 L. 624      2268  LOAD_CONST               True
             2270  STORE_FAST               'all_good'

 L. 625      2272  SETUP_EXCEPT       2336  'to 2336'

 L. 626      2274  LOAD_GLOBAL              int
             2276  LOAD_FAST                'tokens'
             2278  LOAD_CONST               3
             2280  BINARY_SUBSCR    
             2282  CALL_FUNCTION_1       1  '1 positional argument'
             2284  LOAD_DEREF               'line_data'
             2286  LOAD_STR                 'start'
             2288  STORE_SUBSCR     

 L. 627      2290  LOAD_DEREF               'line_data'
             2292  LOAD_STR                 'start'
             2294  BINARY_SUBSCR    
             2296  LOAD_CONST               1
             2298  COMPARE_OP               <
         2300_2302  POP_JUMP_IF_FALSE  2332  'to 2332'

 L. 628      2304  LOAD_FAST                'self'
             2306  LOAD_METHOD              add_line_error
             2308  LOAD_DEREF               'line_data'
             2310  LOAD_STR                 'Start is not a valid 1-based integer coordinate: "%s"'
             2312  LOAD_FAST                'tokens'
             2314  LOAD_CONST               3
             2316  BINARY_SUBSCR    
             2318  BINARY_MODULO    
             2320  LOAD_STR                 'FORMAT'
             2322  LOAD_STR                 'start'
             2324  LOAD_CONST               ('message', 'error_type', 'location')
             2326  BUILD_CONST_KEY_MAP_3     3 
             2328  CALL_METHOD_2         2  '2 positional arguments'
             2330  POP_TOP          
           2332_0  COME_FROM          2300  '2300'
             2332  POP_BLOCK        
             2334  JUMP_FORWARD       2416  'to 2416'
           2336_0  COME_FROM_EXCEPT   2272  '2272'

 L. 629      2336  DUP_TOP          
             2338  LOAD_GLOBAL              ValueError
             2340  COMPARE_OP               exception-match
         2342_2344  POP_JUMP_IF_FALSE  2414  'to 2414'
             2346  POP_TOP          
             2348  POP_TOP          
             2350  POP_TOP          

 L. 630      2352  LOAD_CONST               False
             2354  STORE_FAST               'all_good'

 L. 631      2356  LOAD_FAST                'tokens'
             2358  LOAD_CONST               3
             2360  BINARY_SUBSCR    
             2362  LOAD_DEREF               'line_data'
             2364  LOAD_STR                 'start'
             2366  STORE_SUBSCR     

 L. 632      2368  LOAD_DEREF               'line_data'
             2370  LOAD_STR                 'start'
             2372  BINARY_SUBSCR    
             2374  LOAD_STR                 '.'
             2376  COMPARE_OP               !=
         2378_2380  POP_JUMP_IF_FALSE  2410  'to 2410'

 L. 633      2382  LOAD_FAST                'self'
             2384  LOAD_METHOD              add_line_error
             2386  LOAD_DEREF               'line_data'
             2388  LOAD_STR                 'Start is not a valid integer: "%s"'
             2390  LOAD_DEREF               'line_data'
             2392  LOAD_STR                 'start'
             2394  BINARY_SUBSCR    
             2396  BINARY_MODULO    
             2398  LOAD_STR                 'FORMAT'
             2400  LOAD_STR                 'start'
             2402  LOAD_CONST               ('message', 'error_type', 'location')
             2404  BUILD_CONST_KEY_MAP_3     3 
             2406  CALL_METHOD_2         2  '2 positional arguments'
             2408  POP_TOP          
           2410_0  COME_FROM          2378  '2378'
             2410  POP_EXCEPT       
             2412  JUMP_FORWARD       2416  'to 2416'
           2414_0  COME_FROM          2342  '2342'
             2414  END_FINALLY      
           2416_0  COME_FROM          2412  '2412'
           2416_1  COME_FROM          2334  '2334'

 L. 634      2416  SETUP_EXCEPT       2480  'to 2480'

 L. 635      2418  LOAD_GLOBAL              int
             2420  LOAD_FAST                'tokens'
             2422  LOAD_CONST               4
             2424  BINARY_SUBSCR    
             2426  CALL_FUNCTION_1       1  '1 positional argument'
             2428  LOAD_DEREF               'line_data'
             2430  LOAD_STR                 'end'
             2432  STORE_SUBSCR     

 L. 636      2434  LOAD_DEREF               'line_data'
             2436  LOAD_STR                 'end'
             2438  BINARY_SUBSCR    
             2440  LOAD_CONST               1
             2442  COMPARE_OP               <
         2444_2446  POP_JUMP_IF_FALSE  2476  'to 2476'

 L. 637      2448  LOAD_FAST                'self'
             2450  LOAD_METHOD              add_line_error
             2452  LOAD_DEREF               'line_data'
             2454  LOAD_STR                 'End is not a valid 1-based integer coordinate: "%s"'
             2456  LOAD_FAST                'tokens'
             2458  LOAD_CONST               4
             2460  BINARY_SUBSCR    
             2462  BINARY_MODULO    
             2464  LOAD_STR                 'FORMAT'
             2466  LOAD_STR                 'end'
             2468  LOAD_CONST               ('message', 'error_type', 'location')
             2470  BUILD_CONST_KEY_MAP_3     3 
             2472  CALL_METHOD_2         2  '2 positional arguments'
             2474  POP_TOP          
           2476_0  COME_FROM          2444  '2444'
             2476  POP_BLOCK        
             2478  JUMP_FORWARD       2560  'to 2560'
           2480_0  COME_FROM_EXCEPT   2416  '2416'

 L. 638      2480  DUP_TOP          
             2482  LOAD_GLOBAL              ValueError
             2484  COMPARE_OP               exception-match
         2486_2488  POP_JUMP_IF_FALSE  2558  'to 2558'
             2490  POP_TOP          
             2492  POP_TOP          
             2494  POP_TOP          

 L. 639      2496  LOAD_CONST               False
             2498  STORE_FAST               'all_good'

 L. 640      2500  LOAD_FAST                'tokens'
             2502  LOAD_CONST               4
             2504  BINARY_SUBSCR    
             2506  LOAD_DEREF               'line_data'
             2508  LOAD_STR                 'end'
             2510  STORE_SUBSCR     

 L. 641      2512  LOAD_DEREF               'line_data'
             2514  LOAD_STR                 'end'
             2516  BINARY_SUBSCR    
             2518  LOAD_STR                 '.'
             2520  COMPARE_OP               !=
         2522_2524  POP_JUMP_IF_FALSE  2554  'to 2554'

 L. 642      2526  LOAD_FAST                'self'
             2528  LOAD_METHOD              add_line_error
             2530  LOAD_DEREF               'line_data'
             2532  LOAD_STR                 'End is not a valid integer: "%s"'
             2534  LOAD_DEREF               'line_data'
             2536  LOAD_STR                 'end'
             2538  BINARY_SUBSCR    
             2540  BINARY_MODULO    
             2542  LOAD_STR                 'FORMAT'
             2544  LOAD_STR                 'end'
             2546  LOAD_CONST               ('message', 'error_type', 'location')
             2548  BUILD_CONST_KEY_MAP_3     3 
             2550  CALL_METHOD_2         2  '2 positional arguments'
             2552  POP_TOP          
           2554_0  COME_FROM          2522  '2522'
             2554  POP_EXCEPT       
             2556  JUMP_FORWARD       2560  'to 2560'
           2558_0  COME_FROM          2486  '2486'
             2558  END_FINALLY      
           2560_0  COME_FROM          2556  '2556'
           2560_1  COME_FROM          2478  '2478'

 L. 644      2560  LOAD_FAST                'all_good'
         2562_2564  POP_JUMP_IF_FALSE  2604  'to 2604'
             2566  LOAD_DEREF               'line_data'
             2568  LOAD_STR                 'start'
             2570  BINARY_SUBSCR    
             2572  LOAD_DEREF               'line_data'
             2574  LOAD_STR                 'end'
             2576  BINARY_SUBSCR    
             2578  COMPARE_OP               >
         2580_2582  POP_JUMP_IF_FALSE  2604  'to 2604'

 L. 645      2584  LOAD_FAST                'self'
             2586  LOAD_METHOD              add_line_error
             2588  LOAD_DEREF               'line_data'
             2590  LOAD_STR                 'Start is not less than or equal to end'
             2592  LOAD_STR                 'FORMAT'
             2594  LOAD_STR                 'start,end'
             2596  LOAD_CONST               ('message', 'error_type', 'location')
             2598  BUILD_CONST_KEY_MAP_3     3 
             2600  CALL_METHOD_2         2  '2 positional arguments'
             2602  POP_TOP          
           2604_0  COME_FROM          2580  '2580'
           2604_1  COME_FROM          2562  '2562'

 L. 646      2604  SETUP_EXCEPT       2626  'to 2626'

 L. 647      2606  LOAD_GLOBAL              float
             2608  LOAD_FAST                'tokens'
             2610  LOAD_CONST               5
             2612  BINARY_SUBSCR    
             2614  CALL_FUNCTION_1       1  '1 positional argument'
             2616  LOAD_DEREF               'line_data'
             2618  LOAD_STR                 'score'
             2620  STORE_SUBSCR     
             2622  POP_BLOCK        
             2624  JUMP_FORWARD       2702  'to 2702'
           2626_0  COME_FROM_EXCEPT   2604  '2604'

 L. 648      2626  DUP_TOP          
             2628  LOAD_GLOBAL              ValueError
             2630  COMPARE_OP               exception-match
         2632_2634  POP_JUMP_IF_FALSE  2700  'to 2700'
             2636  POP_TOP          
             2638  POP_TOP          
             2640  POP_TOP          

 L. 649      2642  LOAD_FAST                'tokens'
             2644  LOAD_CONST               5
             2646  BINARY_SUBSCR    
             2648  LOAD_DEREF               'line_data'
             2650  LOAD_STR                 'score'
             2652  STORE_SUBSCR     

 L. 650      2654  LOAD_DEREF               'line_data'
             2656  LOAD_STR                 'score'
             2658  BINARY_SUBSCR    
             2660  LOAD_STR                 '.'
             2662  COMPARE_OP               !=
         2664_2666  POP_JUMP_IF_FALSE  2696  'to 2696'

 L. 651      2668  LOAD_FAST                'self'
             2670  LOAD_METHOD              add_line_error
             2672  LOAD_DEREF               'line_data'
             2674  LOAD_STR                 'Score is not a valid floating point number: "%s"'
             2676  LOAD_DEREF               'line_data'
             2678  LOAD_STR                 'score'
             2680  BINARY_SUBSCR    
             2682  BINARY_MODULO    
             2684  LOAD_STR                 'FORMAT'
             2686  LOAD_STR                 ''
             2688  LOAD_CONST               ('message', 'error_type', 'location')
             2690  BUILD_CONST_KEY_MAP_3     3 
             2692  CALL_METHOD_2         2  '2 positional arguments'
             2694  POP_TOP          
           2696_0  COME_FROM          2664  '2664'
             2696  POP_EXCEPT       
             2698  JUMP_FORWARD       2702  'to 2702'
           2700_0  COME_FROM          2632  '2632'
             2700  END_FINALLY      
           2702_0  COME_FROM          2698  '2698'
           2702_1  COME_FROM          2624  '2624'

 L. 652      2702  LOAD_FAST                'tokens'
             2704  LOAD_CONST               6
             2706  BINARY_SUBSCR    
             2708  LOAD_DEREF               'line_data'
             2710  LOAD_STR                 'strand'
             2712  STORE_SUBSCR     

 L. 653      2714  LOAD_DEREF               'line_data'
             2716  LOAD_STR                 'strand'
             2718  BINARY_SUBSCR    
             2720  LOAD_FAST                'valid_strand'
             2722  COMPARE_OP               not-in
         2724_2726  POP_JUMP_IF_FALSE  2756  'to 2756'

 L. 654      2728  LOAD_FAST                'self'
             2730  LOAD_METHOD              add_line_error
             2732  LOAD_DEREF               'line_data'
             2734  LOAD_STR                 'Strand has illegal characters: "%s"'
             2736  LOAD_FAST                'tokens'
             2738  LOAD_CONST               6
             2740  BINARY_SUBSCR    
             2742  BINARY_MODULO    
             2744  LOAD_STR                 'FORMAT'
             2746  LOAD_STR                 ''
             2748  LOAD_CONST               ('message', 'error_type', 'location')
             2750  BUILD_CONST_KEY_MAP_3     3 
             2752  CALL_METHOD_2         2  '2 positional arguments'
             2754  POP_TOP          
           2756_0  COME_FROM          2724  '2724'

 L. 655      2756  SETUP_EXCEPT       2820  'to 2820'

 L. 656      2758  LOAD_GLOBAL              int
             2760  LOAD_FAST                'tokens'
             2762  LOAD_CONST               7
             2764  BINARY_SUBSCR    
             2766  CALL_FUNCTION_1       1  '1 positional argument'
             2768  LOAD_DEREF               'line_data'
             2770  LOAD_STR                 'phase'
             2772  STORE_SUBSCR     

 L. 657      2774  LOAD_DEREF               'line_data'
             2776  LOAD_STR                 'phase'
             2778  BINARY_SUBSCR    
             2780  LOAD_FAST                'valid_phase'
             2782  COMPARE_OP               not-in
         2784_2786  POP_JUMP_IF_FALSE  2816  'to 2816'

 L. 658      2788  LOAD_FAST                'self'
             2790  LOAD_METHOD              add_line_error
             2792  LOAD_DEREF               'line_data'
             2794  LOAD_STR                 'Phase is not 0, 1, or 2: "%s"'
             2796  LOAD_FAST                'tokens'
             2798  LOAD_CONST               7
             2800  BINARY_SUBSCR    
             2802  BINARY_MODULO    
             2804  LOAD_STR                 'FORMAT'
             2806  LOAD_STR                 ''
             2808  LOAD_CONST               ('message', 'error_type', 'location')
             2810  BUILD_CONST_KEY_MAP_3     3 
             2812  CALL_METHOD_2         2  '2 positional arguments'
             2814  POP_TOP          
           2816_0  COME_FROM          2784  '2784'
             2816  POP_BLOCK        
             2818  JUMP_FORWARD       2932  'to 2932'
           2820_0  COME_FROM_EXCEPT   2756  '2756'

 L. 659      2820  DUP_TOP          
             2822  LOAD_GLOBAL              ValueError
             2824  COMPARE_OP               exception-match
         2826_2828  POP_JUMP_IF_FALSE  2930  'to 2930'
             2830  POP_TOP          
             2832  POP_TOP          
             2834  POP_TOP          

 L. 660      2836  LOAD_FAST                'tokens'
             2838  LOAD_CONST               7
             2840  BINARY_SUBSCR    
             2842  LOAD_DEREF               'line_data'
             2844  LOAD_STR                 'phase'
             2846  STORE_SUBSCR     

 L. 661      2848  LOAD_DEREF               'line_data'
             2850  LOAD_STR                 'phase'
             2852  BINARY_SUBSCR    
             2854  LOAD_STR                 '.'
             2856  COMPARE_OP               !=
         2858_2860  POP_JUMP_IF_FALSE  2892  'to 2892'

 L. 662      2862  LOAD_FAST                'self'
             2864  LOAD_METHOD              add_line_error
             2866  LOAD_DEREF               'line_data'
             2868  LOAD_STR                 'Phase is not a valid integer: "%s"'
             2870  LOAD_DEREF               'line_data'
             2872  LOAD_STR                 'phase'
             2874  BINARY_SUBSCR    
             2876  BINARY_MODULO    
             2878  LOAD_STR                 'FORMAT'
             2880  LOAD_STR                 ''
             2882  LOAD_CONST               ('message', 'error_type', 'location')
             2884  BUILD_CONST_KEY_MAP_3     3 
             2886  CALL_METHOD_2         2  '2 positional arguments'
             2888  POP_TOP          
             2890  JUMP_FORWARD       2926  'to 2926'
           2892_0  COME_FROM          2858  '2858'

 L. 663      2892  LOAD_DEREF               'line_data'
             2894  LOAD_STR                 'type'
             2896  BINARY_SUBSCR    
             2898  LOAD_STR                 'CDS'
             2900  COMPARE_OP               ==
         2902_2904  POP_JUMP_IF_FALSE  2926  'to 2926'

 L. 664      2906  LOAD_FAST                'self'
             2908  LOAD_METHOD              add_line_error
             2910  LOAD_DEREF               'line_data'
             2912  LOAD_STR                 'Phase is required for all CDS features'
             2914  LOAD_STR                 'FORMAT'
             2916  LOAD_STR                 ''
             2918  LOAD_CONST               ('message', 'error_type', 'location')
             2920  BUILD_CONST_KEY_MAP_3     3 
             2922  CALL_METHOD_2         2  '2 positional arguments'
             2924  POP_TOP          
           2926_0  COME_FROM          2902  '2902'
           2926_1  COME_FROM          2890  '2890'
             2926  POP_EXCEPT       
             2928  JUMP_FORWARD       2932  'to 2932'
           2930_0  COME_FROM          2826  '2826'
             2930  END_FINALLY      
           2932_0  COME_FROM          2928  '2928'
           2932_1  COME_FROM          2818  '2818'

 L. 669      2932  LOAD_FAST                'unescaped_field'
             2934  LOAD_FAST                'tokens'
             2936  LOAD_CONST               8
             2938  BINARY_SUBSCR    
             2940  CALL_FUNCTION_1       1  '1 positional argument'
         2942_2944  POP_JUMP_IF_FALSE  2966  'to 2966'

 L. 670      2946  LOAD_FAST                'self'
             2948  LOAD_METHOD              add_line_error
             2950  LOAD_DEREF               'line_data'
             2952  LOAD_STR                 'Attributes must escape the percent (%) sign and any control characters'
             2954  LOAD_STR                 'FORMAT'
             2956  LOAD_STR                 ''
             2958  LOAD_CONST               ('message', 'error_type', 'location')
             2960  BUILD_CONST_KEY_MAP_3     3 
             2962  CALL_METHOD_2         2  '2 positional arguments'
             2964  POP_TOP          
           2966_0  COME_FROM          2942  '2942'

 L. 671      2966  LOAD_GLOBAL              tuple
             2968  LOAD_GENEXPR             '<code_object <genexpr>>'
             2970  LOAD_STR                 'Gff3.parse.<locals>.<genexpr>'
             2972  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2974  LOAD_FAST                'tokens'
             2976  LOAD_CONST               8
             2978  BINARY_SUBSCR    
             2980  LOAD_METHOD              split
             2982  LOAD_STR                 ';'
             2984  CALL_METHOD_1         1  '1 positional argument'
             2986  GET_ITER         
             2988  CALL_FUNCTION_1       1  '1 positional argument'
             2990  CALL_FUNCTION_1       1  '1 positional argument'
             2992  STORE_FAST               'attribute_tokens'

 L. 672      2994  BUILD_MAP_0           0 
             2996  LOAD_DEREF               'line_data'
             2998  LOAD_STR                 'attributes'
             3000  STORE_SUBSCR     

 L. 673      3002  LOAD_GLOBAL              len
             3004  LOAD_FAST                'attribute_tokens'
             3006  CALL_FUNCTION_1       1  '1 positional argument'
             3008  LOAD_CONST               1
             3010  COMPARE_OP               ==
         3012_3014  POP_JUMP_IF_FALSE  3056  'to 3056'
             3016  LOAD_GLOBAL              len
             3018  LOAD_FAST                'attribute_tokens'
             3020  LOAD_CONST               0
             3022  BINARY_SUBSCR    
             3024  CALL_FUNCTION_1       1  '1 positional argument'
             3026  LOAD_CONST               1
             3028  COMPARE_OP               ==
         3030_3032  POP_JUMP_IF_FALSE  3056  'to 3056'
             3034  LOAD_FAST                'attribute_tokens'
             3036  LOAD_CONST               0
             3038  BINARY_SUBSCR    
             3040  LOAD_CONST               0
             3042  BINARY_SUBSCR    
             3044  LOAD_STR                 '.'
             3046  COMPARE_OP               ==
         3048_3050  POP_JUMP_IF_FALSE  3056  'to 3056'

 L. 674  3052_3054  JUMP_FORWARD       4696  'to 4696'
           3056_0  COME_FROM          3048  '3048'
           3056_1  COME_FROM          3030  '3030'
           3056_2  COME_FROM          3012  '3012'

 L. 676  3056_3058  SETUP_LOOP         4696  'to 4696'
             3060  LOAD_FAST                'attribute_tokens'
             3062  GET_ITER         
           3064_0  COME_FROM          4586  '4586'
         3064_3066  FOR_ITER           4694  'to 4694'
             3068  STORE_FAST               'a'

 L. 677      3070  LOAD_GLOBAL              len
             3072  LOAD_FAST                'a'
             3074  CALL_FUNCTION_1       1  '1 positional argument'
             3076  LOAD_CONST               2
             3078  COMPARE_OP               !=
         3080_3082  POP_JUMP_IF_FALSE  3114  'to 3114'

 L. 678      3084  LOAD_FAST                'self'
             3086  LOAD_METHOD              add_line_error
             3088  LOAD_DEREF               'line_data'
             3090  LOAD_STR                 'Attributes must contain one and only one equal (=) sign: "%s"'
             3092  LOAD_STR                 '='
             3094  LOAD_METHOD              join
             3096  LOAD_FAST                'a'
             3098  CALL_METHOD_1         1  '1 positional argument'
             3100  BINARY_MODULO    
             3102  LOAD_STR                 'FORMAT'
             3104  LOAD_STR                 ''
             3106  LOAD_CONST               ('message', 'error_type', 'location')
             3108  BUILD_CONST_KEY_MAP_3     3 
             3110  CALL_METHOD_2         2  '2 positional arguments'
             3112  POP_TOP          
           3114_0  COME_FROM          3080  '3080'

 L. 679      3114  SETUP_EXCEPT       3128  'to 3128'

 L. 680      3116  LOAD_FAST                'a'
             3118  UNPACK_SEQUENCE_2     2 
             3120  STORE_DEREF              'tag'
             3122  STORE_FAST               'value'
             3124  POP_BLOCK        
             3126  JUMP_FORWARD       3164  'to 3164'
           3128_0  COME_FROM_EXCEPT   3114  '3114'

 L. 681      3128  DUP_TOP          
             3130  LOAD_GLOBAL              ValueError
             3132  COMPARE_OP               exception-match
         3134_3136  POP_JUMP_IF_FALSE  3162  'to 3162'
             3138  POP_TOP          
             3140  POP_TOP          
             3142  POP_TOP          

 L. 682      3144  LOAD_FAST                'a'
             3146  LOAD_CONST               0
             3148  BINARY_SUBSCR    
             3150  LOAD_STR                 ''
             3152  ROT_TWO          
             3154  STORE_DEREF              'tag'
             3156  STORE_FAST               'value'
             3158  POP_EXCEPT       
             3160  JUMP_FORWARD       3164  'to 3164'
           3162_0  COME_FROM          3134  '3134'
             3162  END_FINALLY      
           3164_0  COME_FROM          3160  '3160'
           3164_1  COME_FROM          3126  '3126'

 L. 683      3164  LOAD_DEREF               'tag'
         3166_3168  POP_JUMP_IF_TRUE   3200  'to 3200'

 L. 684      3170  LOAD_FAST                'self'
             3172  LOAD_METHOD              add_line_error
             3174  LOAD_DEREF               'line_data'
             3176  LOAD_STR                 'Empty attribute tag: "%s"'
             3178  LOAD_STR                 '='
             3180  LOAD_METHOD              join
             3182  LOAD_FAST                'a'
             3184  CALL_METHOD_1         1  '1 positional argument'
             3186  BINARY_MODULO    
             3188  LOAD_STR                 'FORMAT'
             3190  LOAD_STR                 ''
             3192  LOAD_CONST               ('message', 'error_type', 'location')
             3194  BUILD_CONST_KEY_MAP_3     3 
             3196  CALL_METHOD_2         2  '2 positional arguments'
             3198  POP_TOP          
           3200_0  COME_FROM          3166  '3166'

 L. 685      3200  LOAD_FAST                'value'
             3202  LOAD_METHOD              strip
             3204  CALL_METHOD_0         0  '0 positional arguments'
         3206_3208  POP_JUMP_IF_TRUE   3246  'to 3246'

 L. 686      3210  LOAD_FAST                'self'
             3212  LOAD_ATTR                add_line_error
             3214  LOAD_DEREF               'line_data'
             3216  LOAD_STR                 'Empty attribute value: "%s"'
             3218  LOAD_STR                 '='
             3220  LOAD_METHOD              join
             3222  LOAD_FAST                'a'
             3224  CALL_METHOD_1         1  '1 positional argument'
             3226  BINARY_MODULO    
             3228  LOAD_STR                 'FORMAT'
             3230  LOAD_STR                 ''
             3232  LOAD_CONST               ('message', 'error_type', 'location')
             3234  BUILD_CONST_KEY_MAP_3     3 
             3236  LOAD_GLOBAL              logging
             3238  LOAD_ATTR                WARNING
             3240  LOAD_CONST               ('log_level',)
             3242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3244  POP_TOP          
           3246_0  COME_FROM          3206  '3206'

 L. 687      3246  LOAD_DEREF               'tag'
             3248  LOAD_DEREF               'line_data'
             3250  LOAD_STR                 'attributes'
             3252  BINARY_SUBSCR    
             3254  COMPARE_OP               in
         3256_3258  POP_JUMP_IF_FALSE  3284  'to 3284'

 L. 688      3260  LOAD_FAST                'self'
             3262  LOAD_METHOD              add_line_error
             3264  LOAD_DEREF               'line_data'
             3266  LOAD_STR                 'Found multiple attribute tags: "%s"'
             3268  LOAD_DEREF               'tag'
             3270  BINARY_MODULO    
             3272  LOAD_STR                 'FORMAT'
             3274  LOAD_STR                 ''
             3276  LOAD_CONST               ('message', 'error_type', 'location')
             3278  BUILD_CONST_KEY_MAP_3     3 
             3280  CALL_METHOD_2         2  '2 positional arguments'
             3282  POP_TOP          
           3284_0  COME_FROM          3256  '3256'

 L. 689      3284  LOAD_DEREF               'tag'
             3286  LOAD_FAST                'multi_value_attributes'
             3288  COMPARE_OP               in
         3290_3292  POP_JUMP_IF_FALSE  3764  'to 3764'

 L. 690      3294  LOAD_FAST                'value'
             3296  LOAD_METHOD              find
             3298  LOAD_STR                 ', '
             3300  CALL_METHOD_1         1  '1 positional argument'
             3302  LOAD_CONST               0
             3304  COMPARE_OP               >=
         3306_3308  POP_JUMP_IF_FALSE  3344  'to 3344'

 L. 691      3310  LOAD_FAST                'self'
             3312  LOAD_ATTR                add_line_error
             3314  LOAD_DEREF               'line_data'
             3316  LOAD_STR                 'Found ", " in %s attribute, possible unescaped ",": "%s"'
             3318  LOAD_DEREF               'tag'
             3320  LOAD_FAST                'value'
             3322  BUILD_TUPLE_2         2 
             3324  BINARY_MODULO    
             3326  LOAD_STR                 'FORMAT'
             3328  LOAD_STR                 ''
             3330  LOAD_CONST               ('message', 'error_type', 'location')
             3332  BUILD_CONST_KEY_MAP_3     3 
             3334  LOAD_GLOBAL              logging
             3336  LOAD_ATTR                WARNING
             3338  LOAD_CONST               ('log_level',)
             3340  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3342  POP_TOP          
           3344_0  COME_FROM          3306  '3306'

 L. 693      3344  LOAD_DEREF               'tag'
             3346  LOAD_DEREF               'line_data'
             3348  LOAD_STR                 'attributes'
             3350  BINARY_SUBSCR    
             3352  COMPARE_OP               in
         3354_3356  POP_JUMP_IF_FALSE  3436  'to 3436'

 L. 694      3358  LOAD_DEREF               'tag'
             3360  LOAD_STR                 'Note'
             3362  COMPARE_OP               ==
         3364_3366  POP_JUMP_IF_FALSE  3394  'to 3394'

 L. 695      3368  LOAD_DEREF               'line_data'
             3370  LOAD_STR                 'attributes'
             3372  BINARY_SUBSCR    
             3374  LOAD_DEREF               'tag'
             3376  BINARY_SUBSCR    
             3378  LOAD_METHOD              extend
             3380  LOAD_FAST                'value'
             3382  LOAD_METHOD              split
             3384  LOAD_STR                 ','
             3386  CALL_METHOD_1         1  '1 positional argument'
             3388  CALL_METHOD_1         1  '1 positional argument'
             3390  POP_TOP          
             3392  JUMP_FORWARD       3434  'to 3434'
           3394_0  COME_FROM          3364  '3364'

 L. 697      3394  LOAD_DEREF               'line_data'
             3396  LOAD_STR                 'attributes'
             3398  BINARY_SUBSCR    
             3400  LOAD_DEREF               'tag'
             3402  BINARY_SUBSCR    
             3404  LOAD_METHOD              extend
             3406  LOAD_CLOSURE             'line_data'
             3408  LOAD_CLOSURE             'tag'
             3410  BUILD_TUPLE_2         2 
             3412  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3414  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
             3416  MAKE_FUNCTION_8          'closure'
             3418  LOAD_FAST                'value'
             3420  LOAD_METHOD              split
             3422  LOAD_STR                 ','
             3424  CALL_METHOD_1         1  '1 positional argument'
             3426  GET_ITER         
             3428  CALL_FUNCTION_1       1  '1 positional argument'
             3430  CALL_METHOD_1         1  '1 positional argument'
             3432  POP_TOP          
           3434_0  COME_FROM          3392  '3392'
             3434  JUMP_FORWARD       3454  'to 3454'
           3436_0  COME_FROM          3354  '3354'

 L. 699      3436  LOAD_FAST                'value'
             3438  LOAD_METHOD              split
             3440  LOAD_STR                 ','
             3442  CALL_METHOD_1         1  '1 positional argument'
             3444  LOAD_DEREF               'line_data'
             3446  LOAD_STR                 'attributes'
             3448  BINARY_SUBSCR    
             3450  LOAD_DEREF               'tag'
             3452  STORE_SUBSCR     
           3454_0  COME_FROM          3434  '3434'

 L. 701      3454  LOAD_DEREF               'tag'
             3456  LOAD_STR                 'Note'
             3458  COMPARE_OP               !=
         3460_3462  POP_JUMP_IF_FALSE  3604  'to 3604'
             3464  LOAD_GLOBAL              len
             3466  LOAD_DEREF               'line_data'
             3468  LOAD_STR                 'attributes'
             3470  BINARY_SUBSCR    
             3472  LOAD_DEREF               'tag'
             3474  BINARY_SUBSCR    
             3476  CALL_FUNCTION_1       1  '1 positional argument'
             3478  LOAD_GLOBAL              len
             3480  LOAD_GLOBAL              set
             3482  LOAD_DEREF               'line_data'
             3484  LOAD_STR                 'attributes'
             3486  BINARY_SUBSCR    
             3488  LOAD_DEREF               'tag'
             3490  BINARY_SUBSCR    
             3492  CALL_FUNCTION_1       1  '1 positional argument'
             3494  CALL_FUNCTION_1       1  '1 positional argument'
             3496  COMPARE_OP               !=
         3498_3500  POP_JUMP_IF_FALSE  3604  'to 3604'

 L. 702      3502  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3504  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
             3506  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3508  LOAD_GLOBAL              groupby
             3510  LOAD_GLOBAL              sorted
             3512  LOAD_DEREF               'line_data'
             3514  LOAD_STR                 'attributes'
             3516  BINARY_SUBSCR    
             3518  LOAD_DEREF               'tag'
             3520  BINARY_SUBSCR    
             3522  CALL_FUNCTION_1       1  '1 positional argument'
             3524  CALL_FUNCTION_1       1  '1 positional argument'
             3526  GET_ITER         
             3528  CALL_FUNCTION_1       1  '1 positional argument'
             3530  STORE_FAST               'count_values'

 L. 703      3532  LOAD_FAST                'self'
             3534  LOAD_METHOD              add_line_error
             3536  LOAD_DEREF               'line_data'
             3538  LOAD_STR                 '%s attribute has identical values (count, value): %s'
             3540  LOAD_DEREF               'tag'
             3542  LOAD_STR                 ', '
             3544  LOAD_METHOD              join
             3546  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3548  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
             3550  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3552  LOAD_FAST                'count_values'
             3554  GET_ITER         
             3556  CALL_FUNCTION_1       1  '1 positional argument'
             3558  CALL_METHOD_1         1  '1 positional argument'
             3560  BUILD_TUPLE_2         2 
             3562  BINARY_MODULO    
             3564  LOAD_STR                 'FORMAT'
             3566  LOAD_STR                 ''
             3568  LOAD_CONST               ('message', 'error_type', 'location')
             3570  BUILD_CONST_KEY_MAP_3     3 
             3572  CALL_METHOD_2         2  '2 positional arguments'
             3574  POP_TOP          

 L. 705      3576  LOAD_GLOBAL              list
             3578  LOAD_GLOBAL              set
             3580  LOAD_DEREF               'line_data'
             3582  LOAD_STR                 'attributes'
             3584  BINARY_SUBSCR    
             3586  LOAD_DEREF               'tag'
             3588  BINARY_SUBSCR    
             3590  CALL_FUNCTION_1       1  '1 positional argument'
             3592  CALL_FUNCTION_1       1  '1 positional argument'
             3594  LOAD_DEREF               'line_data'
             3596  LOAD_STR                 'attributes'
             3598  BINARY_SUBSCR    
             3600  LOAD_DEREF               'tag'
             3602  STORE_SUBSCR     
           3604_0  COME_FROM          3498  '3498'
           3604_1  COME_FROM          3460  '3460'

 L. 707      3604  LOAD_DEREF               'tag'
             3606  LOAD_STR                 'Parent'
             3608  COMPARE_OP               ==
         3610_3612  POP_JUMP_IF_FALSE  4690  'to 4690'

 L. 708      3614  SETUP_LOOP         3760  'to 3760'
             3616  LOAD_DEREF               'line_data'
             3618  LOAD_STR                 'attributes'
             3620  BINARY_SUBSCR    
             3622  LOAD_STR                 'Parent'
             3624  BINARY_SUBSCR    
             3626  GET_ITER         
             3628  FOR_ITER           3758  'to 3758'
             3630  STORE_FAST               'feature_id'

 L. 709      3632  SETUP_EXCEPT       3690  'to 3690'

 L. 710      3634  LOAD_DEREF               'line_data'
             3636  LOAD_STR                 'parents'
             3638  BINARY_SUBSCR    
             3640  LOAD_METHOD              append
             3642  LOAD_FAST                'features'
             3644  LOAD_FAST                'feature_id'
             3646  BINARY_SUBSCR    
             3648  CALL_METHOD_1         1  '1 positional argument'
             3650  POP_TOP          

 L. 711      3652  SETUP_LOOP         3686  'to 3686'
             3654  LOAD_FAST                'features'
             3656  LOAD_FAST                'feature_id'
             3658  BINARY_SUBSCR    
             3660  GET_ITER         
             3662  FOR_ITER           3684  'to 3684'
             3664  STORE_FAST               'ld'

 L. 713      3666  LOAD_FAST                'ld'
             3668  LOAD_STR                 'children'
             3670  BINARY_SUBSCR    
             3672  LOAD_METHOD              append
             3674  LOAD_DEREF               'line_data'
             3676  CALL_METHOD_1         1  '1 positional argument'
             3678  POP_TOP          
         3680_3682  JUMP_BACK          3662  'to 3662'
             3684  POP_BLOCK        
           3686_0  COME_FROM_LOOP     3652  '3652'
             3686  POP_BLOCK        
             3688  JUMP_BACK          3628  'to 3628'
           3690_0  COME_FROM_EXCEPT   3632  '3632'

 L. 714      3690  DUP_TOP          
             3692  LOAD_GLOBAL              KeyError
             3694  COMPARE_OP               exception-match
         3696_3698  POP_JUMP_IF_FALSE  3752  'to 3752'
             3700  POP_TOP          
             3702  POP_TOP          
             3704  POP_TOP          

 L. 715      3706  LOAD_FAST                'self'
             3708  LOAD_METHOD              add_line_error
             3710  LOAD_DEREF               'line_data'
             3712  LOAD_STR                 '%s attribute has unresolved forward reference: %s'
             3714  LOAD_DEREF               'tag'
             3716  LOAD_FAST                'feature_id'
             3718  BUILD_TUPLE_2         2 
             3720  BINARY_MODULO    
             3722  LOAD_STR                 'FORMAT'
             3724  LOAD_STR                 ''
             3726  LOAD_CONST               ('message', 'error_type', 'location')
             3728  BUILD_CONST_KEY_MAP_3     3 
             3730  CALL_METHOD_2         2  '2 positional arguments'
             3732  POP_TOP          

 L. 716      3734  LOAD_FAST                'unresolved_parents'
             3736  LOAD_FAST                'feature_id'
             3738  BINARY_SUBSCR    
             3740  LOAD_METHOD              append
             3742  LOAD_DEREF               'line_data'
             3744  CALL_METHOD_1         1  '1 positional argument'
             3746  POP_TOP          
             3748  POP_EXCEPT       
             3750  JUMP_BACK          3628  'to 3628'
           3752_0  COME_FROM          3696  '3696'
             3752  END_FINALLY      
         3754_3756  JUMP_BACK          3628  'to 3628'
             3758  POP_BLOCK        
           3760_0  COME_FROM_LOOP     3614  '3614'
         3760_3762  JUMP_BACK          3064  'to 3064'
           3764_0  COME_FROM          3290  '3290'

 L. 717      3764  LOAD_DEREF               'tag'
             3766  LOAD_STR                 'Target'
             3768  COMPARE_OP               ==
         3770_3772  POP_JUMP_IF_FALSE  4424  'to 4424'

 L. 718      3774  LOAD_FAST                'value'
             3776  LOAD_METHOD              find
             3778  LOAD_STR                 ','
             3780  CALL_METHOD_1         1  '1 positional argument'
             3782  LOAD_CONST               0
             3784  COMPARE_OP               >=
         3786_3788  POP_JUMP_IF_FALSE  3818  'to 3818'

 L. 719      3790  LOAD_FAST                'self'
             3792  LOAD_METHOD              add_line_error
             3794  LOAD_DEREF               'line_data'
             3796  LOAD_STR                 'Value of %s attribute contains unescaped ",": "%s"'
             3798  LOAD_DEREF               'tag'
             3800  LOAD_FAST                'value'
             3802  BUILD_TUPLE_2         2 
             3804  BINARY_MODULO    
             3806  LOAD_STR                 'FORMAT'
             3808  LOAD_STR                 ''
             3810  LOAD_CONST               ('message', 'error_type', 'location')
             3812  BUILD_CONST_KEY_MAP_3     3 
             3814  CALL_METHOD_2         2  '2 positional arguments'
             3816  POP_TOP          
           3818_0  COME_FROM          3786  '3786'

 L. 720      3818  LOAD_FAST                'value'
             3820  LOAD_METHOD              split
             3822  LOAD_STR                 ' '
             3824  CALL_METHOD_1         1  '1 positional argument'
             3826  STORE_FAST               'target_tokens'

 L. 721      3828  LOAD_GLOBAL              len
             3830  LOAD_FAST                'target_tokens'
             3832  CALL_FUNCTION_1       1  '1 positional argument'
             3834  LOAD_CONST               3
             3836  COMPARE_OP               <
         3838_3840  POP_JUMP_IF_TRUE   3856  'to 3856'
             3842  LOAD_GLOBAL              len
             3844  LOAD_FAST                'target_tokens'
             3846  CALL_FUNCTION_1       1  '1 positional argument'
             3848  LOAD_CONST               4
             3850  COMPARE_OP               >
         3852_3854  POP_JUMP_IF_FALSE  3892  'to 3892'
           3856_0  COME_FROM          3838  '3838'

 L. 722      3856  LOAD_FAST                'self'
             3858  LOAD_METHOD              add_line_error
             3860  LOAD_DEREF               'line_data'
             3862  LOAD_STR                 'Target attribute should have 3 or 4 values, got %d: %s'
             3864  LOAD_GLOBAL              len
             3866  LOAD_FAST                'target_tokens'
             3868  CALL_FUNCTION_1       1  '1 positional argument'
             3870  LOAD_GLOBAL              repr
             3872  LOAD_FAST                'tokens'
             3874  CALL_FUNCTION_1       1  '1 positional argument'
             3876  BUILD_TUPLE_2         2 
             3878  BINARY_MODULO    
             3880  LOAD_STR                 'FORMAT'
             3882  LOAD_STR                 ''
             3884  LOAD_CONST               ('message', 'error_type', 'location')
             3886  BUILD_CONST_KEY_MAP_3     3 
             3888  CALL_METHOD_2         2  '2 positional arguments'
             3890  POP_TOP          
           3892_0  COME_FROM          3852  '3852'

 L. 723      3892  BUILD_MAP_0           0 
             3894  LOAD_DEREF               'line_data'
             3896  LOAD_STR                 'attributes'
             3898  BINARY_SUBSCR    
             3900  LOAD_DEREF               'tag'
             3902  STORE_SUBSCR     

 L. 724  3904_3906  SETUP_EXCEPT       4398  'to 4398'

 L. 725      3908  LOAD_FAST                'target_tokens'
             3910  LOAD_CONST               0
             3912  BINARY_SUBSCR    
             3914  LOAD_DEREF               'line_data'
             3916  LOAD_STR                 'attributes'
             3918  BINARY_SUBSCR    
             3920  LOAD_DEREF               'tag'
             3922  BINARY_SUBSCR    
             3924  LOAD_STR                 'target_id'
             3926  STORE_SUBSCR     

 L. 726      3928  LOAD_CONST               True
             3930  STORE_FAST               'all_good'

 L. 727      3932  SETUP_EXCEPT       4012  'to 4012'

 L. 728      3934  LOAD_GLOBAL              int
             3936  LOAD_FAST                'target_tokens'
             3938  LOAD_CONST               1
             3940  BINARY_SUBSCR    
             3942  CALL_FUNCTION_1       1  '1 positional argument'
             3944  LOAD_DEREF               'line_data'
             3946  LOAD_STR                 'attributes'
             3948  BINARY_SUBSCR    
             3950  LOAD_DEREF               'tag'
             3952  BINARY_SUBSCR    
             3954  LOAD_STR                 'start'
             3956  STORE_SUBSCR     

 L. 729      3958  LOAD_DEREF               'line_data'
             3960  LOAD_STR                 'attributes'
             3962  BINARY_SUBSCR    
             3964  LOAD_DEREF               'tag'
             3966  BINARY_SUBSCR    
             3968  LOAD_STR                 'start'
             3970  BINARY_SUBSCR    
             3972  LOAD_CONST               1
             3974  COMPARE_OP               <
         3976_3978  POP_JUMP_IF_FALSE  4008  'to 4008'

 L. 730      3980  LOAD_FAST                'self'
             3982  LOAD_METHOD              add_line_error
             3984  LOAD_DEREF               'line_data'
             3986  LOAD_STR                 'Start value of Target attribute is not a valid 1-based integer coordinate: "%s"'
             3988  LOAD_FAST                'target_tokens'
             3990  LOAD_CONST               1
             3992  BINARY_SUBSCR    
             3994  BINARY_MODULO    
             3996  LOAD_STR                 'FORMAT'
             3998  LOAD_STR                 ''
             4000  LOAD_CONST               ('message', 'error_type', 'location')
             4002  BUILD_CONST_KEY_MAP_3     3 
             4004  CALL_METHOD_2         2  '2 positional arguments'
             4006  POP_TOP          
           4008_0  COME_FROM          3976  '3976'
             4008  POP_BLOCK        
             4010  JUMP_FORWARD       4094  'to 4094'
           4012_0  COME_FROM_EXCEPT   3932  '3932'

 L. 731      4012  DUP_TOP          
             4014  LOAD_GLOBAL              ValueError
             4016  COMPARE_OP               exception-match
         4018_4020  POP_JUMP_IF_FALSE  4092  'to 4092'
             4022  POP_TOP          
             4024  POP_TOP          
             4026  POP_TOP          

 L. 732      4028  LOAD_CONST               False
             4030  STORE_FAST               'all_good'

 L. 733      4032  LOAD_FAST                'target_tokens'
             4034  LOAD_CONST               1
             4036  BINARY_SUBSCR    
             4038  LOAD_DEREF               'line_data'
             4040  LOAD_STR                 'attributes'
             4042  BINARY_SUBSCR    
             4044  LOAD_DEREF               'tag'
             4046  BINARY_SUBSCR    
             4048  LOAD_STR                 'start'
             4050  STORE_SUBSCR     

 L. 734      4052  LOAD_FAST                'self'
             4054  LOAD_METHOD              add_line_error
             4056  LOAD_DEREF               'line_data'
             4058  LOAD_STR                 'Start value of Target attribute is not a valid integer: "%s"'
             4060  LOAD_DEREF               'line_data'
             4062  LOAD_STR                 'attributes'
             4064  BINARY_SUBSCR    
             4066  LOAD_DEREF               'tag'
             4068  BINARY_SUBSCR    
             4070  LOAD_STR                 'start'
             4072  BINARY_SUBSCR    
             4074  BINARY_MODULO    
             4076  LOAD_STR                 'FORMAT'
             4078  LOAD_STR                 ''
             4080  LOAD_CONST               ('message', 'error_type', 'location')
             4082  BUILD_CONST_KEY_MAP_3     3 
             4084  CALL_METHOD_2         2  '2 positional arguments'
             4086  POP_TOP          
             4088  POP_EXCEPT       
             4090  JUMP_FORWARD       4094  'to 4094'
           4092_0  COME_FROM          4018  '4018'
             4092  END_FINALLY      
           4094_0  COME_FROM          4090  '4090'
           4094_1  COME_FROM          4010  '4010'

 L. 735      4094  SETUP_EXCEPT       4174  'to 4174'

 L. 736      4096  LOAD_GLOBAL              int
             4098  LOAD_FAST                'target_tokens'
             4100  LOAD_CONST               2
             4102  BINARY_SUBSCR    
             4104  CALL_FUNCTION_1       1  '1 positional argument'
             4106  LOAD_DEREF               'line_data'
             4108  LOAD_STR                 'attributes'
             4110  BINARY_SUBSCR    
             4112  LOAD_DEREF               'tag'
             4114  BINARY_SUBSCR    
             4116  LOAD_STR                 'end'
             4118  STORE_SUBSCR     

 L. 737      4120  LOAD_DEREF               'line_data'
             4122  LOAD_STR                 'attributes'
             4124  BINARY_SUBSCR    
             4126  LOAD_DEREF               'tag'
             4128  BINARY_SUBSCR    
             4130  LOAD_STR                 'end'
             4132  BINARY_SUBSCR    
             4134  LOAD_CONST               1
             4136  COMPARE_OP               <
         4138_4140  POP_JUMP_IF_FALSE  4170  'to 4170'

 L. 738      4142  LOAD_FAST                'self'
             4144  LOAD_METHOD              add_line_error
             4146  LOAD_DEREF               'line_data'
             4148  LOAD_STR                 'End value of Target attribute is not a valid 1-based integer coordinate: "%s"'
             4150  LOAD_FAST                'target_tokens'
             4152  LOAD_CONST               2
             4154  BINARY_SUBSCR    
             4156  BINARY_MODULO    
             4158  LOAD_STR                 'FORMAT'
             4160  LOAD_STR                 ''
             4162  LOAD_CONST               ('message', 'error_type', 'location')
             4164  BUILD_CONST_KEY_MAP_3     3 
             4166  CALL_METHOD_2         2  '2 positional arguments'
             4168  POP_TOP          
           4170_0  COME_FROM          4138  '4138'
             4170  POP_BLOCK        
             4172  JUMP_FORWARD       4256  'to 4256'
           4174_0  COME_FROM_EXCEPT   4094  '4094'

 L. 739      4174  DUP_TOP          
             4176  LOAD_GLOBAL              ValueError
             4178  COMPARE_OP               exception-match
         4180_4182  POP_JUMP_IF_FALSE  4254  'to 4254'
             4184  POP_TOP          
             4186  POP_TOP          
             4188  POP_TOP          

 L. 740      4190  LOAD_CONST               False
             4192  STORE_FAST               'all_good'

 L. 741      4194  LOAD_FAST                'target_tokens'
             4196  LOAD_CONST               2
             4198  BINARY_SUBSCR    
             4200  LOAD_DEREF               'line_data'
             4202  LOAD_STR                 'attributes'
             4204  BINARY_SUBSCR    
             4206  LOAD_DEREF               'tag'
             4208  BINARY_SUBSCR    
             4210  LOAD_STR                 'end'
             4212  STORE_SUBSCR     

 L. 742      4214  LOAD_FAST                'self'
             4216  LOAD_METHOD              add_line_error
             4218  LOAD_DEREF               'line_data'
             4220  LOAD_STR                 'End value of Target attribute is not a valid integer: "%s"'
             4222  LOAD_DEREF               'line_data'
             4224  LOAD_STR                 'attributes'
             4226  BINARY_SUBSCR    
             4228  LOAD_DEREF               'tag'
             4230  BINARY_SUBSCR    
             4232  LOAD_STR                 'end'
             4234  BINARY_SUBSCR    
             4236  BINARY_MODULO    
             4238  LOAD_STR                 'FORMAT'
             4240  LOAD_STR                 ''
             4242  LOAD_CONST               ('message', 'error_type', 'location')
             4244  BUILD_CONST_KEY_MAP_3     3 
             4246  CALL_METHOD_2         2  '2 positional arguments'
             4248  POP_TOP          
             4250  POP_EXCEPT       
             4252  JUMP_FORWARD       4256  'to 4256'
           4254_0  COME_FROM          4180  '4180'
             4254  END_FINALLY      
           4256_0  COME_FROM          4252  '4252'
           4256_1  COME_FROM          4172  '4172'

 L. 744      4256  LOAD_FAST                'all_good'
         4258_4260  POP_JUMP_IF_FALSE  4316  'to 4316'
             4262  LOAD_DEREF               'line_data'
             4264  LOAD_STR                 'attributes'
             4266  BINARY_SUBSCR    
             4268  LOAD_DEREF               'tag'
             4270  BINARY_SUBSCR    
             4272  LOAD_STR                 'start'
             4274  BINARY_SUBSCR    
             4276  LOAD_DEREF               'line_data'
             4278  LOAD_STR                 'attributes'
             4280  BINARY_SUBSCR    
             4282  LOAD_DEREF               'tag'
             4284  BINARY_SUBSCR    
             4286  LOAD_STR                 'end'
             4288  BINARY_SUBSCR    
             4290  COMPARE_OP               >
         4292_4294  POP_JUMP_IF_FALSE  4316  'to 4316'

 L. 745      4296  LOAD_FAST                'self'
             4298  LOAD_METHOD              add_line_error
             4300  LOAD_DEREF               'line_data'
             4302  LOAD_STR                 'Start is not less than or equal to end'
             4304  LOAD_STR                 'FORMAT'
             4306  LOAD_STR                 ''
             4308  LOAD_CONST               ('message', 'error_type', 'location')
             4310  BUILD_CONST_KEY_MAP_3     3 
             4312  CALL_METHOD_2         2  '2 positional arguments'
             4314  POP_TOP          
           4316_0  COME_FROM          4292  '4292'
           4316_1  COME_FROM          4258  '4258'

 L. 746      4316  LOAD_FAST                'target_tokens'
             4318  LOAD_CONST               3
             4320  BINARY_SUBSCR    
             4322  LOAD_DEREF               'line_data'
             4324  LOAD_STR                 'attributes'
             4326  BINARY_SUBSCR    
             4328  LOAD_DEREF               'tag'
             4330  BINARY_SUBSCR    
             4332  LOAD_STR                 'strand'
             4334  STORE_SUBSCR     

 L. 747      4336  LOAD_DEREF               'line_data'
             4338  LOAD_STR                 'attributes'
             4340  BINARY_SUBSCR    
             4342  LOAD_DEREF               'tag'
             4344  BINARY_SUBSCR    
             4346  LOAD_STR                 'strand'
             4348  BINARY_SUBSCR    
             4350  LOAD_FAST                'valid_attribute_target_strand'
             4352  COMPARE_OP               not-in
         4354_4356  POP_JUMP_IF_FALSE  4394  'to 4394'

 L. 748      4358  LOAD_FAST                'self'
             4360  LOAD_METHOD              add_line_error
             4362  LOAD_DEREF               'line_data'
             4364  LOAD_STR                 'Strand value of Target attribute has illegal characters: "%s"'
             4366  LOAD_DEREF               'line_data'
             4368  LOAD_STR                 'attributes'
             4370  BINARY_SUBSCR    
             4372  LOAD_DEREF               'tag'
             4374  BINARY_SUBSCR    
             4376  LOAD_STR                 'strand'
             4378  BINARY_SUBSCR    
             4380  BINARY_MODULO    
             4382  LOAD_STR                 'FORMAT'
             4384  LOAD_STR                 ''
             4386  LOAD_CONST               ('message', 'error_type', 'location')
             4388  BUILD_CONST_KEY_MAP_3     3 
             4390  CALL_METHOD_2         2  '2 positional arguments'
             4392  POP_TOP          
           4394_0  COME_FROM          4354  '4354'
             4394  POP_BLOCK        
             4396  JUMP_BACK          3064  'to 3064'
           4398_0  COME_FROM_EXCEPT   3904  '3904'

 L. 749      4398  DUP_TOP          
             4400  LOAD_GLOBAL              IndexError
             4402  COMPARE_OP               exception-match
         4404_4406  POP_JUMP_IF_FALSE  4418  'to 4418'
             4408  POP_TOP          
             4410  POP_TOP          
             4412  POP_TOP          

 L. 750      4414  POP_EXCEPT       
             4416  JUMP_BACK          3064  'to 3064'
           4418_0  COME_FROM          4404  '4404'
             4418  END_FINALLY      
         4420_4422  JUMP_BACK          3064  'to 3064'
           4424_0  COME_FROM          3770  '3770'

 L. 752      4424  LOAD_FAST                'value'
             4426  LOAD_METHOD              find
             4428  LOAD_STR                 ','
             4430  CALL_METHOD_1         1  '1 positional argument'
             4432  LOAD_CONST               0
             4434  COMPARE_OP               >=
         4436_4438  POP_JUMP_IF_FALSE  4468  'to 4468'

 L. 753      4440  LOAD_FAST                'self'
             4442  LOAD_METHOD              add_line_error
             4444  LOAD_DEREF               'line_data'
             4446  LOAD_STR                 'Value of %s attribute contains unescaped ",": "%s"'
             4448  LOAD_DEREF               'tag'
             4450  LOAD_FAST                'value'
             4452  BUILD_TUPLE_2         2 
             4454  BINARY_MODULO    
             4456  LOAD_STR                 'FORMAT'
             4458  LOAD_STR                 ''
             4460  LOAD_CONST               ('message', 'error_type', 'location')
             4462  BUILD_CONST_KEY_MAP_3     3 
             4464  CALL_METHOD_2         2  '2 positional arguments'
             4466  POP_TOP          
           4468_0  COME_FROM          4436  '4436'

 L. 754      4468  LOAD_FAST                'value'
             4470  LOAD_DEREF               'line_data'
             4472  LOAD_STR                 'attributes'
             4474  BINARY_SUBSCR    
             4476  LOAD_DEREF               'tag'
             4478  STORE_SUBSCR     

 L. 755      4480  LOAD_DEREF               'tag'
             4482  LOAD_STR                 'Is_circular'
             4484  COMPARE_OP               ==
         4486_4488  POP_JUMP_IF_FALSE  4526  'to 4526'
             4490  LOAD_FAST                'value'
             4492  LOAD_STR                 'true'
             4494  COMPARE_OP               !=
         4496_4498  POP_JUMP_IF_FALSE  4526  'to 4526'

 L. 756      4500  LOAD_FAST                'self'
             4502  LOAD_METHOD              add_line_error
           4504_0  COME_FROM          1708  '1708'
             4504  LOAD_DEREF               'line_data'
             4506  LOAD_STR                 'Value of Is_circular attribute is not "true": "%s"'
             4508  LOAD_FAST                'value'
             4510  BINARY_MODULO    
             4512  LOAD_STR                 'FORMAT'
             4514  LOAD_STR                 ''
             4516  LOAD_CONST               ('message', 'error_type', 'location')
             4518  BUILD_CONST_KEY_MAP_3     3 
             4520  CALL_METHOD_2         2  '2 positional arguments'
             4522  POP_TOP          
             4524  JUMP_BACK          3064  'to 3064'
           4526_0  COME_FROM          4496  '4496'
           4526_1  COME_FROM          4486  '4486'

 L. 757      4526  LOAD_DEREF               'tag'
             4528  LOAD_CONST               None
             4530  LOAD_CONST               1
             4532  BUILD_SLICE_2         2 
             4534  BINARY_SUBSCR    
             4536  LOAD_METHOD              isupper
             4538  CALL_METHOD_0         0  '0 positional arguments'
         4540_4542  POP_JUMP_IF_FALSE  4580  'to 4580'
             4544  LOAD_DEREF               'tag'
             4546  LOAD_FAST                'reserved_attributes'
             4548  COMPARE_OP               not-in
         4550_4552  POP_JUMP_IF_FALSE  4580  'to 4580'

 L. 758      4554  LOAD_FAST                'self'
             4556  LOAD_METHOD              add_line_error
             4558  LOAD_DEREF               'line_data'
             4560  LOAD_STR                 'Unknown reserved (uppercase) attribute: "%s"'
             4562  LOAD_DEREF               'tag'
             4564  BINARY_MODULO    
             4566  LOAD_STR                 'FORMAT'
             4568  LOAD_STR                 ''
             4570  LOAD_CONST               ('message', 'error_type', 'location')
             4572  BUILD_CONST_KEY_MAP_3     3 
             4574  CALL_METHOD_2         2  '2 positional arguments'
             4576  POP_TOP          
             4578  JUMP_BACK          3064  'to 3064'
           4580_0  COME_FROM          4550  '4550'
           4580_1  COME_FROM          4540  '4540'

 L. 759      4580  LOAD_DEREF               'tag'
             4582  LOAD_STR                 'ID'
             4584  COMPARE_OP               ==
         4586_4588  POP_JUMP_IF_FALSE  3064  'to 3064'

 L. 761      4590  LOAD_FAST                'value'
             4592  LOAD_FAST                'features'
             4594  COMPARE_OP               in
         4596_4598  POP_JUMP_IF_FALSE  4676  'to 4676'
             4600  LOAD_FAST                'lines'
             4602  LOAD_CONST               -1
             4604  BINARY_SUBSCR    
             4606  LOAD_STR                 'attributes'
             4608  BINARY_SUBSCR    
             4610  LOAD_DEREF               'tag'
             4612  BINARY_SUBSCR    
             4614  LOAD_FAST                'value'
             4616  COMPARE_OP               !=
         4618_4620  POP_JUMP_IF_FALSE  4676  'to 4676'

 L. 762      4622  LOAD_FAST                'self'
             4624  LOAD_ATTR                add_line_error
             4626  LOAD_DEREF               'line_data'
             4628  LOAD_STR                 'Duplicate ID: "%s" in non-adjacent lines: %s'
             4630  LOAD_FAST                'value'
             4632  LOAD_STR                 ','
             4634  LOAD_METHOD              join
             4636  LOAD_LISTCOMP            '<code_object <listcomp>>'
             4638  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
             4640  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             4642  LOAD_FAST                'features'
             4644  LOAD_FAST                'value'
             4646  BINARY_SUBSCR    
             4648  GET_ITER         
             4650  CALL_FUNCTION_1       1  '1 positional argument'
             4652  CALL_METHOD_1         1  '1 positional argument'
             4654  BUILD_TUPLE_2         2 
             4656  BINARY_MODULO    
             4658  LOAD_STR                 'FORMAT'
             4660  LOAD_STR                 ''
             4662  LOAD_CONST               ('message', 'error_type', 'location')
             4664  BUILD_CONST_KEY_MAP_3     3 
             4666  LOAD_GLOBAL              logging
             4668  LOAD_ATTR                WARNING
             4670  LOAD_CONST               ('log_level',)
             4672  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
           4674_0  COME_FROM          1878  '1878'
             4674  POP_TOP          
           4676_0  COME_FROM          4618  '4618'
           4676_1  COME_FROM          4596  '4596'

 L. 763      4676  LOAD_FAST                'features'
             4678  LOAD_FAST                'value'
             4680  BINARY_SUBSCR    
             4682  LOAD_METHOD              append
             4684  LOAD_DEREF               'line_data'
             4686  CALL_METHOD_1         1  '1 positional argument'
             4688  POP_TOP          
           4690_0  COME_FROM          3610  '3610'
         4690_4692  JUMP_BACK          3064  'to 3064'
             4694  POP_BLOCK        
           4696_0  COME_FROM_LOOP     3056  '3056'
           4696_1  COME_FROM          3052  '3052'
             4696  POP_BLOCK        
             4698  JUMP_FORWARD       4722  'to 4722'
           4700_0  COME_FROM_EXCEPT   2102  '2102'

 L. 764      4700  DUP_TOP          
             4702  LOAD_GLOBAL              IndexError
             4704  COMPARE_OP               exception-match
         4706_4708  POP_JUMP_IF_FALSE  4720  'to 4720'
             4710  POP_TOP          
             4712  POP_TOP          
             4714  POP_TOP          

 L. 765      4716  POP_EXCEPT       
             4718  JUMP_FORWARD       4722  'to 4722'
           4720_0  COME_FROM          4706  '4706'
             4720  END_FINALLY      
           4722_0  COME_FROM          4718  '4718'
           4722_1  COME_FROM          4698  '4698'
           4722_2  COME_FROM          1948  '1948'
           4722_3  COME_FROM          1924  '1924'

 L. 766      4722  LOAD_FAST                'current_line_num'
             4724  LOAD_CONST               1
             4726  INPLACE_ADD      
             4728  STORE_FAST               'current_line_num'

 L. 767      4730  LOAD_FAST                'lines'
             4732  LOAD_METHOD              append
             4734  LOAD_DEREF               'line_data'
             4736  CALL_METHOD_1         1  '1 positional argument'
             4738  POP_TOP          
             4740  JUMP_BACK           124  'to 124'
             4742  POP_BLOCK        
           4744_0  COME_FROM_LOOP      116  '116'

 L. 769      4744  LOAD_GLOBAL              isinstance
             4746  LOAD_FAST                'gff_file'
             4748  LOAD_GLOBAL              str
             4750  CALL_FUNCTION_2       2  '2 positional arguments'
         4752_4754  POP_JUMP_IF_FALSE  4764  'to 4764'

 L. 770      4756  LOAD_FAST                'gff_fp'
             4758  LOAD_METHOD              close
             4760  CALL_METHOD_0         0  '0 positional arguments'
             4762  POP_TOP          
           4764_0  COME_FROM          4752  '4752'

 L. 773      4764  SETUP_LOOP         4858  'to 4858'
             4766  LOAD_FAST                'unresolved_parents'
             4768  GET_ITER         
           4770_0  COME_FROM          4780  '4780'
             4770  FOR_ITER           4856  'to 4856'
             4772  STORE_FAST               'feature_id'

 L. 774      4774  LOAD_FAST                'feature_id'
             4776  LOAD_FAST                'features'
             4778  COMPARE_OP               in
         4780_4782  POP_JUMP_IF_FALSE  4770  'to 4770'

 L. 775      4784  SETUP_LOOP         4852  'to 4852'
             4786  LOAD_FAST                'unresolved_parents'
             4788  LOAD_FAST                'feature_id'
             4790  BINARY_SUBSCR    
             4792  GET_ITER         
             4794  FOR_ITER           4850  'to 4850'
             4796  STORE_FAST               'line'

 L. 776      4798  LOAD_FAST                'self'
             4800  LOAD_METHOD              add_line_error
             4802  LOAD_FAST                'line'
             4804  LOAD_STR                 'Unresolved forward reference: "%s", found defined in lines: %s'
             4806  LOAD_FAST                'feature_id'
             4808  LOAD_STR                 ','
             4810  LOAD_METHOD              join
             4812  LOAD_LISTCOMP            '<code_object <listcomp>>'
             4814  LOAD_STR                 'Gff3.parse.<locals>.<listcomp>'
             4816  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             4818  LOAD_FAST                'features'
             4820  LOAD_FAST                'feature_id'
             4822  BINARY_SUBSCR    
             4824  GET_ITER         
             4826  CALL_FUNCTION_1       1  '1 positional argument'
             4828  CALL_METHOD_1         1  '1 positional argument'
             4830  BUILD_TUPLE_2         2 
             4832  BINARY_MODULO    
             4834  LOAD_STR                 'FORMAT'
             4836  LOAD_STR                 ''
             4838  LOAD_CONST               ('message', 'error_type', 'location')
             4840  BUILD_CONST_KEY_MAP_3     3 
             4842  CALL_METHOD_2         2  '2 positional arguments'
             4844  POP_TOP          
         4846_4848  JUMP_BACK          4794  'to 4794'
             4850  POP_BLOCK        
           4852_0  COME_FROM_LOOP     4784  '4784'
         4852_4854  JUMP_BACK          4770  'to 4770'
             4856  POP_BLOCK        
           4858_0  COME_FROM_LOOP     4764  '4764'

 L. 778      4858  LOAD_FAST                'lines'
             4860  LOAD_FAST                'self'
             4862  STORE_ATTR               lines

 L. 779      4864  LOAD_FAST                'features'
             4866  LOAD_FAST                'self'
             4868  STORE_ATTR               features

 L. 780      4870  LOAD_CONST               1
             4872  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DEREF' instruction at offset 4504

    def descendants(self, line_data):
        """
        BFS graph algorithm
        :param line_data: line_data(dict) with line_data['line_index'] or line_index(int)
        :return: list of line_data(dict)
        """
        try:
            start = line_data['line_index']
        except TypeError:
            start = self.lines[line_data]['line_index']

        visited_set, visited_list, queue = set(), [], [start]
        while queue:
            node = queue.pop(0)
            if node not in visited_set:
                visited_set.add(node)
                visited_list.append(self.lines[node])
                queue.extend([ld['line_index'] for ld in self.lines[node]['children'] if ld['line_index'] not in visited_set])

        return visited_list[1:]

    def ancestors(self, line_data):
        """
        BFS graph algorithm

        :param line_data: line_data(dict) with line_data['line_index'] or line_index(int)
        :return: list of line_data(dict)
        """
        try:
            start = line_data['line_index']
        except TypeError:
            start = self.lines[line_data]['line_index']

        visited_set, visited_list, queue = set(), [], [start]
        while queue:
            node = queue.pop(0)
            if node not in visited_set:
                visited_set.add(node)
                visited_list.append(self.lines[node])
                queue.extend([ld['line_index'] for f in self.lines[node]['parents'] if ld['line_index'] not in visited_set for ld in f])

        return visited_list[1:]

    def adopt(self, old_parent, new_parent):
        """
        Transfer children from old_parent to new_parent

        :param old_parent: feature_id(str) or line_index(int) or line_data(dict) or feature
        :param new_parent: feature_id(str) or line_index(int) or line_data(dict)
        :return: List of children transferred
        """
        try:
            old_id = old_parent['attributes']['ID']
        except TypeError:
            try:
                old_id = self.lines[old_parent]['attributes']['ID']
            except TypeError:
                old_id = old_parent

        old_feature = self.features[old_id]
        old_indexes = [ld['line_index'] for ld in old_feature]
        try:
            new_id = new_parent['attributes']['ID']
        except TypeError:
            try:
                new_id = self.lines[new_parent]['attributes']['ID']
            except TypeError:
                new_id = new_parent

        new_feature = self.features[new_id]
        new_indexes = [ld['line_index'] for ld in new_feature]
        children = old_feature[0]['children']
        new_parent_children_set = set([ld['line_index'] for ld in new_feature[0]['children']])
        for child in children:
            if child['line_index'] not in new_parent_children_set:
                new_parent_children_set.add(child['line_index'])
                for new_ld in new_feature:
                    new_ld['children'].append(child)

                child['parents'].append(new_feature)
                child['attributes']['Parent'].append(new_id)
            child['parents'] = [f for f in child['parents'] if f[0]['attributes']['ID'] != old_id]
            child['attributes']['Parent'] = [d for d in child['attributes']['Parent'] if d != old_id]

        for old_ld in old_feature:
            old_ld['children'] = []

        return children

    def adopted(self, old_child, new_child):
        """
        Transfer parents from old_child to new_child

        :param old_child: line_data(dict) with line_data['line_index'] or line_index(int)
        :param new_child: line_data(dict) with line_data['line_index'] or line_index(int)
        :return: List of parents transferred
        """
        pass

    def overlap(self, line_data_a, line_data_b):
        return line_data_a['seqid'] == line_data_b['seqid'] and (line_data_a['start'] <= line_data_b['start'] and line_data_b['start'] <= line_data_a['end'] or line_data_a['start'] <= line_data_b['end'] and line_data_b['end'] <= line_data_a['end'] or line_data_b['start'] <= line_data_a['start'] and line_data_a['end'] <= line_data_b['end'])

    def remove(self, line_data, root_type=None):
        """
        Marks line_data and all of its associated feature's 'line_status' as 'removed', does not actually remove the line_data from the data structure.
        The write function checks the 'line_status' when writing the gff file.
        Find the root parent of line_data of type root_type, remove all of its descendants.
        If the root parent has a parent with no children after the remove, remove the root parent's parent recursively.

        :param line_data:
        :param root_type:
        :return:
        """
        roots = [ld['parents'] or ld for ld in self.ancestors(line_data) if root_type if not (ld['line_type'] == root_type or root_type)] or [line_data]
        for root in roots:
            root['line_status'] = 'removed'
            root_descendants = self.descendants(root)
            for root_descendant in root_descendants:
                root_descendant['line_status'] = 'removed'

            root_ancestors = self.ancestors(root)
            for root_ancestor in root_ancestors:
                if len([ld for ld in root_ancestor['children'] if ld['line_status'] != 'removed']) == 0:
                    root_ancestor['line_status'] = 'removed'

    def fix(self):
        pass

    def write(self, gff_file, embed_fasta=None, fasta_char_limit=None):
        gff_fp = gff_file
        if isinstance(gff_file, str):
            gff_fp = open(gff_file, 'wb')
        wrote_sequence_region = set()
        sequence_regions = {}
        if self.fasta_external:
            for seqid in self.fasta_external:
                sequence_regions[seqid] = (
                 1, len(self.fasta_external[seqid]['seq']))

        else:
            if self.fasta_embedded:
                for seqid in self.fasta_embedded:
                    sequence_regions[seqid] = (
                     1, len(self.fasta_embedded[seqid]['seq']))

            else:
                wrote_lines = set()
                field_keys = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase']
                reserved_attributes = ['ID', 'Name', 'Alias', 'Parent', 'Target', 'Gap', 'Derives_from', 'Note', 'Dbxref', 'Ontology_term', 'Is_circular']
                attributes_sort_map = defaultdict(int, zip(reserved_attributes, range(len(reserved_attributes), 0, -1)))

                def write_feature(line_data):
                    if line_data['line_status'] == 'removed':
                        return
                    field_list = [str(line_data[k]) for k in field_keys]
                    attribute_list = []
                    for k, v in sorted((line_data['attributes'].items()), key=(lambda x: attributes_sort_map[x[0]]), reverse=True):
                        if isinstance(v, list):
                            v = ','.join(v)
                        attribute_list.append('%s=%s' % (str(k), str(v)))

                    field_list.append(';'.join(attribute_list))
                    gff_fp.write('\t'.join(field_list) + '\n')
                    wrote_lines.add(line_data['line_index'])

                ignore_directives = [
                 '##sequence-region', '###', '##FASTA']
                directives_lines = [line_data for line_data in self.lines if line_data['line_type'] == 'directive' if line_data['directive'] not in ignore_directives]
                for directives_line in directives_lines:
                    gff_fp.write(directives_line['line_raw'])

                root_lines = [line_data for line_data in self.lines if line_data['line_type'] == 'feature' if not line_data['parents']]
                for root_line in root_lines:
                    lines_wrote = len(wrote_lines)
                    if root_line['line_index'] in wrote_lines:
                        continue
                    if root_line['seqid'] not in wrote_sequence_region:
                        if root_line['seqid'] in sequence_regions:
                            gff_fp.write('##sequence-region %s %d %d\n' % (root_line['seqid'], sequence_regions[root_line['seqid']][0], sequence_regions[root_line['seqid']][1]))
                        wrote_sequence_region.add(root_line['seqid'])
                    try:
                        root_feature = self.features[root_line['attributes']['ID']]
                    except KeyError:
                        root_feature = [
                         root_line]

                    for line_data in root_feature:
                        write_feature(line_data)

                    descendants = self.descendants(root_line)
                    for descendant in descendants:
                        if descendant['line_index'] in wrote_lines:
                            continue
                        write_feature(descendant)

                    if lines_wrote != len(wrote_lines):
                        gff_fp.write('###\n')

                fasta = embed_fasta or self.fasta_external or self.fasta_embedded
                if fasta:
                    if embed_fasta != False:
                        gff_fp.write('##FASTA\n')
                        fasta_dict_to_file(fasta, gff_fp, line_char_limit=fasta_char_limit)
                if isinstance(gff_file, str):
                    gff_fp.close()

    def sequence(self, line_data, child_type=None, reference=None):
        """
        Get the sequence of line_data, according to the columns 'seqid', 'start', 'end', 'strand'.
        Requires fasta reference.
        When used on 'mRNA' type line_data, child_type can be used to specify which kind of sequence to return:
        * child_type=None:  pre-mRNA, returns the sequence of line_data from start to end, reverse complement according to strand. (default)
        * child_type='exon':  mature mRNA, concatenates the sequences of children type 'exon'.
        * child_type='CDS':  coding sequence, concatenates the sequences of children type 'CDS'. Use the helper
                             function translate(seq) on the returned value to obtain the protein sequence.

        :param line_data: line_data(dict) with line_data['line_index'] or line_index(int)
        :param child_type: None or feature type(string)
        :param reference: If None, will use self.fasta_external or self.fasta_embedded(dict)
        :return: sequence(string)
        """
        reference = reference or self.fasta_external or self.fasta_embedded
        if not reference:
            raise Exception('External or embedded fasta reference needed')
        try:
            line_index = line_data['line_index']
        except TypeError:
            line_index = self.lines[line_data]['line_index']

        ld = self.lines[line_index]
        if ld['type'] != 'feature':
            return
        seq = reference[ld['seqid']][ld['start'] - 1:ld['end']]
        if ld['strand'] == '-':
            seq = complement(seq[::-1])
        return seq

    def type_tree(self):

        class node(object):

            def __init__(self, value, children=None):
                self.value = value or ''
                self.children = children or set()

            def __repr__(self, level=0):
                ret = '\t' * level + repr(self.value) + '\n'
                for child in sorted((list(self.children)), key=(lambda x: x.value)):
                    ret += child.__repr__(level + 1)

                return ret

        root_set = set()
        node_dict = {}
        feature_line_list = [line_data for line_data in self.lines if line_data['line_type'] == 'feature']
        for line_data in feature_line_list:
            if len(line_data['children']) > 0:
                parent_type = line_data['type']
                if parent_type not in node_dict:
                    node_dict[parent_type] = node(parent_type)
                if len(line_data['parents']) == 0:
                    root_set.add(node_dict[parent_type])
                for child_ld in line_data['children']:
                    child_type = child_ld['type']
                    if child_type not in node_dict:
                        node_dict[child_type] = node(child_type)
                    if parent_type == child_type and child_type == 'mRNA':
                        print(line_data['line_index'], child_ld['line_index'])
                    else:
                        node_dict[parent_type].children.add(node_dict[child_type])

        return sorted((list(root_set)), key=(lambda x: x.value))


try:
    from collections import OrderedDict
except ImportError:
    try:
        from thread import get_ident as _get_ident
    except ImportError:
        from dummy_thread import get_ident as _get_ident

    try:
        from _abcoll import KeysView, ValuesView, ItemsView
    except ImportError:
        pass

    class OrderedDict(dict):
        __doc__ = 'Dictionary that remembers insertion order'

        def __init__(self, *args, **kwds):
            """Initialize an ordered dictionary.  Signature is the same as for
            regular dictionaries, but keyword arguments are not recommended
            because their insertion order is arbitrary.

            """
            if len(args) > 1:
                raise TypeError('expected at most 1 arguments, got %d' % len(args))
            try:
                self._OrderedDict__root
            except AttributeError:
                self._OrderedDict__root = root = []
                root[:] = [
                 root, root, None]
                self._OrderedDict__map = {}

            (self._OrderedDict__update)(*args, **kwds)

        def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
            """od.__setitem__(i, y) <==> od[i]=y"""
            if key not in self:
                root = self._OrderedDict__root
                last = root[0]
                last[1] = root[0] = self._OrderedDict__map[key] = [last, root, key]
            dict_setitem(self, key, value)

        def __delitem__(self, key, dict_delitem=dict.__delitem__):
            """od.__delitem__(y) <==> del od[y]"""
            dict_delitem(self, key)
            link_prev, link_next, key = self._OrderedDict__map.pop(key)
            link_prev[1] = link_next
            link_next[0] = link_prev

        def __iter__(self):
            """od.__iter__() <==> iter(od)"""
            root = self._OrderedDict__root
            curr = root[1]
            while curr is not root:
                yield curr[2]
                curr = curr[1]

        def __reversed__(self):
            """od.__reversed__() <==> reversed(od)"""
            root = self._OrderedDict__root
            curr = root[0]
            while curr is not root:
                yield curr[2]
                curr = curr[0]

        def clear(self):
            """od.clear() -> None.  Remove all items from od."""
            try:
                for node in self._OrderedDict__map.itervalues():
                    del node[:]

                root = self._OrderedDict__root
                root[:] = [root, root, None]
                self._OrderedDict__map.clear()
            except AttributeError:
                pass

            dict.clear(self)

        def popitem(self, last=True):
            """od.popitem() -> (k, v), return and remove a (key, value) pair.
            Pairs are returned in LIFO order if last is true or FIFO order if false.

            """
            if not self:
                raise KeyError('dictionary is empty')
            else:
                root = self._OrderedDict__root
                if last:
                    link = root[0]
                    link_prev = link[0]
                    link_prev[1] = root
                    root[0] = link_prev
                else:
                    link = root[1]
                link_next = link[1]
                root[1] = link_next
                link_next[0] = root
            key = link[2]
            del self._OrderedDict__map[key]
            value = dict.pop(self, key)
            return (key, value)

        def keys(self):
            """od.keys() -> list of keys in od"""
            return list(self)

        def values(self):
            """od.values() -> list of values in od"""
            return [self[key] for key in self]

        def items(self):
            """od.items() -> list of (key, value) pairs in od"""
            return [(key, self[key]) for key in self]

        def iterkeys(self):
            """od.iterkeys() -> an iterator over the keys in od"""
            return iter(self)

        def itervalues(self):
            """od.itervalues -> an iterator over the values in od"""
            for k in self:
                yield self[k]

        def iteritems(self):
            """od.iteritems -> an iterator over the (key, value) items in od"""
            for k in self:
                yield (k, self[k])

        def update(*args, **kwds):
            """od.update(E, **F) -> None.  Update od from dict/iterable E and F.

            If E is a dict instance, does:           for k in E: od[k] = E[k]
            If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
            Or if E is an iterable of items, does:   for k, v in E: od[k] = v
            In either case, this is followed by:     for k, v in F.items(): od[k] = v

            """
            if len(args) > 2:
                raise TypeError('update() takes at most 2 positional arguments (%d given)' % (
                 len(args),))
            else:
                if not args:
                    raise TypeError('update() takes at least 1 argument (0 given)')
            self = args[0]
            other = ()
            if len(args) == 2:
                other = args[1]
            if isinstance(other, dict):
                for key in other:
                    self[key] = other[key]

            else:
                if hasattr(other, 'keys'):
                    for key in other.keys():
                        self[key] = other[key]

                else:
                    for key, value in other:
                        self[key] = value

            for key, value in kwds.items():
                self[key] = value

        _OrderedDict__update = update
        _OrderedDict__marker = object()

        def pop(self, key, default=_OrderedDict__marker):
            """od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
            If key is not found, d is returned if given, otherwise KeyError is raised.

            """
            if key in self:
                result = self[key]
                del self[key]
                return result
            if default is self._OrderedDict__marker:
                raise KeyError(key)
            return default

        def setdefault(self, key, default=None):
            """od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od"""
            if key in self:
                return self[key]
            self[key] = default
            return default

        def __repr__(self, _repr_running={}):
            """od.__repr__() <==> repr(od)"""
            call_key = (
             id(self), _get_ident())
            if call_key in _repr_running:
                return '...'
            _repr_running[call_key] = 1
            try:
                if not self:
                    return '%s()' % (self.__class__.__name__,)
                return '%s(%r)' % (self.__class__.__name__, self.items())
            finally:
                del _repr_running[call_key]

        def __reduce__(self):
            """Return state information for pickling"""
            items = [[k, self[k]] for k in self]
            inst_dict = vars(self).copy()
            for k in vars(OrderedDict()):
                inst_dict.pop(k, None)

            if inst_dict:
                return (
                 self.__class__, (items,), inst_dict)
            return (
             self.__class__, (items,))

        def copy(self):
            """od.copy() -> a shallow copy of od"""
            return self.__class__(self)

        @classmethod
        def fromkeys(cls, iterable, value=None):
            """OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
            and values equal to v (which defaults to None).

            """
            d = cls()
            for key in iterable:
                d[key] = value

            return d

        def __eq__(self, other):
            """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
            while comparison to a regular mapping is order-insensitive.

            """
            if isinstance(other, OrderedDict):
                return len(self) == len(other) and self.items() == other.items()
            return dict.__eq__(self, other)

        def __ne__(self, other):
            return not self == other

        def viewkeys(self):
            """od.viewkeys() -> a set-like object providing a view on od's keys"""
            return KeysView(self)

        def viewvalues(self):
            """od.viewvalues() -> an object providing a view on od's values"""
            return ValuesView(self)

        def viewitems(self):
            """od.viewitems() -> a set-like object providing a view on od's items"""
            return ItemsView(self)