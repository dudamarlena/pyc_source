# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\textreader.py
# Compiled at: 2019-11-27 15:09:36
# Size of source mod 2**32: 19371 bytes
"""
textreader - read text out of various file types
===================================================
"""
import argparse, csv
from . import version
VALIDFTYPES = [
 'xls', 'xlsx', 'docx', 'txt', 'csv']
VALIDLTYPES = [
 'txt', 'csv']
DOCXTABSIZE = 8
TXTABSIZE = 8

class headerError(Exception):
    pass


class parameterError(Exception):
    pass


class TextDictReader:
    __doc__ = "\n    get data from a file in various formats\n    \n    :param filename: name of file to open, or list-like\n    :param fieldxform: {'fieldname1':['hdr11, hdr12, ...'], 'fieldname2':[hdr21, ...], ...}, where fieldnamex will be returned in dict, hdrxx are possible headers for columns\n    :param reqdfields: list of fields required to be in the header\n    :param filetype: if filename is list, this should be filetype list should be interpreted as\n    "

    def __init__(self, filename, fieldxform, reqdfields, filetype='extension'):
        self.file = TextReader(filename, filetype)
        self.fieldxform = fieldxform
        self.reqdfields = reqdfields
        self.field = {}
        self._findhdr()

    def _findhdr(self):
        """
        find the header in the file
        """
        foundhdr = False
        delimited = self.file.getdelimited()
        fields = list(self.fieldxform.keys())
        MINMATCHES = len(self.reqdfields)
        try:
            while 1:
                origline = next(self.file)
                fieldsfound = 0
                line = []
                if not delimited:
                    for word in origline.split():
                        line.append(word.lower())

                else:
                    for word in origline:
                        line.append(str(word).lower())

                for fieldndx in range(len(fields)):
                    f = fields[fieldndx]
                    match = self.fieldxform[f]
                    for m in match:
                        matchfound = False
                        for linendx in range(len(line)):
                            if isinstance(m, str):
                                m = [
                                 m]
                            if linendx + len(m) > len(line):
                                continue
                            if line[linendx:linendx + len(m)] == m:
                                if f not in self.field:
                                    self.field[f] = {}
                                self.field[f]['start'] = linendx
                                self.field[f]['end'] = linendx + len(m)
                                self.field[f]['match'] = m
                                self.field[f]['genfield'] = f
                                fieldsfound += 1
                                matchfound = True
                                break

                        if matchfound:
                            break

                if fieldsfound >= MINMATCHES:
                    fieldsnotfound = []
                    for f in self.reqdfields:
                        if f not in self.field:
                            fieldsnotfound.append(f)

                    if len(fieldsnotfound) != 0:
                        raise headerError('could not find fields {} in header {}'.format(fieldsnotfound, origline))
                    foundfields_dec = sorted([(self.field[f]['start'], self.field[f]) for f in self.field])
                    self.foundfields = [ff[1] for ff in foundfields_dec]
                    if not delimited:
                        delimiters = []
                        thischar = 0
                        foundfields_iter = iter(self.foundfields)
                        thisfield = next(foundfields_iter)
                        while 1:
                            while thischar < len(origline) and origline[thischar] == ' ':
                                thischar += 1

                            if thischar == len(origline):
                                break
                            delimiters.append(thischar)
                            matchfound = False
                            if thisfield is not None:
                                fullmatch = ' '.join(thisfield['match'])
                                if origline[thischar:thischar + len(fullmatch)].lower() == fullmatch:
                                    thischar += len(fullmatch)
                                    matchfound = True
                                    try:
                                        thisfield = next(foundfields_iter)
                                    except StopIteration:
                                        thisfield = None

                                if not matchfound:
                                    while thischar < len(origline) and origline[thischar] != ' ':
                                        thischar += 1

                                if thischar == len(origline):
                                    break

                        self.file.setdelimiter(delimiters)
                    break

            self.fieldhdrs = []
            self.fieldcols = []
            skipped = 0
            for f in self.foundfields:
                self.fieldhdrs.append(f['genfield'])
                currcol = f['start'] - skipped
                self.fieldcols.append(currcol)
                skipped += len(f['match']) - 1

        except StopIteration:
            raise headerError('header not found')

    def __next__(self):
        """
        return dict with generic headers and associated data from file
        """
        rawline = next(self.file)
        filteredline = [rawline[i] for i in range(len(rawline)) if i in self.fieldcols]
        result = dict(list(zip(self.fieldhdrs, filteredline)))
        return result


class TextReader:
    __doc__ = '\n    abstract text reader for several different file types\n    creation of object opens TextReader file\n    \n    :param filename: name of file to open, or list\n    '

    def __init__(self, filename, filetype='extension'):
        """
        open TextReader file
        
        :param filename: name of file to open, or list-like
        :param filetype: if filename is list, this should be filetype list should be interpreted as
        """
        if isinstance(filename, str):
            self.ftype = filename.split('.')[(-1)].lower()
            self.intype = 'file'
            if self.ftype not in VALIDFTYPES:
                raise parameterError('Invalid filename {}: must have extension in {}'.format(filename, VALIDFTYPES))
        else:
            self.ftype = filetype.lower()
            self.intype = 'list'
            if self.ftype not in VALIDLTYPES:
                raise parameterError('Invalid list: must use filetype in {}'.format(VALIDLTYPES))
            if self.ftype in ('xls', 'xlsx'):
                import xlrd
                self.workbook = xlrd.open_workbook(filename)
                self.sheet = self.workbook.sheet_by_index(0)
                self.currrow = 0
                self.nrows = self.sheet.nrows
                self.delimited = True
                self.workbook.release_resources()
            else:
                if self.ftype in ('docx', ):
                    import docx
                    doc = docx.opendocx(filename)
                    self.lines = iter(docx.getdocumenttext(doc))
                    self.delimited = False
                else:
                    if self.ftype in ('txt', ):
                        if self.intype == 'file':
                            self.TXT = open(filename, 'r')
                        else:
                            self.TXT = iter(filename)
                        self.delimited = False
                    elif self.ftype in ('csv', ):
                        if self.intype == 'file':
                            self._CSV = open(filename, 'rb')
                        else:
                            self._CSV = iter(filename)
                        self.CSV = csv.reader(self._CSV)
                        self.delimited = True
        self.delimiters = None
        self.opened = True

    def __next__(self):
        """
        read next line from TextReader file
        raises StopIteration when end of file reached
        
        :rtype: list of cells for the current row
        """
        if not self.opened:
            raise ValueError('I/O operation on a closed file')
        elif self.ftype in ('xls', 'xlsx'):
            if self.currrow >= self.nrows:
                raise StopIteration
            row = self.sheet.row_values(self.currrow)
            self.currrow += 1
            return row
        else:
            if self.ftype in ('docx', ):
                line = next(self.lines)
                line = line.expandtabs(DOCXTABSIZE)
                if self.delimiters:
                    splitline = self.delimit(line)
                    return splitline
                else:
                    return line
            else:
                if self.ftype in ('txt', ):
                    line = next(self.TXT)
                    line = line.expandtabs(TXTABSIZE)
                    if self.delimiters:
                        splitline = self.delimit(line)
                        return splitline
                    else:
                        return line
                elif self.ftype in ('csv', ):
                    row = next(self.CSV)
                    return row

    def close(self):
        """
        close TextReader file
        """
        self.opened = False
        if self.intype == 'list':
            pass
        else:
            if self.ftype in ('xls', 'xlsx'):
                pass
            else:
                if self.ftype in ('docx', ):
                    pass
                else:
                    if self.ftype in ('txt', ):
                        self.TXT.close()
                    elif self.ftype in ('csv', ):
                        self._CSV.close()

    def getdelimited(self):
        """
        return state whether file is delimited
        
        :rtype: True if delimited
        """
        return self.delimited

    def setdelimiter(self, delimiters):
        """
        set delimiters for file as specified in delimiters
        
        :param delimiters: list of character positions to set delimiters at
        """
        if self.delimited:
            raise parameterError('cannot set delimiters for file which is already delimited')
        if not isinstance(delimiters, list):
            raise parameterError('delimiters must be a list of increasing integers')
        lastdelimiter = -1
        for delimiter in delimiters:
            if not isinstance(delimiter, int) or delimiter <= lastdelimiter:
                raise parameterError('delimiters must be a list of increasing integers')
            lastdelimiter = delimiter

        self.delimiters = delimiters
        self.delimited = True

    def delimit(self, s):
        """
        split a string based on delimiters
        
        :param s: string to be split
        :rtype: list of string elements, stripped of white space
        """
        if not self.delimiters:
            raise parameterError('cannot split string if delimiters not set')
        rval = []
        for i in range(len(self.delimiters)):
            start = self.delimiters[i]
            end = self.delimiters[(i + 1)] if i + 1 < len(self.delimiters) else None
            rval.append(s[start:end].strip())

        return rval


def main():
    parser = argparse.ArgumentParser(version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('filename', help='name of file for testing')
    args = parser.parse_args()
    filename = args.filename
    ff = TextReader(filename)
    for i in range(6):
        print(next(ff))

    ff.close()


if __name__ == '__main__':
    main()