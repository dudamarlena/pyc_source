# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/persistent_dict_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 786 bytes
import io, tempfile, unittest
from bibliopixel.util import data_file
from bibliopixel.util.persistent_dict import PersistentDict
DATA_FILE_TEST = '\n{\n  "a": {"foo": "bar", "bang": 1}\n}\n'

class PersistentDictTest(unittest.TestCase):

    def test_reader_writer_data_file(self):
        with tempfile.NamedTemporaryFile('w') as (tf):
            tf.write(DATA_FILE_TEST)
            tf.seek(0)
            pd = PersistentDict(tf.name)
            self.assertEqual(pd, {'a': {'foo':'bar',  'bang':1}})
            pd.clear()
            self.assertEqual(pd, {})
            self.assertEqual(data_file.load(tf.name), pd)
            pd.update(bang={'hi': 'there'})
            self.assertEqual(pd, {'bang': {'hi': 'there'}})
            self.assertEqual(data_file.load(tf.name), pd)