# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/interpreter_option.py
# Compiled at: 2019-06-12 02:08:19
# Size of source mod 2**32: 6494 bytes
from pocsuite3.lib.core.common import is_ipv6_address_format, is_ip_address_format
from pocsuite3.lib.core.exception import PocsuiteValidationException

class Option(object):
    """Option"""

    def __init__(self, default, description='', require=False):
        self.description = description
        self.require = require
        self.display_value = default
        if default:
            self.__set__('', default)
        else:
            self.value = ''

    def __get__(self, instance, owner):
        return self.value

    def __iter__(self):
        iters = dict(((x, y) for x, y in Option.__dict__.items() if x[:2] != '__'))
        iters.update(self.__dict__)
        for x, y in iters.items():
            yield (
             x, y)


class OptIP(Option):
    """OptIP"""

    def __init__(self, default, description='', require=False):
        super().__init__(default, description, require)
        if description == '':
            self.description = 'IPv4 or IPv6 address'
        self.type = 'Ip'

    def __set__(self, instance, value):
        if value:
            if is_ip_address_format(value) or is_ipv6_address_format(value):
                self.value = self.display_value = value
        else:
            raise PocsuiteValidationException('Invalid address. Provided address is not valid IPv4 or IPv6 address.')


class OptPort(Option):
    """OptPort"""

    def __init__(self, default, description='', require=False):
        super().__init__(default, description, require)
        if description == '':
            self.description = 'Target HTTP port'
        self.type = 'Port'

    def __set__(self, instance, value):
        try:
            value = int(value)
            if 0 <= value <= 65535:
                self.display_value = str(value)
                self.value = value
            else:
                raise PocsuiteValidationException('Invalid option. Port value should be between 0 and 65536.')
        except ValueError:
            raise PocsuiteValidationException("Invalid option. Cannot cast '{}' to integer.".format(value))


class OptBool(Option):
    """OptBool"""

    def __init__(self, default, description='', require=False):
        super().__init__(default, description, require)
        if default:
            self.display_value = 'true'
        else:
            self.display_value = 'false'
        self.value = default
        self.type = 'Bool'

    def __set__(self, instance, value):
        if isinstance(value, bool):
            self.value = value
            return
        elif value.lower() == 'true':
            self.value = True
            self.display_value = value
        elif value.lower() == 'false':
            self.value = False
            self.display_value = value
        else:
            raise PocsuiteValidationException('Invalid value. It should be true or false.')


class OptInteger(Option):
    """OptInteger"""

    def __init__(self, default, description='', require=False):
        super().__init__(default, description, require)
        self.type = 'Integer'

    def __set__(self, instance, value):
        try:
            self.display_value = str(value)
            self.value = int(value)
        except ValueError:
            raise PocsuiteValidationException("Invalid option. Cannot cast '{}' to integer.".format(value))


class OptFloat(Option):
    """OptFloat"""

    def __init__(self, default, description='', require=False):
        super().__init__(default, description, require)
        self.type = 'Float'

    def __set__(self, instance, value):
        try:
            self.display_value = str(value)
            self.value = float(value)
        except ValueError:
            raise PocsuiteValidationException("Invalid option. Cannot cast '{}' to float.".format(value))


class OptString(Option):
    """OptString"""

    def __init__(self, default, description='', require=False):
        super().__init__(default, description, require)
        self.type = 'String'

    def __set__(self, instance, value):
        try:
            self.value = self.display_value = str(value)
        except ValueError:
            raise PocsuiteValidationException("Invalid option. Cannot cast '{}' to string.".format(value))


class OptItems(Option):

    def __init__(self, default, description='', selected='', require=False):
        super().__init__(default, description, require)
        self.selected = selected
        self.type = 'Select'
        self.__set__('', selected)
        if description == '':
            self.description = 'You can select {} ,default:{}'.format(repr(default), self.selected)

    def __set__(self, instance, value):
        self.value = value


class OptDict:

    def __init__(self, require=False, selected=False, default={}):
        self.default = {}
        b = ''
        for k, v in default.items():
            self.default[k] = v
            b += '{k}:{v}\n'.format(k=k, v=v)

        self.selected = selected
        self.require = require
        self.type = 'Dict'
        self.__set__('', selected)
        self.description = '{}\nYou can select {} ,default:{}'.format(b, repr(self.default.keys()), self.selected)

    def __set__(self, instance, value):
        self.value = self.default[value] if value in self.default else value