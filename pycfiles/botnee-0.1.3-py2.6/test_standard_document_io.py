# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/test/test_standard_document_io.py
# Compiled at: 2012-03-12 12:20:00
"""
Tests for reading files in standard document format from disk
"""
import botnee, botnee_config

def test_read_directory(test_data):
    """Test of reading of directory"""
    try:
        collector_directory = botnee_config._data_directory + 'test/journal-collector-output/'
        for i in range(3):
            test_data.append({'docs': botnee.standard_document_io.read_directory(collector_directory + 'corpus' + str(i) + '/', 'txt', True)})

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)