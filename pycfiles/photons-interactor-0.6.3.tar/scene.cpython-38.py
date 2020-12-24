# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/models/scene.py
# Compiled at: 2019-09-18 03:34:21
# Size of source mod 2**32: 1760 bytes
from photons_interactor.database.models.scene_spec import make_spec
from photons_interactor.database.connection import Base
from sqlalchemy import Column, Integer, String, Text, Boolean
from delfick_project.norms import sb

class Scene(Base):
    uuid = Column((String(64)), nullable=True, index=True)
    matcher = Column((Text()), nullable=False)
    power = Column((Boolean()), nullable=True)
    color = Column((Text()), nullable=True)
    zones = Column((Text()), nullable=True)
    chain = Column((Text()), nullable=True)
    duration = Column((Integer()), nullable=True)
    __repr_columns__ = ('uuid', 'matcher')

    def as_object(self):
        dct = {'uuid':self.uuid, 
         'matcher':self.matcher, 
         'power':self.power, 
         'color':self.color, 
         'zones':self.zones, 
         'chain':self.chain, 
         'duration':self.duration}
        return (self.Spec(storing=False).empty_normalise)(**dct)

    def as_dict--- This code section failed: ---

 L.  32         0  LOAD_CLOSURE             'ignore'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'Scene.as_dict.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'

 L.  34        10  LOAD_FAST                'self'
               12  LOAD_METHOD              as_object
               14  CALL_METHOD_0         0  ''
               16  LOAD_METHOD              as_dict
               18  CALL_METHOD_0         0  ''
               20  LOAD_METHOD              items
               22  CALL_METHOD_0         0  ''

 L.  32        24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def Spec(kls, storing=True):
        return make_spec(storing=storing)

    @classmethod
    def DelayedSpec(kls, storing=True):
        spec = kls.Spec(storing=storing)

        class delayed(sb.Spec):

            def normalise_filled(self, meta, val):
                val = sb.dictionary_spec.normalise(meta, val)

                def normalise(uuid):
                    if 'uuid' in val:
                        del val['uuid']
                    return spec.normalise(meta, {**{'uuid': uuid}, **val})

                return normalise

        return delayed()