# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/common/ShellUtil.py
# Compiled at: 2013-09-30 09:28:47
import subprocess, logging

def execute(commandList, printOutput=False, nohup=False):
    logger = logging.getLogger()
    strCommandList = []
    for c in commandList:
        strCommandList.append(str(c))

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Run command [%s]', (' ').join(strCommandList))
    if nohup:
        with open('/dev/null', 'rw') as (nullStream):
            p = subprocess.Popen(strCommandList, stdout=nullStream, stderr=nullStream, stdin=nullStream)
            r = p.wait()
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Run command [%s], Return %d', (' ').join(strCommandList), r)
            if r != 0:
                raise IOError('returned %d' % r)
        return
    p = subprocess.Popen(strCommandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        if printOutput:
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                print line,

        r = p.wait()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Run command [%s], Return %d', (' ').join(strCommandList), r)
        if r != 0 or printOutput:
            errMessage = p.stderr.readline()
            errline = errMessage
            while True:
                if errline:
                    print errline,
                else:
                    break
                errline = p.stderr.readline()

        if r != 0:
            raise IOError(errMessage.strip())
    finally:
        p.stderr.close()
        p.stdout.close()