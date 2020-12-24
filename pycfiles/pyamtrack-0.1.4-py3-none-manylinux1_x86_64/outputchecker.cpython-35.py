# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/outputchecker.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 4226 bytes
__doc__ = 'PyAMS_form.outputchecker module\n\nDoctest output checker module.\n'
import doctest as pythondoctest, re, lxml.etree, lxml.doctestcompare
from lxml.doctestcompare import LHTMLOutputChecker
from zope.testing.renormalizing import RENormalizing
__docformat__ = 'restructuredtext'

class OutputChecker(LHTMLOutputChecker, RENormalizing):
    """OutputChecker"""
    _repr_re = re.compile("^<([A-Z]|[^>]+ (at|object) |[a-z]+ \\'[A-Za-z0-9_.]+\\'>)")

    def __init__(self, doctest=pythondoctest, patterns=()):
        RENormalizing.__init__(self, patterns)
        self.doctest = doctest
        doctest.register_optionflag('PARSE_HTML')
        doctest.register_optionflag('PARSE_XML')
        doctest.register_optionflag('NOPARSE_MARKUP')

    def _looks_like_markup(self, s):
        s = s.replace('<BLANKLINE>', '\n').strip()
        return s.startswith('<') and not self._repr_re.search(s)

    def text_compare(self, want, got, strip):
        if want is None:
            want = ''
        if got is None:
            got = ''
        checker = self.doctest.OutputChecker()
        return checker.check_output(want, got, self.doctest.ELLIPSIS | self.doctest.NORMALIZE_WHITESPACE)

    def check_output(self, want, got, optionflags):
        if got == want:
            return True
        for transformer in self.transformers:
            want = transformer(want)
            got = transformer(got)

        return LHTMLOutputChecker.check_output(self, want, got, optionflags)

    def output_difference(self, example, got, optionflags):
        want = example.want
        if not want.strip():
            return LHTMLOutputChecker.output_difference(self, example, got, optionflags)
        original = want
        for transformer in self.transformers:
            want = transformer(want)
            got = transformer(got)

        example.want = want
        result = LHTMLOutputChecker.output_difference(self, example, got, optionflags)
        example.want = original
        difflines = [l for l in result.splitlines() if '(got:' in l]
        if difflines:
            result += '\nLines with differences:\n' + '\n'.join(difflines)
        return result

    def get_parser(self, want, got, optionflags):
        NOPARSE_MARKUP = self.doctest.OPTIONFLAGS_BY_NAME.get('NOPARSE_MARKUP', 0)
        PARSE_HTML = self.doctest.OPTIONFLAGS_BY_NAME.get('PARSE_HTML', 0)
        PARSE_XML = self.doctest.OPTIONFLAGS_BY_NAME.get('PARSE_XML', 0)
        parser = None
        if NOPARSE_MARKUP & optionflags:
            return
        if PARSE_HTML & optionflags:
            parser = lxml.doctestcompare.html_fromstring
        else:
            if PARSE_XML & optionflags:
                parser = lxml.etree.XML
            else:
                if want.strip().lower().startswith('<html') and got.strip().startswith('<html'):
                    parser = lxml.doctestcompare.html_fromstring
                elif self._looks_like_markup(want) and self._looks_like_markup(got):
                    parser = self.get_default_parser()
        return parser