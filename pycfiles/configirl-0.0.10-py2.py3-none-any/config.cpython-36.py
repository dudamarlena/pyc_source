# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/configirl-project/configirl/tests/config.py
# Compiled at: 2020-04-19 20:27:04
# Size of source mod 2**32: 607 bytes
from configirl import ConfigClass, Constant, Derivable

class Config(ConfigClass):
    PROJECT_NAME = Constant(default='my_devops')
    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_PROJECT_NAME_SLUG(self):
        return self.PROJECT_NAME.get_value().replace('_', '-')

    STAGE = Constant(default='dev')
    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return '{}-{}'.format(self.PROJECT_NAME_SLUG.get_value(), self.STAGE.get_value())

    def is_prod_runtime(self):
        return False