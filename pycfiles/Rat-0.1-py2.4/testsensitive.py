# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rat/testsensitive.py
# Compiled at: 2006-01-30 20:06:37
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Tiago Cogumbreiro <cogumbreiro@users.sf.net>'
__copyright__ = 'Copyright 2005, Tiago Cogumbreiro'
import gtk, unittest, sensitive

class TestCounter(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.amount = 0

    def cb(self, amount):
        self.amount = amount

    def test_counter(self):
        counter = sensitive.Counter(self.cb)
        counter.inc()
        self.assertEqual(self.amount, 1)
        counter.inc()
        self.assertEqual(self.amount, 2)
        counter.dec()
        self.assertEqual(self.amount, 1)
        counter.dec()
        self.assertEqual(self.amount, 0)
        counter.dec()
        self.assertEqual(self.amount, -1)


class TestClient(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.amount = 0
        self.counter = sensitive.Counter(self.cb)

    def cb(self, amount):
        self.amount = amount

    def test_client(self):
        self.assertEqual(self.amount, 0)
        client = sensitive.SensitiveClient(self.counter)
        self.assertEqual(self.amount, 0)
        client.set_sensitive(True)
        self.assertEqual(self.amount, 0)
        client.set_sensitive(True)
        self.assertEqual(self.amount, 0)
        client.set_sensitive(False)
        self.assertEqual(self.amount, 1)
        client.set_sensitive(False)
        self.assertEqual(self.amount, 1)
        client.set_sensitive(True)
        self.assertEqual(self.amount, 0)
        client.set_sensitive(False)
        self.assertEqual(self.amount, 1)
        client = None
        self.assertEqual(self.amount, 0)
        return


class TestController(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.lbl = gtk.Label()
        self.cnt = sensitive.SensitiveController(self.lbl)

    def is_sensitive(self):
        return self.lbl.get_property('sensitive')

    def test_0_controller_ref(self):
        self.lbl.set_sensitive(False)
        self.cnt = None
        self.assertTrue(self.is_sensitive())
        self.lbl.set_sensitive(False)
        self.cnt = sensitive.SensitiveController(self.lbl)
        self.assertTrue(self.is_sensitive())
        client = self.cnt.create_client()
        client.set_sensitive(False)
        self.failIf(self.is_sensitive())
        self.cnt = None
        self.assertTrue(self.is_sensitive())
        return

    def test_1_client(self):
        self.assertTrue(self.is_sensitive())
        client = self.cnt.create_client()
        self.assertTrue(self.is_sensitive())
        client.set_sensitive(False)
        self.failIf(self.is_sensitive())
        client.set_sensitive(True)
        self.assertTrue(self.is_sensitive())
        client.set_sensitive(False)
        self.failIf(self.is_sensitive())
        client = None
        self.assertTrue(self.is_sensitive())
        return

    def test_destroy_object(self):
        client = self.cnt.create_client()
        self.lbl.destroy()

    def test_2_signal_bind(self):
        entry = gtk.Entry()
        bind = sensitive.SignalBind(self.cnt)
        bind.bind(entry, 'text', 'changed', lambda text: text != '')
        self.failIf(self.is_sensitive())
        entry.set_text('Foo')
        self.assertTrue(self.is_sensitive())
        entry.set_text('')
        self.failIf(self.is_sensitive())
        bind = None
        self.assertTrue(self.is_sensitive())
        return


def main():
    unittest.main()


if __name__ == '__main__':
    main()