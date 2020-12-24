# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/controller/redirect_controller.py
# Compiled at: 2018-05-31 04:38:42
from summermvc.decorator import *

@rest_controller
class RedirectController(object):

    @request_mapping('/redirect')
    def test_redirect(self, response):
        response.redirect('http://www.baidu.com/')

    @request_mapping('/internal/redirect')
    def test_internal_redirect(self, response):
        response.redirect('/what/the/fuck')

    @request_mapping('/what/the/fuck')
    def what_the_fuck(self, model, arg_format='json'):
        model.add_attribute('info', 'this is what the fuck')
        return arg_format