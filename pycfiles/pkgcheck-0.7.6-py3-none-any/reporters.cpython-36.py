# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/reporters.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 15621 bytes
"""Basic result reporters."""
import csv, json, os, pickle, signal
from collections import defaultdict
from itertools import chain
from multiprocessing import Process, SimpleQueue
from xml.sax.saxutils import escape as xml_escape
from snakeoil import pickling
from snakeoil.decorators import coroutine
from . import base, objects, results

class _ResultsIter:
    __doc__ = 'Iterator handling exceptions within queued results.\n\n    Due to the parallelism of check running, all results are pushed into the\n    results queue as lists of result objects or exception tuples. This iterator\n    forces exceptions to be handled explicitly, by outputting the serialized\n    traceback and signaling scanning processes to end when an exception object\n    is found.\n    '

    def __init__(self, results_q):
        self.pid = os.getpid()
        self.iter = iter(results_q.get, None)

    def __iter__(self):
        return self

    def __next__(self):
        while 1:
            results = next(self.iter)
            if results:
                if isinstance(results, tuple):
                    exc, tb = results
                    print(tb.strip())
                    os.kill(self.pid, signal.SIGINT)
                    return
                break

        return results


class Reporter:
    __doc__ = 'Generic result reporter.'

    def __init__(self, out, verbosity=0, keywords=None):
        """Initialize

        :type out: L{snakeoil.formatters.Formatter}
        :param keywords: result keywords to report, other keywords will be skipped
        """
        self.out = out
        self.verbosity = verbosity
        self._filtered_keywords = set(keywords) if keywords is not None else keywords
        self.report = self._add_report().send
        self.process = self._process_report().send

    def __call__(self, pipe, sort=False):
        results_q = SimpleQueue()
        orig_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_DFL)
        results_iter = _ResultsIter(results_q)
        p = Process(target=(pipe.run), args=(results_q,))
        p.start()
        signal.signal(signal.SIGINT, orig_sigint_handler)
        if pipe.pkg_scan or sort:
            results = set(chain.from_iterable(results_iter))
            for result in sorted(results):
                self.report(result)

        else:
            ordered_results = {scope:[] for scope in reversed(list(base.scopes.values())) if scope.level <= base.repo_scope if scope.level <= base.repo_scope}
            for results in results_iter:
                for result in sorted(results):
                    try:
                        ordered_results[result.scope].append(result)
                    except KeyError:
                        self.report(result)

            for result in chain.from_iterable(sorted(x) for x in ordered_results.values()):
                self.report(result)

        p.join()

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, *excinfo):
        self._finish()
        self.out.stream.flush()

    @coroutine
    def _add_report(self):
        """Add a report result to be processed for output."""
        while 1:
            result = yield
            if self._filtered_keywords is None or result.__class__ in self._filtered_keywords:
                if self.verbosity < 1:
                    if result._filtered:
                        continue
                self.process(result)

    @coroutine
    def _process_report(self):
        """Render and output a report result.."""
        raise NotImplementedError(self._process_report)

    def _start(self):
        """Initialize reporter output."""
        pass

    def _finish(self):
        """Finalize reporter output."""
        pass


class StrReporter(Reporter):
    __doc__ = 'Simple string reporter, pkgcheck-0.1 behaviour.\n\n    Example::\n\n        sys-apps/portage-2.1-r2: sys-apps/portage-2.1-r2.ebuild has whitespace in indentation on line 169\n        sys-apps/portage-2.1-r2: rdepend  ppc-macos: unsolvable default-darwin/macos/10.4, solutions: [ >=app-misc/pax-utils-0.1.13 ]\n        sys-apps/portage-2.1-r2: no change in 75 days, keywords [ ~x86-fbsd ]\n    '
    priority = 0

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._scope_prefix_map = {base.version_scope: '{category}/{package}-{version}: ', 
         base.package_scope: '{category}/{package}: ', 
         base.category_scope: '{category}: '}

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            prefix = (self._scope_prefix_map.get(result.scope, '').format)(**vars(result))
            self.out.write(f"{prefix}{result.desc}")
            self.out.stream.flush()


class FancyReporter(Reporter):
    __doc__ = 'Colored output grouped by result scope.\n\n    Example::\n\n        sys-apps/portage\n          WrongIndentFound: sys-apps/portage-2.1-r2.ebuild has whitespace in indentation on line 169\n          NonsolvableDeps: sys-apps/portage-2.1-r2: rdepend  ppc-macos: unsolvable default-darwin/macos/10.4, solutions: [ >=app-misc/pax-utils-0.1.13 ]\n          StableRequest: sys-apps/portage-2.1-r2: no change in 75 days, keywords [ ~x86 ]\n    '
    priority = 1

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.key = None

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            if result.scope in (base.version_scope, base.package_scope):
                key = f"{result.category}/{result.package}"
            else:
                if result.scope is base.category_scope:
                    key = result.category
                else:
                    key = str(result.scope)
            if key != self.key:
                if self.key is not None:
                    self.out.write()
                self.out.write(self.out.bold, key)
                self.key = key
            self.out.first_prefix.append('  ')
            self.out.later_prefix.append('    ')
            s = ''
            if result.scope is base.version_scope:
                s = f"version {result.version}: "
            self.out.write(self.out.fg(result.color), result.name, self.out.reset, ': ', s, result.desc)
            self.out.first_prefix.pop()
            self.out.later_prefix.pop()
            self.out.stream.flush()


class NullReporter(Reporter):
    __doc__ = 'Reporter used for timing tests; no output.'
    priority = -10000000

    @coroutine
    def _process_report(self):
        while True:
            _result = yield


class JsonReporter(Reporter):
    __doc__ = "Feed of newline-delimited JSON records.\n\n    Note that the format is newline-delimited JSON with each line being related\n    to a separate report. To merge the objects together a tool such as jq can\n    be leveraged similar to the following:\n\n    .. code::\n\n        jq -c -s 'reduce.[]as$x({};.*$x)' orig.json > new.json\n    "
    priority = -1000

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._json_dict = lambda : defaultdict(self._json_dict)
        self._scope_map = {base.version_scope: lambda data, r: data[r.category][r.package][r.version], 
         base.package_scope: lambda data, r: data[r.category][r.package], 
         base.category_scope: lambda data, r: data[r.category]}

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            data = self._json_dict()
            d = self._scope_map.get(result.scope, lambda x, y: x)(data, result)
            d[('_' + result.level)][result.name] = result.desc
            self.out.write(json.dumps(data))
            self.out.stream.flush()


class XmlReporter(Reporter):
    __doc__ = 'Feed of newline-delimited XML reports.'
    priority = -1000
    result_template = '<result><class>%(class)s</class><msg>%(msg)s</msg></result>'
    cat_template = '<result><category>%(category)s</category><class>%(class)s</class><msg>%(msg)s</msg></result>'
    pkg_template = '<result><category>%(category)s</category><package>%(package)s</package><class>%(class)s</class><msg>%(msg)s</msg></result>'
    ver_template = '<result><category>%(category)s</category><package>%(package)s</package><version>%(version)s</version><class>%(class)s</class><msg>%(msg)s</msg></result>'
    scope_map = {base.category_scope: cat_template, 
     base.package_scope: pkg_template, 
     base.version_scope: ver_template}

    def _start(self):
        self.out.write('<checks>')

    def _finish(self):
        self.out.write('</checks>')

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            d = {k:getattr(result, k, '') for k in ('category', 'package', 'version')}
            d['class'] = xml_escape(result.name)
            d['msg'] = xml_escape(result.desc)
            self.out.write(self.scope_map.get(result.scope, self.result_template) % d)


class CsvReporter(Reporter):
    __doc__ = 'Comma-separated value reporter, convenient for shell processing.\n\n    Example::\n\n        ,,,"global USE flag \'big-endian\' is a potential local, used by 1 package: dev-java/icedtea-bin"\n        sys-apps,portage,2.1-r2,sys-apps/portage-2.1-r2.ebuild has whitespace in indentation on line 169\n        sys-apps,portage,2.1-r2,"rdepend  ppc-macos: unsolvable default-darwin/macos/10.4, solutions: [ >=app-misc/pax-utils-0.1.13 ]"\n        sys-apps,portage,2.1-r2,"no change in 75 days, keywords [ ~x86-fbsd ]"\n    '
    priority = -1001

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._writer = csv.writer((self.out),
          doublequote=False,
          escapechar='\\',
          lineterminator='')

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            self._writer.writerow((
             getattr(result, 'category', ''),
             getattr(result, 'package', ''),
             getattr(result, 'version', ''),
             result.desc))


class FormatReporter(Reporter):
    __doc__ = 'Custom format string reporter.'
    priority = -1001

    def __init__(self, format_str, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.format_str = format_str
        self._properties = ('desc', 'level')

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            attrs = vars(result)
            attrs.update((k, getattr(result, k)) for k in self._properties)
            try:
                self.out.write((self.format_str.format)(**attrs))
                self.out.stream.flush()
            except KeyError:
                pass


class DeserializationError(Exception):
    __doc__ = 'Exception occurred while deserializing a data stream.'


class JsonStream(Reporter):
    __doc__ = 'Generate a stream of result objects serialized in JSON.'
    priority = -1001

    @staticmethod
    def to_json(obj):
        """Serialize results and other objects to JSON."""
        if isinstance(obj, results.Result):
            d = {'__class__': obj.__class__.__name__}
            d.update(obj._attrs)
            return d
        else:
            return str(obj)

    @staticmethod
    def from_json(data):
        """Deserialize JSON object to its corresponding result object."""
        try:
            d = json.loads(data)
        except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
            raise DeserializationError(f"failed loading: {data!r}") from e

        try:
            cls = objects.KEYWORDS[d.pop('__class__')]
        except KeyError:
            raise DeserializationError(f"missing result class: {data!r}")

        d = results.Result.attrs_to_pkg(d)
        try:
            return cls(**d)
        except TypeError as e:
            raise DeserializationError(f"failed loading: {data!r}") from e

    @classmethod
    def from_file(cls, f):
        """Deserialize results from a given file handle."""
        try:
            for i, line in enumerate(f, 1):
                yield cls.from_json(line)

        except DeserializationError as e:
            raise DeserializationError(f"invalid entry on line {i}") from e

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            self.out.write(json.dumps(result, default=(self.to_json)))


class PickleStream(Reporter):
    __doc__ = 'Generate a stream of pickled objects using the original pickling protocol.\n\n    For each specific target for checks, a header is pickled detailing the\n    checks used, possible results, and search criteria.\n\n    This reporter uses the original "human-readable" protocol that is backwards\n    compatible with earlier versions of Python.\n    '
    priority = -1001
    protocol = 0

    def _start(self):
        self.out.wrap = False
        self.out.autoline = False

    @staticmethod
    def from_file(f):
        """Deserialize results from a given file handle."""
        try:
            for result in pickling.iter_stream(f):
                if isinstance(result, results.Result):
                    yield result
                else:
                    raise DeserializationError(f"invalid data type: {result!r}")

        except pickle.UnpicklingError as e:
            raise DeserializationError('failed unpickling result') from e

    @coroutine
    def _process_report(self):
        while True:
            result = yield
            try:
                pickle.dump(result, self.out.stream, self.protocol)
            except (AttributeError, TypeError) as e:
                raise TypeError(result, str(e))


class BinaryPickleStream(PickleStream):
    __doc__ = "Dump a binary pickle stream using the highest pickling protocol.\n\n    Unlike `PickleStream`_ which uses the most compatible pickling protocol\n    available, this uses the newest version so it won't be compatible with\n    older versions of Python.\n\n    For more details of the stream, see `PickleStream`_.\n    "
    priority = -1002
    protocol = -1