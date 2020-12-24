# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/design/processor/report.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 18, 2013\n\n@package: ally base\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nModule containing report implementations.\n'
from .spec import IReport, Resolvers, IResolver

class ReportUnused(IReport):
    """
    Implementation for @see: IReport that reports the unused attributes resolvers.
    """
    __slots__ = ('_reports', '_resolvers')

    def __init__(self):
        """
        Construct the report.
        """
        self._reports = {}
        self._resolvers = []

    def open(self, name):
        """
        @see: IReport.open
        """
        assert isinstance(name, str), 'Invalid name %s' % name
        report = self._reports.get(name)
        if not report:
            report = self._reports[name] = ReportUnused()
        return report

    def add(self, resolvers):
        """
        @see: IReport.add
        """
        assert isinstance(resolvers, Resolvers), 'Invalid resolvers %s' % resolvers
        self._resolvers.append(resolvers)

    def report(self):
        """
        Creates the report lines.
        
        @return: list[string]
            The list of string lines.
        """
        st, reported = [], set()
        for resolvers in self._resolvers:
            assert isinstance(resolvers, Resolvers)
            for key, resolver in resolvers.iterate():
                assert isinstance(resolver, IResolver)
                if not resolver.isUsed():
                    if key not in reported:
                        reported.add(key)
                        st.append(('%s.%s for %s' % (key + (resolver,))).strip())
                    else:
                        continue

        if st:
            st.insert(0, 'Unused attributes:')
        for name, report in self._reports.items():
            assert isinstance(report, ReportUnused)
            lines = report.report()
            if lines:
                st.append('Report on %s:' % name)
                st.extend('\t%s' % line for line in lines)
                continue

        return st