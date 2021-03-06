# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/jinja2/jinja2_tools.py
# Compiled at: 2019-12-01 03:44:10
# Size of source mod 2**32: 2525 bytes
import logging, os
from functools import lru_cache
from jinja2 import Environment, BaseLoader, FileSystemLoader, Template
from markupsafe import Markup
from foxylib.tools.file.file_tools import FileToolkit
from foxylib.tools.log.logger_tools import FoxylibLogger

class Jinja2Toolkit:

    @classmethod
    @lru_cache(maxsize=2)
    def _js_escapes(cls):
        h = {'\\':'\\u005C', 
         "'":'\\u0027', 
         '"':'\\u0022', 
         '>':'\\u003E', 
         '<':'\\u003C', 
         '&':'\\u0026', 
         '=':'\\u003D', 
         '-':'\\u002D', 
         ';':'\\u003B', 
         '\u2028':'\\u2028', 
         '\u2029':'\\u2029'}
        h.update((('%c' % z, '\\u%04X' % z) for z in range(32)))
        return h

    @classmethod
    def escape_js(cls, value):
        if value is None:
            return
        else:
            return isinstance(value, str) or value
        return value.replace('"', '\\"')

    @classmethod
    def data2js_escaped(cls, data):
        return {k:cls.escape_js(v) for k, v in data.items()}

    @classmethod
    def tmplt_str2str(cls, str_tmplt, data=None, autoescape=None):
        if autoescape is None:
            autoescape = False
        if data is None:
            data = {}
        template = Template(str_tmplt, autoescape=autoescape)
        return (template.render)(**data)

    @classmethod
    def html2marked(cls, html):
        return Markup(html)

    @classmethod
    def tmplt_str2html(cls, html_tmplt, data=None, autoescape=None):
        if autoescape is None:
            autoescape = True
        s = cls.tmplt_str2str(html_tmplt, data=data, autoescape=autoescape)
        return Markup(s)

    @classmethod
    def tmplt_file2str(cls, filepath, data=None, autoescape=None):
        logger = FoxylibLogger.func_level2logger(cls.tmplt_file2str, logging.DEBUG)
        str_tmplt = FileToolkit.filepath2utf8(filepath)
        return cls.tmplt_str2str(str_tmplt, data=data, autoescape=autoescape)

    @classmethod
    def tmplt_file2html(cls, filepath, data=None, autoescape=None):
        str_tmplt = FileToolkit.filepath2utf8(filepath)
        return cls.tmplt_str2html(str_tmplt, data=data, autoescape=autoescape)


tmplt_str2str = Jinja2Toolkit.tmplt_str2str
tmplt_file2str = Jinja2Toolkit.tmplt_file2str