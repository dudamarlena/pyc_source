# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/meta/metadata_security.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Apr 19, 2012\n\n@package: security\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Ioan v. Pocol\n\nMeta data definition package.\n'
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from ally.support.sqlalchemy.mapper import DeclarativeMetaModel
meta = MetaData()
Base = declarative_base(metadata=meta, metaclass=DeclarativeMetaModel)