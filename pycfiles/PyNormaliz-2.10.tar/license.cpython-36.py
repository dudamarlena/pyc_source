# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/models/license.py
# Compiled at: 2019-04-02 03:08:47
# Size of source mod 2**32: 695 bytes
__doc__ = 'A collection of ORM sqlalchemy models for managing copyright'
from norm import config
from norm.models import Model
from sqlalchemy import Column, Integer, String, exists

class License(Model):
    """License"""
    __tablename__ = 'licenses'
    id = Column(Integer, primary_key=True)
    name = Column((String(256)), nullable=False)


LICENSES = [
 'MIT',
 'Apache-2.0',
 'CC-0',
 'BSD']

def register_licenses():
    for lic in LICENSES:
        in_store = config.session.query(exists().where(License.name == lic)).scalar()
        if not in_store:
            inst = License(name=lic)
            config.session.add(inst)

    config.session.commit()