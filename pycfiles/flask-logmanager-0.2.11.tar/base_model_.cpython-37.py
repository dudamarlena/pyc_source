# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-logmanager/flask_logmanager/models/base_model_.py
# Compiled at: 2019-07-30 10:17:54
# Size of source mod 2**32: 1202 bytes
from pprint import pformat

class Model(object):

    @property
    def _propertys(self):
        return [attr for attr in self.__class__.__dict__ if self.__class__.__dict__[attr].__class__ == property]

    def from_dict(self, data):
        for attr in self._propertys:
            if attr in data.keys():
                setattr(self, attr, data[attr])

        return self

    def to_dict(self):
        """
        Returns the model properties as a dict

        :rtype: dict
        """
        result = {}
        for attr in self._propertys:
            result[attr] = getattr(self, attr)

        return result

    def to_str(self):
        """
        Returns the string representation of the model

        :rtype: str
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other