# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/__init__.py
# Compiled at: 2015-09-04 08:27:04
import os.path
__title__ = 'avroknife'
__author__ = 'Mateusz Kobos, Pawel Szostek'
__email__ = 'mkobos@icm.edu.pl'
__version__ = open(os.path.join(os.path.dirname(__file__), 'RELEASE-VERSION')).read().strip()
__description__ = 'Utility for browsing and simple manipulation of Avro-based files'
__license__ = 'Apache License, Version 2.0'