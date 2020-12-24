# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/settings.py
# Compiled at: 2018-12-07 04:32:38
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os, subprocess, time, sys
from pocsuite.lib.core.revision import getRevisionNumber
from pocsuite import __version__
VERSION = __version__
REVISION = getRevisionNumber()
SITE = 'http://pocsuite.org'
VERSION_STRING = 'pocsuite/%s%s' % (VERSION, '-%s' % REVISION if REVISION else '-nongit-%s' % time.strftime('%Y%m%d', time.gmtime(os.path.getctime(__file__))))
IS_WIN = subprocess.mswindows
PLATFORM = os.name
PYVERSION = sys.version.split()[0]
ISSUES_PAGE = 'https://github.com/knownsec/Pocsuite/issues'
GIT_REPOSITORY = 'https://github.com/knownsec/Pocsuite.git'
GIT_PAGE = 'https://github.com/knownsec/Pocsuite'
LEGAL_DISCLAIMER = 'Usage of pocsuite for attacking targets without prior mutual consent is illegal.'
BANNER = "\x1b[01;33m\n                              ,--. ,--.\n ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.  \x1b[01;37m{\x1b[01;%dm%s\x1b[01;37m}\x1b[01;33m\n| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. :\n| '-' ' '-' \\ `--.-'  `'  ''  |  | |  | \\   --.\n|  |-' `---' `---`----' `----'`--' `--'  `----'\n`--'                                            \x1b[0m\x1b[4;37m%s\x1b[0m\n\n" % (31 + hash(REVISION) % 6 if REVISION else 30, VERSION_STRING.split('/')[(-1)], SITE)
UNICODE_ENCODING = 'utf-8'
INVALID_UNICODE_CHAR_FORMAT = '\\?%02x'
USAGE = 'pocsuite [options]'
INDENT = '  '
POC_ATTRS = ('vulID', 'version', 'author', 'vulDate', 'name', 'appVersion', 'desc',
             'createDate', 'updateDate', 'references', 'appPowerLink', 'vulType',
             'appName')
POC_IMPORTDICT = {'from pocsuite.net import': 'from pocsuite.lib.request.basic import', 
   'from pocsuite.poc import': 'from pocsuite.lib.core.poc import', 
   'from pocsuite.utils import register': 'from pocsuite.lib.core.register import registerPoc as register'}
POC_REGISTER_STRING = '\nfrom pocsuite.api.poc import register\nregister({})'
POC_REGISTER_REGEX = 'register\\(.*\\)'
POC_CLASSNAME_REGEX = 'class\\s+(.*?)\\(POCBase\\)'
POC_REQUIRES_REGEX = 'install_requires\\s*?=\\s*?\\[(.*?)\\]'
OLD_VERSION_CHARACTER = ('from comm import cmdline', 'from comm import generic')
HTTP_DEFAULT_HEADER = {'Accept': '*/*', 
   'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3', 
   'Accept-Language': 'zh-CN,zh;q=0.8', 
   'Cache-Control': 'max-age=0', 
   'Connection': 'keep-alive', 
   'Referer': 'http://www.baidu.com', 
   'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'}
PCS_OPTIONS = {'threads': 1, 
   'url': None, 
   'urlFile': None, 
   'agent': None, 
   'pocFile': None, 
   'isPocString': False, 
   'pocname': None, 
   'referer': None, 
   'Mode': 'verify', 
   'cookie': None, 
   'randomAgent': False, 
   'report': None, 
   'proxy': None, 
   'proxyCred': None, 
   'timeout': 5, 
   'quiet': False, 
   'requires': False, 
   'requiresFreeze': False}
REPORT_TABLEBASE = '    <tbody>\n    %s\n    </tbody>\n    '
REPORT_HTMLBASE = '    <!DOCTYPE html>\n    <html lang="zh-cn">\n        <head>\n            <meta charset="utf-8">\n            <title></title>\n            <style type="text/css">\n            caption{padding-top:8px;padding-bottom:8px;color:#777;text-align:left}th{text-align:left}.table{width:100%%;max-width:100%%;margin-bottom:20px}.table>thead>tr>th,.table>tbody>tr>th,.table>tfoot>tr>th,.table>thead>tr>td,.table>tbody>tr>td,.table>tfoot>tr>td{padding:8px;line-height:1.42857143;vertical-align:top;border-top:1px solid #ddd}.table>thead>tr>th{vertical-align:bottom;border-bottom:2px solid #ddd}.result0{display:none}.result1{}.status{cursor: pointer;}\n            </style>\n            <script>\n                function showDetail(dom){\n                    parent = dom.parentElement;\n                    detail = parent.children[1];\n                    if (detail == undefined){\n                        return;\n                    };\n                    if (detail.className == \'result0\'){\n                        detail.className = \'result1\';\n                    }else{\n                        detail.className = \'result0\';\n                    };\n                }\n            </script>\n        </head>\n        <body>\n            <div class="container">\n                <table class="table">\n                    <thead>\n    %s\n                    </thead>\n    %s\n                </table>\n            </div>\n        </body>\n    </html>\n    '