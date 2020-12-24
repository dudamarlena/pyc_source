# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_engine.py
# Compiled at: 2005-12-18 12:23:16
"""Tests for spyres principle component, the engine.  """
import unittest, time, pdb, spyre
FUZZ = 1e-08

def doNothing():
    pass


class UpdateOnly(spyre.Object):
    __module__ = __name__

    def __init__(self):
        self.displayCount = 0
        self.updateCount = 0

    def display(self):
        self.displayCount += 1

    def update(self):
        self.updateCount += 1


class UpdateList(spyre.Object):
    __module__ = __name__

    def __init__(self):
        self.displayCount = 0
        self.updateCount = 0
        self.updateList = []

    def display(self):
        self.displayCount += 1

    def update(self):
        self.updateCount += 1
        self.updateList.append(time.time())


class UpdateCommit(UpdateOnly):
    __module__ = __name__

    def __init__(self):
        self.displayCount = 0
        self.updateCount = 0
        self.commitCount = 0

    def commit(self):
        self.commitCount += 1


class CommitQuits(UpdateCommit):
    __module__ = __name__

    def __init__(self, lim=1):
        self.displayCount = 0
        self.updateCount = 0
        self.commitCount = 0
        self.limCount = lim

    def commit(self):
        self.commitCount += 1
        if self.commitCount >= self.limCount:
            raise spyre.EngineShutdownException


class CommitQuitsSafety(CommitQuits):
    __module__ = __name__

    def commit(self):
        self.commitCount += 1
        if self.commitCount >= self.limCount:
            print 'DIEINCOMMIT'
            raise spyre.EngineShutdownException


class Regenable(UpdateOnly):
    __module__ = __name__

    def __init__(self):
        self.displayCount = 0
        self.updateCount = 0
        self.regenCount = 0

    def regenerate(self):
        self.regenCount += 1


class IdlingEngine(spyre.Engine):
    """Engine with idle counter"""
    __module__ = __name__

    def __init__(self):
        spyre.Engine.__init__(self)
        self.idleCount = 0

    def idle(self):
        """Runs when the engine is idle"""
        i = 1
        while 1:
            self.idleCount += 1
            i += 1
            yield i


class T01_Engine(unittest.TestCase):
    """Test functions for Light base class."""
    __module__ = __name__

    def setUp(self):
        self.eng = spyre.Engine()
        self.tk = spyre.TimeKeeper()
        self.tk.display_interval = 1.0 / 50.0
        self.eng.runTimer = self.tk

    def test001_commitquit(self):
        """Test that an engine.quit raises shutdown exception. """
        self.assertRaises(spyre.EngineShutdownException, self.eng.quit)

    def test002_commitquit(self):
        """Test that a display object can shutdown engine. """
        cq = CommitQuits()
        self.eng.add(cq)
        self.eng.go()

    def test003_commitquit(self):
        """Test that an all objects get called (displayed) same number of times. """
        ul = UpdateList()
        self.eng.add(ul)
        up = UpdateOnly()
        self.eng.add(up)
        uc = UpdateCommit()
        self.eng.add(uc)
        cq = CommitQuits(25)
        self.eng.add(cq)
        self.eng.go()
        self.assertEqual(up.updateCount - 1, up.displayCount)
        self.assertEqual(cq.updateCount, up.updateCount)
        self.assertEqual(up.updateCount, uc.updateCount)
        self.assertEqual(up.updateCount, 25)
        self.assertEqual(uc.commitCount, uc.updateCount)
        self.assertEqual(ul.updateCount, len(ul.updateList))

    def test011_timer(self):
        """Test that display timer is right. """
        cq = CommitQuits(50)
        self.eng.add(cq)
        t0 = time.time()
        self.eng.go()
        t1 = time.time()
        self.assert_(abs(t1 - t0 - 1) < 0.5, '%s %s' % (t0, t1))

    def test012_timer(self):
        """Test that display timer is right (skip first iter). """
        ul = UpdateList()
        self.eng.add(ul)
        cq = CommitQuits(51)
        self.eng.add(cq)
        self.eng.go()
        t0 = ul.updateList[1]
        t1 = ul.updateList[(-1)]
        self.assert_(abs(t1 - t0 - 1.0) < 0.031, '%s %s' % (t0, t1))

    def test021_timer(self):
        """Test that 25 frames is over 0.4 secs. """
        cq = CommitQuits(25)
        self.eng.add(cq)
        t0 = time.time()
        self.eng.go()
        t1 = time.time()
        self.assert_(t1 - t0 > 0.4, '%s %s' % (t0, t1))

    def test031_addDelay(self):
        """Test that addDelay works for quit. """
        cq = CommitQuitsSafety(51)
        self.eng.add(cq)
        self.tk.addDelay(50, self.eng.quit, ())
        t0 = time.time()
        self.eng.go()
        t1 = time.time()
        self.assert_(t1 - t0 <= 0.4, '%s %s' % (t0, t1))
        self.assert_(cq.updateCount >= 2, cq.updateCount)
        self.assert_(cq.updateCount <= 4, cq.updateCount)

    def test032_addDelay(self):
        """Test that addDelay works for quit. (2 entries) """
        cq = CommitQuits(51)
        self.eng.add(cq)
        self.tk.addDelay(25, doNothing, ())
        self.tk.addDelay(50, self.eng.quit, ())
        t0 = time.time()
        self.eng.go()
        t1 = time.time()
        self.assert_(t1 - t0 <= 0.4, '%s %s' % (t0, t1))
        self.assert_(cq.updateCount >= 2)
        self.assert_(cq.updateCount <= 4)

    def test033_addDelay(self):
        """Test that addDelay works for quit, 4 entries. """
        cq = CommitQuits(51)
        self.eng.add(cq)
        self.tk.addDelay(25, doNothing, ())
        self.tk.addDelay(35, doNothing, ())
        self.tk.addDelay(50, self.eng.quit, ())
        self.tk.addDelay(105, doNothing, ())
        t0 = time.time()
        self.eng.go()
        t1 = time.time()
        self.assert_(t1 - t0 <= 0.4, '%s %s' % (t0, t1))
        self.assert_(cq.updateCount >= 2)
        self.assert_(cq.updateCount < 4)

    def test041_addRemove(self):
        """Test that remove (and add) work """
        cq = CommitQuits()
        self.eng.add(cq)
        self.assertEqual(len(self.eng.objects.objects), 1)
        self.assertEqual(len(self.eng.objects.updateableObjects), 1)
        self.assertEqual(len(self.eng.objects.commitableObjects), 1)
        self.eng.remove(cq)
        self.assertEqual(len(self.eng.objects.objects), 0)
        self.assertEqual(len(self.eng.objects.updateableObjects), 0)
        self.assertEqual(len(self.eng.objects.commitableObjects), 0)

    def test081_reshape(self):
        """Test that reshape raises reinit exception."""
        self.assertRaises(spyre.EngineReInitException, self.eng.reshape, 10, 10)
        self.assertEqual(self.eng.width, 10)
        self.assertEqual(self.eng.height, 10)


class T02_EngineIdle(unittest.TestCase):
    """Test functions for Light base class."""
    __module__ = __name__

    def setUp(self):
        self.eng = IdlingEngine()
        self.tk = spyre.TimeKeeper()
        self.tk.display_interval = 1.0 / 50.0
        self.eng.runTimer = self.tk

    def test061_idle(self):
        """Test that idle gets called."""
        self.tk.addDelay(50, self.eng.quit, ())
        self.eng.go()
        self.assert_(self.eng.idleCount > 1)

    def test081_reshape(self):
        """Neuter reshape test for 'mock engine'. """
        pass


if __name__ == '__main__':
    unittest.main()