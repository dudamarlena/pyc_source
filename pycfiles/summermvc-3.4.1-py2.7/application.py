# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/application.py
# Compiled at: 2018-06-01 04:04:12
import os, sys
from summermvc.mvc import FilePathDispatcherApplication
PROJECT_BASE = '{{PROJECT_BASE_DIRECTORY}}'
SOURCE_ROOT = os.path.join(PROJECT_BASE, 'src/')
sys.path.append(SOURCE_ROOT)
application = FilePathDispatcherApplication(SOURCE_ROOT)
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 8081, application)
    httpd.serve_forever()