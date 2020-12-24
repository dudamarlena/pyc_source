# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/MLF_file.py
# Compiled at: 2011-05-13 03:16:51


class BadFormatError(RuntimeError):

    def __init__(self, *s):
        RuntimeError.__init__(self, *s)


class NotInMLFFile(KeyError):

    def __init__(self, *s):
        KeyError.__init__(self, *s)


class block_MLF_file(object):
    """This class reads in and stores a MLF file.  It does not interpret the interior data,
        but rather just breaks it up into blocks, each corresponding to an utterance.
        """
    Quantum = 1e-07

    def __init__(self, fname, preprocessor=None):
        """Read in a MLF file and store the information in C{self.block}.
                @param fname: Filename to read
                @type fname: str
                @param preprocessor: A function to project the name of each block onto
                        something that you want to use as an index of blocks.
                        Typically, this function cleans up the names, removing asterisks
                        and such.
                @type preprocessor: function str -> str
                """
        if preprocessor is None:
            preprocessor = lambda x: x
        self.block = {}
        self.fname = fname
        self.blockname = {}
        block = []
        fd = open(fname, 'r')
        if fd.readline() != '#!MLF!#\n':
            raise BadFormatError
        inblock = False
        fpattern = None
        blockname = None
        for line in fd.readlines():
            line = line.rstrip()
            if not (inblock or line[0] == '"' and line[(-1)] == '"'):
                raise AssertionError
                blockname = line[1:-1]
                fpattern = preprocessor(blockname)
                inblock = True
            elif inblock and line == '.':
                inblock = False
                self.block[fpattern] = block
                self.blockname[fpattern] = blockname
                block = []
            else:
                block.append(line)

        return

    def get(self, key):
        """Get a block of text from a MLF file.
                """
        try:
            return self.block[key]
        except KeyError:
            raise NotInMLFFile(key, self.fname)

    def get3(self, key, n=3):
        """Get a block of time-aligned labels from a MLF file and interpret it.
                @return: C{(start, end, label, ...)} tuples, with C{start} and C{end} in seconds,
                        C{label} is a string indicating a phoneme or word or whatever.
                        If there is more information on a line, it will be passed along in the tuple.
                @rtype: list(tuple(start, end, label, ...), ...)
                """
        labels = []
        for i, line in enumerate(self.get(key)):
            a = line.split()
            if len(a) >= 3:
                try:
                    a[0] = float(a[0]) * self.Quantum
                    a[1] = float(a[1]) * self.Quantum
                except ValueError:
                    raise BadFormatError, 'Cannot parse line %s : %s : %d' % (self.fname, key, i + 1)

                if len(a) > 3:
                    try:
                        a[3] = float(a[3])
                    except ValueError:
                        raise BadFormatError, 'Cannot parse line %s : %s : %d' % (self.fname, key, i + 1)

            labels.append(tuple(a[:n]))

        labels.sort()
        return labels