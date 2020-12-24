# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/nose_profile/__init__.py
# Compiled at: 2012-09-02 08:28:04
"""This plugin will run tests using the cProfile profiler, which is part of the
standard library for Python >= 2.5. To turn it on, use the ``--with-calltree``
option or set the NOSE_WITH_CALLTREE environment variable. Profiler output can
be controlled with the ``--calltree-sort`` and ``--calltree-restrict`` options,
and the profiler output file may be changed with ``--calltree-stats-file``.

Profile output format is compatible with KCacheGrind.

See the `hotshot documentation`_ in the standard library documentation for
more details on the various output options.

.. _hotshot documentation: http://docs.python.org/library/hotshot.html
"""
import optparse, os, os.path, sys, logging, tempfile
try:
    import cProfile, pstats
except ImportError:
    cProfile, pstats = (None, None)

from nose.plugins.base import Plugin
from nose.util import tolist
from kcachegrind import KCacheGrind
log = logging.getLogger('nose.plugins')

class CallTree(Plugin):
    """
    Use this plugin to run tests using the hotshot profiler. 
    """
    pfile = None
    clean_stats_file = False

    def options(self, parser, env):
        """Register commandline options.
        """
        if not self.available():
            return
        Plugin.options(self, parser, env)
        parser.add_option('--calltree-sort', action='store', dest='calltree_sort', default=env.get('NOSE_CALLTREE_SORT', 'cumulative'), metavar='SORT', help='Set sort order for profiler output')
        parser.add_option('--calltree-stats-file', action='store', dest='calltree_stats_file', metavar='FILE', default=env.get('NOSE_CALLTREE_STATS_FILE'), help='Profiler stats file; default is a new temp file on each run')
        parser.add_option('--calltree-restrict', action='append', dest='calltree_restrict', metavar='RESTRICT', default=env.get('NOSE_CALLTREE_RESTRICT'), help='Restrict profiler output. See help for pstats.Stats for details')

    def available(cls):
        return cProfile is not None

    available = classmethod(available)

    def begin(self):
        """Create profile stats file and load profiler.
        """
        if not self.available():
            return
        self.prof = cProfile.Profile()

    def configure(self, options, conf):
        """Configure plugin.
        """
        if not self.available():
            self.enabled = False
            return
        else:
            Plugin.configure(self, options, conf)
            self.conf = conf
            if options.calltree_stats_file:
                self.pfile = os.path.abspath(options.calltree_stats_file)
                self.clean_stats_file = False
            else:
                self.pfile = None
                self.clean_stats_file = True
            self.fileno = None
            self.sort = options.calltree_sort
            self.restrict = tolist(options.calltree_restrict)
            return

    def prepareTest(self, test):
        """Wrap entire test run in :func:`prof.runcall`.
        """
        if not self.available():
            return
        log.debug('preparing test %s' % test)

        def run_and_profile(result, prof=self.prof, test=test):
            prof.runcall(test, result)

        return run_and_profile

    def report(self, stream):
        """Output profiler report.
        """
        log.debug('saving calltree file')
        self._create_pfile()
        calltree_writer = KCacheGrind([self.prof])
        calltree_writer.output(file(self.pfile, 'w'))
        log.debug('printing profiler report')
        prof_stats = pstats.Stats(self.prof)
        prof_stats.sort_stats(self.sort)
        prof_stats.stream = stream
        if self.restrict:
            log.debug('setting profiler restriction to %s', self.restrict)
            prof_stats.print_stats(*self.restrict)
        else:
            prof_stats.print_stats()

    def finalize(self, result):
        """Clean up stats file, if configured to do so.
        """
        if not self.available():
            return
        else:
            try:
                self.prof.close()
            except AttributeError:
                pass

            if self.clean_stats_file:
                if self.fileno:
                    try:
                        os.close(self.fileno)
                    except OSError:
                        pass

                try:
                    os.unlink(self.pfile)
                except OSError:
                    pass

            return

    def _create_pfile(self):
        if not self.pfile:
            self.fileno, self.pfile = tempfile.mkstemp()
            self.clean_stats_file = True