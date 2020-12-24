# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/devops/config.py
# Compiled at: 2019-09-26 19:05:14
# Size of source mod 2**32: 596 bytes
from configirl import ConfigClass, Constant, Derivable

class Config(ConfigClass):
    METADATA = Constant(default=(dict()))
    PROJECT_NAME = Constant()
    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_project_name_slug(self):
        return self.PROJECT_NAME.get_value().replace('_', '-')

    STAGE = Constant()
    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return '{}-{}'.format(self.PROJECT_NAME_SLUG.get_value(self), self.STAGE.get_value())