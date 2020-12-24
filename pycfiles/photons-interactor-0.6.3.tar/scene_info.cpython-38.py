# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/models/scene_info.py
# Compiled at: 2019-09-18 03:34:21
# Size of source mod 2**32: 536 bytes
from photons_interactor.database.connection import Base
from sqlalchemy import Column, String, Text

class SceneInfo(Base):
    uuid = Column((String(64)), nullable=True, index=True, unique=True)
    label = Column((Text()), nullable=True)
    description = Column((Text()), nullable=True)

    def as_dict--- This code section failed: ---

 L.  12         0  LOAD_FAST                'self'
                2  LOAD_ATTR                uuid
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                label
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                description
               12  LOAD_CONST               ('uuid', 'label', 'description')
               14  BUILD_CONST_KEY_MAP_3     3 
               16  STORE_FAST               'dct'

 L.  13        18  LOAD_CLOSURE             'ignore'
               20  BUILD_TUPLE_1         1 
               22  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               24  LOAD_STR                 'SceneInfo.as_dict.<locals>.<dictcomp>'
               26  MAKE_FUNCTION_8          'closure'

 L.  14        28  LOAD_FAST                'dct'
               30  LOAD_METHOD              items
               32  CALL_METHOD_0         0  ''

 L.  13        34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 22