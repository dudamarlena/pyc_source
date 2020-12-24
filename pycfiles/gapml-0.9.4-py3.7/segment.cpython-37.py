# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/segment.py
# Compiled at: 2018-08-31 14:33:57
# Size of source mod 2**32: 4078 bytes
""" Segment Module for Processing PDF Documents 
Copyright 2018(c), Andrew Ferlitsch
"""
version = '0.9.2'

class Segment(object):
    __doc__ = ' Segment text into Regions '
    HEADING = 1001
    PARAGRAPH = 1002
    PAGENO = 1003
    COPYRIGHT = 1004

    def __init__(self, text):
        """ constructor """
        if text:
            if not isinstance(text, str):
                raise TypeError('String expected for text')
        self._text = text
        self._segments = []
        if text:
            self._segmentation()

    def _segmentation(self):
        """ Split text into:
        Headings
        Paragraphs
        Table of Contents
        Page Numbering
        """
        para = ''
        lines = self._text.split('\n')
        for line in lines:
            s_line = line.strip()
            if s_line == '':
                if para != '':
                    self._segments.append({'text':para,  'tag':self.PARAGRAPH})
                    para = ''
                elif s_line.isupper():
                    if para != '':
                        self._segments.append({'text':para,  'tag':self.PARAGRAPH})
                        para = ''
                    self._segments.append({'text':line,  'tag':self.HEADING})
                elif s_line.lower().startswith('copyright'):
                    if para != '':
                        self._segments.append({'text':para,  'tag':self.PARAGRAPH})
                        para = ''
                    self._segments.append({'text':line,  'tag':self.COPYRIGHT})
                else:
                    pageno = False
                    toks = s_line.split(' ')
                    ntoks = len(toks)
                    if ntoks == 1 and toks[0].isdigit():
                        pageno = True
                    else:
                        if ntoks == 2:
                            if toks[0].lower() in ('page', 'p', 'p.') and toks[1].isdigit():
                                pageno = True
                        elif ntoks == 3:
                            if toks[0] == '-':
                                if toks[1].isdigit():
                                    if toks[2] == '-':
                                        pageno = True
                    if not pageno:
                        heading = True
                        for tok in toks:
                            if not tok == '':
                                if len(tok) == 0:
                                    continue
                                if not tok[0].isdigit():
                                    if not tok[0].isupper():
                                        if tok[0] == '.':
                                            continue
                                        heading = False

            else:
                heading = False
            if heading:
                if para != '':
                    self._segments.append({'text':para,  'tag':self.PARAGRAPH})
                    para = ''
                self._segments.append({'text':line,  'tag':self.HEADING})
            elif pageno:
                if para != '':
                    self._segments.append({'text':para,  'tag':self.PARAGRAPH})
                    para = ''
                self._segments.append({'text':line,  'tag':self.PAGENO})
            elif para != '':
                para += '\n' + line
            else:
                para = line

        if para != '':
            self._segments.append({'text':para,  'tag':self.PARAGRAPH})
            para = ''

    @property
    def segments(self):
        """ Getter for segments """
        return self._segments

    def __len__(self):
        """ return the number of segments """
        return len(self._segments)