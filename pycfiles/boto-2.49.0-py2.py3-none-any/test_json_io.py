# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/test/test_json_io.py
# Compiled at: 2012-02-24 07:17:01
__doc__ = '\nTesting of reading of JSON files. MongoDB functions currently not included.\n'
import sys, botnee

def test_read_json(test_data):
    """Test reading of directory with multiple json documents per file"""
    try:
        test_data = []
        prefix = botnee._data_directory + 'test/json/'
        fnames = ['gutjnl-small-test.txt',
         'jnnp-small-test.txt',
         'combined-small-test.txt']
        for fname in fnames:
            fname = prefix + fname
            test_data.append({'jobjs': botnee.json_io.read_json(fname), 'fname': fname})

        for data in test_data:
            data['ids'] = {}
            if isinstance(data['jobjs'], dict):
                sys.stdout.write(str(data['jobjs']['id']) + '...')
                data['ids'][data['jobjs']['id']] = 0
            for (i, jobj) in enumerate(data['jobjs']):
                sys.stdout.write('\n' + str(i) + ':' + str(jobj['id']) + '...')
                data['ids'][jobj['id']] = i

            assert len(set(data['ids'].values())) == len(data['ids'])
            assert len(set(data['ids'].keys())) == len(data['ids'])

        result = len(test_data) == 3
    except Exception, e:
        print e
        test_data = None
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_get_all_text(test_data):
    """Test of pulling out the body text from JSON documents"""
    try:
        for data in test_data:
            data['docs'] = []
            for jobj in data['jobjs']:
                text = botnee.json_io.get_all_text(jobj)
                data['docs'].append({'body': text, 'guid': jobj['id']})

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)