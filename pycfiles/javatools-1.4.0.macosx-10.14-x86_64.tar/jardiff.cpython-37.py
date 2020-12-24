# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/jardiff.py
# Compiled at: 2018-12-14 21:30:42
# Size of source mod 2**32: 17646 bytes
"""
Utility script and module for producing a set of changes in a JAR
file. Takes the same options as the classdiff script, and in fact uses
the classdiff script's code on each non-identical member in a pair of
JAR files.

:author: Christopher O'Brien  <obriencj@gmail.com>
:licence: LGPL
"""
import sys
from argparse import ArgumentParser
from os.path import isdir
from . import unpack_class
from .change import GenericChange, SuperChange, Addition, Removal
from .change import squash, yield_sorted_by_type
from .classdiff import JavaClassChange, JavaClassReport
from .dirutils import fnmatches
from .manifest import Manifest, ManifestChange
from .manifest import SignatureManifestChange, SignatureBlockFileChange
from .manifest import file_matches_sigfile, file_matches_sigblock
from .ziputils import compare_zips, open_zip, open_zip_entry
from .ziputils import LEFT, RIGHT, DIFF, SAME
__all__ = ('JarChange', 'JarTypeChange', 'JarContentsChange', 'JarManifestChange',
           'JarContentChange', 'JarContentAdded', 'JarContentRemoved', 'JarSignatureFileChange',
           'JarSignatureFileAdded', 'JarSignatureFileRemoved', 'JarSignatureBlockFileChange',
           'JarSignatureBlockFileAdded', 'JarSignatureBlockFileRemoved', 'JarClassChange',
           'JarClassAdded', 'JarClassRemoved', 'JarReport', 'JarContentsReport',
           'JarClassReport', 'cli', 'main', 'cli_jars_diff', 'add_jardiff_optgroup',
           'default_jardiff_options')

class JarTypeChange(GenericChange):
    __doc__ = '\n    exploded vs. zipped and compression level\n    '
    label = 'Jar type'

    def fn_data(self, c):
        return isdir(c)

    def fn_pretty(self, c):
        if isdir(c):
            return 'exploded JAR'
        return 'zipped JAR file'


class JarContentChange(SuperChange):
    __doc__ = '\n    a file or directory changed between JARs\n    '
    label = 'Jar Content'

    def __init__(self, lzip, rzip, entry, is_change=True):
        super(JarContentChange, self).__init__(lzip, rzip)
        self.entry = entry
        self.changed = is_change

    def open_left(self):
        return open_zip_entry(self.ldata, self.entry)

    def open_right(self):
        return open_zip_entry(self.rdata, self.entry)

    def collect_impl(self):
        """
        Content changes refer to more concrete children, but by default
        are empty
        """
        return tuple()

    def get_description(self):
        c = 'has changed' if self.is_change() else 'is unchanged'
        return '%s %s: %s' % (self.label, c, self.entry)

    def is_ignored(self, options):
        return fnmatches(self.entry, *options.ignore_jar_entry) or super(JarContentChange, self).is_ignored(options)


class JarContentAdded(JarContentChange, Addition):
    label = 'Jar Content Added'

    def get_description(self):
        return '%s: %s' % (self.label, self.entry)


class JarContentRemoved(JarContentChange, Removal):
    label = 'Jar Content Removed'

    def get_description(self):
        return '%s: %s' % (self.label, self.entry)


class JarClassAdded(JarContentAdded):
    label = 'Java Class Added'


class JarClassRemoved(JarContentRemoved):
    label = 'Java Class Removed'


class JarClassChange(JarContentChange):
    label = 'Java Class'

    def collect_impl(self):
        if self.is_change():
            with self.open_left() as (lfd):
                linfo = unpack_class(lfd.read())
            with self.open_right() as (rfd):
                rinfo = unpack_class(rfd.read())
            yield JavaClassChange(linfo, rinfo)


class JarClassReport(JarClassChange):
    report_name = 'JavaClassReport'

    def __init__(self, l, r, entry, reporter):
        super(JarClassReport, self).__init__(l, r, entry)
        self.reporter = reporter

    def collect_impl(self):
        if self.is_change():
            with self.open_left() as (lfd):
                linfo = unpack_class(lfd.read())
            with self.open_right() as (rfd):
                rinfo = unpack_class(rfd.read())
            yield JavaClassReport(linfo, rinfo, self.reporter)


class JarManifestChange(JarContentChange):
    label = 'Jar Manifest'

    def collect_impl(self):
        if self.is_change():
            with self.open_left() as (lfd):
                lm = Manifest()
                lm.parse(lfd.read())
            with self.open_right() as (rfd):
                rm = Manifest()
                rm.parse(rfd.read())
            yield ManifestChange(lm, rm)


class JarSignatureFileChange(JarContentChange):
    label = 'Jar Signature File'

    def is_ignored(self, options):
        return options.ignore_jar_signature

    def collect_impl(self):
        if self.is_change():
            with self.open_left() as (lfd):
                lm = Manifest()
                lm.parse(lfd.read())
            with self.open_right() as (rfd):
                rm = Manifest()
                rm.parse(rfd.read())
            yield SignatureManifestChange(lm, rm)


class JarSignatureFileAdded(JarContentAdded):
    label = 'Jar Signature File Added'

    def is_ignored(self, options):
        return options.ignore_jar_signature


class JarSignatureFileRemoved(JarContentRemoved):
    label = 'Jar Signature File Removed'

    def is_ignored(self, options):
        return options.ignore_jar_signature


class JarSignatureBlockFileChange(JarContentChange):
    label = 'Jar Signature Block File'

    def is_ignored(self, options):
        return options.ignore_jar_signature

    def collect_impl(self):
        if self.is_change():
            with self.open_left() as (lfd):
                with self.open_right() as (rfd):
                    lsig = lfd.read()
                    rsig = rfd.read()
            yield SignatureBlockFileChange(lsig, rsig)


class JarSignatureBlockFileAdded(JarContentAdded):
    label = 'Jar Signature Block File Added'

    def is_ignored(self, options):
        return options.ignore_jar_signature


class JarSignatureBlockFileRemoved(JarContentRemoved):
    label = 'Jar Signature Block File Removed'

    def is_ignored(self, options):
        return options.ignore_jar_signature


class GenericFileChange(GenericChange):
    label = 'Generic File'

    def get_description(self):
        return '[generic file change]'

    def fn_pretty(self, side_data):
        return '[data]'


class JarGenericFileChange(JarContentChange):
    label = 'Jar Generic File'

    def collect_impl(self):
        if self.is_change():
            with self.open_left() as (lfd):
                with self.open_right() as (rfd):
                    lsig = lfd.read()
                    rsig = rfd.read()
            yield GenericFileChange(lsig, rsig)


class JarContentsChange(SuperChange):
    label = 'JAR Contents'

    def __init__(self, left_fn, right_fn):
        super(JarContentsChange, self).__init__(left_fn, right_fn)
        self.lzip = None
        self.rzip = None

    @yield_sorted_by_type(JarManifestChange, JarSignatureFileAdded, JarSignatureFileRemoved, JarSignatureFileChange, JarSignatureBlockFileAdded, JarSignatureBlockFileRemoved, JarSignatureBlockFileChange, JarGenericFileChange, JarContentAdded, JarContentRemoved, JarContentChange, JarClassAdded, JarClassRemoved, JarClassChange)
    def collect_impl(self):
        left = self.lzip
        right = self.rzip
        assert left is not None
        assert right is not None
        for event, entry in compare_zips(left, right):
            if event == SAME:
                if entry == 'META-INF/MANIFEST.MF':
                    yield JarManifestChange(left, right, entry, False)
                else:
                    if file_matches_sigfile(entry):
                        yield JarSignatureFileChange(left, right, entry, False)
                    else:
                        if file_matches_sigblock(entry):
                            yield JarSignatureBlockFileChange(left, right, entry, False)
                        else:
                            if fnmatches(entry, '*.class'):
                                yield JarClassChange(left, right, entry, False)
                            else:
                                yield JarContentChange(left, right, entry, False)
            elif event == DIFF:
                if entry == 'META-INF/MANIFEST.MF':
                    yield JarManifestChange(left, right, entry)
                else:
                    if file_matches_sigfile(entry):
                        yield JarSignatureFileChange(left, right, entry)
                    else:
                        if file_matches_sigblock(entry):
                            yield JarSignatureBlockFileChange(left, right, entry)
                        else:
                            if fnmatches(entry, '*.class'):
                                yield JarClassChange(left, right, entry)
                            else:
                                yield JarGenericFileChange(left, right, entry)
            else:
                if event == LEFT:
                    if file_matches_sigfile(entry):
                        yield JarSignatureFileRemoved(left, right, entry)
                    else:
                        if file_matches_sigblock(entry):
                            yield JarSignatureBlockFileRemoved(left, right, entry)
                        else:
                            if fnmatches(entry, '*.class'):
                                yield JarClassRemoved(left, right, entry)
                            else:
                                yield JarContentRemoved(left, right, entry)

    def check_impl(self):
        with open_zip(self.ldata) as (lzip):
            with open_zip(self.rdata) as (rzip):
                self.lzip = lzip
                self.rzip = rzip
                ret = super(JarContentsChange, self).check_impl()
        self.lzip = None
        self.rzip = None
        return ret


class JarChange(SuperChange):
    label = 'JAR'
    change_types = (
     JarTypeChange,
     JarContentsChange)


class JarContentsReport(JarContentsChange):
    __doc__ = '\n    overridden JarContentsChange which will swap out JarClassChange\n    with JarClassReport instances. The check_impl method gains the\n    side effect of causing all JarClassReports gathered to write\n    reports of themselves to file.\n    '

    def __init__(self, left_fn, right_fn, reporter):
        super(JarContentsReport, self).__init__(left_fn, right_fn)
        self.reporter = reporter

    def collect_impl(self):
        for change in JarContentsChange.collect_impl(self):
            if isinstance(change, JarClassChange):
                if change.is_change():
                    name = JarClassReport.report_name
                    sub_r = self.reporter.subreporter(change.entry, name)
                    change = JarClassReport(change.ldata, change.rdata, change.entry, sub_r)
            yield change

    def check_impl(self):
        options = self.reporter.options
        changes = list()
        c = False
        with open_zip(self.ldata) as (lzip):
            with open_zip(self.rdata) as (rzip):
                self.lzip = lzip
                self.rzip = rzip
                for change in self.collect_impl():
                    change.check()
                    c = c or change.is_change()
                    if isinstance(change, JarClassReport):
                        changes.append(squash(change, options=options))
                        change.clear()
                    else:
                        changes.append(change)

        self.lzip = None
        self.rzip = None
        self.changes = changes
        return (c, None)


class JarReport(JarChange):
    __doc__ = '\n    This class has side-effects. Running the check method with the\n    reportdir options set to True will cause the deep checks to be\n    written to file in that directory\n    '
    report_name = 'JarReport'

    def __init__(self, l, r, reporter):
        super(JarReport, self).__init__(l, r)
        self.reporter = reporter

    def collect_impl(self):
        for c in JarChange.collect_impl(self):
            if isinstance(c, JarContentsChange):
                c = JarContentsReport(c.ldata, c.rdata, self.reporter)
            yield c

    def check(self):
        JarChange.check(self)
        self.reporter.run(self)


def cli_jars_diff(options, left, right):
    from .report import quick_report, Reporter
    from .report import JSONReportFormat, TextReportFormat
    reports = getattr(options, 'reports', tuple())
    if reports:
        rdir = options.report_dir or './'
        rpt = Reporter(rdir, JarReport.report_name, options)
        rpt.add_formats_by_name(reports)
        delta = JarReport(left, right, rpt)
    else:
        delta = JarChange(left, right)
    delta.check()
    if not options.silent:
        if options.json:
            quick_report(JSONReportFormat, delta, options)
        else:
            quick_report(TextReportFormat, delta, options)
    if not delta.is_change() or delta.is_ignored(options):
        return 0
    return 1


def cli(options):
    left, right = options.jar
    return cli_jars_diff(options, left, right)


def add_jardiff_optgroup(parser):
    """
    option group specific to the tests in jardiff
    """
    og = parser.add_argument_group('JAR Checking Options')
    og.add_argument('--ignore-jar-entry', action='append', default=[])
    og.add_argument('--ignore-jar-signature', action='store_true',
      default=False,
      help='Ignore JAR signing changes')
    og.add_argument('--ignore-manifest', action='store_true',
      default=False,
      help='Ignore changes to manifests')
    og.add_argument('--ignore-manifest-subsections', action='store_true',
      default=False,
      help='Ignore changes to manifest subsections')
    og.add_argument('--ignore-manifest-key', action='append',
      default=[],
      help='case-insensitive manifest keys to ignore')


def create_optparser(progname=None):
    """
    an OptionParser instance with the appropriate options and groups
    for the jardiff utility
    """
    from .classdiff import add_general_optgroup, add_classdiff_optgroup
    from javatools import report
    parser = ArgumentParser(prog=progname)
    parser.add_argument('jar', nargs=2, help='JAR files to compare')
    add_general_optgroup(parser)
    add_jardiff_optgroup(parser)
    add_classdiff_optgroup(parser)
    report.add_general_report_optgroup(parser)
    report.add_json_report_optgroup(parser)
    report.add_html_report_optgroup(parser)
    return parser


def default_jardiff_options(updates=None):
    """
    generate an options object with the appropriate default values in
    place for API usage of jardiff features. overrides is an optional
    dictionary which will be used to update fields on the options
    object.
    """
    parser = create_optparser()
    options, _args = parser.parse_args(list())
    if updates:
        options._update_careful(updates)
    return options


def main(args=sys.argv):
    """
    main entry point for the jardiff CLI
    """
    parser = create_optparser(args[0])
    return cli(parser.parse_args(args[1:]))