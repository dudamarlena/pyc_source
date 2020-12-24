# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/nose_profile/kcachegrind.py
# Compiled at: 2012-09-02 08:28:04


def label(code):
    if isinstance(code, str):
        return code
    else:
        return '%s %s:%d' % (code.co_name,
         code.co_filename,
         code.co_firstlineno)


class KCacheGrind(object):

    def __init__(self, profilers):
        self.datas = [ profiler.getstats() for profiler in profilers ]
        self.out_file = None
        return

    def output(self, out_file):
        self.out_file = out_file
        print >> out_file, 'events: Ticks'
        self._print_summary()
        for data in self.datas:
            for entry in data:
                self._entry(entry)

    def _print_summary(self):
        max_cost = 0
        for data in self.datas:
            for entry in data:
                totaltime = int(entry.totaltime * 1000)
                max_cost = max(max_cost, totaltime)

        print >> self.out_file, 'summary: %d' % (max_cost,)

    def _entry(self, entry):
        out_file = self.out_file
        code = entry.code
        if isinstance(code, str):
            print >> out_file, 'fi=~'
        else:
            print >> out_file, 'fi=%s' % (code.co_filename,)
        print >> out_file, 'fn=%s' % (label(code),)
        inlinetime = int(entry.inlinetime * 1000)
        if isinstance(code, str):
            print >> out_file, '0 ', inlinetime
        else:
            print >> out_file, '%d %d' % (code.co_firstlineno, inlinetime)
        if entry.calls:
            calls = entry.calls
        else:
            calls = []
        if isinstance(code, str):
            lineno = 0
        else:
            lineno = code.co_firstlineno
        for subentry in calls:
            self._subentry(lineno, subentry)

        print >> out_file

    def _subentry(self, lineno, subentry):
        out_file = self.out_file
        code = subentry.code
        print >> out_file, 'cfn=%s' % (label(code),)
        if isinstance(code, str):
            print >> out_file, 'cfi=~'
            print >> out_file, 'calls=%d 0' % (subentry.callcount,)
        else:
            print >> out_file, 'cfi=%s' % (code.co_filename,)
            print >> out_file, 'calls=%d %d' % (
             subentry.callcount, code.co_firstlineno)
        totaltime = int(subentry.totaltime * 1000)
        print >> out_file, '%d %d' % (lineno, totaltime)