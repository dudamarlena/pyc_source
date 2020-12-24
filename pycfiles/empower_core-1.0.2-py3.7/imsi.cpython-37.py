# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/imsi.py
# Compiled at: 2020-05-10 06:48:34
# Size of source mod 2**32: 4263 bytes
"""international mobile subscriber identity (IMSI)."""
import re
from stdnum import numdb
from stdnum.util import clean, isdigits
from pymodm.errors import ValidationError
from pymodm.base.fields import MongoBaseField
from empower_core.plmnid import PLMNID
from empower_core.serialize import serializable_string

@serializable_string
class IMSI:
    __doc__ = 'international mobile subscriber identity (IMSI).'

    def __init__(self, imsi):
        imsi = clean(imsi, ' -').strip().upper()
        if not isdigits(imsi):
            raise ValueError('Invalid IMSI %s' % imsi)
        if len(imsi) not in (14, 15):
            raise ValueError('Invalid IMSI length %s' % imsi)
        if len(tuple(numdb.get('imsi').split(imsi))) < 2:
            raise ValueError('Invalid IMSI length %s' % imsi)
        self.info = dict(imsi=imsi)
        mcc_info, mnc_info, msin_info = numdb.get('imsi').info(imsi)
        self.info['mcc'] = mcc_info[0]
        self.info.update(mcc_info[1])
        self.info['mnc'] = mnc_info[0]
        self.info.update(mnc_info[1])
        self.info['msin'] = msin_info[0]
        self.info.update(msin_info[1])

    @property
    def plmnid(self):
        """Get mcc."""
        return PLMNID('%s%s' % (self.mcc, self.mnc))

    @property
    def mcc(self):
        """Get mcc."""
        return self.info['mcc']

    @property
    def mnc(self):
        """Get mnc."""
        return self.info['mnc']

    @property
    def msin(self):
        """Get msin."""
        return self.info['msin']

    def to_str(self):
        """Return an ASCII representation of the object."""
        return '%s%s%s' % (self.mcc, self.mnc, self.msin)

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
        if isinstance(other, IMSI):
            return self.to_str() == other.to_str()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"


class IMSIField(MongoBaseField):
    __doc__ = 'A field that stores IMSIs.'

    def __init__(self, verbose_name=None, mongo_name=None, **kwargs):
        (super(IMSIField, self).__init__)(verbose_name=verbose_name, mongo_name=mongo_name, **kwargs)

        def validate_imsi(value):
            try:
                if isinstance(value, IMSI):
                    value = value.to_str()
                return PLMNID(value)
            except ValueError:
                msg = '%r is not a valid IMSI.' % value
                raise ValidationError(msg)

        self.validators.append(validate_imsi)

    @classmethod
    def to_mongo(cls, value):
        """Convert value for storage."""
        try:
            return value.to_str()
        except ValueError:
            msg = '%r is not a valid IMSI.' % value
            raise ValidationError(msg)

    @classmethod
    def to_python(cls, value):
        """Convert value back to Python."""
        try:
            if isinstance(value, IMSI):
                value = value.to_str()
            return IMSI(value)
        except ValueError:
            msg = '%r is not a valid IMSI.' % value
            raise ValidationError(msg)