# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sdb/item.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6885 bytes
import base64

class Item(dict):
    """Item"""

    def __init__(self, domain, name='', active=False):
        """
        :type domain: :py:class:`boto.sdb.domain.Domain`
        :param domain: The domain that this item belongs to.

        :param str name: The name of this item. This name will be used when
            querying for items using methods like
            :py:meth:`boto.sdb.domain.Domain.get_item`
        """
        dict.__init__(self)
        self.domain = domain
        self.name = name
        self.active = active
        self.request_id = None
        self.encoding = None
        self.in_attribute = False
        self.converter = self.domain.connection.converter

    def startElement(self, name, attrs, connection):
        if name == 'Attribute':
            self.in_attribute = True
        self.encoding = attrs.get('encoding', None)

    def decode_value(self, value):
        if self.encoding == 'base64':
            self.encoding = None
            return base64.decodestring(value)
        else:
            return value

    def endElement(self, name, value, connection):
        if name == 'ItemName':
            self.name = self.decode_value(value)
        else:
            if name == 'Name':
                if self.in_attribute:
                    self.last_key = self.decode_value(value)
                else:
                    self.name = self.decode_value(value)
            else:
                if name == 'Value':
                    if self.last_key in self:
                        if not isinstance(self[self.last_key], list):
                            self[self.last_key] = [
                             self[self.last_key]]
                        value = self.decode_value(value)
                        if self.converter:
                            value = self.converter.decode(value)
                        self[self.last_key].append(value)
                    else:
                        value = self.decode_value(value)
                        if self.converter:
                            value = self.converter.decode(value)
                        self[self.last_key] = value
                elif name == 'BoxUsage':
                    try:
                        connection.box_usage += float(value)
                    except:
                        pass

                else:
                    if name == 'RequestId':
                        self.request_id = value
                    else:
                        if name == 'Attribute':
                            self.in_attribute = False
                        else:
                            setattr(self, name, value)

    def load(self):
        """
        Loads or re-loads this item's attributes from SDB.

        .. warning::
            If you have changed attribute values on an Item instance,
            this method will over-write the values if they are different in
            SDB. For any local attributes that don't yet exist in SDB,
            they will be safe.
        """
        self.domain.get_attributes(self.name, item=self)

    def save(self, replace=True):
        """
        Saves this item to SDB.

        :param bool replace: If ``True``, delete any attributes on the remote
            SDB item that have a ``None`` value on this object.
        """
        self.domain.put_attributes(self.name, self, replace)
        if replace:
            del_attrs = []
            for name in self:
                if self[name] is None:
                    del_attrs.append(name)
                    continue

            if len(del_attrs) > 0:
                self.domain.delete_attributes(self.name, del_attrs)

    def add_value(self, key, value):
        """
        Helps set or add to attributes on this item. If you are adding a new
        attribute that has yet to be set, it will simply create an attribute
        named ``key`` with your given ``value`` as its value. If you are
        adding a value to an existing attribute, this method will convert the
        attribute to a list (if it isn't already) and append your new value
        to said list.

        For clarification, consider the following interactive session:

        .. code-block:: python

            >>> item = some_domain.get_item('some_item')
            >>> item.has_key('some_attr')
            False
            >>> item.add_value('some_attr', 1)
            >>> item['some_attr']
            1
            >>> item.add_value('some_attr', 2)
            >>> item['some_attr']
            [1, 2]

        :param str key: The attribute to add a value to.
        :param object value: The value to set or append to the attribute.
        """
        if key in self:
            if not isinstance(self[key], list):
                self[key] = [
                 self[key]]
            self[key].append(value)
        else:
            self[key] = value

    def delete(self):
        """
        Deletes this item in SDB.

        .. note:: This local Python object remains in its current state
            after deletion, this only deletes the remote item in SDB.
        """
        self.domain.delete_item(self)