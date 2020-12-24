# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/abl/cssprocessor/util.py
# Compiled at: 2009-10-20 06:22:04
__doc__ = '\nCopyright (c) 2009 Ableton AG\n\nPermission is hereby granted, free of charge, to any person\nobtaining a copy of this software and associated documentation\nfiles (the "Software"), to deal in the Software without\nrestriction, including without limitation the rights to use,\ncopy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the\nSoftware is furnished to do so, subject to the following\nconditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES\nOF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT\nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\nWHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR\nOTHER DEALINGS IN THE SOFTWARE.\n'

class OverlapError(Exception):
    pass


class Replacer(object):

    def __init__(self, content):
        self.content = content
        self.replacements = []

    def __setitem__(self, position, replacement):
        assert position.step is None
        lc = len(self.content)
        start, stop = position.start, position.stop
        if start is None:
            start = 0
        if stop is None:
            stop = lc
        if start < 0:
            start += lc
        if stop < 0:
            stop += lc
        if not stop <= lc:
            raise IndexError, 'Assignemnt only within content size'
        position = slice(start, stop)
        self.replacements.append((position, replacement))
        return

    def get_value(self):
        return ('').join(iter(self))

    def __iter__(self):
        content = self.content
        replacements = sorted(self.replacements)
        if not replacements:
            yield content
            raise StopIteration
        until = -1
        for (position, _) in replacements:
            if position.start < until:
                raise OverlapError()
            until = position.stop

        offset = 0
        sit = iter(replacements)
        (position, chunk) = sit.next()
        if position.start > 0:
            yield content[:position.start]
        while True:
            if callable(chunk):
                chunk = chunk()
            yield chunk
            stop = position.stop
            try:
                (position, chunk) = sit.next()
            except StopIteration:
                break

            if position.start > stop:
                yield content[stop:position.start]

        if stop < len(content):
            yield content[stop:]