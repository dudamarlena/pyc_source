# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_repository.py
# Compiled at: 2014-10-22 16:00:16
__docformat__ = 'reStructuredText'
__author__ = 'Antonio Messina <antonio.s.messina@gmail.com>'
import os, shutil, tempfile, unittest, nose.tools as nt
from elasticluster.repository import ClusterRepository, MemRepository

class FakeCluster(object):
    """Fake class used for the storage cluster class.  The only thing the
    ClusterRepository class assumes is that the saved class has a `name`
    attribute.
    """

    def __init__(self, name='fake_cluster'):
        self.name = name
        self.nodes = {}

    def __eq__(self, other):
        return self.name == other.name


class MemRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.storage = MemRepository()

    def test_get_all(self):
        clusters = [ FakeCluster('test_%d' % i) for i in range(10) ]
        for cluster in clusters:
            self.storage.save_or_update(cluster)

        new_clusters = self.storage.get_all()
        for cluster in new_clusters:
            nt.assert_true(cluster in clusters)

    def test_get(self):
        clusters = [ FakeCluster('test_%d' % i) for i in range(10) ]
        for cluster in clusters:
            self.storage.save_or_update(cluster)

        new_clusters = [ self.storage.get(cluster.name) for cluster in clusters ]
        for cluster in new_clusters:
            nt.assert_true(cluster in clusters)

    def test_delete(self):
        cluster = FakeCluster('test1')
        self.storage.save_or_update(cluster)
        nt.assert_true(cluster.name in self.storage.clusters)
        self.storage.delete(cluster)
        nt.assert_false(cluster.name in self.storage.clusters)


class ClusterRepositoryTests(MemRepositoryTests):

    def setUp(self):
        self.path = tempfile.mkdtemp()
        self.storage = ClusterRepository(self.path)

    def tearDown(self):
        shutil.rmtree(self.path, ignore_errors=True)
        del self.storage

    def test_delete(self):
        pass

    def test_save_and_delete(self):
        cluster = FakeCluster('test1')
        self.storage.save_or_update(cluster)
        clusterpath = os.path.join(self.path, 'test1.pickle')
        nt.assert_true(os.path.exists(clusterpath))
        self.storage.delete(cluster)
        nt.assert_false(os.path.exists(clusterpath))


if __name__ == '__main__':
    import nose
    nose.runmodule()