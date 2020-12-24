# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/greg/Dropbox/code/dealertrack/flake8-diff/flake8diff/flake8.py
# Compiled at: 2015-07-13 15:56:52
from __future__ import unicode_literals, print_function
import logging, re
from blessings import Terminal
from .exceptions import Flake8NotInstalledError, NotLocatableVCSError, UnsupportedVCSError, VCSNotInstalledError, WrongVCSSpecified
from .utils import _execute
from .vcs import SUPPORTED_VCS
terminal = Terminal()
identity = lambda x: x
logger = logging.getLogger(__name__)
FLAKE8_OUTPUT = b'{filename}:{line}:{char}: {code} {description}'
HEADER_STRING = b'Found violations'
HEADER_OUTPUT = b'{header}: {filename}'
SIMPLE_OUTPUT = b'\t{code} @ {line}:{char} - {description}'
FLAKE8_LINE = re.compile(b'^(?P<filename>[^\\s]+):(?P<line_number>[\\d]+):(?P<char_number>[\\d]+): (?P<error_code>[\\w\\d]*) (?P<description>.*)')
COLORS = {b'off': dict(header=identity, filename=identity, code=identity, line=identity, char=identity, description=identity), 
   b'nocolor': dict(header=terminal.bold_underline, filename=terminal.standout, code=terminal.bold, line=identity, char=identity, description=identity), 
   b'colorful': dict(header=terminal.bold, filename=identity, code=terminal.bold_red, line=terminal.magenta, char=terminal.magenta, description=terminal.cyan), 
   b'dark': dict(header=terminal.bold, filename=identity, code=terminal.bold_red, line=terminal.magenta, char=terminal.magenta, description=terminal.yellow), 
   b'light': dict(header=terminal.bold, filename=identity, code=terminal.bold_red, line=terminal.magenta, char=terminal.magenta, description=terminal.blue)}
COLORS[b'boring'] = COLORS[b'off'].copy()
STRICT_MODES = {b'only_lines': b'only_lines', 
   b'file': b'file'}

class Flake8Diff(object):
    """
    Main class implementing flake8-diff functionality
    """

    def __init__(self, commits, options=None):
        self.commits = commits
        self.options = options
        try:
            self.flake8 = _execute(b'which flake8', strict=True).strip()
        except:
            raise Flake8NotInstalledError()

        self._should_include_violation = getattr(self, (b'_should_include_violation_{0}').format(self.options.get(b'strict_mode', b'only_lines')))

    def get_vcs(self):
        """
        Get appropriate VCS engine
        """
        if self.options.get(b'vcs'):
            vcs = self.options.get(b'vcs')
            if vcs not in SUPPORTED_VCS:
                raise UnsupportedVCSError(vcs)
            supported_vcs = SUPPORTED_VCS[vcs](self.commits, self.options)
            if supported_vcs.is_used() and supported_vcs.check():
                return supported_vcs
            raise WrongVCSSpecified(vcs)
        for vcs in SUPPORTED_VCS.values():
            try:
                vcs = vcs(self.commits, self.options)
            except VCSNotInstalledError:
                logger.error((b'Seems like {0} is not installed').format(vcs.name))
            else:
                if vcs.is_used() and vcs.check():
                    return vcs

        raise NotLocatableVCSError

    def run_flake8(self, filename):
        """
        Run flake8 on a file
        """
        command = filter(None, [
         self.flake8] + self.options.get(b'flake8_options', []) + [filename])
        return _execute((b' ').join(command))

    def color_getter(self, component):
        """
        Get color formatting function for selected theme via options.
        If function is not present in the themes,
        identity function is returned.
        """
        theme = COLORS.get(self.options.get(b'color_theme'), {})
        return theme.get(component, identity)

    def get_color_kwargs(self, details):
        """
        Get string formatting kwargs from violation details
        """
        get = lambda i: details.get(i, b'')
        return dict(line=self.color_getter(b'line')(get(b'line_number')), char=self.color_getter(b'char')(get(b'char_number')), code=self.color_getter(b'code')(get(b'error_code')), description=self.color_getter(b'description')(get(b'description')), filename=self.color_getter(b'filename')(get(b'filename')), header=self.color_getter(b'header')(get(b'header')))

    def _should_include_violation_only_lines(self, violation, changed_lines):
        """
        Check if given violation should be included.

        Since this implements "only_lines" strict mode, this
        only includes the violation if it was introduced in the
        modified files as per VCS diff.
        """
        return violation[b'line_number'] in changed_lines

    def _should_include_violation_file(self, violation, changed_lines):
        """
        Check if given violation should be included.

        Since this implements "file" strict mode, this always
        includes all violations in the report.
        """
        return True

    def _should_include_violation(self, violation, changed_lines):
        raise NotImplementedError(b'This method should be replaced in __init__')

    def process(self):
        """
        Perform the magic
        """
        overall_violations = 0
        vcs = self.get_vcs()
        for filename in vcs.changed_files():
            changed_lines = vcs.changed_lines(filename)
            logger.info((b'checking {0} lines {1}').format(filename, (b', ').join(changed_lines)))
            violations = []
            for violation in self.run_flake8(filename).splitlines():
                matches = FLAKE8_LINE.match(violation)
                if matches:
                    violation_details = matches.groupdict()
                    if self._should_include_violation(violation_details, changed_lines):
                        violations.append(violation_details)
                        if self.options.get(b'standard_flake8_output'):
                            print(FLAKE8_OUTPUT.format(**self.get_color_kwargs(violation_details)))

            overall_violations += len(violations)
            if violations:
                self.options.get(b'standard_flake8_output') or print(HEADER_OUTPUT.format(**self.get_color_kwargs(dict(filename=filename, header=HEADER_STRING))))
                for line in violations:
                    print(SIMPLE_OUTPUT.format(**self.get_color_kwargs(line)))

        return overall_violations == 0