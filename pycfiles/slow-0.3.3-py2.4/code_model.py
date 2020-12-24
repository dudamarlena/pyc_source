# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/code_model.py
# Compiled at: 2006-01-10 04:15:14
import zlib, base64
from xpathmodel import XPathModel, autoconstruct, validate_regexp
_RE_CLASSNAME = '[a-zA-Z][a-zA-Z0-9_]*'
_RE_METHODNAME = _RE_CLASSNAME

class CodeContainer(XPathModel):
    """Code blocks as sub-elements."""
    __module__ = __name__
    DEFAULT_NAMESPACE = 'local'
    _attr_language = './@language'
    _attr_code_type = './@type'
    _val_code_type = 'exec|eval'

    def _get_code(self, _xpath_result):
        """string(./text())"""
        if _xpath_result:
            return zlib.decompress(base64.b64decode(_xpath_result))
        else:
            return ''

    def _set_code(self, code):
        if code:
            self.text = base64.b64encode(zlib.compress(code, 9))
        else:
            self.text = None
        return

    @property
    def compiled_code(self):
        if self.language != 'python':
            self._compiled_code = None
            return
        if hasattr(self, '_compiled_code') and self._compiled_code:
            return self._compiled_code
        else:
            code = self.code
            if code:
                ccode = self._compiled_code = compile(code, '<string>', self.code_type or 'exec')
                return ccode
            else:
                return
        return

    _get_class_name = 'string(./@classname)'

    @validate_regexp(_RE_CLASSNAME)
    def _set_class_name(self, name):
        self.set('classname', name)

    _get_method_name = 'string(./@methodname)'

    @validate_regexp(_RE_METHODNAME)
    def _set_method_name(self, name):
        self.set('methodname', name)