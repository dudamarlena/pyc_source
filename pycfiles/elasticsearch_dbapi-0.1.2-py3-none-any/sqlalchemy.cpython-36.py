# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpgaspar/workarea/preset/elasticsearch-dbapi/es/elastic/sqlalchemy.py
# Compiled at: 2019-11-05 12:13:17
# Size of source mod 2**32: 753 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from es import basesqlalchemy
import es.elastic
logger = logging.getLogger(__name__)

class ESCompiler(basesqlalchemy.BaseESCompiler):
    pass


class ESTypeCompiler(basesqlalchemy.BaseESTypeCompiler):
    pass


class ESDialect(basesqlalchemy.BaseESDialect):
    name = 'elasticsearch'
    scheme = 'http'
    driver = 'rest'
    statement_compiler = ESCompiler
    type_compiler = ESTypeCompiler

    @classmethod
    def dbapi(cls):
        return es.elastic


ESHTTPDialect = ESDialect

class ESHTTPSDialect(ESDialect):
    scheme = 'https'
    default_paramstyle = 'pyformat'