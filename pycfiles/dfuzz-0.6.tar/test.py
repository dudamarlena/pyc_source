# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/tests/test.py
# Compiled at: 2011-05-01 06:47:00
import logging, unittest, test_conf, test_utils, test_sanity, test_loader, test_incident

def get_suite():
    logging.disable(logging.CRITICAL)
    ts = unittest.TestSuite()
    loader = unittest.TestLoader()
    classes = [
     test_sanity.testFindBinary,
     test_sanity.testDirIntegrity,
     test_sanity.testValidators,
     test_loader.testLoader,
     test_conf.testConf,
     test_utils.testUtils,
     test_incident.testIncident]
    for cls in classes:
        ts.addTest(loader.loadTestsFromTestCase(cls))

    return ts


def main():
    logging.disable(logging.CRITICAL)
    unittest.TextTestRunner().run(get_suite())


if __name__ == '__main__':
    main()