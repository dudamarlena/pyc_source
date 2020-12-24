# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/run-core.py
# Compiled at: 2011-04-23 08:43:29
what = '\nimport core\ncore.start()\n'
print 'profiling...'
import cProfile
p = cProfile.Profile()
p.run(what)
stats = p.getstats()
print 'BY CALLS:\n------------------------------------------------------------'

def c(x, y):
    if x.callcount < y.callcount:
        return 1
    else:
        if x.callcount == y.callcount:
            return 0
        return -1


stats.sort(cmp=c)
for line in stats[:100]:
    print '%d %4f %s' % (line.callcount, line.totaltime, line.code)
    if line.calls == None:
        continue
    line.calls.sort(cmp=c)
    for line in line.calls[:10]:
        print '-- %d %4f %s' % (line.callcount, line.totaltime, line.code)

print 'BY TOTALTIME:\n------------------------------------------------------------'

def c(x, y):
    if x.totaltime < y.totaltime:
        return 1
    else:
        if x.totaltime == y.totaltime:
            return 0
        return -1


stats.sort(cmp=c)
for line in stats[:30]:
    print '%d %4f %s' % (line.callcount, line.totaltime, line.code)
    if line.calls == None:
        continue
    line.calls.sort(cmp=c)
    for line in line.calls[:10]:
        print '-- %d %4f %s' % (line.callcount, line.totaltime, line.code)