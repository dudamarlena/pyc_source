# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/models/license.py
# Compiled at: 2019-04-02 03:08:47
# Size of source mod 2**32: 695 bytes
"""A collection of ORM sqlalchemy models for managing copyright"""
from norm import config
from norm.models import Model
from sqlalchemy import Column, Integer, String, exists

class License(Model):
    __doc__ = 'License for sharing Lambdas'
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