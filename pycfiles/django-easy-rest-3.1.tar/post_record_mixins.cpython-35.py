# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jonatan/myprojects/django-easy-rest/easy_rest/test_framework/recorder/post_record_mixins.py
# Compiled at: 2018-09-14 14:50:50
# Size of source mod 2**32: 8885 bytes
from datetime import datetime
from ..resolvers.resolve import get_tests_file, app_exists, get_app_path, in_test
from ..resolvers.settings import get_override_settings
from django.conf import settings
global_template = 'from django.test import TestCase\nfrom {app_name}.views import {view_name}\nfrom django.test import RequestFactory\nfrom django.contrib.auth.models import AnonymousUser, User\nfrom easy_rest.test_framework.resolvers.resolve import register_unittest\nfrom django.test.utils import override_settings\n\nregister_unittest()\n\n\ndef resolve_user(pk):\n    try:\n        return User.objects.get(pk=pk)\n    except Exception:\n        return AnonymousUser()\n\n\n'
new_test = 'class Test{view_name}(TestCase):\n    def __init__(self, *args, **kwargs):\n        super(TestApiTest, self).__init__(*args, **kwargs)\n        self.test = {view_name}()\n\n'
functions_template = '    @override_settings({override_settings})\n    def test_{action}(self):\n        request = RequestFactory()\n        request.data = {request_data}\n        request.user = resolve_user({request_user_pk})\n        result = {result}\n        if type(result) is dict:\n            return self.assertDictEqual(result, self.test.post(request).data)\n        return self.assertEqual(result, self.test.post(request).data)\n\n'

class PostRecordTestGenerator(object):

    def __init__(self, *args, **kwargs):
        """
        this just sets the class to initialize view_name, test_File, current_settings_keys,
        test_file_data, test_file_name to defaults
        :param args:
        :param kwargs:
        """
        self.view_name = None
        self.tests_file = None
        self.use_current_settings_keys = [
         'DEBUG']
        self.test_file_data = ''
        self.test_file_name = 'auto_generated_post_record_test'
        super(PostRecordTestGenerator, self).__init__(*args, **kwargs)

    def init_test(self, app_name):
        """
        this function initializes the test
        :param app_name: the app to test
        :return: None
        """
        if not app_exists(app_name):
            raise Exception("can't find {0} app {1}".format(app_name, 'in {0}'.format(get_app_path(app_name) if settings.DEBUG else '')))
        self.view_name = str(self.__class__.__name__)
        file_name, data = get_tests_file(app_name, file_name='tests.py')
        import_line = 'from .{} import *\n'.format(self.test_file_name)
        if import_line not in data:
            with open(file_name, 'a') as (file):
                file.seek(0)
                file.write(import_line)
        self.tests_file, self.test_file_data = get_tests_file(app_name, data=global_template.format(app_name=app_name, view_name=self.view_name), file_name='auto_generated_post_record_test.py')

    def post(self, request):
        """
        Overriding the original post function
        :param request: WSGI request
        :return: rest_framework.Response
        """
        if in_test():
            return super(PostRecordTestGenerator, self).post(request)
        if not self.view_name or not self.tests_file:
            raise Exception('unsuccessful init maybe you forgot calling init_test ?')
        try:
            action = self._pythonize(request.data[self.function_field_name])
        except Exception:
            action = 'easy_rest_{}_test'.format(self.function_from_time())

        data = super(PostRecordTestGenerator, self).post(request)
        pk = request.user.pk
        self.append_to_test(data=data, action=action, request=request, pk=pk)
        return data

    def append_to_test(self, data, action, request, pk):
        """
        Appending a new test or to original test
        :param data: data of post
        :param action: action of request
        :param request: WSGI request
        :param pk: user pk
        :return: None
        """
        class_declaration = 'class Test{view_name}(TestCase):\n'.format(view_name=self.view_name)
        class_declaration_full = new_test.format(view_name=self.view_name)
        index = self.test_file_data.find(class_declaration)
        if index == -1:
            with open(self.tests_file, 'a') as (file):
                file.write(class_declaration_full + self.format_function(name=action, data=data, request=request, pk=pk))
        else:
            start = ''
            function_name = 'test_{action}'.format(action=action)
            prefix = ''
            end = ''
            before_declaration = True
            with open(self.tests_file, 'r') as (file_read):
                for i, line in enumerate(file_read):
                    if before_declaration:
                        start += line
                    else:
                        end += line
                    if function_name in line:
                        prefix = action
                    if line == class_declaration:
                        before_declaration = False

            name = action if not prefix else self.function_from_time(prefix=prefix)
            with open(self.tests_file, 'w+') as (file):
                file.write(start + self.format_function(name=name, data=data, request=request, pk=pk) + end)

    def format_function(self, name, data, request, pk):
        """
        Formatting a new test
        :param name: test name
        :param data: data of post
        :param request: WSGI request
        :param pk: user pk
        :return: new formatted test
        """
        return functions_template.format(action=name, result=data.data, request_data=request.data, request_user_pk=pk, override_settings=get_override_settings(attributes=self.use_current_settings_keys))

    @staticmethod
    def function_from_time(prefix='', suffix=''):
        """
        Generates a new function name from time
        :param prefix: prefix to append
        :param suffix: suffix to append
        :return: new function name (str)
        """
        return prefix + ('_' if prefix else '') + str(datetime.now()).replace(':', '_').replace('.', '_').replace('-', '_').replace(' ', '_') + ('_' if suffix else '') + suffix