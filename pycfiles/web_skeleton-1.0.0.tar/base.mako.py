# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yuneta-dev/yuneta/^yunos/yunetamonitor/tags/0.00.aa/.cache/yunetamonitor/htmlrendercode/base.mako.py
# Compiled at: 2015-12-28 14:29:58
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1451330998.809122
_enable_loop = True
_template_filename = '/home/yuneta-dev/yuneta/^yunos/yunetamonitor/yunetamonitor/htmlrendercode/base.mako'
_template_uri = '/yunetamonitor/htmlrendercode/base.mako'
_source_encoding = 'ascii'
_exports = []
from ginsfsm.compat import iteritems_

def render_body(context, **pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        metadata = context.get('metadata', UNDEFINED)
        assets_env = context.get('assets_env', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n<!doctype html>\n<html class="no-js" lang="">\n<head>\n    <meta charset="utf-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n    <title>')
        __M_writer(unicode(title))
        __M_writer('</title>\n\n    <link rel="shortcut icon" href="favicon.ico"/>\n    <link rel="apple-touch-icon" href="apple-touch-icon.png"/>\n\n')
        for key, value in iteritems_(metadata):
            if value:
                __M_writer('    <meta name="')
                __M_writer(unicode(key))
                __M_writer('" content="')
                __M_writer(unicode(value))
                __M_writer('">\n')

        __M_writer('\n    <!-- Mobile viewport optimized: h5bp.com/viewport -->\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n\n')
        for url in assets_env['css'].urls():
            __M_writer('    <link rel="stylesheet" href="')
            __M_writer(unicode(url))
            __M_writer('">\n')

        __M_writer('\n')
        for url in assets_env['top_js'].urls():
            __M_writer('    <script src="')
            __M_writer(unicode(url))
            __M_writer('"></script>\n')

        __M_writer('\n</head>\n\n<body>\n\n')
        __M_writer('<!--[if lt IE 8]>\n<div style="border: 1px solid red; margin: 1em; padding: 1em; background-color: #FDD;">\n<strong>Atenci&oacute;n:</strong> Est&aacute; usted utilizando una versi&oacute;n <em>obsoleta</em> de Internet Explorer. Dicha versi&oacute;n est&aacute; <em>descatalogada</em> por Microsoft y puede suponer <em>un serio riesgo para su sistema</em>, adem&aacute;s de no mostrar correctamente las p&aacute;ginas por las que navegue.<br/><h1>Esta aplicaci&oacute;n no es compatible con IExplorer 6/7.</h1>\n<p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>\n</div>\n<![endif]-->\n\n<div id="stdscr">\n</div>\n\n<!-- JavaScript at the bottom for fast page loading -->\n')
        for url in assets_env['bottom_js'].urls():
            __M_writer('<script src="')
            __M_writer(unicode(url))
            __M_writer('"></script>\n')

        __M_writer('\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()