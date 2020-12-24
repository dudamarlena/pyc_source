# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/transforms/transform.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 3473 bytes


class GlueTransform(object):
    __doc__ = 'Base class for all Glue Transforms.\n\n    All Glue transformations should inherit from GlueTransform and define a\n    __call__ method. They can optionally override the name classmethod or use\n    the default of the class name.\n    '

    @classmethod
    def apply(cls, *args, **kwargs):
        transform = cls()
        return transform(*args, **kwargs)

    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def describeArgs(cls):
        """
        Returns: a list of dictionaries, with each corresponding to
        an argument, in the following format:
                [{"name": "<name of argument>",
                 "type": "<type of argument>",
                 "description": "<description of argument>",
                 "optional": "<Boolean>",
                 "defaultValue": "<String default value or None>"}, ...]
        Raises: NotImplementedError if not implemented by Transform
        """
        raise NotImplementedError('describeArgs method not implemented for Transform {}'.format(cls.__name__))

    @classmethod
    def describeReturn(cls):
        """
        Returns: A dictionary with information about the return type,
        in the following format:
                {"type": "<return type>",
                "description": "<description of output>"}
        Raises: NotImplementedError if not implemented by Transform
        """
        raise NotImplementedError('describeReturn method not implemented for Transform {}'.format(cls.__name__))

    @classmethod
    def describeTransform(cls):
        """
        Returns: A string describing the transform, e.g.
                "Base class for all Glue Transforms"
        Raises: NotImplementedError if not implemented by Transform
        """
        raise NotImplementedError('describeTransform method not implemented for Transform {}'.format(cls.__name__))

    @classmethod
    def describeErrors(cls):
        """
        Returns: A list of dictionaries, each describing possible errors thrown by
        this transform, in the following format:
                [{"type": "<type of error>",
                 "description": "<description of error>"}]
        Raises: NotImplementedError if not implemented by Transform
        """
        raise NotImplementedError('describeErrors method not implemented for Transform {}'.format(cls.__name__))

    @classmethod
    def describe(cls):
        return {'transform': {'name':cls.name(),  'args':cls.describeArgs(), 
                       'returns':cls.describeReturn(), 
                       'description':cls.describeTransform(), 
                       'raises':cls.describeErrors(), 
                       'location':'internal'}}

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __repr__(self):
        return '<Transform: {}>'.format(self.name())