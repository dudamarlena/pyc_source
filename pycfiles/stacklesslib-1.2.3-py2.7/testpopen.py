# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\testpopen.py
# Compiled at: 2017-12-11 20:12:50
import os, re, threading
from ..replacements.popen import FileChannel
os_popen4 = getattr(os, 'popen4', None)

def popen4(cmd, mode='t', bufsize=-1):
    pstdin, pstdout = FileChannel(), FileChannel()

    def func():
        try:
            try:
                for i in range(10):
                    l = '%d' % i * 10 + '\n'
                    pstdout.send(l)

            except Exception as e:
                c, e = sys.exc_info()[:2]
                import traceback
                traceback.print_exc()
                pstdout.send_exception(c, e)

        finally:
            pstdout.close()

    t = threading.Thread(target=func)
    t.start()
    return (pstdin, pstdout)


def read_process(cmd, args=''):
    pipein, pipeout = popen4('%s %s' % (cmd, args))
    try:
        firstline = pipeout.readline()
        if re.search('(not recognized|No such file|not found)', firstline, re.IGNORECASE):
            raise IOError('%s must be on your system path.' % cmd)
        output = firstline + pipeout.read()
    finally:
        pipeout.close()

    return output


done = False

def foo():
    global done
    try:
        output = read_process('foo')
    finally:
        done = True


if __name__ == '__main__':
    import stackless
    stackless.tasklet(foo)()
    while not done:
        stackless.run()