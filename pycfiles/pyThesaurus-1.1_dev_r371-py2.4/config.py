# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/config.py
# Compiled at: 2008-10-06 10:31:21
relations = [
 '=', '-', '#', '<', '>', '!', '~']
relation_name = {'=': 'Equivalentes', '-': 'Relacionados', '#': 'Ocultos', '<': 'Más ámplios', '>': 'Más específicos', '!': 'Distintos', '~': 'Similares'}
relations_precedence = [
 '!', '<', '>', '=', '~', '-', '#']
matrix_comparation = [
 [
  0, -3, -3, -3, -3, -5, -3], [-3, 0, -3, -3, -3, -5, -3], [-3, -3, 0, -3, -3, -5, -3], [-5, -3, -3, 0, -5, -5, -3], [-3, -3, -3, -5, 0, -5, -3], [-5, -5, -5, -5, -5, 0, -5], [-3, -3, -3, -3, -3, -5, 0]]
minimum_score = -5