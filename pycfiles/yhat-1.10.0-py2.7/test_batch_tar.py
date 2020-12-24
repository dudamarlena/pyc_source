# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_batch_tar.py
# Compiled at: 2017-04-26 17:15:42
from __future__ import absolute_import
import unittest, tarfile, os, json
from yhat.deployment.save_session import save_function
from yhat import batch

def external_func():
    print 'Hello from outside the class!'


class BatchTestCase(unittest.TestCase):
    test_archive = '.tmp_yhat_job_test.tar.gz'

    def setUp(self):
        print 'creating tar...'
        with open('yhat.yaml', 'w') as (f):
            f.write("yum install lsof\necho 'Installs complete!'")
        with open('requirements.txt', 'w') as (f):
            f.write('nose==1.3.7\nmock==1.3.0')

    def tearDown(self):
        os.remove(self.test_archive)
        files = [
         'yhat.yaml', 'requirements.txt']
        for f in files:
            if os.path.isfile(f):
                os.remove(f)

    class TestBatchJob(batch.BatchJob):

        def execute():
            print 'Hello'
            external_func()

    def test_create_bundle_tar(self):
        batch_job = self.TestBatchJob('test_job', username='bob', apikey='123', url='http://localhost:9000')
        bundle = save_function(batch_job.__class__, globals())
        bundle_str = json.dumps(bundle)
        print 'checking tar contents...'
        batch_job._BatchJob__create_bundle_tar(bundle_str, self.test_archive)
        with tarfile.open(self.test_archive, 'r:gz') as (f):
            requirements = f.extractfile('requirements.txt').read()
            print 'checking requirements...'
            self.assertIn('nose==1.3.7', requirements)
            self.assertIn('mock==1.3.0', requirements)
            print 'checking yaml...'
            yaml_file = f.extractfile('yhat.yaml').read()
            self.assertIn('Installs complete!', yaml_file)
            self.assertIn('yum install lsof', yaml_file)
            print 'checking bundle...'
            bundle = f.extractfile('bundle.json').read()
            self.assertIn('print(\\"Hello\\")', bundle)
            self.assertIn('Hello from outside the class!', bundle)


if __name__ == '__main__':
    unittest.main()