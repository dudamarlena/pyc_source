# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/response/BaseResponse.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1150 bytes


class BaseResponse:
    response = None

    def __init__(self, response):
        self.response = response

    def get_response_property_name(self, property_name, response=None, exact_name=False):
        if not property_name is None:
            if property_name == '':
                raise Exception('propertyName must not be null/empty.')
            if response is None:
                if self.response is not None:
                    response = self.response
            if response is None:
                return
        elif not exact_name:
            if property_name not in response:
                if property_name[0] == property_name[0].upper():
                    other_case_property_name = property_name[0].lower()
                else:
                    other_case_property_name = property_name[0].upper()
                if len(property_name) > 1:
                    other_case_property_name += property_name[1:]
                property_name = other_case_property_name
                if property_name not in response:
                    property_name = property_name.lower()
                if property_name not in response:
                    property_name = property_name.upper()
        return response.get(property_name)