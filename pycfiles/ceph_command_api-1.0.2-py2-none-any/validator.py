# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ceph_api/validator.py
# Compiled at: 2016-05-31 14:30:36
import six
__author__ = 'Chris Holcombe <chris.holcombe@canonical.com>'

def validator(value, valid_type, valid_range=None):
    """
    Used to validate these: http://docs.ceph.com/docs/master/rados/operations/pools/#set-pool-values
    Example input:
        validator(value=1,
                  valid_type=int,
                  valid_range=[0, 2])
    This says I'm testing value=1.  It must be an int inclusive in [0,2]

    :param value: The value to validate
    :param valid_type: The type that value should be.
    :param valid_range: A range of values that value can assume.
    :return:
    """
    assert isinstance(value, valid_type), ('{} is not a {}').format(value, valid_type)
    if valid_range is not None:
        assert isinstance(valid_range, list), ('valid_range must be a list, was given {}').format(valid_range)
        if valid_type is six.string_types:
            assert value in valid_range, ('{} is not in the list {}').format(value, valid_range)
        else:
            if len(valid_range) != 2:
                raise ValueError(('Invalid valid_range list of {} for {}.  List must be [min,max]').format(valid_range, value))
            assert value >= valid_range[0], ('{} is less than minimum allowed value of {}').format(value, valid_range[0])
            assert value <= valid_range[1], ('{} is greater than maximum allowed value of {}').format(value, valid_range[1])
    return