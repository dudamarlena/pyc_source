# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/report.py
# Compiled at: 2019-06-21 15:26:13
# Size of source mod 2**32: 17322 bytes
"""
Classes for representing changes as formatted text.

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: LGPL
"""
from __future__ import print_function
import sys
from abc import ABCMeta, abstractmethod
from argparse import Action
import Cheetah.DummyTransaction as DummyTransaction
from functools import partial
from json import dump, JSONEncoder
from os.path import exists, join, relpath
from six import add_metaclass
from six.moves import range
from .dirutils import copydir, makedirsp
_BUFFERING = 65536
__all__ = ('Reporter', 'ReportFormat', 'quick_report', 'add_general_report_optgroup',
           'JSONReportFormat', 'add_json_report_optgroup', 'TextReportFormat', 'CheetahReportFormat',
           'add_html_report_optgroup')

class Reporter(object):
    __doc__ = '\n    Collects multiple report formats for use in presenting a change\n    '

    def __init__(self, basedir, entry, options):
        self.basedir = basedir
        self.entry = entry
        self.options = options
        self.breadcrumbs = tuple()
        self.formats = set()
        self._formats = None

    def get_relative_breadcrumbs(self):
        """
        get the breadcrumbs as relative to the basedir
        """
        basedir = self.basedir
        crumbs = self.breadcrumbs
        return [(relpath(b, basedir), e) for b, e in crumbs]

    def add_formats_by_name(self, rfmt_list):
        """
        adds formats by short label descriptors, such as 'txt', 'json', or
        'html'
        """
        for fmt in rfmt_list:
            if fmt == 'json':
                self.add_report_format(JSONReportFormat)
            else:
                if fmt in ('txt', 'text'):
                    self.add_report_format(TextReportFormat)

    def add_report_format(self, report_format):
        """
        Add an output format to this reporter. report_format should be a
        ReportFormat subtype. It will be instantiated when the
        reporter is run.
        """
        self.formats.add(report_format)

    def subreporter(self, subpath, entry):
        """
        create a reporter for a sub-report, with updated breadcrumbs and
        the same output formats
        """
        newbase = join(self.basedir, subpath)
        r = Reporter(newbase, entry, self.options)
        crumbs = list(self.breadcrumbs)
        crumbs.append((self.basedir, self.entry))
        r.breadcrumbs = crumbs
        r.formats = set(self.formats)
        return r

    def setup(self):
        """
        instantiates all report formats that have been added to this
        reporter, and calls their setup methods.
        """
        if self._formats:
            return
        basedir = self.basedir
        options = self.options
        crumbs = self.get_relative_breadcrumbs()
        fmts = list()
        for fmt_class in self.formats:
            fmt = fmt_class(basedir, options, crumbs)
            fmt.setup()
            fmts.append(fmt)

        self._formats = fmts

    def run(self, change):
        """
        runs the report format instances in this reporter. Will call setup
        if it hasn't been called already
        """
        if self._formats is None:
            self.setup()
        entry = self.entry
        for fmt in self._formats:
            fmt.run(change, entry)

        self.clear()

    def clear(self):
        """
        calls clear on any report format instances created during setup
        and drops the cache
        """
        if self._formats:
            for fmt in self._formats:
                fmt.clear()

        self._formats = None


@add_metaclass(ABCMeta)
class ReportFormat(object):
    __doc__ = '\n    Base class of a report format provider. Override to describe a\n    concrete format type\n    '
    extension = '.report'

    def __init__(self, basedir, options, breadcrumbs=tuple()):
        self.basedir = basedir
        self.options = options
        self.breadcrumbs = breadcrumbs

    @abstractmethod
    def run_impl(self, change, entry, out):
        """
        override to actually produce output
        """
        pass

    def run(self, change, entry, out=None):
        """
        setup for run, including creating an output file if needed. Calls
        run_impl when ready. If out and entry are both None,
        sys.stdout is used
        """
        if out:
            self.run_impl(change, entry, out)
            return
        if entry:
            basedir = self.basedir or './'
            makedirsp(basedir)
            fn = join(basedir, entry + self.extension)
            with open(fn, 'wt', _BUFFERING) as (out):
                self.run_impl(change, entry, out)
            return fn
        self.run_impl(change, entry, sys.stdout)
        return

    def setup(self):
        """
        override if the report format has behavior which can be done ahead
        of time, such as copying files or creating directories
        """
        pass

    def clear(self):
        """
        clear up the internal references of this format. Called by the
        parent reporter at the end of run
        """
        self.basedir = None
        self.options = None
        self.breadcrumbs = None


class _opt_cb_report(Action):
    __doc__ = '\n    callback for the --report option in general_report_optgroup\n    '

    def __call__(self, parser, options, values, option_string=None):
        if not hasattr(options, 'reports'):
            options.reports = list()
        elif ',' in values:
            options.reports.extend((v for v in values.split(',') if v))
        else:
            options.reports.append(values)


def add_general_report_optgroup(parser):
    """
    General Reporting Options
    """
    g = parser.add_argument_group('Reporting Options')
    g.add_argument('--report-dir', action='store', default=None)
    g.add_argument('--report', action=_opt_cb_report, help='comma-separated list of report formats')


class JSONReportFormat(ReportFormat):
    __doc__ = '\n    renders a Change and all of its children to a JSON object. Can use\n    options from the jon_report_optgroup option group\n    '
    extension = '.json'

    def run_impl(self, change, entry, out):
        options = self.options
        indent = getattr(options, 'json_indent', 2)
        data = {'runtime_options':options.__dict__, 
         'report':change}
        cls = partial(JSONChangeEncoder, options)
        try:
            dump(data, out, sort_keys=True, indent=indent, cls=cls)
        except TypeError:
            print(data)
            raise


def add_json_report_optgroup(parser):
    """
    Option group for the JSON report format
    """
    g = parser.add_argument_group('JSON Report Options')
    g.add_argument('--json-indent', action='store', default=2, type=int)


class JSONChangeEncoder(JSONEncoder):
    __doc__ = '\n    A specialty JSONEncoder which knows how to represent Change\n    instances (or anything with a simplify method), and sequences (by\n    rendering them into tuples)\n    '

    def __init__(self, options, *a, **k):
        (JSONEncoder.__init__)(self, *a, **k)
        self.options = options

    def default(self, o):
        if hasattr(o, 'simplify'):
            return o.simplify(self.options)
        try:
            i = iter(o)
        except TypeError:
            return JSONEncoder.default(self, o)
        else:
            return tuple(i)


class TextReportFormat(ReportFormat):
    __doc__ = '\n    Renders the change as indented text\n    '
    extension = '.text'

    def run_impl(self, change, entry, out):
        options = self.options
        _indent_change(change, out, options, 0)


def _indent_change(change, out, options, indent):
    """
    recursive function to print indented change descriptions
    """
    show_unchanged = getattr(options, 'show_unchanged', False)
    show_ignored = getattr(options, 'show_ignored', False)
    show = False
    desc = change.get_description()
    if change.is_change():
        if change.is_ignored(options):
            if show_ignored:
                show = True
                _indent(out, indent, desc, ' [IGNORED]')
        else:
            show = True
            _indent(out, indent, desc)
    else:
        if show_unchanged:
            show = True
            _indent(out, indent, desc)
    if show:
        indent += 1
        for sub in change.collect():
            _indent_change(sub, out, options, indent)


def _indent(stream, indent, *msgs):
    """ write a message to a text stream, with indentation. Also ensures that
    the output encoding of the messages is safe for writing. """
    for x in range(0, indent):
        stream.write('  ')

    for x in msgs:
        stream.write(x.encode('ascii', 'backslashreplace').decode('ascii'))

    stream.write('\n')


class CheetahReportFormat(ReportFormat):
    __doc__ = '\n    HTML output for a Change\n    '
    extension = '.html'

    def _relative--- This code section failed: ---

 L. 414         0  LOAD_FAST                'uri'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 'http:'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_TRUE     40  'to 40'

 L. 415        10  LOAD_FAST                'uri'
               12  LOAD_METHOD              startswith
               14  LOAD_STR                 'https:'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_JUMP_IF_TRUE     40  'to 40'

 L. 416        20  LOAD_FAST                'uri'
               22  LOAD_METHOD              startswith
               24  LOAD_STR                 'file:'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  POP_JUMP_IF_TRUE     40  'to 40'

 L. 417        30  LOAD_FAST                'uri'
               32  LOAD_METHOD              startswith
               34  LOAD_STR                 '/'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_JUMP_IF_FALSE    44  'to 44'
             40_0  COME_FROM            28  '28'
             40_1  COME_FROM            18  '18'
             40_2  COME_FROM             8  '8'

 L. 418        40  LOAD_FAST                'uri'
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L. 420        44  LOAD_GLOBAL              exists
               46  LOAD_FAST                'uri'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  POP_JUMP_IF_FALSE    64  'to 64'

 L. 421        52  LOAD_GLOBAL              relpath
               54  LOAD_FAST                'uri'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                basedir
               60  CALL_FUNCTION_2       2  '2 positional arguments'
               62  RETURN_VALUE     
             64_0  COME_FROM            50  '50'

 L. 424        64  LOAD_FAST                'uri'
               66  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 64

    def _relative_uris(self, uri_list):
        """
        if uris in list are relative, re-relate them to our basedir
        """
        return [u for u in (self._relative(uri) for uri in uri_list) if u]

    def setup(self):
        """
        copies default stylesheets and javascript files if necessary, and
        appends them to the options
        """
        from javatools import cheetah
        options = self.options
        datadir = getattr(options, 'html_copy_data', None)
        return getattr(options, 'html_data_copied', False) or datadir or None
        datasrc = join(cheetah.__path__[0], 'data')
        javascripts = list()
        stylesheets = list()
        for _orig, copied in copydir(datasrc, datadir):
            if copied.endswith('.js'):
                javascripts.append(copied)

        javascripts.extend(getattr(options, 'html_javascripts', tuple()))
        stylesheets.extend(getattr(options, 'html_stylesheets', tuple()))
        options.html_javascripts = javascripts
        options.html_stylesheets = stylesheets
        options.html_data_copied = True

    def run_impl(self, change, entry, out):
        """
        sets up the report directory for an HTML report. Obtains the
        top-level Cheetah template that is appropriate for the change
        instance, and runs it.

        The cheetah templates are supplied the following values:
         * change - the Change instance to report on
         * entry - the string name of the entry for this report
         * options - the cli options object
         * breadcrumbs - list of backlinks
         * javascripts - list of .js links
         * stylesheets - list of .css links

        The cheetah templates are also given a render_change method
        which can be called on another Change instance to cause its
        template to be resolved and run in-line.
        """
        options = self.options
        javascripts = self._relative_uris(options.html_javascripts)
        stylesheets = self._relative_uris(options.html_stylesheets)
        template_class = resolve_cheetah_template(type(change))
        template = template_class()
        template.transaction = DummyTransaction()
        template.transaction.response(resp=out)
        template.change = change
        template.entry = entry
        template.options = options
        template.breadcrumbs = self.breadcrumbs
        template.javascripts = javascripts
        template.stylesheets = stylesheets
        template.render_change = lambda c: self.run_impl(c, entry, out)
        template.respond()
        template.shutdown()


def _compose_cheetah_template_map(cache):
    """
    does the work of composing the cheetah template map into the given
    cache
    """
    from .cheetah import get_templates
    import javatools
    for template_type in get_templates():
        if '_' not in template_type.__name__:
            continue
        tn = template_type.__name__
        pn, cn = tn.split('_', 1)
        pk = getattr(javatools, pn, None)
        if pk is None:
            __import__('javatools.' + pn)
            pk = getattr(javatools, pn, None)
        cc = getattr(pk, cn, None)
        if cc is None:
            raise Exception('no change class for template %s' % tn)
        cache[cc] = template_type

    return cache


_template_cache = dict()

def cheetah_template_map(cache=None):
    """
    a map of change types to cheetah template types. Used in
    resolve_cheetah_template
    """
    if cache is None:
        cache = _template_cache
    return cache or _compose_cheetah_template_map(cache)


def resolve_cheetah_template(change_type):
    """
    return the appropriate cheetah template class for the given change
    type, using the method-resolution-order of the change type.
    """
    tm = cheetah_template_map()
    for t in change_type.mro():
        tmpl = tm.get(t)
        if tmpl:
            return tmpl

    raise Exception('No template for class %s' % change_type.__name__)


def add_html_report_optgroup(parser):
    """
    Option group for the HTML report format
    """
    g = parser.add_argument_group('HTML Report Options')
    g.add_argument('--html-stylesheet', action='append', dest='html_stylesheets',
      default=(list()))
    g.add_argument('--html-javascript', action='append', dest='html_javascripts',
      default=(list()))
    g.add_argument('--html-copy-data', action='store', default=None, help='Copy default resources to the given directory and enable them in the template')


def quick_report(report_type, change, options):
    """
    writes a change report via report_type to options.output or
    sys.stdout
    """
    report = report_type(None, options)
    if options.output:
        with open(options.output, 'w') as (out):
            report.run(change, None, out)
    else:
        report.run(change, None, sys.stdout)