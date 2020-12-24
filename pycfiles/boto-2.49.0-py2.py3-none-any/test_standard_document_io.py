# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/test/test_standard_document_io.py
# Compiled at: 2012-03-12 12:20:00
__doc__ = '\nTests for reading files in standard document format from disk\n'
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

    return (result, test_data)