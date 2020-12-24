# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tome\writeText.py
# Compiled at: 2013-04-26 21:45:24
"""
Copyright 2013 Brian Mearns

This file is part of Tome.

Tome is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Tome is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Tome.  If not, see <http://www.gnu.org/licenses/>.
"""
import Tome, cStringIO, wrapUtil

class TextWriter(object):

    def __init__(self, linewidth=None):
        self.__linewidth = linewidth
        self.__chapterNotes = []
        self.__noteNumber = 1

    def writeBlockSegment(self, ostream, begin, end, segment, prefix='', suffix=''):
        ostream.write(begin)
        notFirst = False
        for par in segment:
            if isinstance(par, Tome.TextSegment) and len(par.text().strip()) == 0:
                continue
            if not isinstance(par, Tome.TaggedSegment) or par.tag() != 'p':
                raise Exception('Block node may only contain "p" elements: found "%s"' % par.tag())
            if notFirst:
                ostream.write('\n\n' + prefix)
            notFirst = True
            for cseg in par:
                self.writeSegment(ostream, cseg)

            ostream.write(suffix)

        ostream.write(end)

    def writeSegment(self, ostream, segment):
        if isinstance(segment, Tome.TaggedSegment):
            tag = segment.tag()
            if tag == 'pre':
                close = ''
            else:
                if tag == 'b':
                    ostream.write('*')
                    close = '*'
                elif tag == 'i':
                    ostream.write('/')
                    close = '/'
                elif tag == 'em':
                    ostream.write('**')
                    close = '**'
                elif tag == 'u':
                    ostream.write('_')
                    close = '_'
                else:
                    if tag == 'ellips':
                        ostream.write('...')
                        return
                    if tag == 'md':
                        ostream.write('---')
                        return
                    if tag == 'nd':
                        ostream.write('--')
                        return
                    if tag == 'sp':
                        ostream.write(' ')
                        return
                    if tag == 'lnbrk':
                        ostream.write('\n')
                        return
                    if tag in ('grave', 'acute', 'circumflex', 'umlaut', 'tilde', 'cedilla'):
                        close = ''
                    else:
                        if tag == 'q':
                            return self.writeBlockSegment(ostream, '"', '"', segment, prefix='"')
                        if tag == 'sq':
                            return self.writeBlockSegment(ostream, "'", "'", segment, prefix="'")
                        if tag == 'n':
                            enStream = cStringIO.StringIO()
                            self.writeBlockSegment(enStream, '', '', segment)
                            note = enStream.getvalue()
                            enStream.close()
                            self.__chapterNotes[(-1)].append(note)
                            ostream.write('[%d]' % self.__noteNumber)
                            self.__noteNumber += 1
                            return
                        if tag == 'bq':
                            return self.writeBlockSegment(ostream, '\n\n"', '"\n\n', segment)
                        raise Exception('Unhandled tag: %s' % tag)
                for seg in segment:
                    self.writeSegment(ostream, seg)

            ostream.write(close)
        elif isinstance(segment, Tome.TextSegment):
            content = segment.text()
            ostream.write(content)
        else:
            raise TypeError('Unexpected type for segment.')

    def writeParagraphs(self, ostream, text, linewidth=None, indent='', tag=None, parBreak='\n\n'):
        if linewidth is None:
            linewidth = self.__linewidth
        if linewidth is not None:
            linewidth -= len(indent)
        for subpar in text.splitlines():
            if len(subpar) > 0:
                lines = self.wrapText(subpar, linewidth)
                self.writeJustified(ostream, lines, linewidth, indent, tag)
                tag = None
                ostream.write(parBreak)

        return

    def wrapText(self, text, linewidth=None, remain=None):
        """
        Generates an array of lines, each line is an array of words, such that the word fit
        into the specified linewidth.

        :param int remain:
            Specifies how many columns remain on the current line. Default is all of them.

        """
        if linewidth is None:
            linewidth = self.__linewidth
        return wrapUtil.wrapText(text, linewidth, remain)

    def writeCenteredLine(self, ostream, line, linewidth=None, width=None):
        if linewidth is None:
            linewidth = self.__linewidth
        if linewidth is None:
            ostream.write(line + '\n')
            return
        else:
            if width is None:
                width = linewidth
            lines = self.wrapText(line, width)
            for line in lines:
                line = (' ').join(line)
                length = len(line)
                diff = linewidth - length
                lpadd = (diff + 1) / 2
                ostream.write(' ' * lpadd + line + '\n')

            return

    def writeHr(self, ostream, width, linewidth=None, char='-'):
        hr = char * width
        if linewidth is None:
            linewidth = self.__linewidth
        if linewidth is None:
            ostream.write(hr + '\n')
            return
        else:
            diff = linewidth - width
            lpadd = (diff + 1) / 2
            ostream.write(' ' * lpadd + hr + '\n')
            return

    def writeJustified(self, ostream, lines, linewidth=None, indent='', tag=None):
        """
        Lines should be a list of lines, each line is a list of words.
        """
        if linewidth is None:
            linewidth = self.__linewidth
        if linewidth is None:
            ostream.write(('\n').join(indent + (' ').join(line) for line in lines))
            return
        else:
            prefix = indent
            if tag is not None:
                prefix = tag
            for line in lines[:-1]:
                required = len(('').join(line))
                leftOver = linewidth - required
                spCount = len(line) - 1
                if spCount == 0:
                    ostream.write(indent + line[0])
                    continue
                spacesPer = int(float(leftOver) / float(spCount))
                padd = ' ' * spacesPer
                leftOver = leftOver - spacesPer * spCount
                spaces = [
                 spacesPer] * spCount
                while leftOver > 0:
                    longestLength = None
                    longestLevel = None
                    longestI = None
                    for i in xrange(spCount):
                        length = len(line[i])
                        if longestLength is None:
                            longestLength = length
                            longestLevel = spaces[i]
                            longestI = i
                        elif spaces[i] < longestLevel:
                            longestLength = length
                            longestLevel = spaces[i]
                            longestI = i
                        elif spaces[i] == longestLevel and length > longestLength:
                            longestLength = length
                            longestLevel = spaces[i]
                            longestI = i

                    spaces[longestI] += 1
                    leftOver -= 1

                ostream.write(prefix)
                for i in xrange(spCount):
                    ostream.write(line[i] + ' ' * spaces[i])
                    if leftOver > 0:
                        ostream.write(' ')
                        leftOver -= 1

                ostream.write(line[(-1)] + '\n')
                prefix = indent

            if len(lines) > 0:
                ostream.write(prefix + (' ').join(lines[(-1)]))
            return

    def writeText(self, tome, ostream):
        ostream.write('\n\n\n')
        titleWidth = int(0.7 * float(self.__linewidth))
        if titleWidth < 20:
            titleWidth = self.__linewidth
        lmTitles = tome.allTitles()
        if len(lmTitles) > 0:
            for title in tome.allTitles():
                self.writeCenteredLine(ostream, title, self.__linewidth, titleWidth)
                self.writeHr(ostream, 3, self.__linewidth)

            ostream.write('\n')
        lmAuthors = tome.authors()
        if len(lmAuthors) > 0:
            for author in lmAuthors:
                self.writeCenteredLine(ostream, author, self.__linewidth)

            ostream.write('\n')
        if len(lmTitles) > 0 or len(lmAuthors) > 0:
            ostream.write('\n\n\n')
        chNum = 0
        for part in tome:
            for book in part:
                for chapter in book:
                    chNum += 1
                    self.__chapterNotes.append([])
                    chFirstNoteNum = self.__noteNumber
                    self.writeCenteredLine(ostream, 'Chapter %d' % chNum, self.__linewidth, titleWidth)
                    chAllTitles = chapter.allTitles()
                    if len(chAllTitles) > 0:
                        for title in chAllTitles:
                            self.writeCenteredLine(ostream, title, self.__linewidth, titleWidth)

                    else:
                        ostream.write('\n')
                    self.writeHr(ostream, 9)
                    ostream.write('\n')
                    scCount = len(chapter)
                    lastScene = scCount - 1
                    for i in xrange(scCount):
                        scene = chapter[i]
                        parCount = len(scene)
                        for j in xrange(parCount):
                            paragraph = scene[j]
                            tag = paragraph.tag()
                            if tag not in ('p', 'pre'):
                                raise Exception('Invalid toplevel element in scene: %s' % tag)
                            preformatted = tag == 'pre'
                            parStream = cStringIO.StringIO()
                            for k in xrange(len(paragraph)):
                                self.writeSegment(parStream, paragraph[k])

                            text = parStream.getvalue()
                            parStream.close()
                            if preformatted:
                                ostream.write(text)
                            else:
                                self.writeParagraphs(ostream, text)

                        if i < lastScene:
                            self.writeHr(ostream, 3, char='*')
                            ostream.write('\n')

                    ostream.write('\n')
                    if len(self.__chapterNotes[(-1)]) > 0:
                        notesTitle = 'Notes for Chapter %d' % chNum
                        ostream.write('    %s\n' % notesTitle)
                        ostream.write('    ' + '-' * len(notesTitle) + '\n')
                        self.writeChapterNotes(ostream, self.__chapterNotes[(-1)], chFirstNoteNum)
                    ostream.write('\n')

        ostream.write('\n')
        if self.__noteNumber > 1:
            self.writeCenteredLine(ostream, 'All Chapter Notes', self.__linewidth, titleWidth)
            ostream.write('\n')
            noteNumber = 1
            chNum = 0
            for notes in self.__chapterNotes:
                chNum += 1
                if len(notes) > 0:
                    notesTitle = 'Notes for Chapter %d' % chNum
                    ostream.write('    %s\n' % notesTitle)
                    ostream.write('    ' + '-' * len(notesTitle) + '\n')
                    self.writeChapterNotes(ostream, notes, noteNumber)
                    noteNumber += len(notes)

    def writeChapterNotes(self, ostream, notes, firstNoteNum):
        noteNumber = firstNoteNum
        for note in notes:
            bullet = '    [%d]  ' % noteNumber
            lead = len(bullet)
            padd = ' ' * lead
            self.writeParagraphs(ostream, note, self.__linewidth - 4, padd, bullet)
            ostream.write('\n')
            noteNumber += 1

        ostream.write('\n')


if __name__ == '__main__':
    import sys
    parser = Tome.TomeOtlParser(sys.stdin, filename='<stdin>', debug=True)
    tome = parser.tome()
    writer = TextWriter(78)
    writer.writeText(tome, sys.stdout)