# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/check_docking/inspect.py
# Compiled at: 2015-02-08 01:35:53
__doc__ = '对传入的request data 检测模块.\n'
__author__ = 'kylinfish@126.com'
__date__ = '2015/01/20'
import sys, six, traceback
from functools import wraps
from django.conf import settings
from django.utils.importlib import import_module

def request_data_inspect(request):
    u"""客户传入值验证处理模块, web handle调用.

        :param request: 请求对象

        步骤:
            检查请求方法是否错误.
            检查必传项是否缺失.

            检查传入项是否存在.
            检查传入项数据类型.
    """
    message = None
    url_path = request.get_full_path().lstrip('/')
    url_method = request.method
    url_data = rest_api_url[url_path]
    if url_method in url_data:
        message = 'kylin: request method error.'
    else:
        dict_data = getattr(request, url_method)
        if len(dict_data) > 0:
            for key, value in url_data[url_method].items():
                if value['must'] and key not in dict_data.keys():
                    message = 'kylin: [%s] must data item missing.' % key

            for key, value in dict_data.items():
                if key not in url_data[url_method]:
                    message = 'kylin: [%s] invalid incoming parameter.' % key
                elif type(value) != url_data[url_method][key]['type']:
                    message = 'kylin: [%s] invalid data type.' % key

    six.print_(message)
    return message


def request_inspect(request):
    u"""给装饰函数使用的一种方式.

        控制阀门的一种方式.
    """
    if getattr(settings, 'IS_DATA_INSPECT', None):
        return request_data_inspect(request)
    else:
        return


def debug_request(func=None):
    u"""检测view函数, 非middleware, 用decorator方式.

        :param func: view 函数

        settings.py items DEBUG = True:

    """
    if settings.DEBUG:

        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            try:
                message = request_inspect(request)
                if message:
                    return message
                response = func(request, *args, **kwargs)
                return response
            except Exception as e:
                six.print_(e)
                traceback.print_exc(file=sys.stdout)

        return returned_wrapper


def get_check_config():
    u"""获取检测依赖配置数据
    """
    check_config = getattr(settings, 'INSPECT_PROFILE', None)
    if check_config:
        try:
            project_catalog = import_module(check_config)
            return project_catalog.REST_API_URL
        except ImportError:
            raise ImportError("ImportError: No module named check_config, please usage: 'manage.py inspectprofile'.")

    return


rest_api_url = get_check_config()