# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/pexpectTest.py
# Compiled at: 2011-11-02 15:34:09
import os, time, pexpect, sys

def getProcessResults(cmd, timeLimit=20):
    """
  executes 'cmd' as a child process and returns the child's output,
  the duration of execution, and the process exit status. Aborts if
  child process does not generate output for 'timeLimit' seconds.
  """
    output = ''
    startTime = time.time()
    child = pexpect.spawn(cmd, timeout=10)
    child.logfile = sys.stdout
    while True:
        try:
            output += child.read_nonblocking(timeout=timeLimit).replace('\r', '')
        except pexpect.EOF as e:
            print(str(e))
            break
        except pexpect.TIMEOUT as e:
            print(str(e))
            output += '\nProcess aborted by FlashTest after %s seconds.\n' % timeLimit
            print(child.isalive())
            child.kill(9)
            break

    endTime = time.time()
    child.close(force=True)
    duration = endTime - startTime
    exitStatus = child.exitstatus
    return (
     output, duration, exitStatus)


cmd = './ticker.py'
result, duration, exitStatus = getProcessResults(cmd)
print('result: %s' % result)
print('duration: %s' % duration)
print('exit-status: %s' % exitStatus)