# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/teamscale_client/utils.py
# Compiled at: 2020-03-30 02:50:39


def auto_str(cls):
    """Annotation that provides a default __str__ method for objects.
    
    Example: 
        Annotating a class with the ``@auto_str`` annotation::
        
            >>> @auto_str
                class Dummy(object):
                    def __init__(self, a):
                        self.a = a
                    
            >>> sample = Dummy("test")
            >>> print(sample) 
            Dummy(a=test)
    """

    def __str__(self):
        return '%s(%s)' % (
         type(self).__name__,
         (', ').join('%s=%s' % item for item in vars(self).items()))

    cls.__str__ = __str__
    return cls


def to_json(obj):
    """Utility method for converting an object to a json encoded string. 
    
    Takes care of all the necessary setup.
    
    Args:
        obj (object): The object that should be encoded.
        
    Returns:
        str: The encoded version of the given object.
    """
    import jsonpickle
    jsonpickle.set_encoder_options('simplejson', sort_keys=True)
    return jsonpickle.encode(obj, unpicklable=False)