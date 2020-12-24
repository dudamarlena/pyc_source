# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/tools/fileio.py
# Compiled at: 2008-06-27 12:04:08
import os, tempfile

class TempTracker(object):
    """Keeps track of temporary files/dirs that are created.

      >>> tracker = TempTracker()

    Make sure gen_tempfile provides a filename and then write some test data.

      >>> tmpf = tracker.gen_tempfile()
      >>> tmpf
      '.../cluemapper.testing_...'
      >>> f = open(tmpf, 'w')
      >>> f.write('hello world')
      >>> f.close()
      >>> os.path.exists(tmpf)
      True

    Make sure gen_tempdir provides a directory that exists.

      >>> tmpd = tracker.gen_tempdir()
      >>> tmpd
      '.../cluemapper.testing_...'
      >>> os.makedirs(os.path.join(tmpd, '1', '2'))
      >>> f = open(os.path.join(tmpd, '1', 'foo.txt'), 'w')
      >>> f.close()
      >>> os.path.exists(tmpd)
      True

    Cleanup should remove all traces of this.

      >>> tracker.cleanup()
      >>> os.path.exists(tmpf)
      False
      >>> os.path.exists(tmpd)
      False

    """

    def __init__(self):
        self.tempfiles = []
        self.tempdirs = []

    def gen_tempfile(self):
        (handler, tmp) = tempfile.mkstemp('', 'cluemapper.testing_')
        self.tempfiles.append(tmp)
        return tmp

    def gen_tempdir(self):
        tmp = tempfile.mkdtemp('', 'cluemapper.testing_')
        self.tempdirs.append(tmp)
        return tmp

    def cleanup(self):
        while len(self.tempfiles) > 0:
            tmp = self.tempfiles.pop()
            if os.path.exists(tmp):
                os.remove(tmp)

        while len(self.tempdirs) > 0:
            tmp = self.tempdirs.pop()
            if os.path.exists(tmp):
                for (dirpath, dirnames, files) in os.walk(tmp, topdown=False):
                    for x in files:
                        os.remove(os.path.join(dirpath, x))

                    os.rmdir(dirpath)