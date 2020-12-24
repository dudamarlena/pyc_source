# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/BaseIPC.py
# Compiled at: 2008-10-19 12:19:52
'''Base IPC class. Subclass it to create your own IPC classes.

When doing so, make sure you set the following:

- Its doc string, so a string explanation can be generated for an
  instance of your subclass.
- 'Parameters' class attribute to a list of named parameters you accept at creation, 
  prefixing optional parameters with "?", e.g. "?depth"

For example
-----------

A custom IPC class to report a theft taking place! ::

    class Theft(Kamaelia.BaseIPC.IPC):
        """Something has been stolen!"""
        
        Parameters = ["?who","what"]
        
So what happens when we use it? ::

    >>> ipc = Theft(who="Sam", what="sweeties")
    >>> ipc.__doc__
    'Something has been stolen!'
    >>> ipc.who
    'Sam'
    >>> ipc.what
    'sweeties'

'''

class IPC(object):
    """explanation %(foo)s did %(bar)s"""
    Parameters = []

    def __init__(self, **kwds):
        super(IPC, self).__init__()
        for param in self.Parameters:
            optional = False
            if param[:1] == '?':
                param = param[1:]
                optional = True
            if not kwds.has_key(param):
                if not optional:
                    raise ValueError(param + ' not given as a parameter to ' + str(self.__class__.__name__))
                else:
                    self.__dict__[param] = None
            else:
                self.__dict__[param] = kwds[param]
                del kwds[param]

        for additional in kwds.keys():
            raise ValueError('Unknown parameter ' + additional + ' to ' + str(self.__class__.__name__))

        self.__dict__.update(kwds)
        return

    def __str__(self):
        return self.__class__.__doc__ % self.__dict__