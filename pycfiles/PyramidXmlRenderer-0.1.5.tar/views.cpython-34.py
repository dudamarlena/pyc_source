# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python34\lib\site-packages\pyramid_ueditor\pyramid_ueditor\views.py
# Compiled at: 2015-06-05 03:34:04
# Size of source mod 2**32: 5048 bytes
__all__ = []
__author__ = 'lfblogs (email:13701242710@163.com)'
__version__ = '1.0.1'
import json, re
from pyramid.view import view_config
from pyramid.response import Response
from .utils import Uploader
from .settings import JSON_CONFIG, JSON_FILE, UEDITOR_UPLOAD_ROOT

def ueditor(request):
    return {}


@view_config(route_name='ueditorupload', renderer='json')
def ueditorupload(request):
    """
        UEditor文件上传接口
        SETTINGS 实例化传入的配置项
        result 返回结果
    """
    minetype = 'application/json'
    result = {}
    action = request.GET.get('action')
    SETTINGS = JSON_CONFIG
    if SETTINGS is {}:
        with open(JSON_FILE) as (fp):
            try:
                SETTINGS = json.loads(re.sub('\\/\\*.*\\/', '', fp.read()))
            except:
                SETTINGS = {}

    if action == 'config':
        result = SETTINGS
    else:
        if action in ('uploadimage', 'uploadfile', 'uploadvideo'):
            if action == 'uploadimage':
                FieldName = SETTINGS.get('imageFieldName')
                settings = {'pathFormat': SETTINGS.get('imagePathFormat'), 
                 'maxSize': SETTINGS.get('imageMaxSize'), 
                 'allowFiles': SETTINGS.get('imageAllowFiles')}
            else:
                if action == 'uploadvideo':
                    FieldName = SETTINGS.get('videoFieldName')
                    settings = {'pathFormat': SETTINGS.get('videoPathFormat'), 
                     'maxSize': SETTINGS.get('videoMaxSize'), 
                     'allowFiles': SETTINGS.get('videoAllowFiles')}
                else:
                    FieldName = SETTINGS.get('fileFieldName')
                    settings = {'pathFormat': SETTINGS.get('filePathFormat'), 
                     'maxSize': SETTINGS.get('fileMaxSize'), 
                     'allowFiles': SETTINGS.get('fileAllowFiles')}
            if FieldName in request.params:
                Field = request.params[FieldName]
                uploader = Uploader(Field, settings, UEDITOR_UPLOAD_ROOT)
                result = uploader.getFileInfo()
            else:
                result['state'] = '上传接口错误'
        else:
            if action in 'uploadscrawl':
                FieldName = SETTINGS.get('scrawlFieldName')
                settings = {'pathFormat': SETTINGS.get('scrawlPathFormat'), 
                 'maxSize': SETTINGS.get('scrawlMaxSize'), 
                 'allowFiles': SETTINGS.get('scrawlAllowFiles'), 
                 'oriName': 'scrawl.png'}
                if FieldName in request.params:
                    Field = request.params[FieldName]
                    uploader = Uploader(Field, settings, UEDITOR_UPLOAD_ROOT, 'base64')
                    result = uploader.getFileInfo()
                else:
                    result['state'] = '上传接口错误'
            else:
                if action in 'catchimage':
                    FieldName = SETTINGS.get('catcherFieldName')
                    settings = {'pathFormat': SETTINGS.get('catchPathFormat'), 
                     'maxSize': SETTINGS.get('catchMaxSize'), 
                     'allowFiles': SETTINGS.get('catchAllowFiles'), 
                     'oriName': 'remote.png'}
                    if FieldName in request.params:
                        source = []
                    elif '%s[]' % FieldName in request.params:
                        source = request.params.getlist('%s[]' % FieldName)
                    _list = []
                    for imgurl in source:
                        uploader = Uploader(imgurl, settings, UEDITOR_UPLOAD_ROOT, 'remote')
                        info = uploader.getFileInfo()
                        _list.append({'state': info['state'], 
                         'url': info['url'], 
                         'original': info['original'], 
                         'source': imgurl})

                    result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
                    result['list'] = _list
                else:
                    result['state'] = '服务器请求接口错误'
    result = json.dumps(result)
    if 'callback' in request.GET:
        callback = request.GET.get('callback')
        if re.match('^[\\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            minetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不符合规则'})
    resp = Response(result)
    resp.minetype = minetype
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return resp