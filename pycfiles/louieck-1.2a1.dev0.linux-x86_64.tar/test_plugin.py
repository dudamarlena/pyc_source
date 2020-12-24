# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/louieck/test/test_plugin.py
# Compiled at: 2018-05-31 10:36:55
"""Louie plugin tests."""
import unittest, louie
try:
    import qt
    if not hasattr(qt.qApp, 'for_testing'):
        _app = qt.QApplication([])
        _app.for_testing = True
        qt.qApp = _app
except ImportError:
    qt = None

class ReceiverBase(object):

    def __init__(self):
        self.args = []
        self.live = True

    def __call__(self, arg):
        self.args.append(arg)


class Receiver1(ReceiverBase):
    pass


class Receiver2(ReceiverBase):
    pass


class Plugin1(louie.Plugin):

    def is_live(self, receiver):
        """ReceiverBase instances are only live if their `live`
        attribute is True"""
        if isinstance(receiver, ReceiverBase):
            return receiver.live
        return True


class Plugin2(louie.Plugin):

    def is_live(self, receiver):
        """Pretend all Receiver2 instances are not live."""
        if isinstance(receiver, Receiver2):
            return False
        return True


def test_only_one_instance():
    louie.reset()
    plugin1a = Plugin1()
    plugin1b = Plugin1()
    louie.install_plugin(plugin1a)
    try:
        louie.install_plugin(plugin1b)
    except louie.error.PluginTypeError:
        pass
    else:
        raise Exception('PluginTypeError not raised')


def test_is_live():
    louie.reset()
    receiver1a = Receiver1()
    receiver1b = Receiver1()
    receiver2a = Receiver2()
    receiver2b = Receiver2()
    louie.connect(receiver1a, 'sig')
    louie.connect(receiver1b, 'sig')
    louie.connect(receiver2a, 'sig')
    louie.connect(receiver2b, 'sig')
    louie.send('sig', arg='foo')
    assert receiver1a.args == ['foo']
    assert receiver1b.args == ['foo']
    assert receiver2a.args == ['foo']
    assert receiver2b.args == ['foo']
    plugin1 = Plugin1()
    louie.install_plugin(plugin1)
    receiver1a.live = False
    receiver2b.live = False
    louie.send('sig', arg='bar')
    assert receiver1a.args == ['foo']
    assert receiver1b.args == ['foo', 'bar']
    assert receiver2a.args == ['foo', 'bar']
    assert receiver2b.args == ['foo']
    plugin2 = Plugin2()
    louie.remove_plugin(plugin1)
    louie.install_plugin(plugin2)
    louie.send('sig', arg='baz')
    assert receiver1a.args == ['foo', 'baz']
    assert receiver1b.args == ['foo', 'bar', 'baz']
    assert receiver2a.args == ['foo', 'bar']
    assert receiver2b.args == ['foo']
    louie.install_plugin(plugin1)
    louie.send('sig', arg='fob')
    assert receiver1a.args == ['foo', 'baz']
    assert receiver1b.args == ['foo', 'bar', 'baz', 'fob']
    assert receiver2a.args == ['foo', 'bar']
    assert receiver2b.args == ['foo']


if qt is not None:

    def test_qt_plugin():
        louie.reset()

        class Receiver(qt.QWidget):

            def __init__(self):
                qt.QObject.__init__(self)
                self.args = []

            def receive(self, arg):
                self.args.append(arg)

        receiver1 = Receiver()
        receiver2 = Receiver()
        louie.connect(receiver1.receive, 'sig')
        louie.connect(receiver2.receive, 'sig')
        receiver2.close(True)
        louie.send('sig', arg='foo')
        assert receiver1.args == ['foo']
        assert receiver2.args == ['foo']
        plugin = louie.QtWidgetPlugin()
        louie.install_plugin(plugin)
        louie.send('sig', arg='bar')
        assert receiver1.args == ['foo', 'bar']
        assert receiver2.args == ['foo']