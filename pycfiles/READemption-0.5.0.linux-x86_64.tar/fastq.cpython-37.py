# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/fastq.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 1720 bytes


class FastqParser(object):
    __doc__ = 'A class for parsing and handling fastQ files.\n\n    Currently only taking care of the sequences not the quality\n    strings. Only four line entries can be handled\n    '

    def entries(self, fastq_fh):
        """Go line by line though the file and return fastq entries. """
        current_header = ''
        current_sequence = ''
        virgin = True
        entry_line_counter = 0
        for line in fastq_fh:
            if line[0] == '@':
                if virgin is False:
                    if entry_line_counter == 4:
                        entry_line_counter = 1
                        yield (current_header, current_sequence)
                        current_header = line[1:-1]
                        current_sequence = ''
                elif line[0] == '@':
                    if virgin is True:
                        virgin = False
                        current_header = line[1:-1]
                        entry_line_counter = 1
                entry_line_counter += 1
                if entry_line_counter == 2:
                    current_sequence = line[:-1]

        if not (current_header == '' and current_sequence == ''):
            yield (
             current_header, current_sequence)

    def single_entry_file_header(self, fastq_fh):
        first_line = fastq_fh.readline()
        header = first_line[1:-1]
        fastq_fh.seek(0)
        return header

    def header_id(self, header):
        """Return only the id of a fastq header

        Everything after the first white space is discard.
        """
        return header.split()[0]