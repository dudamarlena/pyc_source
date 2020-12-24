# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/messenger/slack/tests/test_foxylib_slack.py
# Compiled at: 2020-01-08 12:53:55
# Size of source mod 2**32: 7693 bytes
import asyncio, concurrent.futures, json, logging, os, signal, time
from datetime import datetime
from functools import lru_cache, partial
from multiprocessing import Process
from unittest import TestCase, mock
from unittest.mock import Mock, ANY
import pytest
from aiohttp import web, WSCloseCode
from slack.web.slack_response import SlackResponse
from foxylib.tools.collections.collections_tool import l_singleton2obj
from slack import RTMClient, WebClient
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.messenger.slack.events.file_shared import FileSharedEvent
from foxylib.tools.messenger.slack.foxylib_slack import FoxylibSlack, FoxylibChannel
from foxylib.tools.messenger.slack.methods.files.upload import FilesUploadMethod
from foxylib.tools.messenger.slack.methods.response_tool import SlackResponseTool
from foxylib.tools.messenger.slack.slack_tool import SlackFiletype, SlackFile, SlackTool, FileUploadMethod
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool
from foxylib.tools.process.process_tool import ProcessTool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestFoxylibSlack(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='Auth error when running from travis CI')
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        web_client = FoxylibSlack.web_client()
        channel = FoxylibChannel.V.FOXYLIB
        filepath = os.path.join(FILE_DIR, 'test_01.txt')
        response = FilesUploadMethod.invoke(web_client, channel, filepath)
        self.assertTrue(SlackResponseTool.response2is_ok(response))
        j_response = SlackResponseTool.response2j_resopnse(response)
        hyp = j_response
        ref = {'ok':True, 
         'file':{'name':'test_01.txt', 
          'title':'test 01', 
          'mimetype':'text/plain', 
          'filetype':'text', 
          'pretty_type':'Plain Text', 
          'user':'US8SU4H8W', 
          'editable':True, 
          'size':30, 
          'mode':'snippet', 
          'is_external':False, 
          'external_type':'', 
          'is_public':True, 
          'public_url_shared':False, 
          'display_as_bot':False, 
          'username':'', 
          'lines':3, 
          'lines_more':0, 
          'preview_is_truncated':False, 
          'comments_count':0, 
          'is_starred':False, 
          'shares':{},  'channels':[
           'CS7V80KGE'], 
          'groups':[],  'ims':[],  'has_rich_preview':False}}
        self.assertEqual(FileUploadMethod.j_response2norm(hyp), ref)
        j_file = FilesUploadMethod.j_response2j_file(j_response)
        file_id = SlackFile.j_file2id(j_file)
        (web_client.files_delete)(**{'file': file_id})

    @pytest.mark.skip(reason='Auth error when running from travis CI')
    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)
        web_client = FoxylibSlack.web_client()
        channel = FoxylibChannel.V.FOXYLIB
        filepath = os.path.join(FILE_DIR, 'test_01.txt')
        response = FilesUploadMethod.invoke(web_client, channel, filepath)
        self.assertTrue(SlackResponseTool.response2is_ok(response))
        j_response = SlackResponseTool.response2j_resopnse(response)
        j_file = FilesUploadMethod.j_response2j_file(j_response)
        logger.debug(json.dumps({'j_file': j_file}, indent=2))
        self.assertEqual(SlackFile.j_file2mimetype(j_file), MimetypeTool.V.TEXT_PLAIN)
        url_private = SlackFile.j_file2url_private(j_file)
        self.assertEqual(MimetypeTool.url2mimetype(url_private), MimetypeTool.V.TEXT_PLAIN)
        token = FoxylibSlack.xoxp_token()
        logger.debug({'url_private':url_private,  'token':token})
        utf8 = SlackTool.fileurl_token2utf8(url_private, token)
        logger.debug({'utf8': utf8})
        self.assertEqual(utf8, FileTool.filepath2utf8(filepath))
        file_id = SlackFile.j_file2id(j_file)
        (web_client.files_delete)(**{'file': file_id})

    @pytest.mark.skip(reason='RTM not receiving message event yet')
    def test_03(self):

        @RTMClient.run_on(event='message')
        def say_hello(**payload):
            data = payload['data']
            print(data.get('text'))

        def sync_loop(rtm_client):
            web_client = FoxylibSlack.web_client()
            for i in range(3):
                time.sleep(1)
                msg = 'Hi there: #{} @ {}'.format(i + 1, datetime.now())
                print('Hi there: #{} @ {}'.format(i + 1, datetime.now()))

            rtm_client.stop()

        async def slack_main():
            loop = asyncio.get_event_loop()
            rtm_client = RTMClient(token=(FoxylibSlack.xoxb_token()), run_async=True, loop=loop)
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            await asyncio.gather(loop.run_in_executor(executor, partial(sync_loop, rtm_client)), rtm_client.start())

        asyncio.run(slack_main())