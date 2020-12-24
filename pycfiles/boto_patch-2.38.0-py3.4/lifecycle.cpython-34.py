# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/lifecycle.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8254 bytes
from boto.compat import six

class Rule(object):
    __doc__ = "\n    A Lifecycle rule for an S3 bucket.\n\n    :ivar id: Unique identifier for the rule. The value cannot be longer\n        than 255 characters. This value is optional. The server will\n        generate a unique value for the rule if no value is provided.\n\n    :ivar prefix: Prefix identifying one or more objects to which the\n        rule applies. If prefix is not provided, Boto generates a default\n        prefix which will match all objects.\n\n    :ivar status: If 'Enabled', the rule is currently being applied.\n        If 'Disabled', the rule is not currently being applied.\n\n    :ivar expiration: An instance of `Expiration`. This indicates\n        the lifetime of the objects that are subject to the rule.\n\n    :ivar transition: An instance of `Transition`.  This indicates\n        when to transition to a different storage class.\n\n    "

    def __init__(self, id=None, prefix=None, status=None, expiration=None, transition=None):
        self.id = id
        self.prefix = '' if prefix is None else prefix
        self.status = status
        if isinstance(expiration, six.integer_types):
            self.expiration = Expiration(days=expiration)
        else:
            self.expiration = expiration
        self.transition = transition

    def __repr__(self):
        return '<Rule: %s>' % self.id

    def startElement(self, name, attrs, connection):
        if name == 'Transition':
            self.transition = Transition()
            return self.transition
        if name == 'Expiration':
            self.expiration = Expiration()
            return self.expiration

    def endElement(self, name, value, connection):
        if name == 'ID':
            self.id = value
        else:
            if name == 'Prefix':
                self.prefix = value
            else:
                if name == 'Status':
                    self.status = value
                else:
                    setattr(self, name, value)

    def to_xml(self):
        s = '<Rule>'
        if self.id is not None:
            s += '<ID>%s</ID>' % self.id
        s += '<Prefix>%s</Prefix>' % self.prefix
        s += '<Status>%s</Status>' % self.status
        if self.expiration is not None:
            s += self.expiration.to_xml()
        if self.transition is not None:
            s += self.transition.to_xml()
        s += '</Rule>'
        return s


class Expiration(object):
    __doc__ = '\n    When an object will expire.\n\n    :ivar days: The number of days until the object expires\n\n    :ivar date: The date when the object will expire. Must be\n        in ISO 8601 format.\n    '

    def __init__(self, days=None, date=None):
        self.days = days
        self.date = date

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Days':
            self.days = int(value)
        elif name == 'Date':
            self.date = value

    def __repr__(self):
        if self.days is None:
            how_long = 'on: %s' % self.date
        else:
            how_long = 'in: %s days' % self.days
        return '<Expiration: %s>' % how_long

    def to_xml(self):
        s = '<Expiration>'
        if self.days is not None:
            s += '<Days>%s</Days>' % self.days
        elif self.date is not None:
            s += '<Date>%s</Date>' % self.date
        s += '</Expiration>'
        return s


class Transition(object):
    __doc__ = '\n    A transition to a different storage class.\n\n    :ivar days: The number of days until the object should be moved.\n\n    :ivar date: The date when the object should be moved.  Should be\n        in ISO 8601 format.\n\n    :ivar storage_class: The storage class to transition to.  Valid\n        values are GLACIER.\n\n    '

    def __init__(self, days=None, date=None, storage_class=None):
        self.days = days
        self.date = date
        self.storage_class = storage_class

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Days':
            self.days = int(value)
        else:
            if name == 'Date':
                self.date = value
            elif name == 'StorageClass':
                self.storage_class = value

    def __repr__(self):
        if self.days is None:
            how_long = 'on: %s' % self.date
        else:
            how_long = 'in: %s days' % self.days
        return '<Transition: %s, %s>' % (how_long, self.storage_class)

    def to_xml(self):
        s = '<Transition>'
        s += '<StorageClass>%s</StorageClass>' % self.storage_class
        if self.days is not None:
            s += '<Days>%s</Days>' % self.days
        elif self.date is not None:
            s += '<Date>%s</Date>' % self.date
        s += '</Transition>'
        return s


class Lifecycle(list):
    __doc__ = '\n    A container for the rules associated with a Lifecycle configuration.\n    '

    def startElement(self, name, attrs, connection):
        if name == 'Rule':
            rule = Rule()
            self.append(rule)
            return rule

    def endElement(self, name, value, connection):
        setattr(self, name, value)

    def to_xml(self):
        """
        Returns a string containing the XML version of the Lifecycle
        configuration as defined by S3.
        """
        s = '<?xml version="1.0" encoding="UTF-8"?>'
        s += '<LifecycleConfiguration>'
        for rule in self:
            s += rule.to_xml()

        s += '</LifecycleConfiguration>'
        return s

    def add_rule(self, id=None, prefix='', status='Enabled', expiration=None, transition=None):
        """
        Add a rule to this Lifecycle configuration.  This only adds
        the rule to the local copy.  To install the new rule(s) on
        the bucket, you need to pass this Lifecycle config object
        to the configure_lifecycle method of the Bucket object.

        :type id: str
        :param id: Unique identifier for the rule. The value cannot be longer
            than 255 characters. This value is optional. The server will
            generate a unique value for the rule if no value is provided.

        :type prefix: str
        :iparam prefix: Prefix identifying one or more objects to which the
            rule applies.

        :type status: str
        :param status: If 'Enabled', the rule is currently being applied.
            If 'Disabled', the rule is not currently being applied.

        :type expiration: int
        :param expiration: Indicates the lifetime, in days, of the objects
            that are subject to the rule. The value must be a non-zero
            positive integer. A Expiration object instance is also perfect.

        :type transition: Transition
        :param transition: Indicates when an object transitions to a
            different storage class. 
        """
        rule = Rule(id, prefix, status, expiration, transition)
        self.append(rule)