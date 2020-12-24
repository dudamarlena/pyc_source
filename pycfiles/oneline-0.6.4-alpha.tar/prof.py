# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/plugins/prof.py
# Compiled at: 2014-09-06 21:58:19
"""This plugin will run tests using the hotshot profiler, which is part
of the standard library. To turn it on, use the ``--with-profile`` option
or set the NOSE_WITH_PROFILE environment variable. Profiler output can be
controlled with the ``--profile-sort`` and ``--profile-restrict`` options,
and the profiler output file may be changed with ``--profile-stats-file``.

See the `hotshot documentation`_ in the standard library documentation for
more details on the various output options.

.. _hotshot documentation: http://docs.python.org/library/hotshot.html
"""
try:
    import hotshot
    from hotshot import stats
except ImportError:
    hotshot, stats = (None, None)

import logging, os, sys, tempfile
from nose.plugins.base import Plugin
from nose.util import tolist
log = logging.getLogger('nose.plugins')

class Profile(Plugin):
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
        parser.add_option('--profile-sort', action='store', dest='profile_sort', default=env.get('NOSE_PROFILE_SORT', 'cumulative'), metavar='SORT', help='Set sort order for profiler output')
        parser.add_option('--profile-stats-file', action='store', dest='profile_stats_file', metavar='FILE', default=env.get('NOSE_PROFILE_STATS_FILE'), help='Profiler stats file; default is a new temp file on each run')
        parser.add_option('--profile-restrict', action='append', dest='profile_restrict', metavar='RESTRICT', default=env.get('NOSE_PROFILE_RESTRICT'), help='Restrict profiler output. See help for pstats.Stats for details')

    def available(cls):
        return hotshot is not None

    available = classmethod(available)

    def begin(self):
        """Create profile stats file and load profiler.
        """
        if not self.available():
            return
        self._create_pfile()
        self.prof = hotshot.Profile(self.pfile)

    def configure(self, options, conf):
        """Configure plugin.
        """
        if not self.available():
            self.enabled = False
            return
        else:
            Plugin.configure(self, options, conf)
            self.conf = conf
            if options.profile_stats_file:
                self.pfile = options.profile_stats_file
                self.clean_stats_file = False
            else:
                self.pfile = None
                self.clean_stats_file = True
            self.fileno = None
            self.sort = options.profile_sort
            self.restrict = tolist(options.profile_restrict)
            return

    def prepareTest(self, test):
        """Wrap entire test run in :func:`prof.runcall`.
        """
        if not self.available():
            return
        log.debug('preparing test %s' % test)

        def run_and_profile(result, prof=self.prof, test=test):
            self._create_pfile()
            prof.runcall(test, result)

        return run_and_profile

    def report(self, stream):
        """Output profiler report.
        """
        log.debug('printing profiler report')
        self.prof.close()
        prof_stats = stats.load(self.pfile)
        prof_stats.sort_stats(self.sort)
        compat_25 = hasattr(prof_stats, 'stream')
        if compat_25:
            tmp = prof_stats.stream
            prof_stats.stream = stream
        else:
            tmp = sys.stdout
            sys.stdout = stream
        try:
            if self.restrict:
                log.debug('setting profiler restriction to %s', self.restrict)
                prof_stats.print_stats(*self.restrict)
            else:
                prof_stats.print_stats()
        finally:
            if compat_25:
                prof_stats.stream = tmp
            else:
                sys.stdout = tmp

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