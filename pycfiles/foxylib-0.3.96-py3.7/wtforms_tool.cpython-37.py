# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/wtforms/wtforms_tool.py
# Compiled at: 2020-02-07 17:23:40
# Size of source mod 2**32: 857 bytes
from functools import lru_cache
from wtforms.i18n import DummyTranslations
from foxylib.tools.collections.collections_tool import DictTool

class WTFormsTool:

    @classmethod
    @lru_cache(maxsize=2)
    def dummy_translation(cls):
        return DummyTranslations()

    @classmethod
    def h_gettext2translations(cls, h_gettext):

        class Translations(DummyTranslations):

            def gettext(self, str_in):
                if str_in in h_gettext:
                    return h_gettext[str_in]
                return super(Translations).gettext(str_in)

        return Translations()

    @classmethod
    def form2j_form(cls, form):
        if not form:
            return form
        return DictTool.filter(lambda k, v: v, form.patch_data)

    @classmethod
    def boundfield2name(cls, boundfield):
        return boundfield.short_name