# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_basic.py
# Compiled at: 2016-04-12 23:03:20
from __future__ import unicode_literals
import os, json, unittest, xmltodict
from httmock import urlmatch, HTTMock, response
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import NeedParamError, ParseError, OfficialAPIError
from wechat_sdk.messages import TextMessage, ImageMessage, VoiceMessage, VideoMessage, ShortVideoMessage, LinkMessage, LocationMessage, EventMessage, UnknownMessage
TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURE_PATH = os.path.join(TESTS_PATH, b'fixtures')

@urlmatch(netloc=b'(.*\\.)?api\\.weixin\\.qq\\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace(b'/cgi-bin/', b'').replace(b'/', b'_')
    if path.startswith(b'_'):
        path = path[1:]
    res_file = os.path.join(FIXTURE_PATH, b'%s.json' % path)
    content = {b'errcode': 99999, 
       b'errmsg': b'can not find fixture %s' % res_file}
    headers = {b'Content-Type': b'application/json'}
    try:
        with open(res_file, b'rb') as (f):
            content = json.loads(f.read().decode(b'utf-8'))
    except (IOError, ValueError) as e:
        print e

    return response(200, content, headers, request=request)


class WechatBasicTestCase(unittest.TestCase):
    token = b'test_token'
    appid = b'wxn5rg4orc9ajgq0yb'
    appsecret = b'y5tjcmn76i4mrsdcyebxzkdv0h1qjefk'
    fixtures_access_token = b'HoVFaIslbrofqJgkR0Svcx2d4za0RJKa3H6A_NjzhBbm96Wtg_a3ifUYQvOfJmV76QTcCpNubcsnOLmDopu2hjWfFeQSCE4c8QrsxwE_N3w'
    fixtures_jsapi_ticket = b'bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA'
    test_message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1348831860</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[测试信息]]></Content>\n<MsgId>1234567890123456</MsgId>\n</xml>'

    def test_check_signature(self):
        signature = b'41f929117dd6231a953f632cfb3be174b8e3ef08'
        timestamp = b'1434295379'
        nonce = b'ueivlkyhvdng46da0qxr52qzcjabjmo7'
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce)
        wechat = WechatBasic(token=self.token)
        self.assertTrue(wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce))
        self.assertFalse(wechat.check_signature(signature=signature, timestamp=timestamp + b'2', nonce=nonce))

    def test_grant_token(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.grant_token()
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.grant_token()
            self.assertEqual(resp[b'access_token'], self.fixtures_access_token)
            self.assertEqual(resp[b'expires_in'], 7200)
            self.assertEqual(wechat.conf.access_token, self.fixtures_access_token)

    def test_grant_jsapi_ticket(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.grant_jsapi_ticket()
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.grant_jsapi_ticket()
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')
            self.assertEqual(resp[b'ticket'], self.fixtures_jsapi_ticket)
            self.assertEqual(resp[b'expires_in'], 7200)
            self.assertEqual(wechat.conf.jsapi_ticket, self.fixtures_jsapi_ticket)

    def test_access_token(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            print wechat.conf.access_token
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            access_token = wechat.conf.access_token
            self.assertEqual(access_token, self.fixtures_access_token)

    def test_jsapi_ticket(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            print wechat.conf.jsapi_ticket
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            jsapi_ticket = wechat.conf.jsapi_ticket
            self.assertEqual(jsapi_ticket, self.fixtures_jsapi_ticket)

    def test_generate_jsapi_signature(self):
        noncestr = b'Wm3WZYTPz0wzccnW'
        jsapi_ticket = b'sM4AOVdWfPE4DxkXGEs8VMCPGGVi4C3VM0P37wVUCFvkVAy_90u5h9nbSlYy3-Sl-HhTdfl2fzFy1AOcHKP7qg'
        timestamp = 1414587457
        url = b'http://mp.weixin.qq.com?params=value'
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.generate_jsapi_signature(timestamp=timestamp, noncestr=noncestr, url=url)
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            signature = wechat.generate_jsapi_signature(timestamp=timestamp, noncestr=noncestr, url=url, jsapi_ticket=jsapi_ticket)
            self.assertEqual(signature, b'0f9de62fce790f9a083d5c99e95740ceb90c27ed')

    def test_parse_data_bad_message(self):
        bad_message = b'xml>a2341'
        wechat = WechatBasic()
        with self.assertRaises(ParseError):
            wechat.parse_data(data=bad_message)

    def test_parse_data_text_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1348831860</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[this is a test]]></Content>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, TextMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1348831860)
        self.assertEqual(message.type, b'text')
        self.assertEqual(message.content, b'this is a test')

    def test_parse_data_image_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1348831860</CreateTime>\n<MsgType><![CDATA[image]]></MsgType>\n<PicUrl><![CDATA[this is a url]]></PicUrl>\n<MediaId><![CDATA[media_id]]></MediaId>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, ImageMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1348831860)
        self.assertEqual(message.type, b'image')
        self.assertEqual(message.media_id, b'media_id')

    def test_parse_data_voice_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1357290913</CreateTime>\n<MsgType><![CDATA[voice]]></MsgType>\n<MediaId><![CDATA[media_id]]></MediaId>\n<Format><![CDATA[Format]]></Format>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, VoiceMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, b'voice')
        self.assertEqual(message.media_id, b'media_id')
        self.assertEqual(message.format, b'Format')
        self.assertIsNone(message.recognition)

    def test_parse_data_voice_recognition(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1357290913</CreateTime>\n<MsgType><![CDATA[voice]]></MsgType>\n<MediaId><![CDATA[media_id]]></MediaId>\n<Format><![CDATA[Format]]></Format>\n<Recognition><![CDATA[腾讯微信团队]]></Recognition>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, VoiceMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, b'voice')
        self.assertEqual(message.media_id, b'media_id')
        self.assertEqual(message.format, b'Format')
        self.assertEqual(message.recognition, b'腾讯微信团队')

    def test_parse_data_video_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1357290913</CreateTime>\n<MsgType><![CDATA[video]]></MsgType>\n<MediaId><![CDATA[media_id]]></MediaId>\n<ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, VideoMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, b'video')
        self.assertEqual(message.media_id, b'media_id')
        self.assertEqual(message.thumb_media_id, b'thumb_media_id')

    def test_parse_data_short_video_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1357290913</CreateTime>\n<MsgType><![CDATA[shortvideo]]></MsgType>\n<MediaId><![CDATA[media_id]]></MediaId>\n<ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, ShortVideoMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, b'shortvideo')
        self.assertEqual(message.media_id, b'media_id')
        self.assertEqual(message.thumb_media_id, b'thumb_media_id')

    def test_parse_data_location_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1351776360</CreateTime>\n<MsgType><![CDATA[location]]></MsgType>\n<Location_X>23.134521</Location_X>\n<Location_Y>113.358803</Location_Y>\n<Scale>20</Scale>\n<Label><![CDATA[位置信息]]></Label>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, LocationMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1351776360)
        self.assertEqual(message.type, b'location')
        self.assertEqual(message.location, (23.134521, 113.358803))
        self.assertEqual(message.scale, 20)
        self.assertEqual(message.label, b'位置信息')

    def test_parse_data_link_message(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>1351776360</CreateTime>\n<MsgType><![CDATA[link]]></MsgType>\n<Title><![CDATA[公众平台官网链接]]></Title>\n<Description><![CDATA[公众平台官网链接]]></Description>\n<Url><![CDATA[url]]></Url>\n<MsgId>1234567890123456</MsgId>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, LinkMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 1351776360)
        self.assertEqual(message.type, b'link')
        self.assertEqual(message.title, b'公众平台官网链接')
        self.assertEqual(message.description, b'公众平台官网链接')
        self.assertEqual(message.url, b'url')

    def test_parse_data_subscribe_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[FromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[subscribe]]></Event>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'subscribe')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertIsNone(message.ticket)
        self.assertIsNone(message.key)

    def test_parse_data_unsubscribe_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[FromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[unsubscribe]]></Event>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'unsubscribe')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'FromUser')
        self.assertEqual(message.time, 123456789)

    def test_parse_data_subscribe_qrscene_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[FromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[subscribe]]></Event>\n<EventKey><![CDATA[qrscene_123123]]></EventKey>\n<Ticket><![CDATA[TICKET]]></Ticket>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'subscribe')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, b'qrscene_123123')
        self.assertEqual(message.ticket, b'TICKET')

    def test_parse_data_scan_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[FromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[SCAN]]></Event>\n<EventKey><![CDATA[SCENE_VALUE]]></EventKey>\n<Ticket><![CDATA[TICKET]]></Ticket>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'scan')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, b'SCENE_VALUE')
        self.assertEqual(message.ticket, b'TICKET')

    def test_parse_data_location_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[fromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[LOCATION]]></Event>\n<Latitude>23.137466</Latitude>\n<Longitude>113.352425</Longitude>\n<Precision>119.385040</Precision>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'location')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'fromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.latitude, 23.137466)
        self.assertEqual(message.longitude, 113.352425)
        self.assertEqual(message.precision, 119.38504)

    def test_parse_data_click_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[FromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[CLICK]]></Event>\n<EventKey><![CDATA[EVENTKEY]]></EventKey>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'click')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, b'EVENTKEY')

    def test_parse_data_view_event(self):
        message = b'<xml>\n<ToUserName><![CDATA[toUser]]></ToUserName>\n<FromUserName><![CDATA[FromUser]]></FromUserName>\n<CreateTime>123456789</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[VIEW]]></Event>\n<EventKey><![CDATA[www.qq.com]]></EventKey>\n</xml>'
        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message
        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, b'view')
        self.assertEqual(message.target, b'toUser')
        self.assertEqual(message.source, b'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, b'www.qq.com')

    def test_response_text(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        response_xml_1 = wechat.response_text(b'test message')
        response_xml_2 = wechat.response_text(b'测试文本')
        response_xml_3 = wechat.response_text(b'测试文本')
        response_xml_4 = wechat.response_text(b'<h1>你好</h1>')
        response_xml_5 = wechat.response_text(b'<h1>你好</h1>', escape=True)
        response_1 = xmltodict.parse(response_xml_1)
        response_2 = xmltodict.parse(response_xml_2)
        response_3 = xmltodict.parse(response_xml_3)
        response_4 = xmltodict.parse(response_xml_4)
        response_5 = xmltodict.parse(response_xml_5)
        self.assertEqual(response_1[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(response_1[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(response_1[b'xml'][b'MsgType'], b'text')
        self.assertEqual(response_1[b'xml'][b'Content'], b'test message')
        self.assertEqual(response_2[b'xml'][b'Content'], b'测试文本')
        self.assertEqual(response_3[b'xml'][b'Content'], b'测试文本')
        self.assertEqual(response_4[b'xml'][b'Content'], b'<h1>你好</h1>')
        self.assertEqual(response_5[b'xml'][b'Content'], b'&lt;h1&gt;你好&lt;/h1&gt;')

    def test_response_image(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.response_image(media_id=b'xurkvi9gl')
        resp = xmltodict.parse(resp_xml)
        self.assertEqual(resp[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(resp[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(resp[b'xml'][b'MsgType'], b'image')
        self.assertEqual(resp[b'xml'][b'Image'][b'MediaId'], b'xurkvi9gl')

    def test_response_voice(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.response_voice(media_id=b'xurkvi9gl')
        resp = xmltodict.parse(resp_xml)
        self.assertEqual(resp[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(resp[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(resp[b'xml'][b'MsgType'], b'voice')
        self.assertEqual(resp[b'xml'][b'Voice'][b'MediaId'], b'xurkvi9gl')

    def test_response_video(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.response_video(media_id=b'xurkvi9gl', title=b'测试视频', description=b'测试描述')
        resp = xmltodict.parse(resp_xml)
        self.assertEqual(resp[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(resp[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(resp[b'xml'][b'MsgType'], b'video')
        self.assertEqual(resp[b'xml'][b'Video'][b'MediaId'], b'xurkvi9gl')
        self.assertEqual(resp[b'xml'][b'Video'][b'Title'], b'测试视频')
        self.assertEqual(resp[b'xml'][b'Video'][b'Description'], b'测试描述')

    def test_response_music(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.response_music(music_url=b'http://mp3.baidu.com', title=b'测试音乐', description=b'测试描述', hq_music_url=b'http://baidu.com/')
        resp = xmltodict.parse(resp_xml)
        self.assertEqual(resp[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(resp[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(resp[b'xml'][b'MsgType'], b'music')
        self.assertEqual(resp[b'xml'][b'Music'][b'Title'], b'测试音乐')
        self.assertEqual(resp[b'xml'][b'Music'][b'Description'], b'测试描述')
        self.assertEqual(resp[b'xml'][b'Music'][b'MusicUrl'], b'http://mp3.baidu.com')
        self.assertEqual(resp[b'xml'][b'Music'][b'HQMusicUrl'], b'http://baidu.com/')

    def test_response_news(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.response_news(articles=[
         {b'title': b'第一条新闻标题', 
            b'description': b'第一条新闻描述，这条新闻没有预览图', 
            b'url': b'http://www.google.com.hk/'},
         {b'title': b'第二条新闻标题, 这条新闻无描述', 
            b'picurl': b'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg', 
            b'url': b'http://www.github.com/'},
         {b'title': b'第三条新闻标题', 
            b'description': b'第三条新闻描述', 
            b'picurl': b'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg', 
            b'url': b'http://www.v2ex.com/'}])
        resp = xmltodict.parse(resp_xml)
        self.assertEqual(resp[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(resp[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(resp[b'xml'][b'MsgType'], b'news')
        self.assertEqual(resp[b'xml'][b'ArticleCount'], b'3')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][0][b'Title'], b'第一条新闻标题')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][0][b'Description'], b'第一条新闻描述，这条新闻没有预览图')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][0][b'Url'], b'http://www.google.com.hk/')
        self.assertIsNone(resp[b'xml'][b'Articles'][b'item'][0][b'PicUrl'])
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][1][b'Title'], b'第二条新闻标题, 这条新闻无描述')
        self.assertIsNone(resp[b'xml'][b'Articles'][b'item'][1][b'Description'])
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][1][b'Url'], b'http://www.github.com/')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][1][b'PicUrl'], b'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][2][b'Title'], b'第三条新闻标题')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][2][b'Description'], b'第三条新闻描述')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][2][b'Url'], b'http://www.v2ex.com/')
        self.assertEqual(resp[b'xml'][b'Articles'][b'item'][2][b'PicUrl'], b'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg')

    def test_group_transfer_message(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.group_transfer_message()
        resp = xmltodict.parse(resp_xml)
        self.assertEqual(resp[b'xml'][b'ToUserName'], b'fromUser')
        self.assertEqual(resp[b'xml'][b'FromUserName'], b'toUser')
        self.assertEqual(resp[b'xml'][b'MsgType'], b'transfer_customer_service')

    def test_create_menu(self):
        menu_info = {b'button': [
                     {b'type': b'click', 
                        b'name': b'今日歌曲', 
                        b'key': b'V1001_TODAY_MUSIC'},
                     {b'type': b'click', 
                        b'name': b'歌手简介', 
                        b'key': b'V1001_TODAY_SINGER'},
                     {b'name': b'菜单', 
                        b'sub_button': [
                                      {b'type': b'view', 
                                         b'name': b'搜索', 
                                         b'url': b'http://www.soso.com/'},
                                      {b'type': b'view', 
                                         b'name': b'视频', 
                                         b'url': b'http://v.qq.com/'},
                                      {b'type': b'click', 
                                         b'name': b'赞一下我们', 
                                         b'key': b'V1001_GOOD'}]}]}
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.create_menu(menu_info)
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.create_menu(menu_info)
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_get_menu(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_menu()
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_menu()
            self.assertEqual(resp[b'menu'], {b'button': [
                         {b'type': b'click', 
                            b'name': b'今日歌曲', 
                            b'key': b'V1001_TODAY_MUSIC', 
                            b'sub_button': []},
                         {b'type': b'click', 
                            b'name': b'歌手简介', 
                            b'key': b'V1001_TODAY_SINGER', 
                            b'sub_button': []},
                         {b'name': b'菜单', 
                            b'sub_button': [
                                          {b'type': b'view', 
                                             b'name': b'搜索', 
                                             b'url': b'http://www.soso.com/', 
                                             b'sub_button': []},
                                          {b'type': b'view', 
                                             b'name': b'视频', 
                                             b'url': b'http://v.qq.com/', 
                                             b'sub_button': []},
                                          {b'type': b'click', 
                                             b'name': b'赞一下我们', 
                                             b'key': b'V1001_GOOD', 
                                             b'sub_button': []}]}]})

    def test_delete_menu(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.delete_menu()
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.delete_menu()
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_create_group(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.create_group(b'测试组')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.create_group(b'测试组')
            self.assertEqual(resp[b'group'][b'id'], 107)
            self.assertEqual(resp[b'group'][b'name'], b'test')

    def test_get_group(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_groups()
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_groups()
            self.assertEqual(resp[b'groups'][0][b'id'], 0)
            self.assertEqual(resp[b'groups'][0][b'name'], b'未分组')
            self.assertEqual(resp[b'groups'][0][b'count'], 72596)
            self.assertEqual(resp[b'groups'][1][b'id'], 1)
            self.assertEqual(resp[b'groups'][1][b'name'], b'黑名单')
            self.assertEqual(resp[b'groups'][1][b'count'], 36)
            self.assertEqual(resp[b'groups'][2][b'id'], 2)
            self.assertEqual(resp[b'groups'][2][b'name'], b'星标组')
            self.assertEqual(resp[b'groups'][2][b'count'], 8)
            self.assertEqual(resp[b'groups'][3][b'id'], 104)
            self.assertEqual(resp[b'groups'][3][b'name'], b'华东媒')
            self.assertEqual(resp[b'groups'][3][b'count'], 4)
            self.assertEqual(resp[b'groups'][4][b'id'], 106)
            self.assertEqual(resp[b'groups'][4][b'name'], b'★不测试组★')
            self.assertEqual(resp[b'groups'][4][b'count'], 1)

    def test_get_group_by_id(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_group_by_id(b'13441123412341')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_group_by_id(b'12554647777')
            self.assertEqual(resp[b'groupid'], 102)

    def test_update_group(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.update_group(23, b'asfff')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.update_group(11, b'113444')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_move_user(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.move_user(b'123412', 1241234)
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.update_group(b'21341', 12341234)
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_get_user_info(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_user_info(b'123412412341234')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_user_info(b'3253634563425234')
            self.assertEqual(resp[b'subscribe'], 1)
            self.assertEqual(resp[b'openid'], b'o6_bmjrPTlm6_2sgVt7hMZOPfL2M')
            self.assertEqual(resp[b'nickname'], b'Band')
            self.assertEqual(resp[b'sex'], 1)
            self.assertEqual(resp[b'language'], b'zh_CN')
            self.assertEqual(resp[b'city'], b'广州')
            self.assertEqual(resp[b'province'], b'广东')
            self.assertEqual(resp[b'country'], b'中国')
            self.assertEqual(resp[b'headimgurl'], b'http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0')
            self.assertEqual(resp[b'subscribe_time'], 1382694957)
            self.assertEqual(resp[b'unionid'], b'o6_bmasdasdsad6_2sgVt7hMZOPfL')
            self.assertEqual(resp[b'remark'], b'')
            self.assertEqual(resp[b'groupid'], 0)

    def test_get_followers(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_followers()
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_followers()
            self.assertEqual(resp[b'total'], 2)
            self.assertEqual(resp[b'count'], 2)
            self.assertEqual(resp[b'data'], {b'openid': [
                         b'', b'OPENID1', b'OPENID2']})
            self.assertEqual(resp[b'next_openid'], b'NEXT_OPENID')

    def test_send_text_message(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_text_message(b'asdfasdfdf', b'asdadsfd')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_text_message(b'13412412341234242', b'测试')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_send_image_message(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_image_message(b'afasdfadsf', b'asfdadfsadfsdfas')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_image_message(b'asdfasdfdfas', b'12342341234')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_send_voice_message(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_voice_message(b'asdfasdf', b'safddsafasddfsaadsf')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_voice_message(b'safasf', b'123412343423241')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_send_video_message(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_video_message(b'asfasdfadsf', b'123412342134')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_video_message(b'safasf', b'123412343423241')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_send_music_message(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_music_message(b'231412341234', b'http://www.baidu.com', b'http://www.google.com', b'12341234')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_music_message(b'231412341234', b'http://www.baidu.com', b'http://www.google.com', b'12341234')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_send_article_message(self):
        article_info = [
         {b'title': b'第一条新闻标题', 
            b'description': b'第一条新闻描述，这条新闻没有预览图', 
            b'url': b'http://www.google.com.hk/'},
         {b'title': b'第二条新闻标题, 这条新闻无描述', 
            b'picurl': b'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg', 
            b'url': b'http://www.github.com/'},
         {b'title': b'第三条新闻标题', 
            b'description': b'第三条新闻描述', 
            b'picurl': b'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg', 
            b'url': b'http://www.v2ex.com/'}]
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_article_message(b'12341234234', article_info)
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_article_message(b'safasf', article_info)
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')

    def test_create_qrcode(self):
        data = {b'action_name': b'QR_LIMIT_STR_SCENE', b'action_info': {b'scene': {b'scene_str': b'123'}}}
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.create_qrcode(data)
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.create_qrcode(data)
            self.assertEqual(resp[b'ticket'], b'gQH47joAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL2taZ2Z3TVRtNzJXV1Brb3ZhYmJJAAIEZ23sUwMEmm3sUw==')
            self.assertEqual(resp[b'expire_seconds'], 60)
            self.assertEqual(resp[b'url'], b'http://weixin.qq.com/q/kZgfwMTm72WWPkovabbI')

    def test_get_template_id(self):
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_template_id(b'aafeewr')
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_template_id(b'123412431234')
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')
            self.assertEqual(resp[b'template_id'], b'Doclyl5uP7Aciu-qZ7mJNPtWkbkYnWBWVja26EGbNyk')

    def test_send_template_message(self):
        data = {b'first': {b'value': b'恭喜你购买成功！', 
                      b'color': b'#173177'}, 
           b'keynote1': {b'value': b'巧克力', 
                         b'color': b'#173177'}, 
           b'keynote2': {b'value': b'39.8元', 
                         b'color': b'#173177'}, 
           b'keynote3': {b'value': b'2014年9月16日', 
                         b'color': b'#173177'}, 
           b'remark': {b'value': b'欢迎再次购买！', 
                       b'color': b'#173177'}}
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_template_message(b'12341234', b'123412341234', data)
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_template_message(b'12341234', b'123412341', data)
            self.assertEqual(resp[b'errcode'], 0)
            self.assertEqual(resp[b'errmsg'], b'ok')
            self.assertEqual(resp[b'msgid'], 200228332)

    def test_check_official_error(self):
        wechat = WechatBasic()
        data = {b'errcode': 10001, 
           b'errmsg': b'test error message'}
        with self.assertRaises(OfficialAPIError) as (exc):
            wechat._check_official_error(data)
        self.assertEqual(exc.exception.errcode, 10001)
        self.assertEqual(exc.exception.errmsg, b'test error message')
        self.assertEqual(exc.exception.__str__(), b'10001: test error message')
        data = {b'errcode': 10000}
        with self.assertRaises(OfficialAPIError) as (exc):
            wechat._check_official_error(data)
        self.assertEqual(exc.exception.errcode, 10000)
        self.assertEqual(exc.exception.errmsg, b'')
        self.assertEqual(exc.exception.__str__(), b'10000: ')