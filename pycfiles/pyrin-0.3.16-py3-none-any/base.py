# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mono/workspace/pyrin_project/src/pyrin/packaging/base.py
# Compiled at: 2020-03-21 10:24:50
"""
packaging base module.
"""
from pyrin.core.structs import CoreObject
from pyrin.settings.static import DEFAULT_COMPONENT_KEY

class Package(CoreObject):
    """
    package base class.

    all application python packages should be subclassed from this.
    except some base packages like `application`, `core` and `utils` that
    should not implement Package class.
    """
    NAME = None
    DEPENDS = []
    ENABLED = True
    COMPONENT_NAME = None
    COMPONENT_CUSTOM_KEY = DEFAULT_COMPONENT_KEY
    CONFIG_STORE_NAMES = []
    EXTRA_CONFIG_STORE_NAMES = []

    def load_configs(self, config_services):
        """
        loads all required configs of this package.

        :param Module config_services: configuration services dependency.
                                       to be able to overcome circular dependency problem,
                                       we should inject configuration services dependency
                                       into this method. because all other packages are
                                       referenced `packaging.base` module in them, so we
                                       can't import `pyrin.configuration.services` in this
                                       module. this is more beautiful in comparison to
                                       importing it inside this method.
        """
        if len(self.CONFIG_STORE_NAMES) > 0:
            config_services.load_configurations(defaults=self.config_defaults, ignore_on_existed=True, *self.CONFIG_STORE_NAMES)
        if len(self.EXTRA_CONFIG_STORE_NAMES) > 0:
            config_services.create_config_files(ignore_on_existed=True, *self.EXTRA_CONFIG_STORE_NAMES)
        self._load_configs(config_services)

    def _load_configs(self, config_services):
        """
        loads all required configs of this package.

        this method is intended for overriding by
        subclasses to do custom configurations.

        :param Module config_services: configuration services dependency.
                                       to be able to overcome circular dependency problem,
                                       we should inject configuration services dependency
                                       into this method. because all other packages are
                                       referenced `packaging.base` module in them, so we
                                       can't import `pyrin.configuration.services` in this
                                       module. this is more beautiful in comparison to
                                       importing it inside this method.
        """
        pass

    @property
    def config_defaults(self):
        """
        gets config store default values that should be sent to config parser.

        it is used for interpolation.
        this method is intended to be overridden by subclasses.

        :rtype: dict
        """
        return