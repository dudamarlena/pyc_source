# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/src/executor.py
# Compiled at: 2016-01-15 21:29:16
import os, sys, signal, subprocess, threading, logging
__all__ = 'Executor'

class Executor:

    def __init__(self, command):
        self.__command = command
        self.__process = None
        return

    def __command_reader(self):
        while True:
            nextline = self.__process.stdout.readline()
            if nextline == '' and self.__process.poll() != None:
                break
            sys.stdout.write(nextline)
            sys.stdout.flush()

        logging.debug('Terminated (return code: %s)' % self.__process.returncode)
        return

    def restart(self):
        if self.kill():
            logging.debug('Restarting `%s`' % self.__command)
        else:
            logging.debug('Executing `%s`' % self.__command)
        self.__process = subprocess.Popen(self.__command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        threading.Thread(target=self.__command_reader).start()

    def kill(self):
        if self.__process:
            try:
                os.killpg(os.getpgid(self.__process.pid), signal.SIGTERM)
                self.__process.wait()
                return True
            except OSError:
                logging.debug('No process to kill')

        return False