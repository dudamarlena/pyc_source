# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seqplot/seqplot_helpers.py
# Compiled at: 2014-10-06 05:10:23
import sys

class Alignment(object):
    """ Store alignment information """

    def __init__(self, name=None, fasta=None):
        self.name = name
        self.fasta = fasta
        self.members = []
        self.attach_sequences()

    def __repr__(self):
        ids = self.members
        return ('Alignment:{},{}').format(self.name, ids)

    def __len__(self):
        try:
            return len(self.members[0].sequence)
        except TypeError as err:
            sys.stderr.write(err)
            sys.stderr.write('attach_sequences first')
            return 0

    def attach_sequences(self):
        """Read fasta file, create Sequence objects and attach them to self.members"""
        print (
         'FASTA:', self.fasta)
        for seq in FastaParser.read_fasta(self.fasta):
            new_seq = Sequence(name=seq[0], sequence=seq[1])
            self.members.append(new_seq)


class Sequence(object):

    def __init__(self, name='', sequence=None, is_foreground=False):
        self.name = name
        self.sequence = sequence

    def __repr__(self):
        return ('Sequence: {}').format(self.name)


class FastaParser(object):

    @staticmethod
    def read_fasta(fasta, delim=None, as_id=0):
        """read from fasta fasta file 'fasta'
        and split sequence id at 'delim' (if set)

        example:

        >idpart1|idpart2

        ATGTGA

        and 'delim="|"' returns ("idpart1", "ATGTGA")
        """
        name = ''
        fasta = open(fasta, 'r')
        while True:
            line = name or fasta.readline()
            if not line:
                break
            seq = []
            while True:
                name = fasta.readline()
                name = name.rstrip()
                if not name or name.startswith('>'):
                    break
                else:
                    seq.append(name)

            joined_seq = ('').join(seq)
            line = line[1:]
            if delim:
                line = line.split(delim)[as_id]
            yield (
             line.rstrip(), joined_seq.rstrip())

        fasta.close()


class Colorizer:
    """ Color residues """

    @staticmethod
    def cinema(char):
        if char in ('H', 'K', 'R'):
            return (0, 0, 200)
        if char in ('D', 'E'):
            return (200, 0, 0)
        if char in ('S', 'T', 'N', 'Q'):
            return (0, 200, 0)
        if char in ('A', 'V', 'L', 'I', 'M'):
            return (255, 255, 255)
        if char in ('F', 'W', 'Y'):
            return (255, 0, 255)
        if char in ('P', 'G'):
            return (165, 42, 42)
        if char in ('C', ):
            return (255, 255, 0)
        if char in ('B', 'Z', 'X'):
            return (190, 190, 190)

    @staticmethod
    def lesk(char):
        if char in ('G', 'A', 'S', 'T'):
            return (255, 165, 0)
        else:
            if char in ('C', 'V', 'I', 'L', 'P', 'F', 'Y', 'M', 'W'):
                return (0, 255, 0)
            if char in ('N', 'Q', 'H', 'M'):
                return (255, 0, 255)
            if char in ('D', 'E'):
                return (255, 0, 0)
            if char in ('K', 'R'):
                return (0, 0, 255)
            return (23, 23, 23)

    @staticmethod
    def clustal(char):
        if char in ('G', 'P', 'S', 'T'):
            return (255, 165, 0)
        else:
            if char in ('H', 'K', 'R'):
                return (255, 0, 0)
            if char in ('F', 'W', 'Y', 'B'):
                return (0, 0, 255)
            if char in ('I', 'L', 'M', 'V'):
                return (0, 255, 0)
            return (23, 23, 23)

    @staticmethod
    def shapely(char):
        pass

    @staticmethod
    def maeditor(char):
        if char in ('A', 'G'):
            return (32, 178, 170)
        else:
            if char in ('C', ):
                return (0, 255, 0)
            if char in ('D', 'E', 'N', 'Q'):
                return (0, 100, 0)
            if char in ('I', 'L', 'M', 'V'):
                return (0, 0, 255)
            if char in ('F', 'W', 'Y'):
                return (218, 112, 214)
            if char in ('H', ):
                return (0, 0, 100)
            if char in ('K', 'R'):
                return (255, 165, 0)
            if char in ('P', ):
                return (255, 192, 203)
            if char in ('S', 'T'):
                return (255, 0, 0)
            if char in ('-', ):
                return (242, 242, 242)
            if char in ('X', ):
                return (23, 23, 23)
            return (0, 0, 0)

    @staticmethod
    def aacid(char):
        if char in ('A', ):
            return (235, 0, 124)
        if char in ('R', ):
            return (255, 13, 0)
        if char in ('N', ):
            return (149, 0, 219)
        if char in ('D', ):
            return (159, 247, 0)
        if char in ('C', ):
            return (50, 238, 0)
        if char in ('Q', ):
            return (0, 216, 180)
        if char in ('E', ):
            return (180, 249, 0)
        if char in ('G', ):
            return (251, 0, 29)
        if char in ('H', ):
            return (255, 44, 0)
        if char in ('I', ):
            return (255, 133, 0)
        if char in ('L', ):
            return (239, 0, 101)
        if char in ('K', ):
            return (0, 226, 84)
        if char in ('M', ):
            return (0, 190, 114)
        if char in ('F', ):
            return (0, 100, 183)
        if char in ('P', ):
            return (101, 232, 0)
        if char in ('S', ):
            return (255, 76, 0)
        if char in ('T', ):
            return (107, 23, 153)
        if char in ('W', ):
            return (156, 16, 144)
        if char in ('Y', ):
            return (183, 221, 23)
        if char in ('V', ):
            return (230, 230, 24)
        if char in ('-', ):
            return (255, 255, 255)
        if char in ('X', ):
            return (180, 180, 180)

    @staticmethod
    def dna_color(char):
        if char in ('A', ):
            return (255, 0, 0)
        if char in ('a', ):
            return (127, 0, 0)
        if char in ('T', ):
            return (0, 255, 0)
        if char in ('t', ):
            return (0, 175, 0)
        if char in ('G', ):
            return (0, 0, 255)
        if char in ('g', ):
            return (0, 0, 175)
        if char in ('C', ):
            return (255, 255, 0)
        if char in ('c', ):
            return (175, 175, 0)
        if char in ('-', ):
            return (180, 180, 180)
        sys.stderr.write(('Found character: {}\n').format(char))
        raise WrongInputException

    @staticmethod
    def color(char, colorscheme=None):
        colorfunc = Colorizer.maeditor
        if colorscheme:
            if colorscheme == 'cinema':
                colorfunc = Colorizer.cinema
            elif colorscheme == 'lesk':
                colorfunc = Colorizer.lesk
            elif colorscheme == 'clustal':
                colorfunc = Colorizer.clustal
            elif colorscheme == 'shapely':
                colorfunc = Colorizer.shapely
            elif colorscheme == 'dna':
                colorfunc = Colorizer.dna_color
            elif colorscheme == 'aacid':
                colorfunc = Colorizer.aacid
            elif colorscheme == 'maeditor' or colorscheme == 'default':
                colorfunc = Colorizer.maeditor
        return colorfunc(char)


class WrongInputException(Exception):
    pass