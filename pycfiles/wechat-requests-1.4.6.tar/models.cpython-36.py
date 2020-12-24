# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\message\models.py
# Compiled at: 2018-05-16 03:48:42
# Size of source mod 2**32: 4226 bytes
from bs4 import BeautifulSoup
from wechat.compat import basestring

class MessageTypes(object):

    def __init__(self):
        raise NotImplementedError()

    TEXT = 'text'
    LINK = 'link'
    IMAGE = 'image'
    EVENT = 'event'
    VOICE = 'voice'
    VIDEO = 'video'
    LOCATION = 'location'
    SHORT_VIDEO = 'shortvideo'


class MessageEventTypes(object):

    def __init__(self):
        raise NotImplementedError()

    VIEW = 'VIEW'
    SCAN = 'SCAN'
    CLICK = 'CLICK'
    LOCATION = 'LOCATION'
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'


class XMLMessage(object):
    __doc__ = "微信消息，对应微信API接口中定义的XML，例如:\n     <xml>\n     <ToUserName><![CDATA[toUser]]></ToUserName>\n     <FromUserName><![CDATA[fromUser]]></FromUserName>\n     <CreateTime>1348831860</CreateTime>\n     <MsgType><![CDATA[text]]></MsgType>\n     <Content><![CDATA[this is a test]]></Content>\n     <MsgId>1234567890123456</MsgId>\n     </xml>\n\n    可直接通过.ToUserName访问xml每个节点的值(为unicode)，该类为不可变的！！\n    如果进行属性设置会得到异常\n\n    例如如果raw_xml为上面的xml片段，那么：\n\n    wm = WeixinMessage(raw_xml)\n    xm.ToUserName 为 u'toUser'\n    xm.CreateTime 为 u'1348831860'\n\n    该实例提供所有类型的微信消息的通用属性：\n    id, from_openid, to_openid和create_timestamp以及content\n    可直接过wm.id, wm.from_openid, wm.to_openid和wm.create_timestamp\n    以及wm.content来获取\n\n    "

    def __init__(self, raw_xml):
        if not isinstance(raw_xml, basestring):
            raise TypeError('raw_xml not basestring type')
        object.__setattr__(self, 'soup', BeautifulSoup(raw_xml, 'xml'))
        object.__setattr__(self, 'raw', raw_xml)

    def __getattr__(self, key):
        if key in ('soup', 'raw'):
            return object.__getattribute__(self, key)
        else:
            if hasattr(self.soup, key):
                if getattr(self.soup, key) is not None:
                    return getattr(self.soup, key).text
            return

    def __setattr__(self, key, value):
        raise AttributeError(key)

    @property
    def type(self):
        return self.MsgType

    @property
    def content(self):
        if self.is_text():
            return self.Content
        else:
            if self.is_event():
                if self.Event == 'CLICK':
                    return self.EventKey
            return '[{}]'.format(self.type)

    def is_event(self):
        return self.type == MessageTypes.EVENT

    def is_text(self):
        return self.type == MessageTypes.TEXT

    def is_image(self):
        return self.type == MessageTypes.IMAGE

    def is_voice(self):
        return self.type == MessageTypes.VOICE

    def is_video(self):
        return self.type == MessageTypes.VIDEO

    def is_shortvideo(self):
        return self.type == MessageTypes.SHORT_VIDEO

    def is_location(self):
        return self.type == MessageTypes.LOCATION

    def is_link(self):
        return self.type == MessageTypes.LINK

    def is_subscribe_event(self):
        return all([
         self.is_event(),
         self.Event == MessageEventTypes.SUBSCRIBE])

    def is_unsubscribe_event(self):
        return all([
         self.is_event(),
         self.Event == MessageEventTypes.UNSUBSCRIBE])

    def is_qrscene_subscribe_event(self):
        return all([
         self.is_subscribe_event(),
         self.EventKey.startswith('qrscene_')])

    def is_scan_event(self):
        return all([
         self.is_event(),
         self.Event == MessageEventTypes.SCAN])

    def is_click_event(self):
        return all([
         self.is_event(),
         self.Event == MessageEventTypes.CLICK])

    @property
    def id(self):
        if self.is_event():
            return -1
        else:
            return int(self.MsgId)

    @property
    def from_openid(self):
        return self.FromUserName

    @property
    def to_openid(self):
        return self.ToUserName

    @property
    def create_timestamp(self):
        return int(self.CreateTime)

    def __str__(self):
        return self.raw