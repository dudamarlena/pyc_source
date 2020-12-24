# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\Python\enigmapad\Enigma\pyhinavrophonetic-1.0.0\pyhinavrophonetic\utils\config.py
# Compiled at: 2016-09-24 12:32:24
__doc__ = 'Python implementation of Avro Phonetic in hindi.\n\n-------------------------------------------------------------------------------\nCopyright (C) 2016 Subrata Sarkar <subrotosarkar32@gmail.com>\nmodified by:- Subrata Sarkar <subrotosarkar32@gmail.com>\noriginal by:- Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.\nCopyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.\n\nThis file is part of pyAvroPhonetic.\n\npyAvroPhonetic is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\npyAvroPhonetic is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with pyAvroPhonetic.  If not, see <http://www.gnu.org/licenses/>.\n\n'
import os, simplejson as json, codecs
BASE_PATH = os.path.dirname(__file__)
AVRO_DICT_FILE = BASE_PATH + '\\resources\\avrodict.json'
AVRO_DICT = json.load(codecs.open(AVRO_DICT_FILE, encoding='utf-8'))
AVRO_VOWELS = set(AVRO_DICT['data']['vowel'])
AVRO_CONSONANTS = set(AVRO_DICT['data']['consonant'])
AVRO_CASESENSITIVES = set(AVRO_DICT['data']['casesensitive'])
AVRO_NUMBERS = set(AVRO_DICT['data']['number'])