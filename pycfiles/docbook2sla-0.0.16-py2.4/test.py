# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/test.py
# Compiled at: 2008-03-14 13:07:50
from docbook2sla import DocBook2Sla
d2s = DocBook2Sla()
print '===================================='
print ' Test Article                       '
print '===================================='
print '=== test with named output files ==='
print d2s.create('tests/data/xml/article+id.xml', 'tests/data/scribus/clean134.sla', output_filename='tests/data/output/create_output.sla')
print d2s.syncronize('tests/data/xml/article-1+id.xml', 'tests/data/output/create_output.sla', output_filename='tests/data/output/syncronize_output.sla')
print '=== test with unnamed output files ==='
print d2s.create('tests/data/xml/article+id.xml', 'tests/data/scribus/clean134.sla')
print d2s.syncronize('tests/data/xml/article-1+id.xml', 'tests/data/output/create_output.sla')
print '===================================='
print ' Test Book                          '
print '===================================='
print '=== test with named output files ==='
print d2s.create('tests/data/xml/article+id.xml', 'tests/data/scribus/clean134.sla', output_filename='tests/data/output/create_output.sla')
print d2s.syncronize('tests/data/xml/article-1+id.xml', 'tests/data/output/create_output.sla', output_filename='tests/data/output/syncronize_output.sla')
print '=== test with unnamed output files ==='
print d2s.create('tests/data/xml/article+id.xml', 'tests/data/scribus/clean134.sla')
print d2s.syncronize('tests/data/xml/article-1+id.xml', 'tests/data/output/create_output.sla')