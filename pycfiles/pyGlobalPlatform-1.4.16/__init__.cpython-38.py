# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Repos\TestLibs\pyglobal\pyglobal\__init__.py
# Compiled at: 2020-05-06 00:06:30
# Size of source mod 2**32: 4607 bytes
from .__meta__ import version as __version__
__all__ = [
 'GlobalSettings', 'get', 'set', 'clear', 'default']
try:
    from .cglobal import GlobalSettings
except (ImportError, Exception):

    class GlobalSettings(object):
        """GlobalSettings"""

        def __init__(self):
            self._GlobalSettings__container = {}

        def __get_scope(self, scope=None):
            if scope not in self._GlobalSettings__container:
                self._GlobalSettings__container[scope] = {}
            return self._GlobalSettings__container[scope]

        def get--- This code section failed: ---

 L.  30         0  SETUP_FINALLY        22  'to 22'

 L.  31         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _GlobalSettings__get_scope
                6  LOAD_FAST                'scope'
                8  CALL_METHOD_1         1  ''
               10  LOAD_METHOD              get
               12  LOAD_FAST                'key'
               14  LOAD_FAST                'default'
               16  CALL_METHOD_2         2  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.  32        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  LOAD_GLOBAL              Exception
               28  BUILD_TUPLE_2         2 
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  33        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'
               46  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 22

        def set(self, key, value, scope=None):
            """Set the stored value with the given key.

            Args:
                 key (str): Key to access the stored object with.
                 value (object): Store this object.
                 scope (str)[None]: Additional key to prevent clashing.
            """
            self._GlobalSettings__get_scopescope[key] = value

        def default(self, key, value, scope=None):
            """Set the default value for the given key.

            Args:
                 key (str): Key to access the stored object with.
                 value (object): Store this object.
                 scope (str)[None]: Additional key to prevent clashing.
            """
            self._GlobalSettings__get_scopescope.setdefaultkeyvalue

        def clear(self, key=None, scope=None):
            """Clear the given key or all storage for the scope if the given key is None.

             Args:
                 key (str)[None]: Key to access the stored object with.
                 scope (str)[None]: Additional key to prevent clashing.
            """
            if key is None:
                if scope is None:
                    scope = '__DEFAULT__'
                try:
                    del self._GlobalSettings__container[scope]
                except:
                    pass

            else:
                try:
                    del self._GlobalSettings__get_scopescope[key]
                except:
                    pass


else:
    GLOBAL_SETTING = None

    def get(key, default=None, scope=None):
        """Return the stored value for the given key.

    Args:
        key (str): Key to access the stored object with.
        default (object)[None]: If the key does not exist return this default value.
        scope (str)[None]: Additional key to prevent clashing.

    Returns:
        value (object): Value or default value that was stored.
    """
        global GLOBAL_SETTING
        if GLOBAL_SETTING is None:
            GLOBAL_SETTING = GlobalSettings()
        return GLOBAL_SETTING.get(key, default, scope)


    def set(key, value, scope=None):
        """Set the stored value with the given key.

    Args:
         key (str): Key to access the stored object with.
         value (object): Store this object.
         scope (str)[None]: Additional key to prevent clashing.
    """
        global GLOBAL_SETTING
        if GLOBAL_SETTING is None:
            GLOBAL_SETTING = GlobalSettings()
        GLOBAL_SETTING.set(key, value, scope)


    def default(key, value, scope=None):
        """Set the default value for the given key.

    Args:
         key (str): Key to access the stored object with.
         value (object): Store this object.
         scope (str)[None]: Additional key to prevent clashing.
    """
        global GLOBAL_SETTING
        if GLOBAL_SETTING is None:
            GLOBAL_SETTING = GlobalSettings()
        GLOBAL_SETTING.default(key, value, scope)


    def clear(key=None, scope=None):
        """Clear the given key or all storage for the scope if the given key is None.

     Args:
         key (str)[None]: Key to access the stored object with.
         scope (str)[None]: Additional key to prevent clashing.
    """
        global GLOBAL_SETTING
        if GLOBAL_SETTING is None:
            GLOBAL_SETTING = GlobalSettings()
        GLOBAL_SETTING.clearkeyscope