# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Subrata Sarkar\Text\Class XI\kaka\bangla key1.4\banglakey1.4\BanglaKey 3.0\pyhinavrophonetic\utils\config.py
# Compiled at: 2016-09-23 13:45:58
"""Python implementation of Avro Phonetic in hindi.

-------------------------------------------------------------------------------
Copyright (C) 2016 Subrata Sarkar <subrotosarkar32@gmail.com>
modified by:- Subrata Sarkar <subrotosarkar32@gmail.com>
original by:- Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.
Copyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.

This file is part of pyAvroPhonetic.

pyAvroPhonetic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyAvroPhonetic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyAvroPhonetic.  If not, see <http://www.gnu.org/licenses/>.

"""
import os, simplejson as json, codecs
BASE_PATH = os.path.dirname(__file__)
AVRO_DICT_FILE = BASE_PATH + '\\resources\\avrodict.json'
AVRO_DICT = json.load(codecs.open(AVRO_DICT_FILE, encoding='utf-8'))
AVRO_VOWELS = set(AVRO_DICT['data']['vowel'])
AVRO_CONSONANTS = set(AVRO_DICT['data']['consonant'])
AVRO_CASESENSITIVES = set(AVRO_DICT['data']['casesensitive'])
AVRO_NUMBERS = set(AVRO_DICT['data']['number'])