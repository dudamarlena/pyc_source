# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/codeblock.py
# Compiled at: 2018-12-02 17:44:03
# Size of source mod 2**32: 3489 bytes
"""
code block related directives.
"""
import attr
from .base import Directive
from ..base import RstObj

@attr.s
class Code(RstObj):
    __doc__ = '\n    Pure text code Snippet.\n    '
    text = attr.ib(default=None)
    meta_not_none_fields = ('text', )


@attr.s
class CodeBlockEmpty(Directive):
    __doc__ = '\n    Example::\n\n        ::\n\n            your code ...\n    '
    code = attr.ib(default=None,
      validator=(attr.validators.instance_of(Code)))
    meta_not_none_fields = ('code', )


@attr.s
class CodeBlockBase(CodeBlockEmpty):
    code = attr.ib(default=None,
      validator=(attr.validators.instance_of(Code)))
    meta_lang = ''

    class LangOptions(object):
        empty = ''
        python = 'python'
        ruby = 'ruby'
        r = 'r'
        perl = 'perl'
        c = 'c'
        cpp = 'cpp'
        html = 'html'
        css = 'css'
        javascript = 'javascript'
        sql = 'sql'
        scala = 'scala'
        make = 'make'
        bash = 'bash'

    @property
    def template_name(self):
        return '{}.{}.rst'.format(self.__module__, 'CodeBlockBase')

    @classmethod
    def from_string(cls, value):
        """
        Construct CodeBlock from string.
        """
        return cls(code=Code(text=value))


code_block_doc_string = '\n:param code: :class:`Code`.\n\nExample:: {}\n\n    .. code-block: python\n\n        your code ...\n'.strip()

@attr.s
class CodeBlock(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.empty
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockPython(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.python
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockRuby(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.ruby
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockR(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.r
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockPerl(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.perl
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockC(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.c
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockCPP(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.cpp
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockHTML(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.html
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockCSS(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.css
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockJavaScript(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.javascript
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockSQL(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.sql
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockScala(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.scala
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockMake(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.make
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockBash(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.bash
    __doc__ = code_block_doc_string.format(meta_lang)