# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/fasta.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 1377 bytes


class FastaParser(object):
    __doc__ = ' A class for parsing and handling fasta files. '

    def entries(self, fasta_fh):
        """Go line by line though the file and return fasta entries. """
        current_header = ''
        current_sequence = ''
        virgin = True
        for line in fasta_fh:
            if line[0] == '>' and virgin is False:
                yield (
                 current_header, current_sequence)
                current_header = line[1:-1]
                current_sequence = ''
            elif line[0] == '>' and virgin is True:
                virgin = False
                current_header = line[1:-1]
            else:
                current_sequence += line[:-1]

        if not (current_header == '' and current_sequence == ''):
            yield (
             current_header, current_sequence)

    def single_entry_file_header(self, fasta_fh):
        first_line = fasta_fh.readline()
        header = first_line[1:-1]
        fasta_fh.seek(0)
        return header

    def header_id(self, header):
        """Return only the id of a fasta header

        Everything after the first white space is discard.
        """
        return header.split()[0]