# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/diffval/pyval.py
# Compiled at: 2010-10-25 18:27:36
import glob, os, shutil, tempfile, session, test

class pysession(session.session):

    def __init__(self, test, include=[], log=None):
        _pop = os.getcwd()
        src = os.path.dirname(test)
        dst = tempfile.mkdtemp()
        search = os.path.join(src, os.path.splitext(os.path.basename(test))[0])
        for file in glob.glob(search + '*'):
            shutil.copy(os.path.join(src, file), os.path.join(dst, os.path.basename(file)))

        self._args = [
         os.path.join(dst, os.path.basename(test))]
        os.chdir(dst)
        self._input = None
        env = os.environ
        env['PYTHONPATH'] = (':').join(include)
        session.session.__init__(self, executable='python', log=log)
        shutil.rmtree(dst)
        os.chdir(_pop)
        return


class pytest(test.test):

    def _create(self):
        return pysession(test=self._path, include=self._include, log=self._log)

    def _checksuccess(self):
        if 'stdout' in self._results:
            if self._results['stdout'] == []:
                self._results['stdout'] += ['']
        if 'stdout' in self._expects:
            self._expects['stdout'] += ['']
        return test.test._checksuccess(self)