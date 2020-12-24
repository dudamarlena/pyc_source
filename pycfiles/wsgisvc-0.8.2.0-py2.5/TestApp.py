# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\TestApp.py
# Compiled at: 2009-06-13 08:56:37
import sys, testing

def paste_deploy_app(global_conf, full_stack=True, **app_conf):

    def pdWsgiApp(environ, start_response):
        return wsgiHandler(environ, start_response)

    return pdWsgiApp


def wsgiHandler(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [
     '\n<html>\n<body>\n<title>Hello %(subject)s</title>\n    <p>Hello %(subject)s!</p>\n    <p>SCRIPT_NAME:%(script_name)s <br>\n    PATH_INFO:%(path_info)s <p>\n    SYS_PATH: %(sys_path)s <p>\n</body>\n' % {'subject': 'world', 'script_name': environ['SCRIPT_NAME'], 'path_info': environ['PATH_INFO'], 'sys_path': sys.path}]