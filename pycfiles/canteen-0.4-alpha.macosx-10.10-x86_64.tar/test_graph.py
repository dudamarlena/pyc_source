# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_model/test_graph.py
# Compiled at: 2014-09-26 04:50:19
"""

  graph model tests
  ~~~~~~~~~~~~~~~~~

  tests graph-extended models.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
from canteen import model
from canteen.test import FrameworkTest
from canteen.model.adapter import inmemory

class TestPerson(model.Vertex):
    """ sample person (also a vertex) """
    firstname = basestring
    lastname = basestring


class TestTeammates(TestPerson > TestPerson):
    """ sample teammate-ship (edge that connects two people) """
    year_met = int


class VertexModelTests(FrameworkTest):
    """ Tests `model.Vertex`. """
    subject = inmemory.InMemoryAdapter()

    def test_construct(self):
        """ Test constructing a `Vertex` model """
        return TestPerson(key=model.VertexKey(TestPerson, 'sup'), firstname='John', lastname='Doe')

    def test_vertex_put(self):
        """ Test saving a `Vertex` model to storage """
        return self.test_construct().put(adapter=self.subject)

    def test_vertex_get(self):
        """ Test retrieving a `Vertex` by its key """
        assert TestPerson.get(self.test_vertex_put(), adapter=self.subject)

    def test_vertex_repr(self):
        """ Test string representation of a `Vertex` """
        p = TestPerson.get(self.test_vertex_put(), adapter=self.subject)
        assert 'Person' in repr(p)
        assert 'Person' in repr(TestPerson)
        assert 'Vertex' in repr(model.Vertex)


class EdgeModelTests(FrameworkTest):
    """ Tests `model.Edge`. """
    subject = inmemory.InMemoryAdapter()

    def test_spawn_directed(self):
        """ Test spawning directed `Edge` classes """

        class TestFriends(TestPerson > TestPerson):
            """ friend relationship """
            pass

        assert issubclass(TestFriends, model.Edge)
        assert not TestFriends.__spec__.directed

        class TestFriends(TestPerson < TestPerson):
            """ friend relationship """
            pass

        assert issubclass(TestFriends, model.Edge)
        assert not TestFriends.__spec__.directed

    def test_spawn_undirected(self):
        """ Test spawning undirected `Edge` classes """

        class Gift(TestPerson >> TestPerson):
            """ friend relationship """
            pass

        assert issubclass(Gift, model.Edge)
        assert Gift.__spec__.directed

        class Gift(TestPerson << TestPerson):
            """ friend relationship """
            pass

        assert issubclass(Gift, model.Edge)
        assert Gift.__spec__.directed

    def test_construct_undirected(self):
        """ Test constructing an undirected `Edge` model """
        sam, alex = TestPerson(firstname='Sam'), TestPerson(firstname='Alex')
        sam_to_alex = TestTeammates(sam, alex, key=model.EdgeKey(TestTeammates, 'sup'), year_met=2003)
        return sam_to_alex

    def test_construct_directed(self):
        """ Test constructing a directed `Edge` model """
        ian, david = TestPerson(firstname='Sam'), TestPerson(firstname='Alex')
        ian_to_david = TestTeammates(ian, david, key=model.EdgeKey(TestTeammates, 'sup'), year_met=2003)
        return ian_to_david

    def test_undirected_edge_put(self):
        """ Test saving an undirected `Edge` model """
        return self.test_construct_undirected().put(adapter=self.subject)

    def test_directed_edge_put(self):
        """ Test saving a directed `Edge` model """
        return self.test_construct_directed().put(adapter=self.subject)

    def test_undirected_edge_get(self):
        """ Test retrieving an undirected `Edge` by its key """
        assert TestTeammates.get(self.test_undirected_edge_put(), adapter=self.subject)

    def test_directed_edge_get(self):
        """ Test retrieving a directed `Edge` by its key """
        assert TestTeammates.get(self.test_directed_edge_put(), adapter=self.subject)