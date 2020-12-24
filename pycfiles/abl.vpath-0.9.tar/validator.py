# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/abl/cssprocessor/validator.py
# Compiled at: 2010-06-16 07:49:46
__doc__ = '\nCopyright (c) 2009 Ableton AG\n\nPermission is hereby granted, free of charge, to any person\nobtaining a copy of this software and associated documentation\nfiles (the "Software"), to deal in the Software without\nrestriction, including without limitation the rights to use,\ncopy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the\nSoftware is furnished to do so, subject to the following\nconditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES\nOF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT\nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\nWHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR\nOTHER DEALINGS IN THE SOFTWARE.\n'
from __future__ import absolute_import, with_statement
import sys, pprint
from textwrap import dedent
import argparse
from pyparsing import ParseException
from abl.vpath.base import URI
from .parser import URINode
from .rewriter import RewriteParser

class CSSValidator(object):

    def __init__(self, filename, verbose=False, roots=()):
        self.filename = filename
        root_mapping = []
        for path in roots:
            if isinstance(path, tuple):
                root_mapping.append(path)
            else:
                if ':' in path:
                    (prefix, path) = path.split(':', 1)
                else:
                    prefix = '/'
                assert path.startswith('/'), '%s must start with /'
                root_mapping.append((prefix, URI('file://%s' % path)))

        self.root_mapping = root_mapping
        self.verbose = verbose
        self.warnings = []

    def validate(self):
        if not self.filename.exists() or self.filename.isdir():
            self.error('No such file: %r' % self.filename)
        self.relative_base = self.filename.directory()
        self.report('Attempting to parse CSS file %s' % self.filename)
        parser = RewriteParser(self)
        with self.filename.open() as (inf):
            content = inf.read()
        try:
            res = parser.parseString(content)
        except ParseException, e:
            message = 'ERROR: Malformed CSS, text is: <<<%s>>>' % e.pstr
            self.warnings.append(message)
            print message

    def declaration_parse_action(self, input, loc, tokens):
        property_ = tokens[0]
        if property_ in ('background', 'background-image'):
            uris = [ uri for uri in tokens if isinstance(uri, URINode) ]
            if not uris:
                return
            assert len(uris) == 1
            image_url = uris[0]
            path = image_url.path
            if image_url.relative:
                if not (self.relative_base / path).exists():
                    self.warning('Relative resource not found: %s' % path)
            elif not self.check_for_absoulte_resource(path):
                self.warning('Absolute resource not found: %s' % path)

    def check_for_absoulte_resource(self, resource_path):
        for (prefix, path) in self.root_mapping:
            if resource_path.startswith(prefix):
                rest = resource_path[len(prefix):]
                if rest.startswith('/'):
                    rest = rest[1:]
                if (path / rest).exists():
                    return True

        return False

    def error(self, msg):
        sys.stderr.write(msg)
        sys.stderr.write('\n')
        sys.exit(1)

    def report(self, msg):
        if self.verbose:
            print msg

    def warning(self, msg):
        self.warnings.append(msg)
        print 'WARNING:', msg


def validator():
    parser = argparse.ArgumentParser()
    parser.add_argument('cssfile', help=dedent('\n                        The CSS-file to validate.\n                        '))
    parser.add_argument('--root', help=dedent("\n                        To resolve absolute paths, you need to give\n                        at least on root-path.\n\n                        You can specify several.\n\n                        It's also possible to give a prefix by using\n                        a colon.\n\n                        So\n\n                          --root=/resources:/home/user/project/public/resources\n\n                        will be used to resolve resources that start with '/resources'.\n                        "), action='append', dest='roots', default=[])
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])
    validator = CSSValidator(URI('file://%s' % args.cssfile), roots=args.roots, verbose=args.verbose)
    validator.validate()