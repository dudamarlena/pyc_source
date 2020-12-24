# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/ec2object.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 5554 bytes
__doc__ = '\nRepresents an EC2 Object\n'
from boto.ec2.tag import TagSet

class EC2Object(object):

    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        setattr(self, name, value)


class TaggedEC2Object(EC2Object):
    """TaggedEC2Object"""

    def __init__(self, connection=None):
        super(TaggedEC2Object, self).__init__(connection)
        self.tags = TagSet()

    def startElement(self, name, attrs, connection):
        if name == 'tagSet':
            return self.tags
        else:
            return

    def add_tag(self, key, value='', dry_run=False):
        """
        Add a tag to this object.  Tags are stored by AWS and can be used
        to organize and filter resources.  Adding a tag involves a round-trip
        to the EC2 service.

        :type key: str
        :param key: The key or name of the tag being stored.

        :type value: str
        :param value: An optional value that can be stored with the tag.
                      If you want only the tag name and no value, the
                      value should be the empty string.
        """
        self.add_tags({key: value}, dry_run)

    def add_tags(self, tags, dry_run=False):
        """
        Add tags to this object.  Tags are stored by AWS and can be used
        to organize and filter resources.  Adding tags involves a round-trip
        to the EC2 service.

        :type tags: dict
        :param tags: A dictionary of key-value pairs for the tags being stored.
                     If for some tags you want only the name and no value, the
                     corresponding value for that tag name should be an empty
                     string.
        """
        status = self.connection.create_tags([
         self.id], tags, dry_run=dry_run)
        if self.tags is None:
            self.tags = TagSet()
        self.tags.update(tags)

    def remove_tag(self, key, value=None, dry_run=False):
        """
        Remove a tag from this object.  Removing a tag involves a round-trip
        to the EC2 service.

        :type key: str
        :param key: The key or name of the tag being stored.

        :type value: str
        :param value: An optional value that can be stored with the tag.
                      If a value is provided, it must match the value currently
                      stored in EC2.  If not, the tag will not be removed.  If
                      a value of None is provided, the tag will be
                      unconditionally deleted.
                      NOTE: There is an important distinction between a value
                      of '' and a value of None.
        """
        self.remove_tags({key: value}, dry_run)

    def remove_tags(self, tags, dry_run=False):
        """
        Removes tags from this object.  Removing tags involves a round-trip
        to the EC2 service.

        :type tags: dict
        :param tags: A dictionary of key-value pairs for the tags being removed.
                     For each key, the provided value must match the value
                     currently stored in EC2.  If not, that particular tag will
                     not be removed.  However, if a value of None is provided,
                     the tag will be unconditionally deleted.
                     NOTE: There is an important distinction between a value of
                     '' and a value of None.
        """
        status = self.connection.delete_tags([
         self.id], tags, dry_run=dry_run)
        for key, value in tags.items():
            if key in self.tags:
                if value is None or value == self.tags[key]:
                    del self.tags[key]
                else:
                    continue