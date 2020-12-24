# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/messenger/slack/foxylib_slack.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 1299 bytes
import logging
from functools import lru_cache, partial
from slack import RTMClient, WebClient
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.messenger.slack.slack_tool import SlackTool
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.function.function_tool import FunctionTool

class FoxylibSlack:

    @classmethod
    def xoxb_token(cls):
        logger = FoxylibLogger.func_level2logger(cls.xoxb_token, logging.DEBUG)
        token = EnvTool.k2v('SLACK_BOT_USER_OAUTH_ACCESS_TOKEN')
        return token

    @classmethod
    def xoxp_token(cls):
        logger = FoxylibLogger.func_level2logger(cls.xoxp_token, logging.DEBUG)
        token = EnvTool.k2v('SLACK_OAUTH_ACCESS_TOKEN')
        return token

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def rtm_client(cls):
        return SlackTool.token2rtm_client(cls.xoxb_token())

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def web_client(cls):
        return SlackTool.token2web_client(cls.xoxb_token())


class FoxylibChannel:

    class Value:
        FOXYLIB = 'foxylib'

    V = Value