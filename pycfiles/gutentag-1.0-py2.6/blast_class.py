# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tagbase\gutentag\blast_class.py
# Compiled at: 2009-07-13 23:06:10
import os, sys, threading

class Worker(threading.Thread):

    def __init__(self, assembly, program, seq, queue):
        self.assembly = assembly
        self.program = program
        self.assembly = assembly
        self.seq = seq
        self.__queue = queue
        threading.Thread.__init__(self)

    def run(self):
        command = 'blastall -d %s -p %s < %s' % (assembly, program, seq)
        try:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            stdout_value = proc.communicate()[0]
            retcode = proc.returncode
            print '\tstdout:', repr(stdout_value)
            if retcode < 0:
                print 'Child was terminated by signal', retcode
            else:
                print 'Child returned', retcode
                self.__queue.put(stdout_value)
        except:
            print 'Execution failed:'


def makeNewDB(inputFile, seqtype):
    """
    Makes new blast database
    Returns retcode 
    """
    if seqtype == 'protein':
        st = 'T'
    else:
        st = 'F'
    command = 'formatdb -i %s -p %s' % (inputFile, st)
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        retcode = proc.returncode
        print '\tstdout:', repr(stdout_value)
        if retcode < 0:
            print 'Child was terminated by signal', retcode
        else:
            print 'Child returned', retcode
            return retcode
    except:
        print 'Execution failed:'


def runBlastAll(assembly, program, seq):
    """ 
    runs blastall 
    returns results
    """
    command = 'blastall -d %s -p %s < %s' % (assembly, program, seq)
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        retcode = proc.returncode
        print '\tstdout:', repr(stdout_value)
        if retcode < 0:
            print 'Child was terminated by signal', retcode
        else:
            print 'Child returned', retcode
            return stdout_value
    except:
        print 'Execution failed:'