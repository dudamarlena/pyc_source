# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/ExtractDoi.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 2681 bytes
import re, os
from .Exceptions import AbortException
from .Prompt import promptOptions, promptString
from .TermOutput import msg
from .BaseWork import Work
from .AnsiBib import printBibliography, printWork
from .ReadPdf import getPdfTxt
_doiRegexStr = re.compile('10[.][0-9]{4,}[^\\s"/<>]*/[^\\s"<>]+')

def _chopPeriod(x):
    if x[(-1)] == '.':
        return x[:-1]
    else:
        return x


def extractDois(fname):
    pdfData = '\n'.join(getPdfTxt(fname))
    dois = [_chopPeriod(x.lower()) for x in _doiRegexStr.findall(pdfData)]
    seen = set()
    return [x for x in dois if not (x in seen or seen.add(x))]


def entryFromPdf(fname):
    dois = extractDois(fname)
    maxChoices = 5

    def chunker():
        lst = []
        for doi in dois:
            try:
                e = Work.from_doi(doi)
                if e:
                    lst.append(e)
            except ValueError:
                pass

            if len(lst) == maxChoices:
                yield lst
                lst = []

        if lst:
            yield lst

    showMsg = True
    for chunkId, bibChunk in enumerate(chunker()):
        if len(bibChunk) == 1:
            if chunkId == 0:
                return bibChunk[0]
        if showMsg:
            msg('Found %d putative DOIs in %s:\n', len(dois), fname)
            showMsg = False
        printBibliography(bibChunk)
        choice = None
        while choice is None:
            try:
                choice = promptOptions('Choose reference for ' + os.path.basename(fname), [str(x + 1) for x in range(len(bibChunk))] + ['n', 'q'])
                if choice.lower() == 'q':
                    raise AbortException
                if choice.lower() == 'n':
                    choice = None
                    break
                choice = int(choice)
                if not 1 <= choice <= len(bibChunk):
                    raise ValueError
                else:
                    msg()
                    return bibChunk[(choice - 1)]
            except ValueError:
                msg.warning('Invalid response')
                choice = None


def entryFromUser(fname):
    while 1:
        doi = promptString('Enter DOI for {} '.format(os.path.basename(fname)))
        if doi.lower() == 'q':
            raise AbortException
        bibData = Work.from_doi(doi)
        if bibData is None:
            msg.warning('Doi not found.')
        else:
            printWork(bibData)
            response = promptOptions('OK', ['y', 'n', 'q'], default='y')
            if response == 'q':
                raise AbortException
            else:
                if response == 'y':
                    return bibData