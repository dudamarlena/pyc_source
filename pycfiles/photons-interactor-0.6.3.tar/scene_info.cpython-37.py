# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/models/scene_info.py
# Compiled at: 2020-02-25 22:11:59
# Size of source mod 2**32: 536 bytes
from photons_interactor.database.connection import Base
from sqlalchemy import Column, String, Text

class SceneInfo(Base):
    uuid = Column((String(64)), nullable=True, index=True, unique=True)
    label = Column((Text()), nullable=True)
    description = Column((Text()), nullable=True)

    def as_dict(self, ignore=None):
        dct = {'uuid':self.uuid, 
         'label':self.label,  'description':self.description}
        return {k:v for k, v in dct.items()}