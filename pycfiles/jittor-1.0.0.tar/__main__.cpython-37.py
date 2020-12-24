# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/__main__.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 1343 bytes
if __name__ == '__main__':
    import unittest, os
    suffix = '__main__.py'
    assert __file__.endswith(suffix)
    test_dir = __file__[:-len(suffix)]
    skip_l = int(os.environ.get('test_skip_l', '0'))
    skip_r = int(os.environ.get('test_skip_r', '1000000'))
    test_only = None
    if 'test_only' in os.environ:
        test_only = set(os.environ.get('test_only').split(','))
    test_files = os.listdir(test_dir)
    test_files = sorted(test_files)
    suite = unittest.TestSuite()
    for _, test_file in enumerate(test_files):
        if not test_file.startswith('test_'):
            continue
        if not _ < skip_l:
            if _ > skip_r:
                continue
            test_name = test_file.split('.')[0]
            if test_only:
                if test_name not in test_only:
                    continue
            print('Add Test', _, test_name)
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName('jittor.test.' + test_name))

    unittest.TextTestRunner(verbosity=3).run(suite)