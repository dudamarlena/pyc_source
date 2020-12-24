# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/google/ocr/tool.py
# Compiled at: 2019-12-01 03:44:10
# Size of source mod 2**32: 693 bytes
import logging
from nose.tools import assert_true
from foxylib.tools.collections.collections_tools import l_singleton2obj
from foxylib.tools.json.json_tools import jdown
from foxylib.tools.log.logger_tools import FoxylibLogger

class GoogleOCRTool:

    @classmethod
    def j_page2text(cls, j_page):
        logger = FoxylibLogger.func_level2logger(cls.j_page2text, logging.DEBUG)
        j_response_list = jdown(j_page, ['responses'])
        if j_response_list is None:
            return
        assert_true(j_response_list, j_page)
        j_response = l_singleton2obj(j_response_list)
        str_text = jdown(j_response, ['fullTextAnnotation', 'text'])
        return str_text