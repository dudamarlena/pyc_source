# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/varprocessor.py
# Compiled at: 2016-08-21 08:21:17
# Size of source mod 2**32: 2286 bytes
__doc__ = '\nThis module implements the logic to process a a variable in the recipe header\n'
import sys, os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import logging, re
from functools import partial
from bprc.utils import vlog
from bprc.utils import errlog
from bprc.utils import verboseprint
from bprc.utils import httpstatuscodes
from bprc.utils import php_sub_pattern
from bprc.utils import var_sub_pattern
from bprc.utils import file_sub_pattern
from bprc.utils import _insert_file_param
import bprc.cli
from bprc._version import __version__

class VarProcessor:
    """VarProcessor"""

    def __init__(self, variables):
        """Instantiates the Step Processor Object"""
        self.variables = variables

    def _try_val(self, val):
        """Tries to convert a string to the type it looks like it should be"""
        import ast
        try:
            val = ast.literal_eval(val)
        except Exception:
            pass

        return val

    def parse(self, val, src):
        """parses the current variable.
        See http://stackoverflow.com/questions/7087905/python-with-regex-to-replace-strings-recursively"""
        vlog('Variable parser initialised for variable ' + str(val))
        subbed_text, n = var_sub_pattern.subn(lambda m: str(self.parse(eval("src['" + m.group(1) + "']"), src)), str(val))
        return self._try_val(subbed_text)

    def fileparse(self, val, src):
        """does file substitutions on the current variable"""
        vlog('Filename parser initialised for variable ' + str(val))
        file_substituted_text, n = file_sub_pattern.subn(partial(_insert_file_param, recipe=None, variables=None), str(val))
        vlog('Files: Made ' + str(n) + ' file substitutions. Result: ' + str(val) + '=' + file_substituted_text)
        return file_substituted_text