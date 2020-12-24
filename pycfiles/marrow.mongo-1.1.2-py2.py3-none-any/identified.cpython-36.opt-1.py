# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/identified.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1219 bytes
from ... import Document
from ...field import ObjectId

class Identified(Document):
    __doc__ = "A document utilizing this trait mix-in contains a MongoDB _id key.\n\t\n\tThis provides a read-only property to retrieve the creation time as `created`.\n\t\n\tIdentifiers are constructed on document instantiation; this means inserts are already provided an ID, bypassing\n\tthe driver's behaviour of only returning one after a successful insert. This allows for the pre-construction\n\tof graphs of objects prior to any of them being saved, though, until all references are resolveable, the data\n\tis effectively in a broken, inconsistent state.  (Use bulk updates and plan for rollback in the event of failure!)\n\t\n\tNo need for an explicit index on this as MongoDB will provide one automatically.\n\t"
    __pk__ = 'id'
    id = ObjectId('_id', assign=True, write=False, repr=False)

    def __eq__(self, other):
        """Equality comparison between the identifiers of the respective documents."""
        if isinstance(other, Document):
            return self.id == other.id
        else:
            return self.id == other

    def __ne__(self, other):
        """Inverse equality comparison between the backing store and other value."""
        return not self == other