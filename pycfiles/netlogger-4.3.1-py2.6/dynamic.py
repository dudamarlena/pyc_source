# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/dynamic.py
# Compiled at: 2010-04-29 00:14:32
"""
Dynamic parser module that determines which actual parser
to use on a per-line basis.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: dynamic.py 24753 2010-04-29 04:14:31Z dang $'
import re
from netlogger.parsers.base import BaseParser, LINE_SKIPPED
from netlogger.nlapi import quotestr

class Parser(BaseParser):
    """A meta-parser that matches parser modules to a given
    line based on a header. The expected header
    is given by regular expression. For each input line, values of matching
    named groups, e.g. `(?P<name>'expr')`,
    are used to select the parser to use for that line.

    Parameters:
        - pattern {REGEX}: Regular expression to extract the header
        - show_header_groups {yes,no,no*}: A list of named groups in the
            header expression include in the output event.
            If None, False, or empty, no named header parts will not be included.
            If True, include any/all header parts.
        - header_groups_prefix {STRING,'syslog.'*}: String prefix to add to each name in the
            header group, to avoid name-clashes with the names already in the event record. 
            The default prefix reflects the primary use-case of parsing a syslog-ng
            receiver's output.
    """

    def __init__(self, f, pattern=None, show_header_groups=False, header_groups_prefix='syslog.', **kw):
        self.header = re.compile('^' + pattern)
        self.modules = {}
        val = show_header_groups
        if val is True:
            self._show_hdr = True
        elif not val:
            self._show_hdr = False
        else:
            self._show_hdr = dict.fromkeys(val)
        self._pfx = str(header_groups_prefix)
        BaseParser.__init__(self, f, fullname=__name__, **kw)

    def add(self, module_name, named_patterns, module_instance):
        """Add a module and the dictionary of patterns (with the name of
        the matching group as the key, and a compiled regular expression
        as the value) that should match it.
        An empty dictionary for 'named_patterns' will match anything.
        """
        self.modules[module_name] = (
         named_patterns, module_instance)

    def _getParsers(self):
        """Return dictionary { parser_name : parser_instance }
        """
        pdict = {}
        for (name, (pat_dict, parser)) in self.modules.items():
            pdict[name] = parser

        return pdict

    def getParameters(self):
        """Get parameters, i.e. persistent state, from all parsers.

        Return as a dictionary { parser_name : parameters_dict }
        """
        result = {}
        for (name, instance) in self._getParsers().items():
            param = instance.getParameters()
            self.log.debug('state.get', module=name, value=param)
            result[name] = param

        return result

    def setParameters(self, all_param):
        """Set parameters, i.e. persistent state, into all the parsers.

        Input is in the same form as that returned by getParameters()
        """
        for (name, instance) in self._getParsers().items():
            if all_param.has_key(name):
                param = all_param[name]
                self.log.debug('state.set', module=name, value=param)
                instance.setParameters(param)

    def getParserForLine(self, line):
        """Find parser instance matching the header that
        will be extracted from the string 'line'.

        Return triple:  parser instance, start of the line body, and the
        matched header parts as a dictionary.
        """
        matchobj = self.header.match(line)
        if matchobj is None:
            return (None, None, None)
        else:
            group_dict = matchobj.groupdict()
            matched_parser = None
            for (name, (pat_dict, parser)) in self.modules.items():
                if not pat_dict:
                    matched_parser = parser
                    continue
                matched = True
                for (key, value) in pat_dict.items():
                    if not group_dict.has_key(key) or not value.match(group_dict[key]):
                        matched = False
                        break

                if matched:
                    matched_parser = parser
                    break

            if matched_parser:
                matched_parser.setHeaderValues(group_dict)
                return (
                 matched_parser, matchobj.span()[1], group_dict)
            return (None, None, None)
            return

    def process(self, line):
        (parser, offs, groups) = self.getParserForLine(line)
        if parser is None:
            return LINE_SKIPPED
        else:
            r = parser.process(line[offs:].strip())
            if r and self._show_hdr:
                r = self._add_hdr_groups(r, groups)
            return r

    def _add_hdr_groups(self, r, groups):
        """Add header groups to each returned value.
        """
        header_values = {}
        if self._show_hdr is True:
            for (key, value) in groups.items():
                header_values[self._pfx + key] = value

        for (key, value) in groups.items():
            if self._show_hdr.has_key(key):
                header_values[self._pfx + key] = value

        if header_values:
            for value in r:
                value.update(header_values)

        return r

    def __str__(self):
        return 'dynamic(%s)' % (',').join(self.modules.keys())