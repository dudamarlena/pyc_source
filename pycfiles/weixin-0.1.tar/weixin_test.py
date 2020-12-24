# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xiangchao/proj/weixin/tests/weixin_test.py
# Compiled at: 2013-05-24 10:12:16
from nose.tools import *
from weixin.Weixin import Weixin
import hashlib, time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def test_weixin_token():
    weixinhandler = Weixin('weixin-token')
    assert_equal(weixinhandler.token, 'weixin-token')


def test_verify_requset():
    token = 'weixin-token'
    weixinhandler = Weixin(token)
    timestamp = str(int(time.time()))
    nonce = 'hello'
    echostr = 'good'
    args = [token, timestamp, nonce]
    args.sort()
    signature = hashlib.sha1(('').join(args)).hexdigest()
    is_verify, new_echo = weixinhandler.verify_request(signature=signature, timestamp=timestamp, nonce=nonce, echostr=echostr)
    assert_equal(is_verify, True)
    assert_equal(new_echo, echostr)
    is_verify, new_echo = weixinhandler.verify_request(signature=signature, timestamp='1223434334', nonce=nonce, echostr=echostr)
    assert_equal(is_verify, False)
    assert_equal(new_echo, echostr)


def test_handle_request():
    weixinhandler = Weixin(token='weixin')
    body = '\n        <xml>\n        <ToUserName><![CDATA[toUser]]></ToUserName>\n        <FromUserName><![CDATA[fromUser]]></FromUserName>\n        <CreateTime>1348831860</CreateTime>\n        <MsgType><![CDATA[text]]></MsgType>\n        <Content><![CDATA[this is a test]]></Content>\n        <MsgId>1234567890123456</MsgId>\n        </xml>\n    '
    params = weixinhandler.handle_request(body)
    assert_equal(params['ToUserName'], 'toUser')
    assert_equal(params['FromUserName'], 'fromUser')
    assert_equal(params['CreateTime'], 1348831860)
    assert_equal(params['MsgType'], 'text')
    assert_equal(params['Content'], 'this is a test')
    assert_equal(params['MsgId'], 1234567890123456)
    assert_equal(weixinhandler.MsgType, 'text')
    assert_equal(weixinhandler.ToUserName, 'toUser')
    assert_equal(weixinhandler.FromUserName, 'fromUser')
    assert_equal(weixinhandler.CreateTime, 1348831860)
    assert_equal(weixinhandler.FuncFlag, 0)


def test_cdata():
    weixinhandler = Weixin(token='weixin-token')
    cdata_str = weixinhandler._cdata('hello')
    assert_equal(cdata_str, '<![CDATA[hello]]>')


def test_toxml():
    weixinhandler = Weixin(token='weixin-token')
    dic1 = {'name': 'cloudaice', 'age': 23}
    xml = weixinhandler._toxml(dic1)
    root = ET.fromstring('<xml>' + xml + '</xml>')
    params = dict()
    for elem in root:
        params[elem.tag] = elem.text

    if 'age' in params:
        params['age'] = int(params['age'])
    assert_equal(params, dic1)


def test_music():
    weixinhandler = Weixin(token='weixin-token')
    content = dict(Title='天空之城', Description='著名陶笛音乐', MusicUrl='http://cloudaice.com/music', HQMusicUrl='http://cloudaice.com/hqmusic')
    weixinhandler.music(content)
    root = ET.fromstring(weixinhandler.content.encode('utf-8'))
    params = dict()
    for elem in root:
        params[elem.tag] = elem.text

    assert_equal(content, params)


def test_text():
    weixinhandler = Weixin(token='weixin-token')
    content = '你好，我在测试微信开放API的Python包'
    weixinhandler.text(content)
    assert_equal(weixinhandler.content, '<Content><![CDATA[你好，我在测试微信开放API的Python包]]></Content>')


def test_news():
    weixinhandler = Weixin(token='weixin-token')
    content = [
     dict(Title='Python Web 开发之道', Description='Tornado 是一个好框架', PicUrl='http://cloudaice.com/tornado', Url='http://cloudaice.com/tornado'),
     dict(Title='Python 开发微信应用', Description='使用Python开发微信应用', PicUrl='http://cloudaice.com/python', Url='http://cloudaice.com/weixin')]
    weixinhandler.news(content)
    weixincontent = '<xml>' + weixinhandler.content + '</xml>'
    root = ET.fromstring(weixincontent.encode('utf-8'))

    def foo(root):
        dic = {}
        for elem in root:
            if elem.text is None:
                if elem.tag in dic:
                    if isinstance(dic[elem.tag], list):
                        dic[elem.tag].append(foo(elem))
                    else:
                        dic[elem.tag] = [
                         dic[elem.tag]]
                        dic[elem.tag].append(foo(elem))
                else:
                    dic[elem.tag] = foo(elem)
            elif elem.tag in dic:
                if isinstance(dic[elem.tag], list):
                    dic[elem.tag].append(elem.text)
                else:
                    dic[elem.tag] = [
                     dic[elem.tag]]
                    dic[elem.tag].append(elem.text)
            else:
                dic[elem.tag] = elem.text

        return dic

    params = foo(root)
    if 'ArticleCount' in params:
        params['ArticleCount'] = int(params['ArticleCount'])
    content = {'ArticleCount': 2, 'Articles': {'item': content}}
    assert_equal(params, content)