# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/mptt/tests/testcases.py
# Compiled at: 2009-10-31 23:19:40
import re
from django.test import TestCase
from mptt.exceptions import InvalidMove
from mptt.tests import doctests
from mptt.tests.models import Category, Genre

def get_tree_details(nodes):
    """Creates pertinent tree details for the given list of nodes."""
    opts = nodes[0]._meta
    return ('\n').join([ '%s %s %s %s %s %s' % (n.pk, getattr(n, '%s_id' % opts.parent_attr) or '-', getattr(n, opts.tree_id_attr), getattr(n, opts.level_attr), getattr(n, opts.left_attr), getattr(n, opts.right_attr)) for n in nodes
                       ])


leading_whitespace_re = re.compile('^\\s+', re.MULTILINE)

def tree_details(text):
    """
    Trims leading whitespace from the given text specifying tree details
    so triple-quoted strings can be used to provide tree details in a
    readable format (says who?), to be compared with the result of using
    the ``get_tree_details`` function.
    """
    return leading_whitespace_re.sub('', text)


class ReparentingTestCase(TestCase):
    """
    Test that trees are in the appropriate state after reparenting and
    that reparented items have the correct tree attributes defined,
    should they be required for use after a save.
    """
    fixtures = [
     'genres.json']

    def test_new_root_from_subtree(self):
        shmup = Genre.objects.get(id=6)
        shmup.parent = None
        shmup.save()
        self.assertEqual(get_tree_details([shmup]), '6 - 3 0 1 6')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('1 - 1 0 1 10\n                                         2 1 1 1 2 9\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 2 1 2 7 8\n                                         9 - 2 0 1 6\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 5\n                                         6 - 3 0 1 6\n                                         7 6 3 1 2 3\n                                         8 6 3 1 4 5'))
        return

    def test_new_root_from_leaf_with_siblings(self):
        platformer_2d = Genre.objects.get(id=3)
        platformer_2d.parent = None
        platformer_2d.save()
        self.assertEqual(get_tree_details([platformer_2d]), '3 - 3 0 1 2')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('1 - 1 0 1 14\n                                         2 1 1 1 2 7\n                                         4 2 1 2 3 4\n                                         5 2 1 2 5 6\n                                         6 1 1 1 8 13\n                                         7 6 1 2 9 10\n                                         8 6 1 2 11 12\n                                         9 - 2 0 1 6\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 5\n                                         3 - 3 0 1 2'))
        return

    def test_new_child_from_root(self):
        action = Genre.objects.get(id=1)
        rpg = Genre.objects.get(id=9)
        action.parent = rpg
        action.save()
        self.assertEqual(get_tree_details([action]), '1 9 2 1 6 21')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('9 - 2 0 1 22\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 5\n                                         1 9 2 1 6 21\n                                         2 1 2 2 7 14\n                                         3 2 2 3 8 9\n                                         4 2 2 3 10 11\n                                         5 2 2 3 12 13\n                                         6 1 2 2 15 20\n                                         7 6 2 3 16 17\n                                         8 6 2 3 18 19'))

    def test_move_leaf_to_other_tree(self):
        shmup_horizontal = Genre.objects.get(id=8)
        rpg = Genre.objects.get(id=9)
        shmup_horizontal.parent = rpg
        shmup_horizontal.save()
        self.assertEqual(get_tree_details([shmup_horizontal]), '8 9 2 1 6 7')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('1 - 1 0 1 14\n                                         2 1 1 1 2 9\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 2 1 2 7 8\n                                         6 1 1 1 10 13\n                                         7 6 1 2 11 12\n                                         9 - 2 0 1 8\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 5\n                                         8 9 2 1 6 7'))

    def test_move_subtree_to_other_tree(self):
        shmup = Genre.objects.get(id=6)
        trpg = Genre.objects.get(id=11)
        shmup.parent = trpg
        shmup.save()
        self.assertEqual(get_tree_details([shmup]), '6 11 2 2 5 10')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('1 - 1 0 1 10\n                                         2 1 1 1 2 9\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 2 1 2 7 8\n                                         9 - 2 0 1 12\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 11\n                                         6 11 2 2 5 10\n                                         7 6 2 3 6 7\n                                         8 6 2 3 8 9'))

    def test_move_child_up_level(self):
        shmup_horizontal = Genre.objects.get(id=8)
        action = Genre.objects.get(id=1)
        shmup_horizontal.parent = action
        shmup_horizontal.save()
        self.assertEqual(get_tree_details([shmup_horizontal]), '8 1 1 1 14 15')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('1 - 1 0 1 16\n                                         2 1 1 1 2 9\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 2 1 2 7 8\n                                         6 1 1 1 10 13\n                                         7 6 1 2 11 12\n                                         8 1 1 1 14 15\n                                         9 - 2 0 1 6\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 5'))

    def test_move_subtree_down_level(self):
        shmup = Genre.objects.get(id=6)
        platformer = Genre.objects.get(id=2)
        shmup.parent = platformer
        shmup.save()
        self.assertEqual(get_tree_details([shmup]), '6 2 1 2 9 14')
        self.assertEqual(get_tree_details(Genre.tree.all()), tree_details('1 - 1 0 1 16\n                                         2 1 1 1 2 15\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 2 1 2 7 8\n                                         6 2 1 2 9 14\n                                         7 6 1 3 10 11\n                                         8 6 1 3 12 13\n                                         9 - 2 0 1 6\n                                         10 9 2 1 2 3\n                                         11 9 2 1 4 5'))

    def test_invalid_moves(self):
        action = Genre.objects.get(id=1)
        action.parent = action
        platformer = Genre.objects.get(id=2)
        platformer.parent = platformer
        self.assertRaises(InvalidMove, action.save)
        self.assertRaises(InvalidMove, platformer.save)
        platformer_4d = Genre.objects.get(id=5)
        action.parent = platformer_4d
        platformer.parent = platformer_4d
        self.assertRaises(InvalidMove, action.save)
        self.assertRaises(InvalidMove, platformer.save)
        self.assertEquals(action.parent, platformer_4d)
        self.assertEquals(platformer.parent, platformer_4d)


class DeletionTestCase(TestCase):
    """
    Tests that the tree structure is maintained appropriately in various
    deletion scenrios.
    """
    fixtures = [
     'categories.json']

    def test_delete_root_node(self):
        Category(name='Preceding root').insert_at(Category.objects.get(id=1), 'left', commit=True)
        Category(name='Following root').insert_at(Category.objects.get(id=1), 'right', commit=True)
        self.assertEqual(get_tree_details(Category.tree.all()), tree_details('11 - 1 0 1 2\n                                         1 - 2 0 1 20\n                                         2 1 2 1 2 7\n                                         3 2 2 2 3 4\n                                         4 2 2 2 5 6\n                                         5 1 2 1 8 13\n                                         6 5 2 2 9 10\n                                         7 5 2 2 11 12\n                                         8 1 2 1 14 19\n                                         9 8 2 2 15 16\n                                         10 8 2 2 17 18\n                                         12 - 3 0 1 2'), 'Setup for test produced unexpected result')
        Category.objects.get(id=1).delete()
        self.assertEqual(get_tree_details(Category.tree.all()), tree_details('11 - 1 0 1 2\n                                         12 - 3 0 1 2'))

    def test_delete_last_node_with_siblings(self):
        Category.objects.get(id=9).delete()
        self.assertEqual(get_tree_details(Category.tree.all()), tree_details('1 - 1 0 1 18\n                                         2 1 1 1 2 7\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 1 1 1 8 13\n                                         6 5 1 2 9 10\n                                         7 5 1 2 11 12\n                                         8 1 1 1 14 17\n                                         10 8 1 2 15 16'))

    def test_delete_last_node_with_descendants(self):
        Category.objects.get(id=8).delete()
        self.assertEqual(get_tree_details(Category.tree.all()), tree_details('1 - 1 0 1 14\n                                         2 1 1 1 2 7\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 1 1 1 8 13\n                                         6 5 1 2 9 10\n                                         7 5 1 2 11 12'))

    def test_delete_node_with_siblings(self):
        Category.objects.get(id=6).delete()
        self.assertEqual(get_tree_details(Category.tree.all()), tree_details('1 - 1 0 1 18\n                                         2 1 1 1 2 7\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         5 1 1 1 8 11\n                                         7 5 1 2 9 10\n                                         8 1 1 1 12 17\n                                         9 8 1 2 13 14\n                                         10 8 1 2 15 16'))

    def test_delete_node_with_descendants_and_siblings(self):
        """
        Regression test for Issue 23 - we used to use pre_delete, which
        resulted in tree cleanup being performed for every node being
        deleted, rather than just the node on which ``delete()`` was
        called.
        """
        Category.objects.get(id=5).delete()
        self.assertEqual(get_tree_details(Category.tree.all()), tree_details('1 - 1 0 1 14\n                                         2 1 1 1 2 7\n                                         3 2 1 2 3 4\n                                         4 2 1 2 5 6\n                                         8 1 1 1 8 13\n                                         9 8 1 2 9 10\n                                         10 8 1 2 11 12'))


class IntraTreeMovementTestCase(TestCase):
    pass


class InterTreeMovementTestCase(TestCase):
    pass


class PositionedInsertionTestCase(TestCase):
    pass