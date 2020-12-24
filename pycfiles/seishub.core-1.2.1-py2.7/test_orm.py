# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\db\tests\test_orm.py
# Compiled at: 2010-12-23 17:42:43
from seishub.core.db import DEFAULT_PREFIX
from seishub.core.db.manager import meta
from seishub.core.db.orm import DbAttributeProxy, DB_NULL, DB_LIMIT, Serializable, Relation, LazyAttribute, DbStorage, db_property, DbError, DbObjectProxy
from seishub.core.test import SeisHubEnvironmentTestCase
import sqlalchemy as sa, unittest
test_meta = meta
test_parent_tab = sa.Table(DEFAULT_PREFIX + 'test_parent', test_meta, sa.Column('id', sa.Integer, primary_key=True, autoincrement=True), sa.Column('data', sa.Text), sa.Column('child1_rel', sa.Integer), sa.Column('child2_rel', sa.Integer), useexisting=True)
test_child1_tab = sa.Table(DEFAULT_PREFIX + 'test_child1', test_meta, sa.Column('id', sa.Integer, primary_key=True, autoincrement=True), sa.Column('data', sa.Text), useexisting=True)
test_child2_tab = sa.Table(DEFAULT_PREFIX + 'test_child2', test_meta, sa.Column('id', sa.Integer, primary_key=True, autoincrement=True), sa.Column('data', sa.Text), sa.Column('grandchild_rel', sa.Integer), useexisting=True)
test_grandchild_tab = sa.Table(DEFAULT_PREFIX + 'test_grandchild', test_meta, sa.Column('id', sa.Integer, primary_key=True, autoincrement=True), sa.Column('data', sa.Text), useexisting=True)
test_lego_bricks = sa.Table(DEFAULT_PREFIX + 'test_lego_bricks', test_meta, sa.Column('id', sa.Integer, primary_key=True, autoincrement=True), sa.Column('owner_rel', sa.Integer), sa.Column('owner2_rel', sa.Integer), sa.Column('color', sa.Text), sa.Column('size', sa.Integer), useexisting=True)

class LegoBrick(Serializable):
    db_table = test_lego_bricks
    db_mapping = {'_id': 'id', 'color': 'color', 
       'size': 'size'}

    def __init__(self, color=None, size=None):
        self.color = color
        self.size = size


class GrandChild(Serializable):
    db_table = test_grandchild_tab
    db_mapping = {'_id': 'id', 'data': 'data', 
       'lego': Relation(LegoBrick, 'owner_rel', lazy=False, relation_type='to-many', cascading_delete=True)}

    def __init__(self, data=None, lego=None):
        self.data = data
        self.lego = lego


class Child1(Serializable):
    db_table = test_child1_tab
    db_mapping = {'_id': 'id', 'data': LazyAttribute('data')}

    def __init__(self, data=None):
        self.data = data

    def setData(self, value):
        self._data = value

    def getData(self):
        return self._data

    data = db_property(getData, setData, attr='_data')


class Child2(Serializable):
    db_table = test_child2_tab
    db_mapping = {'_id': 'id', 'data': 'data', 
       'grandchild': Relation(GrandChild, 'grandchild_rel', lazy=False, cascading_delete=False), 
       'lego': Relation(LegoBrick, 'owner2_rel', lazy=False, relation_type='to-many', cascading_delete=True)}

    def __init__(self, data=None, grandchild=None, lego=None):
        self.data = data
        self.grandchild = grandchild
        self.lego = lego

    def setData(self, value):
        self._data = value

    def getData(self):
        return self._data

    data = db_property(getData, setData, attr='_data')


class Parent(Serializable):
    db_table = test_parent_tab
    db_mapping = {'_id': 'id', 'data': 'data', 
       'child1': Relation(Child1, 'child1_rel', lazy=False, cascading_delete=True), 
       'child2': Relation(Child2, 'child2_rel', lazy=True, cascading_delete=False)}

    def __init__(self, data=None, child1=None, child2=None):
        self.data = data
        self.child1 = child1
        self.child2 = child2

    def setChild1(self, value):
        self._child1 = value

    def getChild1(self):
        return self._child1

    child1 = db_property(getChild1, setChild1, attr='_child1')

    def setChild2(self, value):
        self._child2 = value

    def getChild2(self):
        return self._child2

    child2 = db_property(getChild2, setChild2, attr='_child2')


class ORMTest(SeisHubEnvironmentTestCase):

    def setUp(self):
        self.db = DbStorage(self.env.db, debug=False)
        brick1 = LegoBrick('red', 2)
        brick2 = LegoBrick('blue', 1)
        brick3 = LegoBrick('yellow', 1)
        brick4 = LegoBrick('black', 3)
        brick5 = LegoBrick('white', 4)
        grandchild = GrandChild("I'm a grandchild.", [brick1, brick2, brick3])
        child1 = Child1("I'm child1.")
        child2 = Child2("I'm child2.", grandchild, [brick4, brick5])
        child3 = Child2("I'm child3.")
        self.parent1 = Parent("I'm parent of child 1 and child 2.", child1, child2)
        self.parent2 = Parent("I'm parent of child 1 and child 3.", child1, child3)

    def tearDown(self):
        test_parent_tab.drop()
        test_child1_tab.drop()
        test_child2_tab.drop()
        test_grandchild_tab.drop()
        test_lego_bricks.drop()

    def testStore(self):
        self.assertEqual(self.parent1._id, None)
        self.assertEqual(self.parent2._id, None)
        self.db.store(self.parent1, cascading=True)
        assert self.parent1._id
        assert self.parent1.child1._id
        assert self.parent1.child2._id
        assert self.parent1.child2.grandchild._id
        assert self.parent1.child2.grandchild.lego[0]._id
        assert self.parent1.child2.grandchild.lego[1]._id
        assert self.parent1.child2.grandchild.lego[2]._id
        self.assertEqual(self.parent2.child1._id, self.parent1.child1._id)
        self.assertRaises(DbError, self.db.store, self.parent2, cascading=True)
        self.db.store(self.parent2.child2, self.parent2)
        assert self.parent2._id
        assert self.parent2.child2._id
        return

    def testPickup(self):
        self.db.store(self.parent1, cascading=True)
        self.db.store(self.parent2.child2, self.parent2)
        all = self.db.pickup(Parent, _order_by={'data': 'asc'})
        self.assertEqual(len(all), 2)
        self.assertEqual(all[0].data, "I'm parent of child 1 and child 2.")
        self.assertEqual(all[1].data, "I'm parent of child 1 and child 3.")
        all = self.db.pickup(Parent, _order_by={'child2': {'data': 'desc'}})
        self.assertEqual(len(all), 2)
        self.assertEqual(all[0].data, "I'm parent of child 1 and child 3.")
        self.assertEqual(all[1].data, "I'm parent of child 1 and child 2.")
        self.assertEqual(all[0].child1, all[1].child1)
        parent1 = self.db.pickup(Parent, _id=self.parent1._id)
        parent2 = self.db.pickup(Parent, _id=self.parent2._id)
        self.assertEqual(len(parent1), 1)
        self.assertEqual(len(parent2), 1)
        parent1 = all[1]
        parent2 = all[0]
        self.assertEqual(parent1.data, "I'm parent of child 1 and child 2.")
        self.assertEqual(type(parent1._child1), Child1)
        self.assertEqual(type(parent1._child2), DbObjectProxy)
        self.assertEqual(type(parent1.child1._data), DbAttributeProxy)
        self.assertEqual(parent1.child1.data, "I'm child1.")
        assert isinstance(parent1.child1._data, basestring)
        assert isinstance(parent1.child2._data, basestring)
        self.assertEqual(parent1.child2.data, "I'm child2.")
        self.assertEqual(type(parent1.child2.grandchild), GrandChild)
        self.assertEqual(parent1.child2.grandchild.data, "I'm a grandchild.")
        self.assertEqual(len(parent1.child2.lego), 2)
        self.assertEqual(parent1.child2.lego[0].color, 'black')
        self.assertEqual(parent1.child2.lego[1].color, 'white')
        self.assertEqual(len(parent1.child2.grandchild.lego), 3)
        self.assertEqual(parent1.child2.grandchild.lego[0].color, 'red')
        self.assertEqual(parent1.child2.grandchild.lego[1].color, 'blue')
        self.assertEqual(parent1.child2.grandchild.lego[2].color, 'yellow')
        self.assertEqual(parent2.child2.grandchild, None)
        parent = self.db.pickup(Parent, child1=self.parent1.child1)
        self.assertEqual(len(parent), 2)
        parent = self.db.pickup(Parent, child2=self.parent2.child2)
        self.assertEqual(len(parent), 1)
        parent = parent[0]
        self.assertEqual(parent.data, "I'm parent of child 1 and child 3.")
        parent = self.db.pickup(Parent, child2={'data': "I'm child3."})
        self.assertEqual(len(parent), 1)
        parent = parent[0]
        self.assertEqual(parent.data, "I'm parent of child 1 and child 3.")
        parent = self.db.pickup(Parent, child2={'grandchild': {'data': "I'm a grandchild."}})
        self.assertEqual(len(parent), 1)
        parent = parent[0]
        self.assertEqual(parent.data, "I'm parent of child 1 and child 2.")
        child3 = self.db.pickup(Child2, grandchild=DB_NULL)
        self.assertEqual(len(child3), 1)
        self.assertEqual(child3[0].data, "I'm child3.")
        parent2 = self.db.pickup(Parent, child2={'grandchild': DB_NULL})
        self.assertEqual(len(parent2), 1)
        self.assertEqual(parent2[0].data, "I'm parent of child 1 and child 3.")
        all = self.db.pickup(Parent, _order_by={'data': 'desc'}, _limit=1)
        self.assertEqual(len(all), 1)
        self.assertEqual(all[0].data, "I'm parent of child 1 and child 3.")
        all = self.db.pickup(Parent, _order_by={'data': 'desc'}, _limit=1, _offset=1)
        self.assertEqual(len(all), 1)
        self.assertEqual(all[0].data, "I'm parent of child 1 and child 2.")
        child2 = self.db.pickup(Child2, _id=self.parent1.child2._id, grandchild={'lego': DB_LIMIT('color', 'max')})
        self.assertEqual(len(child2[0].lego), 2)
        self.assertEqual(len(child2[0].grandchild.lego), 1)
        self.assertEqual(child2[0].grandchild.lego[0].color, 'yellow')
        child2 = self.db.pickup(Child2, _id=self.parent1.child2._id, grandchild={'lego': DB_LIMIT('color', 'min')})
        self.assertEqual(len(child2[0].lego), 2)
        self.assertEqual(len(child2[0].grandchild.lego), 1)
        self.assertEqual(child2[0].grandchild.lego[0].color, 'blue')
        grandchild = self.db.pickup(GrandChild, _id=self.parent1.child2.grandchild._id, lego=DB_LIMIT('size', 'max'))[0]
        self.assertEqual(len(grandchild.lego), 1)
        self.assertEqual(grandchild.lego[0].size, 2)
        self.assertEqual(grandchild.lego[0].color, 'red')
        child4 = Child2("I'm a child2 but have no parent.", None, [
         LegoBrick('black', 1)])
        self.db.store(child4, cascading=True)
        all_child2 = self.db.pickup(Child2)
        self.assertEqual(len(all_child2), 3)
        child2 = all_child2[0]
        child3 = all_child2[1]
        child4 = all_child2[2]
        assert child2.grandchild
        assert not child3.grandchild
        assert not child4.grandchild
        self.assertEqual(len(child2.lego), 2)
        self.assertEqual(child2.lego[0].color, 'black')
        self.assertEqual(child2.lego[0].size, 3)
        self.assertEqual(child2.lego[1].color, 'white')
        self.assertEqual(child2.lego[1].size, 4)
        self.assertEqual(len(child3.lego), 0)
        self.assertEqual(len(child4.lego), 1)
        self.assertEqual(child4.lego[0].color, 'black')
        self.assertEqual(child4.lego[0].size, 1)
        child2_with_lego = self.db.pickup(Child2, lego=DB_LIMIT('color', 'fixed', 'black'))
        self.assertEqual(len(child2_with_lego), 2)
        child2 = child2_with_lego[0]
        child4 = child2_with_lego[1]
        self.assertEqual(len(child2.lego), 1)
        self.assertEqual(child2.lego[0].color, 'black')
        self.assertEqual(child2.lego[0].size, 3)
        self.assertEqual(len(child4.lego), 1)
        self.assertEqual(child4.lego[0].color, 'black')
        self.assertEqual(child4.lego[0].size, 1)
        parent1 = self.db.pickup(Parent, _id=self.parent1._id, child2={'grandchild': {'lego': DB_LIMIT('color', 'max')}})
        return

    def testUpdate(self):
        self.db.store(self.parent1, cascading=True)
        self.db.store(self.parent2.child2, self.parent2)
        parent1 = self.db.pickup(Parent, _id=self.parent1._id)[0]
        self.assertEquals(parent1.data, "I'm parent of child 1 and child 2.")
        parent1.data = 'I am parent.'
        assert parent1._id
        self.db.update(parent1)
        parent1 = self.db.pickup(Parent, _id=self.parent1._id)[0]
        self.assertEquals(parent1.data, 'I am parent.')
        parent1.child2.lego.append(LegoBrick('gray', 10))
        parent1.child2.lego[0].size = 10
        self.db.update(parent1, cascading=True)
        parent1 = self.db.pickup(Parent, _id=self.parent1._id)[0]
        self.assertEquals(len(parent1.child2.lego), 3)
        self.assertEquals(parent1.child2.lego[2].color, 'gray')
        self.assertEquals(parent1.child2.lego[2].size, 10)
        self.assertEquals(parent1.child2.lego[0].size, 10)

    def testDrop(self):
        self.db.store(self.parent1, cascading=True)
        self.db.store(self.parent2.child2, self.parent2)
        self.db.drop(Parent, data="I'm parent of child 5 and child 6.")
        all = self.db.pickup(Parent)
        self.assertEqual(len(all), 2)
        self.db.drop(Parent, data="I'm parent of child 1 and child 2.")
        parent = self.db.pickup(Parent, _id=self.parent1._id)
        self.assertEqual(parent, [])
        child1 = self.db.pickup(Child1, _id=self.parent1.child1._id)
        self.assertEqual(child1, [])
        child2 = self.db.pickup(Child2, _id=self.parent1.child2._id)
        self.assertEqual(len(child2), 1)
        grandchild = self.db.pickup(GrandChild, _id=self.parent1.child2.grandchild._id)
        self.assertEqual(len(grandchild), 1)
        self.db.drop(Child2, grandchild=self.parent1.child2.grandchild)
        child2 = self.db.pickup(Child2, _id=self.parent1.child2._id)
        self.assertEqual(child2, [])
        self.db.drop(Parent, child2={'data': "I'm child3."})
        parent = self.db.pickup(Parent, _id=self.parent2._id)
        self.assertEqual(parent, [])
        self.db.drop(Child2, grandchild=DB_NULL)
        child3 = self.db.pickup(Child2, _id=self.parent2.child2._id)
        self.assertEqual(child3, [])
        parent = self.db.pickup(Parent, data="I'm parent of child 1 and child 3.")
        self.db.drop(GrandChild)
        grandchild = self.db.pickup(GrandChild)
        self.assertEqual(grandchild, [])
        legobricks = self.db.pickup(LegoBrick)
        self.assertEqual(legobricks, [])


def suite():
    return unittest.makeSuite(ORMTest, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')