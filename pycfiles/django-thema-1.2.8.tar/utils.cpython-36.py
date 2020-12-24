# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/tests/utils.py
# Compiled at: 2018-03-07 08:36:10
# Size of source mod 2**32: 3297 bytes
import os
from os import path
from shutil import rmtree
from os.path import join
TEMPORARY_TEST_DATA_DIR = join(path.dirname(path.realpath(__file__)), 'test_data')

class ThemaTemporaryFilesMixin(object):
    random_codes = {'AMVD':{'en':('City & town planning: architectural aspects', 'See also: RPC Urban & municipal planning'), 
      'da':('Byplanlægning: arkitektoniske aspekter', 'Se også: RPC Byplanlægning og kommuneplanlægning'), 
      'es':('Urbanismo: aspectos arquitectónicos', 'Ver también: RPC Planificación urbana y municipal'), 
      'parent':'AMV', 
      'notes':'See also: RPC Urban & municipal planning', 
      'related_categories':[
       'RPC']}, 
     'MBNH4':{'en':('Birth control, contraception, family planning', ''), 
      'da':('Prævention, fødselskontrol og familieplanlægning', ''), 
      'es':('Control de la natalidad, anticoncepción y planificación familiar', ''), 
      'parent':'MBNH', 
      'related_categories':[]}, 
     'PBB':{'en':('Philosophy of mathematics', ''), 
      'da':('Matematikkens filosofi', ''), 
      'es':('Filosofía de las matemáticas', ''), 
      'parent':'PB', 
      'related_categories':[]}, 
     'RGBR':{'en':('Coral reefs', ''), 
      'da':('Koralrev', ''), 
      'es':('Arrecifes de coral', ''), 
      'parent':'RGB', 
      'related_categories':[]}, 
     'VXQM':{'en':('Monsters & legendary beings', 'See also: JBGB Folklore, myths & legends'), 
      'da':('Monstre og mytiske væsner', 'Se også: JBGB Folklore, myter og legender'), 
      'es':('Monstruos y seres legendarios', 'Ver también: JBGB Folclore, mitos y leyendas'), 
      'parent':'VXQ', 
      'related_categories':[
       'JBGB']}, 
     'MBX':{'en':('History of medicine', 'See also: NHTF History: plagues, diseases etc'), 
      'da':('Medicinsk historie', 'Her: lægevidenskabens historie. Se også: NHTF Historie: Pest og epidemiske sygdomme'), 
      'es':('Historia de la medicina', 'Ver también: NHTF Historia: plagas, enfermedades, etc.'), 
      'parent':'MB', 
      'related_categories':[
       'NHTF']}}

    def setUp(self):
        """Create a temporary location for testing files."""
        if not path.exists(TEMPORARY_TEST_DATA_DIR):
            os.makedirs(TEMPORARY_TEST_DATA_DIR)

    def tearDown(self):
        """Remove the temporary test location and all its content."""
        rmtree(TEMPORARY_TEST_DATA_DIR)