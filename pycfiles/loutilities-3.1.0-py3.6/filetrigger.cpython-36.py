# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\filetrigger.py
# Compiled at: 2019-11-25 16:48:03
# Size of source mod 2**32: 8147 bytes
"""
filetrigger - watch a directory for a file appearance, then trigger indicated action
============================================================================================

Provides filetrigger class, which can be used to process a file when it discovers that file is placed in a specified directory.
    
"""
from optparse import OptionParser
import time, glob, tempfile, shutil, os, os.path, subprocess, sys

class invalidParameter(Exception):
    pass


class filetrigger:
    __doc__ = "\n    When :meth:`run` executed, periodically checks dir for a file which does not start \n    with 'tmp.'. \n    \n    When a file arrives in triggerdir, the file is moved to an 'active' temporary directory, \n    :meth:`cleanup` is invoked, the previous file is deleted,  then :meth:`processfile`\n    is invoked.  \n    \n    This class must be inherited.  In the inherited class, :meth:`processfile` and \n    :meth:`cleanup` must be overridden.\n    \n    :param triggerdir: directory to check for arrival of file\n    :param period: period in seconds between checking triggerdir\n    :param exitevent: caller will set this event when exit is desired (optional)\n    "

    def __init__(self, triggerdir, period, exitevent=None):
        self.triggerdir = triggerdir
        self.period = period
        self.exitevent = exitevent

    def processfile(self, activefilepath):
        """
        This method must be overridden by the inheriting class.  This method processes
        the activefilepath until :meth:`cleanup` is invoked.
        
        This method must not block the caller.
        
        :param activefilepath: path of file which has been "activated" by being placed in triggerdir
        """
        pass

    def cleanup(self, lastfilepath):
        """
        This method must be overridden by the inheriting class.  Expectation is that
        this class will stop the action being done by :meth:`processfile`. 
        
        This method must block the caller until any cleanup is completed.
        
        :param lastfilepath: path of file which has been "activated" by being placed in triggerdir
        """
        pass

    def run(self):
        """
        Invoke this method to start execution
        """
        activedir = tempfile.mkdtemp(prefix='filetrigger')
        self.prevfile = None
        try:
            try:
                while 1:
                    if self.exitevent:
                        if self.exitevent.is_set():
                            break
                    time.sleep(self.period)
                    files = glob.glob('{0}/*'.format(self.triggerdir))
                    files = [f for f in files if os.path.basename(f)[0:4] != 'tmp.']
                    if len(files) > 1:
                        raise invalidParameter('multiple files found in {0}: {1}'.format(self.triggerdir, files))
                    if len(files) == 1:
                        thisfile = files[0]
                        filebase = os.path.basename(thisfile)
                        src = os.path.join(self.triggerdir, filebase)
                        activefile = os.path.join(activedir, filebase)
                        shutil.move(src, activefile)
                        if self.prevfile is not None:
                            self.cleanup(self.prevfile)
                            os.remove(self.prevfile)
                        self.processfile(activefile)
                        self.prevfile = activefile

            except KeyboardInterrupt:
                pass

        finally:
            if self.prevfile is not None:
                self.cleanup(self.prevfile)
            shutil.rmtree(activedir)


class _testfiletrigger(filetrigger):
    __doc__ = '\n    for unit test only\n    '

    def __init__(self, triggerdir):
        self.triggerdir = triggerdir
        filetrigger.__init__(self, self.triggerdir, 5)

    def processfile(self, activefilepath):
        """
        This method must not block the caller.
        
        :param activefilepath: path of file which has been "activated" by being placed in triggerdir
        """
        self.activeprocess = subprocess.Popen(['python', activefilepath, activefilepath], stdout=(sys.stdout), stderr=(sys.stderr))

    def cleanup(self, lastfilepath):
        """
        This method must block the caller until any cleanup is completed.
        
        :param lastfilepath: path of file which has been "activated" by being placed in triggerdir
        """
        self.activeprocess.terminate()


def main():
    """
    Use main to model your application to call :meth:`run`, or to test this module
    """
    usage = '  ./filetrigger.py directory  \n'
    usage += '     where: directory is directory to look for file appearance'
    parser = OptionParser(usage=usage)
    options, args = parser.parse_args()
    if len(args) != 1:
        raise invalidParameter('requires directory parameter')
    directory = args.pop(0)
    directory = os.path.abspath(directory)
    tc = _testfiletrigger(directory)
    tc.run()


if __name__ == '__main__':
    main()