# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/test_util/compat.py
# Compiled at: 2010-06-19 05:25:39
__all__ = [
 'EnvironmentStub']
from trac import __version__ as trac_version
if trac_version.startswith('0.12'):
    from trac.test import EnvironmentStub
    EnvironmentStub = EnvironmentStub
else:
    from trac.env import Environment
    from trac.test import EnvironmentStub

    class FixedEnvironmentStub(EnvironmentStub):
        """Since the release of trac 0.11 a lot of bugs were fixed in the 
        EnvironmentStub. This class provides backports of these fixes so plugins
        can support older trac versions as well."""

        def __init__(self, default_data=False, enable=None):
            super(FixedEnvironmentStub, self).__init__(default_data=default_data, enable=enable)
            if enable is not None:
                self.config.set('components', 'trac.*', 'disabled')
            for name_or_class in enable or ():
                config_key = self.normalize_configuration_key(name_or_class)
                self.config.set('components', config_key, 'enabled')

            return

        def normalize_configuration_key(self, name_or_class):
            name = name_or_class
            if not isinstance(name_or_class, basestring):
                name = name_or_class.__module__ + '.' + name_or_class.__name__
            return name.lower()

        def is_component_enabled(self, cls):
            return Environment.is_component_enabled(self, cls)

        def get_known_users(self, db=None):
            return self.known_users


    EnvironmentStub = FixedEnvironmentStub