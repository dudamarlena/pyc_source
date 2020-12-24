# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/editor.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.exception import FormatError
import tempfile, os

class DictEditor(object):
    """
    dictionary textual editor.
    it invokes an external editor for editing a python dictionary
    """
    __module__ = __name__

    def __init__(self, dict):
        self.dict = dict

    def _createFile(self):
        (self.fd, self.path) = tempfile.mkstemp()
        self.file = os.fdopen(self.fd, 'w')

    def _writeFile(self):
        for k in self.dict.keys():
            self.file.write('%s: %s\n' % (k, self.format(self.dict[k])))

        self.file.flush()
        self.file.close()

    def _readFile(self):
        dict = {}
        self.file.seek(0)
        for rawline in self.file:
            line = rawline.strip()
            if not line:
                continue
            try:
                (attr, value) = line.split(':', 1)
            except ValueError:
                raise FormatError, 'dict format error'

            value = self.eval(value.strip())
            dict[attr.strip()] = value

        return dict

    def format(self, value):
        return value

    def eval(self, value):
        if value[0] == '[':
            value = eval(value)
        return value

    def _cleanup(self):
        self.file.close()
        os.remove(self.path)

    def edit(self):
        """
        invokes an external editor on the textual rapresentation
        of the dictionary and returns the modified dictionary,
        or None if no modify was done
        """
        self._createFile()
        self._writeFile()
        if not self._invokeEditor():
            self._cleanup()
            return
        self.file = open(self.path)
        res = self._readFile()
        self._cleanup()
        if res == self.dict:
            return
        return res

    def _invokeEditor(self):
        """
        returns True if file changed
        """
        oldStat = os.stat(self.path)
        if os.getenv('EDITOR'):
            os.system('%s %s' % (os.getenv('EDITOR'), self.path))
        else:
            os.system('%s %s' % ('vi', self.path))
        newStat = os.stat(self.path)
        return oldStat != newStat


class TextEditor(object):
    """
    textual editor.
    it invokes an external editor for editing a python str
    """
    __module__ = __name__

    def __init__(self, text):
        self.text = text

    def _createFile(self):
        (self.fd, self.path) = tempfile.mkstemp()
        self.file = os.fdopen(self.fd, 'w')

    def _writeFile(self):
        self.file.write(self.text)
        self.file.flush()
        self.file.close()

    def _readFile(self):
        self.file.seek(0)
        text = self.file.read()
        return text

    def format(self, value):
        return value

    def eval(self, value):
        if value[0] == '[':
            value = eval(value)
        return value

    def _cleanup(self):
        self.file.close()
        os.remove(self.path)

    def edit(self):
        """
        invokes an external editor on the textual rapresentation
        of the dictionary and returns the modified dictionary,
        or None if no modify was done
        """
        self._createFile()
        self._writeFile()
        if not self._invokeEditor():
            self._cleanup()
            return
        self.file = open(self.path)
        res = str(self._readFile())
        self._cleanup()
        if res == self.text:
            return
        return res

    def _invokeEditor(self):
        """
        returns True if file changed
        """
        oldStat = os.stat(self.path)
        if os.getenv('EDITOR'):
            os.system('%s %s' % (os.getenv('EDITOR'), self.path))
        else:
            os.system('%s %s' % ('vi', self.path))
        newStat = os.stat(self.path)
        return oldStat != newStat


from salamoia.tests import *
runDocTests()