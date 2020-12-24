# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/notification/emailbuilder.py
# Compiled at: 2009-03-12 11:08:18
"""
EmailBuilder is a tool to construct complex MIME documents as defined by a
control file and content from a source, typically a file system directory.

The document structure and content is driven by a file called "parts.lst".

Email Structure Examples
========================

Simple, Plain Text Email
~~~~~~~~~~~~~~~~~~~~~~~~

parts.lst
---------
text/plain: body.txt

body.txt
--------
The text of the message.

Plain Text/HTML Email
~~~~~~~~~~~~~~~~~~~~~

parts.lst
---------
multipart/alternative:
    text/plain: body.txt
    text/html: body.html

body.txt
--------
The text of the message.

body.html
---------
<p>The text of the message.</p>

"""
import codecs, os.path, re
from email.MIMEMultipart import MIMEMultipart
PARTS = 'parts.lst'

class EmailBuilderError(Exception):
    pass


class EmailBuilder(object):

    def __init__(self, source, headers):
        self.source = source
        self.headers = headers

    def build(self):
        msg = MIMEMultipart()
        for (k, v) in self.headers.items():
            msg[k] = v

        parts = [
         (
          None, msg)]
        for line in self.source[PARTS]:
            if not line.strip():
                continue
            (indent, contentType, filename, args) = self._parsePartLine(line)
            while indent <= parts[(-1)][0] and parts[(-1)][0] is not None:
                parts.pop()

            mainType = contentType[0]
            partFactory = getattr(self, 'part_%s' % (mainType,), None)
            if partFactory is None:
                raise MailBuilderError('No factory for %r parts' % (mainType,))
            part = partFactory(contentType, filename)
            for (k, v) in args.items():
                part[k] = v

            parts[(-1)][1].attach(part)
            parts.append((indent, part))

        return msg

    def part_multipart(self, contentType, filename):
        return MIMEMultipart(contentType[1])

    def part_text(self, contentType, filename):
        from email.MIMEText import MIMEText
        f = codecs.getreader('utf-8')(self.source[filename])
        try:
            return MIMEText(f.read(), contentType[1])
        finally:
            f.close()

    def part_image(self, contentType, filename):
        from email.MIMEImage import MIMEImage
        return MIMEImage(self.source[filename].read(), contentType[1])

    def part_application(self, contentType, filename):
        from email.MIMEApplication import MIMEApplication
        return MIMEApplication(self.source[filename].read(), contentType[1])

    def _parsePartLine(self, part):
        d = re.match('^(?P<indent> *?)(?P<contentType>[a-z]+/[a-z]+):(?P<rest>.*)$', part).groupdict()
        indent = len(d['indent'])
        contentType = tuple(d['contentType'].split('/'))
        rest = d['rest'].strip()
        if not rest:
            filename = None
            args = {}
        else:
            rest = rest.split(None)
            filename, args = rest[:1], rest[1:]
            filename = filename[0]
            args = dict([ arg.split('=', 1) for arg in args ])
        return (
         indent, contentType, filename, args)


class FileSystemSource(object):

    def __init__(self, dir):
        if not os.path.exists(dir) or not os.path.isdir(dir):
            raise EmailBuilderError('Invalid directory %r' % (dir,))
        self.dir = dir
        self.openFiles = []

    def __getitem__(self, name):
        f = file(os.path.join(self.dir, name))
        self.openFiles.append(f)
        return f

    def close(self):
        for f in self.openFiles:
            f.close()