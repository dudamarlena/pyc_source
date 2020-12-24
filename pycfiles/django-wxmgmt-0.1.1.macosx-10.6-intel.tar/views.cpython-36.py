# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lidayan/pyenv/python3/pypi-distribute/lib/python3.6/site-packages/wxmgmt/views.py
# Compiled at: 2018-02-25 20:14:49
# Size of source mod 2**32: 5804 bytes
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging, hashlib, json, time, pytz, datetime, uuid
from . import models, signature
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api(request, tenantName):
    """
    微信后端访问入口
    """
    logger.debug('request method(%s),url(%s),params(%s)' % (request.method, request.get_raw_uri(), request.GET))
    signature_params = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echostr = request.GET.get('echostr')
    tenant = models.Tenant.objects.filter(name=tenantName).first()
    if not tenant:
        return HttpResponse('没有找到对应的公众号信息--%s' % tenantName)
    else:
        if request.method == 'GET':
            hash_sha1 = hashlib.sha1(''.join([tenant.token, timestamp, nonce]).encode('utf8'))
            if hash_sha1.hexdigest() != signature_params:
                logger.debug('认证失败, %s, %s' % (hash_sha1, signature_params))
            return HttpResponse(echostr)
        if request.method == 'POST':
            json.dumps((request.data), indent=4)
            if request.data.get('MsgType') == 'text':
                return render(request, 'text_message.tpl', {'ToUserName':request.data.get('FromUserName'), 
                 'FromUserName':request.data.get('ToUserName'), 
                 'CreateTime':time.mktime(datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)).timetuple()), 
                 'Content':'你好！'})
            else:
                if request.data.get('MsgType') == 'event':
                    if request.data.get('Event') == 'subscribe':
                        openid = request.data.get('FromUserName')
                        account = models.Account.sync_account(tenant, openid)
                        return render(request, 'text_message.tpl', {'ToUserName':request.data.get('FromUserName'), 
                         'FromUserName':request.data.get('ToUserName'), 
                         'CreateTime':time.mktime(datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)).timetuple()), 
                         'Content':'%s, 欢迎你：加入合作，门店新增客户、车主免费洗车轻松搞定！' % account.nickname})
                    else:
                        if request.data.get('MsgType') == 'event':
                            if request.data.get('Event') == 'unsubscribe':
                                openid = request.data.get('FromUserName')
                                account = tenant.account_set.filter(openid=openid).first()
                                if account:
                                    account.status = 'unsubscribe'
                                    account.save()
                                return HttpResponse()
                        else:
                            if request.data.get('MsgType') == 'event':
                                if request.data.get('Event') == 'CLICK':
                                    msg = '点击测试'
                                    if request.data.get('EventKey') == 'kefudianhua':
                                        msg = tenant.kefuxinxi
                                    return render(request, 'text_message.tpl', {'ToUserName':request.data.get('FromUserName'), 
                                     'FromUserName':request.data.get('ToUserName'), 
                                     'CreateTime':time.mktime(datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)).timetuple()), 
                                     'MsgType':'text', 
                                     'Content':msg})
                        if request.data.get('MsgType') == 'event':
                            if request.data.get('Event') == 'scancode_push':
                                return render(request, 'text_message.tpl', {'ToUserName':request.data.get('FromUserName'), 
                                 'FromUserName':request.data.get('ToUserName'), 
                                 'CreateTime':time.mktime(datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)).timetuple()), 
                                 'MsgType':'text', 
                                 'Content':'扫描结果- '})
                else:
                    if request.data.get('MsgType') == 'event':
                        if request.data.get('Event') == 'VIEW':
                            return render(request, 'text_message.tpl', {'ToUserName':request.data.get('FromUserName'), 
                             'FromUserName':request.data.get('ToUserName'), 
                             'CreateTime':time.mktime(datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)).timetuple()), 
                             'MsgType':'text', 
                             'Content':'view跳转 '})
                return HttpResponse()
        else:
            return HttpResponse()


@require_http_methods(['GET'])
def jsticket(request, tenantName):
    """
    #获取 jsapi-ticket
    ###request get
    <pre><code>{
    }</pre></code>

    ###response
    <pre><code>{
        "status": true,
        "message": "success",
        "code": 200,
        "value": {
            "url": "xxx",
            "timestamp": xxxx,
            "signature": "xxxx",
            "appid": "xxxx",
            "noncestr": "xxxx"
        }
    }</pre></code>
    """
    logger.debug('request method(%s),url(%s),body(%s)' % (request.method, request.get_raw_uri(), request.body))
    tenant = models.Tenant.objects.filter(name=tenantName).first()
    if not tenant:
        return HttpResponse('没有找到对应的公众号信息--%s' % tenantName)
    else:
        data = {'jsapi_ticket':tenant.jsapi_ticket, 
         'url':request.META.get('HTTP_REFERER', request.get_raw_uri()), 
         'timestamp':int(time.mktime(timezone.now().timetuple())), 
         'noncestr':str(uuid.uuid4()).replace('-', '')}
        data['signature'] = signature(data, 'sha1')
        data['appid'] = tenant.appid
        del data['jsapi_ticket']
        return HttpResponse(data=data)