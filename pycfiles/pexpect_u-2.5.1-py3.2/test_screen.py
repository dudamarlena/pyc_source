# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_screen.py
# Compiled at: 2011-11-02 15:34:09
from pexpect import screen
import unittest
from . import PexpectTestCase
fill1_target = 'XXXXXXXXXX\n' + 'XOOOOOOOOX\n' + 'XO::::::OX\n' + 'XO:oooo:OX\n' + 'XO:o..o:OX\n' + 'XO:o..o:OX\n' + 'XO:oooo:OX\n' + 'XO::::::OX\n' + 'XOOOOOOOOX\n' + 'XXXXXXXXXX'
fill2_target = 'XXXXXXXXXXX\n' + 'XOOOOOOOOOX\n' + 'XO:::::::OX\n' + 'XO:ooooo:OX\n' + 'XO:o...o:OX\n' + 'XO:o.+.o:OX\n' + 'XO:o...o:OX\n' + 'XO:ooooo:OX\n' + 'XO:::::::OX\n' + 'XOOOOOOOOOX\n' + 'XXXXXXXXXXX'
put_target = '\\.3.5.7.9/\n' + '.........2\n' + '3.........\n' + '.........4\n' + '5...\\/....\n' + '..../\\...6\n' + '7.........\n' + '.........8\n' + '9.........\n' + '/2.4.6.8.\\'
scroll_target = '\\.3.5.7.9/\n' + '\\.3.5.7.9/\n' + '\\.3.5.7.9/\n' + '\\.3.5.7.9/\n' + '5...\\/....\n' + '..../\\...6\n' + '/2.4.6.8.\\\n' + '/2.4.6.8.\\\n' + '/2.4.6.8.\\\n' + '/2.4.6.8.\\'
insert_target = 'ZXZZZZZZXZ\n' + '.........2\n' + '3.........\n' + '.........4\n' + 'Z5...\\/...\n' + '..../Z\\...\n' + '7.........\n' + '.........8\n' + '9.........\n' + 'ZZ/2.4.6ZZ'
get_region_target = ['......', '.\\/...', './\\...', '......']

class screenTestCase(PexpectTestCase.PexpectTestCase):

    def make_screen_with_put(self):
        s = screen.screen(10, 10)
        s.fill('.')
        for r in range(1, s.rows + 1):
            if r % 2:
                s.put_abs(r, 1, str(r))
            else:
                s.put_abs(r, s.cols, str(r))

        for c in range(1, s.cols + 1):
            if c % 2:
                s.put_abs(1, c, str(c))
            else:
                s.put_abs(s.rows, c, str(c))

        s.put_abs(1, 1, '\\')
        s.put_abs(1, s.cols, '/')
        s.put_abs(s.rows, 1, '/')
        s.put_abs(s.rows, s.cols, '\\')
        s.put_abs(5, 5, '\\')
        s.put_abs(5, 6, '/')
        s.put_abs(6, 5, '/')
        s.put_abs(6, 6, '\\')
        return s

    def test_fill(self):
        s = screen.screen(10, 10)
        s.fill_region(10, 1, 1, 10, 'X')
        s.fill_region(2, 2, 9, 9, 'O')
        s.fill_region(8, 8, 3, 3, ':')
        s.fill_region(4, 7, 7, 4, 'o')
        s.fill_region(6, 5, 5, 6, '.')
        assert str(s) == fill1_target
        s = screen.screen(11, 11)
        s.fill_region(1, 1, 11, 11, 'X')
        s.fill_region(2, 2, 10, 10, 'O')
        s.fill_region(9, 9, 3, 3, ':')
        s.fill_region(4, 8, 8, 4, 'o')
        s.fill_region(7, 5, 5, 7, '.')
        s.fill_region(6, 6, 6, 6, '+')
        assert str(s) == fill2_target

    def test_put(self):
        s = self.make_screen_with_put()
        assert str(s) == put_target

    def test_get_region(self):
        s = self.make_screen_with_put()
        r = s.get_region(4, 4, 7, 9)
        assert r == get_region_target

    def test_cursor_save(self):
        s = self.make_screen_with_put()
        s.cursor_home(5, 5)
        c = s.get()
        s.cursor_save()
        s.cursor_home()
        s.cursor_forward()
        s.cursor_down()
        s.cursor_unsave()
        assert s.cur_r == 5 and s.cur_c == 5
        assert c == s.get()

    def test_scroll(self):
        s = self.make_screen_with_put()
        s.scroll_screen_rows(1, 4)
        s.scroll_down()
        s.scroll_down()
        s.scroll_down()
        s.scroll_down()
        s.scroll_down()
        s.scroll_down()
        s.scroll_screen_rows(7, 10)
        s.scroll_up()
        s.scroll_up()
        s.scroll_up()
        s.scroll_up()
        s.scroll_up()
        s.scroll_up()
        assert str(s) == scroll_target

    def test_insert(self):
        s = self.make_screen_with_put()
        s.insert_abs(10, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(10, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(1, 1, 'Z')
        s.insert_abs(5, 1, 'Z')
        s.insert_abs(6, 6, 'Z')
        s.cursor_home(1, 1)
        s.insert('Z')
        s.insert('Z')
        s.insert('Z')
        s.insert('Z')
        s.insert_abs(1, 8, 'X')
        s.insert_abs(1, 2, 'X')
        s.insert_abs(10, 9, 'Z')
        s.insert_abs(10, 9, 'Z')
        assert str(s) == insert_target


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(screenTestCase, 'test')