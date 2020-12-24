# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/interfaces.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 5148 bytes
"""
Defines functional models as interfaces to specify the functionality most
classes must provide in order to fulfill the puzzle-friendliness
"""
from abc import ABCMeta, abstractmethod
from bitcoin import base58

class Serializable(object):
    __doc__ = '\n    Defines a model for a class that will be serializable, this means, will\n    have methods to transform the class into an array of bytes and to create\n    a new object of the class from an array of bytes.\n\n    Those arrays of bytes will always have to be compatible with the bytes\n    specified in the Bitcoin protocol\n\n    When we say an array of bytes we mean an instance of Python 3 `bytes`\n    object\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def serialize(self):
        """
        Serializes the contents of the current class into an array of bytes so
        the object can be represented as an array of bytes compatible with what
        the Bitcoin protocol specifies

        Returns:
            bytes: data of the class serialized in a bytes object
        """
        raise NotImplementedError("Class should have implemented this, but developers of the app aren't so fast")

    @classmethod
    def deserialize(cls, data):
        """
        Deserializes the contents of the data passed to try make them fit into
        the class model to create a new object from this data. If the data has
        invalid length or invalid data, appropiate exceptions will be raised.

        Please implement this method in a way that the bytes data can be sized
        more than the strictly required size, specially for variable sized
        fields, so it will help caller methods to detect size after calling
        deserialization

        As a class method, the method returns an instance of a filled object

        Args:
            cls (class): class of the object to deserialize
            data (bytes): a bytes object containing data to de-serialize

        Returns:
            cls(): an instance of the class filled with the data if succeeded

        Raises:
            ValueError: if data can't be fit into the model
        """
        raise NotImplementedError("Class should have implemented this, but developers of the app aren't so fast")

    def __len__(self):
        """
        Returns the length in bytes of the serialized object

        Returns:
            int: number of bytes the serialized object takes
        """
        return len(self.serialize())


class Encodable(object):
    __doc__ = '\n    This interface defines that classes who inherit from it can be encoded into\n    an object and decoded from an object. The difference between the previous\n    class is that the serializable class is supposed to serialize to bytes\n    objects and be deserialized from them. An encodable class when encoded\n    contains enough information to then decode the output and obtain the same\n    information but with the difference that when encoding, the result is not\n    an array of bytes and is an object, most times a string object\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def encode(self):
        """
        Encodes the information of the class into an object so that this object
        can be then decoded into another object of this class with the same
        information

        Returns:
            object: object containing the encoded information of the class
        """
        pass

    @classmethod
    def decode(cls, obj):
        """
        Decodes the object passed and tries to generate a new object of the
        class with the contents of the passed object

        Args:
            cls (class): class to decode the object into
            obj (object): object containing information to set class status

        Returns:
            cls(): an object with the status filled

        Raises:
            ValueError: if object passed can't be decoded
        """
        pass


class Base58Encodable(Encodable):
    __doc__ = '\n    Same as previous Encodable interface, but specifies that will be encoded\n    into a base58 string and decoded from a base58 string.\n\n    Also provides a default, and valid implementation\n    '

    def encode(self):
        """
        Returns the object as a base-58 string with the array of bytes (the
        serialized object)
        """
        return base58.encode(self.serialize())

    @classmethod
    def decode(cls, string):
        """
        Given a base-58 encoded object, decodes it and deserializes it,
        returning a new object containing the deserialized information

        Args:
            string (str): base-58 encoded string

        Returns:
            cls: a new object filled with the values that the string contained

        Raises:
            ValueError: if can't be decoded
        """
        return cls.deserialize(base58.decode(string))

    def __str__(self):
        """ Returns the field as a printable string """
        return '<%s:%s>' % (self.encode(), self.__class__.__name__)