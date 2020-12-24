# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\tools\debug\functionprofiler.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'GrosBedo'
__version__ = '0.4.3'
noprofiler = False
try:
    import profile, pstats
except:
    noprofiler = True

import sys, os
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(pathname, 'b3', 'lib'))
from kthread import *
from profilebrowser import *
try:
    from runsnakerun import runsnake
except:
    pass

def runprofile(mainfunction, output, timeout=60):
    if noprofiler == True:
        print 'ERROR: profiler and/or pstats library missing ! Please install it (probably package named python-profile) before running a profiling !'
        return False

    def profileb3():
        profile.run(mainfunction, output)

    print '=> SAVING MODE\n\n'
    print 'Calibrating the profiler...'
    cval = calibrateprofile()
    print 'Initializing the profiler...'
    b3main = KThread(target=profileb3)
    print 'Will now run the profiling and terminate it in %s seconds. Results will be saved in %s' % (str(timeout), str(output))
    print '\nCountdown:'
    for i in range(0, 5):
        print str(5 - i)
        time.sleep(1)

    print '0\nStarting to profile...'
    b3main.start()
    time.sleep(float(timeout))
    print '\n\nFinishing the profile and saving to the file %s' % str(output)
    b3main.kill()
    print '=> Profile done ! Exiting...'
    return True


def calibrateprofile():
    pr = profile.Profile()
    calib = []
    crepeat = 10
    for i in range(crepeat):
        calib.append(pr.calibrate(10000))

    final = sum(calib) / crepeat
    profile.Profile.bias = final
    return final


def subprocessprofileb3(profiler, mainfunction, output):
    profiler.run(mainfunction)


def runprofilesubprocess(mainfunction, output, timeout=60):
    try:
        print 'PROFILER SAVING MODE\n--------------------\n'
        print 'Preparing the profiler...'
        profiler = cProfile.Profile()
        b3main = multiprocessing.Process(target=subprocessprofileb3, args=(profiler, mainfunction, output))
        print 'Will now run the profiling and terminate it in %s seconds. Results will be saved in %s' % (str(timeout), str(output))
        print '\nCountdown:'
        for i in range(0, 6):
            print str(5 - i)
            time.sleep(1)

        print 'Starting to profile...'
        b3main.start()
        time.sleep(float(timeout))
        print '\n\nFinishing the profile and saving to the file %s' % str(output)
        print '=> Profile done ! Exiting...'
        profiler2 = posh.share(profiler)
        profiler2.dump_stats(output)
        raise SystemExit(222)
    except SystemExit as e:
        print 'SystemExit!'
        sys.exit(223)


def parseprofile(profilelog, out):
    file = open(out, 'w')
    print 'Opening the profile in %s...' % profilelog
    p = pstats.Stats(profilelog, stream=file)
    print 'Generating the stats, please wait...'
    file.write('=== All stats:\n')
    p.strip_dirs().sort_stats(-1).print_stats()
    file.write('=== Cumulative time:\n')
    p.sort_stats('cumulative').print_stats(100)
    file.write('=== Time:\n')
    p.sort_stats('time').print_stats(100)
    file.write('=== Time + cumulative time:\n')
    p.sort_stats('time', 'cum').print_stats(0.5, 'init')
    file.write('=== Callees:\n')
    p.print_callees()
    file.write('=== Callers:\n')
    p.print_callers()
    file.close()
    print 'Stats generated and saved to %s.' % out
    print 'Everything is done. Exiting'


def browseprofile(profilelog):
    print 'Starting the pstats profile browser...\n'
    try:
        browser = ProfileBrowser(profilelog)
        print >> browser.stream, 'Welcome to the profile statistics browser. Type help to get started.'
        browser.cmdloop()
        print >> browser.stream, 'Goodbye.'
    except KeyboardInterrupt:
        pass


def browseprofilegui(profilelog):
    app = runsnake.RunSnakeRunApp(0)
    app.OnInit(profilelog)
    app.MainLoop()