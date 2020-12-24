# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/reply.py
# Compiled at: 2016-04-12 23:03:20
import time
from .messages import WechatMessage

class WechatReply(object):

    def __init__(self, message=None, **kwargs):
        if 'source' not in kwargs and isinstance(message, WechatMessage):
            kwargs['source'] = message.target
        if 'target' not in kwargs and isinstance(message, WechatMessage):
            kwargs['target'] = message.source
        if 'time' not in kwargs:
            kwargs['time'] = int(time.time())
        self._args = dict()
        for k, v in kwargs.items():
            self._args[k] = v

    def render(self):
        raise NotImplementedError()


class TextReply(WechatReply):
    """
    回复文字消息
    """
    TEMPLATE = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[text]]></MsgType>\n    <Content><![CDATA[{content}]]></Content>\n    </xml>\n    '

    def __init__(self, message, content):
        u"""
        :param message: WechatMessage 对象
        :param content: 文字回复内容
        """
        super(TextReply, self).__init__(message=message, content=content)

    def render(self):
        return TextReply.TEMPLATE.format(**self._args)


class ImageReply(WechatReply):
    """
    回复图片消息
    """
    TEMPLATE = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[image]]></MsgType>\n    <Image>\n    <MediaId><![CDATA[{media_id}]]></MediaId>\n    </Image>\n    </xml>\n    '

    def __init__(self, message, media_id):
        u"""
        :param message: WechatMessage 对象
        :param media_id: 图片的 MediaID
        """
        super(ImageReply, self).__init__(message=message, media_id=media_id)

    def render(self):
        return ImageReply.TEMPLATE.format(**self._args)


class VoiceReply(WechatReply):
    """
    回复语音消息
    """
    TEMPLATE = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[voice]]></MsgType>\n    <Voice>\n    <MediaId><![CDATA[{media_id}]]></MediaId>\n    </Voice>\n    </xml>\n    '

    def __init__(self, message, media_id):
        u"""
        :param message: WechatMessage 对象
        :param media_id: 语音的 MediaID
        """
        super(VoiceReply, self).__init__(message=message, media_id=media_id)

    def render(self):
        return VoiceReply.TEMPLATE.format(**self._args)


class VideoReply(WechatReply):
    """
    回复视频消息
    """
    TEMPLATE = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[video]]></MsgType>\n    <Video>\n    <MediaId><![CDATA[{media_id}]]></MediaId>\n    <Title><![CDATA[{title}]]></Title>\n    <Description><![CDATA[{description}]]></Description>\n    </Video>\n    </xml>\n    '

    def __init__(self, message, media_id, title=None, description=None):
        u"""
        :param message: WechatMessage对象
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        """
        title = title or ''
        description = description or ''
        super(VideoReply, self).__init__(message=message, media_id=media_id, title=title, description=description)

    def render(self):
        return VideoReply.TEMPLATE.format(**self._args)


class MusicReply(WechatReply):
    """
    回复音乐消息
    """
    TEMPLATE_THUMB = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[music]]></MsgType>\n    <Music>\n    <Title><![CDATA[{title}]]></Title>\n    <Description><![CDATA[{description}]]></Description>\n    <MusicUrl><![CDATA[{music_url}]]></MusicUrl>\n    <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>\n    <ThumbMediaId><![CDATA[{thumb_media_id}]]></ThumbMediaId>\n    </Music>\n    </xml>\n    '
    TEMPLATE_NOTHUMB = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[music]]></MsgType>\n    <Music>\n    <Title><![CDATA[{title}]]></Title>\n    <Description><![CDATA[{description}]]></Description>\n    <MusicUrl><![CDATA[{music_url}]]></MusicUrl>\n    <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>\n    </Music>\n    </xml>\n    '

    def __init__(self, message, title='', description='', music_url='', hq_music_url='', thumb_media_id=None):
        title = title or ''
        description = description or ''
        music_url = music_url or ''
        hq_music_url = hq_music_url or music_url
        super(MusicReply, self).__init__(message=message, title=title, description=description, music_url=music_url, hq_music_url=hq_music_url, thumb_media_id=thumb_media_id)

    def render(self):
        if self._args['thumb_media_id']:
            return MusicReply.TEMPLATE_THUMB.format(**self._args)
        else:
            return MusicReply.TEMPLATE_NOTHUMB.format(**self._args)


class Article(object):

    def __init__(self, title=None, description=None, picurl=None, url=None):
        self.title = title or ''
        self.description = description or ''
        self.picurl = picurl or ''
        self.url = url or ''


class ArticleReply(WechatReply):
    TEMPLATE = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[news]]></MsgType>\n    <ArticleCount>{count}</ArticleCount>\n    <Articles>{items}</Articles>\n    </xml>\n    '
    ITEM_TEMPLATE = '\n    <item>\n    <Title><![CDATA[{title}]]></Title>\n    <Description><![CDATA[{description}]]></Description>\n    <PicUrl><![CDATA[{picurl}]]></PicUrl>\n    <Url><![CDATA[{url}]]></Url>\n    </item>\n    '

    def __init__(self, message, **kwargs):
        super(ArticleReply, self).__init__(message, **kwargs)
        self._articles = []

    def add_article(self, article):
        if len(self._articles) >= 10:
            raise AttributeError("Can't add more than 10 articles in an ArticleReply")
        else:
            self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(ArticleReply.ITEM_TEMPLATE.format(title=article.title, description=article.description, picurl=article.picurl, url=article.url))

        self._args['items'] = ('').join(items)
        self._args['count'] = len(items)
        return ArticleReply.TEMPLATE.format(**self._args)


class GroupTransferReply(WechatReply):
    """
    客服群发转发消息
    """
    TEMPLATE = '\n    <xml>\n    <ToUserName><![CDATA[{target}]]></ToUserName>\n    <FromUserName><![CDATA[{source}]]></FromUserName>\n    <CreateTime>{time}</CreateTime>\n    <MsgType><![CDATA[transfer_customer_service]]></MsgType>\n    </xml>\n    '

    def __init__(self, message):
        u"""
        :param message: WechatMessage 对象
        """
        super(GroupTransferReply, self).__init__(message=message)

    def render(self):
        return GroupTransferReply.TEMPLATE.format(**self._args)