# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\vep_core\Serendip\config.py
# Compiled at: 2014-05-29 17:15:05
__author__ = 'kohlmannj'

class Config(object):
    DEBUG = False
    TESTING = False
    DEFAULT_CORPUS_NAME = 'ShakespeareChunked_50'
    NAME = 'Serendip[ity]'
    WEB_ROOT = '/'
    TOPICMODEL_STATIC_CACHE = True
    TOPICMODEL_STATIC_SVG_CACHE = False
    TEXTVIEWER_DEFAULT_NUM_TAG_MAPS = 8000


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    NAME = 'Ser·ənˈ·dip[·itē] (Dev)'


class TestingConfig(DevelopmentConfig):
    TESTING = True
    NAME = 'u"Ser\\xb7\\u0259n\\u02c8\\xb7dip[\\xb7it\\u0113]" (Testing)'