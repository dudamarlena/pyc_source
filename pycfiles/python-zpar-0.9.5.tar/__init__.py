# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nmadnani/work/python-zpar/zpar/__init__.py
# Compiled at: 2014-11-10 20:04:17
"""
:author: Nitin Madnani (nmadnani@ets.org)
:organization: ETS
"""
import _ctypes, ctypes as c, os, sys
from .Tagger import Tagger
from .Parser import Parser
from .DepParser import DepParser
__all__ = [
 'Tagger', 'Parser', 'DepParser']

class ZPar(object):
    """The ZPar wrapper object"""

    def __init__(self, modelpath):
        super(ZPar, self).__init__()
        base_path = os.path.dirname(os.path.abspath(__file__))
        zpar_path = os.path.join(base_path, 'dist', 'zpar.so')
        self.libptr = c.cdll.LoadLibrary(zpar_path)
        self._initialize = self.libptr.initialize
        self._initialize.restype = c.c_void_p
        self._initialize.argtypes = None
        self._zpar_session_obj = self._initialize()
        self.modelpath = modelpath
        self.tagger = None
        self.parser = None
        self.depparser = None
        return

    def close(self):
        _unload_models = self.libptr.unload_models
        _unload_models.restype = None
        _unload_models.argtypes = [c.c_void_p]
        self.libptr.unload_models(self._zpar_session_obj)
        if self.tagger:
            self.tagger.cleanup()
        if self.parser:
            self.parser.cleanup()
        if self.depparser:
            self.depparser.cleanup()
        self.tagger = None
        self.parser = None
        self.depparser = None
        self.modelpath = None
        _ctypes.dlclose(self.libptr._handle)
        self.libptr = None
        self._zpar_session_obj = None
        return

    def __enter__(self):
        """Enable ZPar to be used as a ContextManager"""
        return self

    def __exit__(self, type, value, traceback):
        """Clean up when done"""
        self.close()

    def get_tagger(self):
        if not self.libptr:
            raise Exception('Cannot get tagger from uninitialized ZPar environment.')
            return
        else:
            self.tagger = Tagger(self.modelpath, self.libptr, self._zpar_session_obj)
            return self.tagger
            return

    def get_parser(self):
        if not self.libptr:
            raise Exception('Cannot get parser from uninitialized ZPar environment.')
            return
        else:
            self.parser = Parser(self.modelpath, self.libptr, self._zpar_session_obj)
            return self.parser
            return

    def get_depparser(self):
        if not self.libptr:
            raise Exception('Cannot get parser from uninitialized ZPar environment.')
            return
        else:
            self.depparser = DepParser(self.modelpath, self.libptr, self._zpar_session_obj)
            return self.depparser
            return