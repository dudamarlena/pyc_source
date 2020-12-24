# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/reference.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 2831 bytes
import importlib
from firestore import Document, Collection
from firestore.datatypes.base import Base
from firestore.db.connection import ResultSet

class Reference(Base):
    __doc__ = 'Firestore referable elements i.e. Project ID,\n    Document ID etc.\n    '
    __slots__ = ('_name', 'doc_ref', 'py_type')

    def __init__(self, *args, **kwargs):
        try:
            self.doc_ref = args[0]
        except IndexError:
            raise TypeError('Reference type must accept a document to reference and can not be empty')

        self.py_type = Document
        whitelist = (
         Document, Collection)
        try:
            passed = issubclass(self.doc_ref, whitelist) or isinstance(self.doc_ref, whitelist)
        except:
            raise ValueError
        else:
            if not passed:
                raise ValueError(f"Reference must be a {Document}")

    def cast(self, instance, value):
        """
        Since validate in the reference descriptor
        returns a __loaded__ document we take
        advantage of that to return the docref
        """
        doc = self.validate(value, instance)
        return doc.__loaded__

    def __get__(self, instance, metadata):
        """
        Get the document that is being referenced. If the
        document was assigned directly then value will be
        set else load a new document and return
        """
        if self.value:
            return self.value
        __loaded_ref__ = instance.get_field(self)
        if __loaded_ref__:
            return self.doc_ref(__loaded_ref__.get().to_dict())

    def __set__(self, instance, value):
        """
        Set the reference document with a lookup to
        Google Cloud Firestore for existence of such
        a reference.
        Also set mutated on the instance to true as the instance
        has changed after the reference is set
        """
        doc = self.validate(value, instance)
        self.value = doc
        instance.add_field(self, self.value.__loaded__)
        instance.__mutated__ = True

    def validate(self, value, instance=None):
        if isinstance(value, str):
            result_set = self.doc_ref.get(value)
            if not result_set:
                msg = f"Could not dereference {self.doc_ref} from {value}"
                raise ValueError(msg)
            return result_set.first()
        if isinstance(value, self.doc_ref):
            if value.__loaded__:
                return value
            msg = f"Reference document {value} not yet saved to GCF"
            raise ValueError(msg)
        else:
            clsname = type(instance).__name__
            raise AttributeError(f"{clsname} expected a `{self.doc_ref}` not a {type(value)}")