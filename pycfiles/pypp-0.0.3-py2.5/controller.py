# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pypp\controller.py
# Compiled at: 2009-03-07 10:40:11
""" Controller class
    project: pypp
    
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: controller.py 13 2009-03-07 15:40:10Z jeanlou.dupont $'
__all__ = [
 'Controller']
import os, sys
from preprocessor import Tpl

class Controller(object):
    """ Controller class
    """

    def __init__(self):
        self._loader = None
        self._processed = {}
        return

    def handle_import_module(self, name, rpath, path, file, desc, global_scope):
        """ Callback for the PEP302 import_module function 
        """
        if name in self._processed:
            return
        self._processed[name] = path
        if file:
            processed_file = self.preprocessModule(name, file)
        else:
            processed_file = self.preprocessPackage(name, path)
        try:
            return self._loader(name, processed_file, rpath, desc, global_scope)
        except ImportError:
            pass

        return

    def preprocessModule(self, name, file):
        """ Preprocess a module
        """
        path = file.name
        file.close()
        return self._preprocessFile(name, path)

    def preprocessPackage(self, name, path):
        """ Preprocess a package
        """
        return self._preprocessFile(name, path)

    def _preprocessFile(self, name, path):
        """ Preprocess a source file.
        """
        processed_path = path + '.pypp'
        if self._isFresh(path, processed_path):
            return self._returnFile(processed_path)
        try:
            file = open(path)
            text = file.read()
        except:
            raise ImportError

        if text.find('#.pypp') == -1:
            return file
        file.close()
        dir = os.path.dirname(path)
        rendered = Tpl(text, dirs=dir).render()
        try:
            try:
                file = open(processed_path, 'w')
                file.write(rendered)
            except Exception, e:
                raise RuntimeError('pypp: error writing rendered file, path(%s) exception(%s)' % (processed_path, e))

        finally:
            file.close()

        try:
            file = open(processed_path)
        except Exception, e:
            raise RuntimeError('pypp: error opening rendered file, path(%s) exception(%s)' % (processed_path, e))

        return file

    def _returnFile(self, filepath):
        """ Opens 
        """
        try:
            file = open(filepath, 'r')
            return file
        except:
            raise ImportError

    def _isFresh(self, source_filepath, compiled_filepath):
        """ Verifies if the compiled source file is fresh.
            If we have an error of any sort, assume we have
            to process the file anyhow. This covers the cases:
            - no processed file is available yet
            - no processed file is available and there won't be any 
        """
        try:
            s_mtime = os.path.getmtime(source_filepath)
            c_mtime = os.path.getmtime(compiled_filepath)
        except:
            return False

        return c_mtime > s_mtime

    def _processed(self):
        """ for debugging purpose
        """
        for i in self._processed:
            yield i