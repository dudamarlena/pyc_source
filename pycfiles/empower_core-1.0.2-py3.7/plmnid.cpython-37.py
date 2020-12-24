# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/plmnid.py
# Compiled at: 2020-05-10 06:48:34
# Size of source mod 2**32: 3955 bytes
"""Public land mobile network identifier (PLMNID)."""
from stdnum import numdb
from stdnum.util import clean, isdigits
from pymodm.errors import ValidationError
from pymodm.base.fields import MongoBaseField
from empower_core.serialize import serializable_string

@serializable_string
class PLMNID:
    __doc__ = 'Public land mobile network  identifier (PLMNID).'

    def __init__(self, plmnid):
        plmnid = clean(plmnid, ' -').strip().upper()
        if not isdigits(plmnid):
            raise ValueError('Invalid PLMNID %s' % plmnid)
        if len(plmnid) not in (4, 5):
            raise ValueError('Invalid PLMNID length %s' % plmnid)
        if len(tuple(numdb.get('imsi').split(plmnid))) < 2:
            raise ValueError('Invalid PLMNID format %s' % plmnid)
        self.info = dict(plmnid=plmnid)
        mcc_info, mnc_info = numdb.get('imsi').info(plmnid)
        self.info['mcc'] = mcc_info[0]
        self.info.update(mcc_info[1])
        self.info['mnc'] = mnc_info[0]
        self.info.update(mnc_info[1])

    @property
    def mcc(self):
        """Get mcc."""
        return self.info['mcc']

    @property
    def mnc(self):
        """Get mnc."""
        return self.info['mnc']

    def to_str(self):
        """Return an ASCII representation of the object."""
        return '%s%s' % (self.mcc, self.mnc)

    def to_tuple(self):
        """Return a tuple representation of the object."""
        return tuple(self.info.values())

    def to_dict(self):
        """Return a dict representation of the object."""
        return self.info

    def __str__(self):
        return self.to_str()

    def __len__(self):
        return len(self.to_str())

    def __hash__(self):
        return hash(self.to_str())

    def __eq__(self, other):
        if isinstance(other, PLMNID):
            return self.to_str() == other.to_str()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"


class PLMNIDField(MongoBaseField):
    __doc__ = 'A field that stores PLMNIDs.'

    def __init__(self, verbose_name=None, mongo_name=None, **kwargs):
        (super(PLMNIDField, self).__init__)(verbose_name=verbose_name, mongo_name=mongo_name, **kwargs)

        def validate_plmnid(value):
            try:
                if isinstance(value, PLMNID):
                    value = value.to_str()
                return PLMNID(value)
            except ValueError:
                msg = '%r is not a valid PLMNID.' % value
                raise ValidationError(msg)

        self.validators.append(validate_plmnid)

    @classmethod
    def to_mongo(cls, value):
        """Convert value for storage."""
        try:
            return value.to_str()
        except ValueError:
            msg = '%r is not a valid PLMNID.' % value
            raise ValidationError(msg)

    @classmethod
    def to_python(cls, value):
        """Convert value back to Python."""
        try:
            if isinstance(value, PLMNID):
                value = value.to_str()
            return PLMNID(value)
        except ValueError:
            msg = '%r is not a valid PLMNID.' % value
            raise ValidationError(msg)