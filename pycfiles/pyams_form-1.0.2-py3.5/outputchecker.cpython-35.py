# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/outputchecker.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 4226 bytes
"""PyAMS_form.outputchecker module

Doctest output checker module.
"""
import doctest as pythondoctest, re, lxml.etree, lxml.doctestcompare
from lxml.doctestcompare import LHTMLOutputChecker
from zope.testing.renormalizing import RENormalizing
__docformat__ = 'restructuredtext'

class OutputChecker(LHTMLOutputChecker, RENormalizing):
    __doc__ = 'Doctest output checker which is better equippied to identify\n    HTML markup than the checker from the ``lxml.doctestcompare``\n    module. It also uses the text comparison function from the\n    built-in ``doctest`` module to allow the use of ellipsis.\n\n    Also, we need to support RENormalizing.\n    '
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