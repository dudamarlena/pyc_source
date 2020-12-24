# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/controller/user_controller.py
# Compiled at: 2018-05-30 05:31:20
from summermvc.decorator import *
from summermvc.mvc import HTTPStatus
from summermvc.field import *

@rest_controller
class UserController(object):
    _user_service = AutoWiredField()

    @post_construct
    def setup(self):
        print 'user controller is constructed'

    @pre_destroy
    def teardown(self):
        print 'user controller will be destroyed'

    @request_mapping('/get/user')
    def get_user(self, arg_userid, model, arg_format='json'):
        data = self._user_service.get_user_by_id(arg_userid)
        model.add_attribute('user_info', data)
        return arg_format

    @request_mapping('/get/user/(\\d+)')
    def get_user_2(self, model, path_var_1, arg_format='json'):
        model.add_attribute('user_info', self._user_service.get_user_by_id(path_var_1))
        if True:
            raise RuntimeError('just for test ``exception handler``')
        return arg_format

    @exception_handler('/get/user/(\\d+)', RuntimeError)
    def handle_runtime_error(self, model, response, arg_format='json'):
        response.set_status(HTTPStatus.InternalError)
        model.add_attribute('exception_happens', True)
        return arg_format