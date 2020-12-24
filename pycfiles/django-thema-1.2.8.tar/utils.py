# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/tests/utils.py
# Compiled at: 2018-03-07 08:00:28
from __future__ import unicode_literals
import os
from os import path
from shutil import rmtree
from os.path import join
TEMPORARY_TEST_DATA_DIR = join(path.dirname(path.realpath(__file__)), b'test_data')

class ThemaTemporaryFilesMixin(object):
    random_codes = {b'AMVD': {b'en': b'City & town planning: architectural aspects', 
                 b'da': b'Byplanlægning: arkitektoniske aspekter', 
                 b'es': b'Urbanismo: aspectos arquitectónicos', 
                 b'parent': b'AMV', 
                 b'notes': b'See also: RPC Urban & municipal planning', 
                 b'related_categories': [
                                       b'RPC']}, 
       b'MBNH4': {b'en': b'Birth control, contraception, family planning', 
                  b'da': b'Prævention, fødselskontrol og familieplanlægning', 
                  b'es': b'Control de la natalidad, anticoncepción y planificación familiar', 
                  b'parent': b'MBNH', 
                  b'notes': b'', 
                  b'related_categories': []}, 
       b'PBB': {b'en': b'Philosophy of mathematics', 
                b'da': b'Matematikkens filosofi', 
                b'es': b'Filosofía de las matemáticas', 
                b'parent': b'PB', 
                b'notes': b'', 
                b'related_categories': []}, 
       b'RGBR': {b'en': b'Coral reefs', 
                 b'da': b'Koralrev', 
                 b'es': b'Arrecifes de coral', 
                 b'parent': b'RGB', 
                 b'notes': b'', 
                 b'related_categories': []}, 
       b'VXQM': {b'en': b'Monsters & legendary beings', 
                 b'da': b'Monstre og mytiske væsner', 
                 b'es': b'Monstruos y seres legendarios', 
                 b'parent': b'VXQ', 
                 b'notes': b'See also: JBGB Folklore, myths & legends', 
                 b'related_categories': [
                                       b'JBGB']}}

    def setUp(self):
        """Create a temporary location for testing files."""
        if not path.exists(TEMPORARY_TEST_DATA_DIR):
            os.makedirs(TEMPORARY_TEST_DATA_DIR)

    def tearDown(self):
        """Remove the temporary test location and all its content."""
        rmtree(TEMPORARY_TEST_DATA_DIR)