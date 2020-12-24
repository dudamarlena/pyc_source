# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/messenger/slack/methods/response_tool.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 210 bytes


class SlackResponseTool:

    @classmethod
    def response2is_ok(cls, response):
        return response['ok'] is True

    @classmethod
    def response2j_resopnse(cls, response):
        return response.data