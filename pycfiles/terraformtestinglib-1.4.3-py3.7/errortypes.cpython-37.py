# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/terraformtestinglib/terraformtestinglib/utils/errortypes.py
# Compiled at: 2019-10-22 09:06:51
# Size of source mod 2**32: 4896 bytes
"""
Main code for errortypes.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from collections import namedtuple
from colored import fore, style
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
RuleError = namedtuple('RuleError', ['resource_type', 'entity', 'field', 'regex', 'value', 'original_value'])
ConfigurationError = namedtuple('ConfigurationError', [
 'resource_type', 'entity', 'field', 'regex', 'value', 'original_value'])

class ResourceError:
    __doc__ = 'Models the Resource error and provides a nice printed version.'

    def __init__(self, filename, resource, entity, field, regex, value, original_value):
        self.filename = filename
        self.resource = resource
        self.entity = entity
        self.field = field
        self.regex = regex
        self.value = value
        self.original_value = original_value

    def __str__(self):
        filename = fore.RED + style.BOLD + self.filename + '/' + self.resource + style.RESET
        resource = fore.RED + style.BOLD + self.entity + style.RESET
        regex = fore.RED + style.BOLD + self.regex + style.RESET
        value = fore.RED + style.BOLD + self.value + style.RESET
        field = fore.RED + style.BOLD + self.field + style.RESET
        text = 'Naming convention not followed on file {filename} for resource {resource} for field {field}\n\tRegex not matched : {regex}\n\tValue             : {value}'.format(filename=filename,
          resource=resource,
          regex=regex,
          value=value,
          field=field)
        if self.original_value:
            original = fore.RED + style.BOLD + self.original_value + style.RESET
            text += '\n\tOriginal Value    : {original}'.format(original=original)
        return text


class FilenameError:
    __doc__ = 'Models the Filename error and provides a nice printed version.'

    def __init__(self, filename, resource, target):
        self.filename = filename
        self.resource = resource
        self.target = target

    def __str__(self):
        filename = fore.RED + style.BOLD + self.filename + '/' + self.resource + style.RESET
        resource = fore.RED + style.BOLD + self.resource + style.RESET
        target = fore.RED + style.BOLD + self.target + style.RESET
        return 'Filename positioning not followed on file {filename} for resource {resource}. \n\tShould be in file : {target}.'.format(filename=filename,
          resource=resource,
          target=target)