# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/models/fields/DateField.py
# Compiled at: 2016-04-19 10:47:47
"""
.. module:: DateField
    :synopsis: A :mod:`mongoengine` custom field that stores a
        :class:`datetime.date` object as a :class:`datetime.datetime`.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""
from mongoengine.fields import DateTimeField
from datetime import datetime, date

class DateField(DateTimeField):
    """A datetime.date field.

    Looks to the outside world like a ``datatime.date``, but functions
    as a ``datetime.datetime`` object in the database.
    """

    def to_python(self, value):
        """Convert from :class:``datetime.datetime`` to
        :class:``datetime.date``.

        This overwrites the :class:`mongoengine.fields.DateTimeField`` method
        for accessing the value of this field.

        :param value: The date from mongo
        :type value: :class:`datetime.datetime` or :class:`datetime.date`
        :returns: The same date
        :rtype: :class:`datetime.date`
        :raises: ValueError
        """
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        raise ValueError("Unkown type '%r' of variable %r", type(value), value)