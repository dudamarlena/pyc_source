# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/commonruntime/SettingsLoader.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 2492 bytes
""" Class description goes here. """
from abc import ABCMeta, abstractmethod
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
from dataclay.commonruntime.Runtime import getRuntime
import six

@six.add_metaclass(ABCMeta)
class AbstractLoader(object):
    __doc__ = 'An abstraction to allow lazy evaluation of settings fields.\n\n    See dataclay.conf._SettingsHub to check the behaviour and purpose of this\n    class. The different loaders expose an abstraction to allow lazy and late\n    initialization of variable values.\n    '

    @abstractmethod
    def __init__(self, settings_object):
        self._settings = settings_object

    @abstractmethod
    def load_value(self):
        """Perform the active load of the requested value.

        This is typically executed only once, as the settings will store the
        real object in its place.

        :return: The expected commonruntime value for the settings field.
        """
        pass


class AccountIdLoader(AbstractLoader):

    def __init__(self, settings_object, field_of_account_name):
        self._field = field_of_account_name
        super(AccountIdLoader, self).__init__(settings_object)

    def load_value(self):
        account_name = getattr(self._settings, self._field)
        return getRuntime().ready_clients['@LM'].get_account_id(account_name)


class AccountCredentialLoader(AbstractLoader):

    def __init__(self, settings_object, field_of_account_id, field_of_account_password):
        self._field_id = field_of_account_id
        self._field_password = field_of_account_password
        super(AccountCredentialLoader, self).__init__(settings_object)

    def load_value(self):
        return (
         getattr(self._settings, self._field_id),
         getattr(self._settings, self._field_password))