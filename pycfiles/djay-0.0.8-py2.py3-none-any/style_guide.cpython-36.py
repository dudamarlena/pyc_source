# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/style_guide.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 21226 bytes
"""Implementation of the StyleGuide used by Flake8."""
import collections, contextlib, copy, enum, itertools, linecache, logging, sys
from typing import Dict, List, Optional, Set, Union
from flake8 import defaults
from flake8 import statistics
from flake8 import utils
__all__ = ('StyleGuide', )
LOG = logging.getLogger(__name__)
if sys.version_info < (3, 2):
    from functools32 import lru_cache
else:
    from functools import lru_cache

class Selected(enum.Enum):
    __doc__ = 'Enum representing an explicitly or implicitly selected code.'
    Explicitly = 'explicitly selected'
    Implicitly = 'implicitly selected'


class Ignored(enum.Enum):
    __doc__ = 'Enum representing an explicitly or implicitly ignored code.'
    Explicitly = 'explicitly ignored'
    Implicitly = 'implicitly ignored'


class Decision(enum.Enum):
    __doc__ = 'Enum representing whether a code should be ignored or selected.'
    Ignored = 'ignored error'
    Selected = 'selected error'


@lru_cache(maxsize=512)
def find_noqa(physical_line):
    return defaults.NOQA_INLINE_REGEXP.search(physical_line)


_Violation = collections.namedtuple('Violation', [
 'code',
 'filename',
 'line_number',
 'column_number',
 'text',
 'physical_line'])

class Violation(_Violation):
    __doc__ = 'Class representing a violation reported by Flake8.'

    def is_inline_ignored(self, disable_noqa):
        """Determine if a comment has been added to ignore this line.

        :param bool disable_noqa:
            Whether or not users have provided ``--disable-noqa``.
        :returns:
            True if error is ignored in-line, False otherwise.
        :rtype:
            bool
        """
        physical_line = self.physical_line
        if disable_noqa:
            return False
        if physical_line is None:
            physical_line = linecache.getline(self.filename, self.line_number)
        noqa_match = find_noqa(physical_line)
        if noqa_match is None:
            LOG.debug('%r is not inline ignored', self)
            return False
        codes_str = noqa_match.groupdict()['codes']
        if codes_str is None:
            LOG.debug('%r is ignored by a blanket ``# noqa``', self)
            return True
        else:
            codes = set(utils.parse_comma_separated_list(codes_str))
            if self.code in codes or self.code.startswith(tuple(codes)):
                LOG.debug('%r is ignored specifically inline with ``# noqa: %s``', self, codes_str)
                return True
            LOG.debug('%r is not ignored inline with ``# noqa: %s``', self, codes_str)
            return False

    def is_in(self, diff):
        """Determine if the violation is included in a diff's line ranges.

        This function relies on the parsed data added via
        :meth:`~StyleGuide.add_diff_ranges`. If that has not been called and
        we are not evaluating files in a diff, then this will always return
        True. If there are diff ranges, then this will return True if the
        line number in the error falls inside one of the ranges for the file
        (and assuming the file is part of the diff data). If there are diff
        ranges, this will return False if the file is not part of the diff
        data or the line number of the error is not in any of the ranges of
        the diff.

        :returns:
            True if there is no diff or if the error is in the diff's line
            number ranges. False if the error's line number falls outside
            the diff's line number ranges.
        :rtype:
            bool
        """
        if not diff:
            return True
        else:
            line_numbers = diff.get(self.filename)
            if not line_numbers:
                return False
            return self.line_number in line_numbers


class DecisionEngine(object):
    __doc__ = 'A class for managing the decision process around violations.\n\n    This contains the logic for whether a violation should be reported or\n    ignored.\n    '

    def __init__(self, options):
        """Initialize the engine."""
        self.cache = {}
        self.selected = tuple(options.select)
        self.extended_selected = tuple(sorted((options.extended_default_select), reverse=True))
        self.enabled_extensions = tuple(options.enable_extensions)
        self.all_selected = tuple(sorted((self.selected + self.enabled_extensions), reverse=True))
        self.ignored = tuple(sorted((itertools.chain(options.ignore, options.extend_ignore)),
          reverse=True))
        self.using_default_ignore = set(self.ignored) == set(defaults.IGNORE)
        self.using_default_select = set(self.selected) == set(defaults.SELECT)

    def _in_all_selected(self, code):
        return self.all_selected and code.startswith(self.all_selected)

    def _in_extended_selected(self, code):
        return self.extended_selected and code.startswith(self.extended_selected)

    def was_selected(self, code):
        """Determine if the code has been selected by the user.

        :param str code:
            The code for the check that has been run.
        :returns:
            Selected.Implicitly if the selected list is empty,
            Selected.Explicitly if the selected list is not empty and a match
            was found,
            Ignored.Implicitly if the selected list is not empty but no match
            was found.
        """
        if self._in_all_selected(code):
            return Selected.Explicitly
        else:
            if not self.all_selected:
                if self._in_extended_selected(code):
                    return Selected.Implicitly
            return Ignored.Implicitly

    def was_ignored(self, code):
        """Determine if the code has been ignored by the user.

        :param str code:
            The code for the check that has been run.
        :returns:
            Selected.Implicitly if the ignored list is empty,
            Ignored.Explicitly if the ignored list is not empty and a match was
            found,
            Selected.Implicitly if the ignored list is not empty but no match
            was found.
        """
        if self.ignored:
            if code.startswith(self.ignored):
                return Ignored.Explicitly
        return Selected.Implicitly

    def more_specific_decision_for(self, code):
        select = find_first_match(code, self.all_selected)
        extra_select = find_first_match(code, self.extended_selected)
        ignore = find_first_match(code, self.ignored)
        if select and ignore:
            if self.using_default_ignore:
                if not self.using_default_select:
                    return Decision.Selected
            return find_more_specific(select, ignore)
        else:
            if extra_select:
                if ignore:
                    return find_more_specific(extra_select, ignore)
                else:
                    if select or extra_select and self.using_default_select:
                        return Decision.Selected
                    if select is None:
                        if extra_select is None or not self.using_default_ignore:
                            return Decision.Ignored
            else:
                if select is None:
                    if not self.using_default_select:
                        if ignore is None:
                            if self.using_default_ignore:
                                return Decision.Ignored
            return Decision.Selected

    def make_decision(self, code):
        """Decide if code should be ignored or selected."""
        LOG.debug('Deciding if "%s" should be reported', code)
        selected = self.was_selected(code)
        ignored = self.was_ignored(code)
        LOG.debug('The user configured "%s" to be "%s", "%s"', code, selected, ignored)
        if selected is Selected.Explicitly or selected is Selected.Implicitly:
            if ignored is Selected.Implicitly:
                decision = Decision.Selected
        if selected is Selected.Explicitly and ignored is Ignored.Explicitly or selected is Ignored.Implicitly and ignored is Selected.Implicitly:
            decision = self.more_specific_decision_for(code)
        else:
            if selected is Ignored.Implicitly or ignored is Ignored.Explicitly:
                decision = Decision.Ignored
        return decision

    def decision_for(self, code):
        """Return the decision for a specific code.

        This method caches the decisions for codes to avoid retracing the same
        logic over and over again. We only care about the select and ignore
        rules as specified by the user in their configuration files and
        command-line flags.

        This method does not look at whether the specific line is being
        ignored in the file itself.

        :param str code:
            The code for the check that has been run.
        """
        decision = self.cache.get(code)
        if decision is None:
            decision = self.make_decision(code)
            self.cache[code] = decision
            LOG.debug('"%s" will be "%s"', code, decision)
        return decision


class StyleGuideManager(object):
    __doc__ = 'Manage multiple style guides for a single run.'

    def __init__(self, options, formatter, decider=None):
        """Initialize our StyleGuide.

        .. todo:: Add parameter documentation.
        """
        self.options = options
        self.formatter = formatter
        self.stats = statistics.Statistics()
        self.decider = decider or DecisionEngine(options)
        self.style_guides = []
        self.default_style_guide = StyleGuide(options,
          formatter, (self.stats), decider=decider)
        self.style_guides = list(itertools.chain([
         self.default_style_guide], self.populate_style_guides_with(options)))

    def populate_style_guides_with(self, options):
        """Generate style guides from the per-file-ignores option.

        :param options:
            The original options parsed from the CLI and config file.
        :type options:
            :class:`~optparse.Values`
        :returns:
            A copy of the default style guide with overridden values.
        :rtype:
            :class:`~flake8.style_guide.StyleGuide`
        """
        per_file = utils.parse_files_to_codes_mapping(options.per_file_ignores)
        for filename, violations in per_file:
            yield self.default_style_guide.copy(filename=filename,
              extend_ignore_with=violations)

    @lru_cache(maxsize=None)
    def style_guide_for(self, filename):
        """Find the StyleGuide for the filename in particular."""
        guides = sorted((g for g in self.style_guides if g.applies_to(filename)),
          key=(lambda g: len(g.filename or '')))
        if len(guides) > 1:
            return guides[(-1)]
        else:
            return guides[0]

    @contextlib.contextmanager
    def processing_file(self, filename):
        """Record the fact that we're processing the file's results."""
        guide = self.style_guide_for(filename)
        with guide.processing_file(filename):
            yield guide

    def handle_error(self, code, filename, line_number, column_number, text, physical_line=None):
        """Handle an error reported by a check.

        :param str code:
            The error code found, e.g., E123.
        :param str filename:
            The file in which the error was found.
        :param int line_number:
            The line number (where counting starts at 1) at which the error
            occurs.
        :param int column_number:
            The column number (where counting starts at 1) at which the error
            occurs.
        :param str text:
            The text of the error message.
        :param str physical_line:
            The actual physical line causing the error.
        :returns:
            1 if the error was reported. 0 if it was ignored. This is to allow
            for counting of the number of errors found that were not ignored.
        :rtype:
            int
        """
        guide = self.style_guide_for(filename)
        return guide.handle_error(code, filename, line_number, column_number, text, physical_line)

    def add_diff_ranges(self, diffinfo):
        """Update the StyleGuides to filter out information not in the diff.

        This provides information to the underlying StyleGuides so that only
        the errors in the line number ranges are reported.

        :param dict diffinfo:
            Dictionary mapping filenames to sets of line number ranges.
        """
        for guide in self.style_guides:
            guide.add_diff_ranges(diffinfo)


class StyleGuide(object):
    __doc__ = "Manage a Flake8 user's style guide."

    def __init__(self, options, formatter, stats, filename=None, decider=None):
        """Initialize our StyleGuide.

        .. todo:: Add parameter documentation.
        """
        self.options = options
        self.formatter = formatter
        self.stats = stats
        self.decider = decider or DecisionEngine(options)
        self.filename = filename
        if self.filename:
            self.filename = utils.normalize_path(self.filename)
        self._parsed_diff = {}

    def __repr__(self):
        """Make it easier to debug which StyleGuide we're using."""
        return '<StyleGuide [{}]>'.format(self.filename)

    def copy(self, filename=None, extend_ignore_with=None, **kwargs):
        """Create a copy of this style guide with different values."""
        filename = filename or self.filename
        options = copy.deepcopy(self.options)
        options.ignore.extend(extend_ignore_with or [])
        return StyleGuide(options,
          (self.formatter), (self.stats), filename=filename)

    @contextlib.contextmanager
    def processing_file(self, filename):
        """Record the fact that we're processing the file's results."""
        self.formatter.beginning(filename)
        yield self
        self.formatter.finished(filename)

    def applies_to(self, filename):
        """Check if this StyleGuide applies to the file.

        :param str filename:
            The name of the file with violations that we're potentially
            applying this StyleGuide to.
        :returns:
            True if this applies, False otherwise
        :rtype:
            bool
        """
        if self.filename is None:
            return True
        else:
            return utils.matches_filename(filename,
              patterns=[
             self.filename],
              log_message=('{!r} does %(whether)smatch "%(path)s"'.format(self)),
              logger=LOG)

    def should_report_error(self, code):
        """Determine if the error code should be reported or ignored.

        This method only cares about the select and ignore rules as specified
        by the user in their configuration files and command-line flags.

        This method does not look at whether the specific line is being
        ignored in the file itself.

        :param str code:
            The code for the check that has been run.
        """
        return self.decider.decision_for(code)

    def handle_error(self, code, filename, line_number, column_number, text, physical_line=None):
        """Handle an error reported by a check.

        :param str code:
            The error code found, e.g., E123.
        :param str filename:
            The file in which the error was found.
        :param int line_number:
            The line number (where counting starts at 1) at which the error
            occurs.
        :param int column_number:
            The column number (where counting starts at 1) at which the error
            occurs.
        :param str text:
            The text of the error message.
        :param str physical_line:
            The actual physical line causing the error.
        :returns:
            1 if the error was reported. 0 if it was ignored. This is to allow
            for counting of the number of errors found that were not ignored.
        :rtype:
            int
        """
        disable_noqa = self.options.disable_noqa
        if not column_number:
            column_number = 0
        error = Violation(code, filename, line_number, column_number + 1, text, physical_line)
        error_is_selected = self.should_report_error(error.code) is Decision.Selected
        is_not_inline_ignored = error.is_inline_ignored(disable_noqa) is False
        is_included_in_diff = error.is_in(self._parsed_diff)
        if error_is_selected and is_not_inline_ignored and is_included_in_diff:
            self.formatter.handle(error)
            self.stats.record(error)
            return 1
        else:
            return 0

    def add_diff_ranges(self, diffinfo):
        """Update the StyleGuide to filter out information not in the diff.

        This provides information to the StyleGuide so that only the errors
        in the line number ranges are reported.

        :param dict diffinfo:
            Dictionary mapping filenames to sets of line number ranges.
        """
        self._parsed_diff = diffinfo


def find_more_specific(selected, ignored):
    if selected.startswith(ignored):
        if selected != ignored:
            return Decision.Selected
    return Decision.Ignored


def find_first_match(error_code, code_list):
    startswith = error_code.startswith
    for code in code_list:
        if startswith(code):
            break
    else:
        return

    return code