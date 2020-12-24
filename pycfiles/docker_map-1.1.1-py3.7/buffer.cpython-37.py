# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/build/buffer.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 3927 bytes
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
import six
from tempfile import NamedTemporaryFile
from io import BytesIO

class FinalizedError(Exception):
    __doc__ = '\n    Exception type for indicating that a modification operation has been attempted on a :class:`~DockerBuffer` object,\n    that had already been finalized earlier.\n    '


class DockerBuffer(six.with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Abstract class for managing Docker file-like objects. Subclasses must override :meth:`create_fileobj` with\n    which constructs the actual file-like object. :meth:`save` should be implemented for saving to an actual file.\n    '

    def __init__(self, *args, **kwargs):
        self._fileobj = self.create_fileobj()
        self._finalized = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def create_fileobj(self):
        """
        Initializes a new file object.

        :return: File object.
        :rtype: file
        """
        pass

    def check_not_finalized(self):
        """
        Checks if the object has been marked as finalized. Should be called once before every write operation.

        :raise FinalizedError: If the object is finalized, and no further changes can be made.
        """
        if self._finalized:
            raise FinalizedError('File cannot be changed after it has been finalized.')

    @property
    def fileobj(self):
        """
        Read-only property, returning the reference to the file-like object.

        :return:
        """
        return self._fileobj

    def getvalue(self):
        """
        Returns the current value of the buffer.

        :return: Representation if the buffer.
        :rtype: unicode | str
        """
        return self._fileobj.getvalue()

    def finalize(self):
        """
        Marks the buffer as finalized, indicating that no further write operations should be performed. Subclasses
        should perform final operations just before this.
        """
        self._finalized = True

    @abstractmethod
    def save(self, name):
        """
        Saves the buffer content (e.g. to a file). This is abstract since it depends the type of the backing file-like
        object. Implementations will usually finalize the buffer.

        :param name: Name to store the contents under.
        :type name: unicode | str
        """
        pass

    def close(self):
        """
        Close the file object.
        """
        self._fileobj.close()


class DockerStringBuffer(six.with_metaclass(ABCMeta, DockerBuffer)):
    __doc__ = '\n    Partial implementation of :class:`~DockerBuffer`, backed by a :class:`~BytesIO` buffer.\n    '

    def create_fileobj(self):
        return BytesIO()

    def save(self, name):
        """
        Save the string buffer to a file. Finalizes prior to saving.

        :param name: File path.
        :type name: unicode | str
        """
        self.finalize()
        with open(name, 'wb+') as (f):
            if six.PY3:
                f.write(self.fileobj.getbuffer())
            else:
                f.write(self.fileobj.getvalue().encode('utf-8'))


class DockerTempFile(six.with_metaclass(ABCMeta, DockerBuffer)):
    __doc__ = '\n    Partial implementation of :class:`~DockerBuffer`, backed by a :class:`~tempfile.NamedTemporaryFile`.\n    '

    def create_fileobj(self):
        return NamedTemporaryFile('wb+')

    def save(self, name):
        """
        Copy the contents of the temporary file somewhere else. Finalizes prior to saving.

        :param name: File path.
        :type name: unicode | str
        """
        self.finalize()
        with open(name, 'wb+') as (f):
            buf = self._fileobj.read()
            while buf:
                f.write(buf)
                buf = self._fileobj.read()