# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/dockarea/DockArea.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 11464 bytes
from ..Qt import QtCore, QtGui
from .Container import *
from .DockDrop import *
from .Dock import Dock
from .. import debug
import weakref

class DockArea(Container, QtGui.QWidget, DockDrop):

    def __init__(self, temporary=False, home=None):
        Container.__init__(self, self)
        QtGui.QWidget.__init__(self)
        DockDrop.__init__(self, allowedAreas=['left', 'right', 'top', 'bottom'])
        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.docks = weakref.WeakValueDictionary()
        self.topContainer = None
        self.raiseOverlay()
        self.temporary = temporary
        self.tempAreas = []
        self.home = home

    def type(self):
        return 'top'

    def addDock(self, dock=None, position='bottom', relativeTo=None, **kwds):
        """Adds a dock to this area.
        
        ============== =================================================================
        **Arguments:**
        dock           The new Dock object to add. If None, then a new Dock will be 
                       created.
        position       'bottom', 'top', 'left', 'right', 'above', or 'below'
        relativeTo     If relativeTo is None, then the new Dock is added to fill an 
                       entire edge of the window. If relativeTo is another Dock, then 
                       the new Dock is placed adjacent to it (or in a tabbed 
                       configuration for 'above' and 'below'). 
        ============== =================================================================
        
        All extra keyword arguments are passed to Dock.__init__() if *dock* is
        None.        
        """
        if dock is None:
            dock = Dock(**kwds)
        else:
            if relativeTo is None or relativeTo is self:
                if self.topContainer is None:
                    container = self
                    neighbor = None
                else:
                    container = self.topContainer
                    neighbor = None
            else:
                if isinstance(relativeTo, basestring):
                    relativeTo = self.docks[relativeTo]
                container = self.getContainer(relativeTo)
                neighbor = relativeTo
            neededContainer = {'bottom':'vertical', 
             'top':'vertical', 
             'left':'horizontal', 
             'right':'horizontal', 
             'above':'tab', 
             'below':'tab'}[position]
            if neededContainer != container.type():
                if container.type() == 'tab':
                    neighbor = container
                    container = container.container()
            if neededContainer != container.type():
                if neighbor is None:
                    container = self.addContainer(neededContainer, self.topContainer)
                else:
                    container = self.addContainer(neededContainer, neighbor)
        insertPos = {'bottom':'after',  'top':'before', 
         'left':'before', 
         'right':'after', 
         'above':'before', 
         'below':'after'}[position]
        old = dock.container()
        container.insert(dock, insertPos, neighbor)
        dock.area = self
        self.docks[dock.name()] = dock
        if old is not None:
            old.apoptose()
        return dock

    def moveDock(self, dock, position, neighbor):
        """
        Move an existing Dock to a new location. 
        """
        if position in ('left', 'right', 'top', 'bottom'):
            if neighbor is not None:
                if neighbor.container() is not None:
                    if neighbor.container().type() == 'tab':
                        neighbor = neighbor.container()
        self.addDock(dock, position, neighbor)

    def getContainer(self, obj):
        if obj is None:
            return self
        return obj.container()

    def makeContainer(self, typ):
        if typ == 'vertical':
            new = VContainer(self)
        elif typ == 'horizontal':
            new = HContainer(self)
        elif typ == 'tab':
            new = TContainer(self)
        return new

    def addContainer(self, typ, obj):
        """Add a new container around obj"""
        new = self.makeContainer(typ)
        container = self.getContainer(obj)
        container.insert(new, 'before', obj)
        if obj is not None:
            new.insert(obj)
        self.raiseOverlay()
        return new

    def insert(self, new, pos=None, neighbor=None):
        if self.topContainer is not None:
            self.topContainer.containerChanged(None)
        self.layout.addWidget(new)
        self.topContainer = new
        new._container = self
        self.raiseOverlay()

    def count(self):
        if self.topContainer is None:
            return 0
        return 1

    def resizeEvent(self, ev):
        self.resizeOverlay(self.size())

    def addTempArea(self):
        if self.home is None:
            area = DockArea(temporary=True, home=self)
            self.tempAreas.append(area)
            win = TempAreaWindow(area)
            area.win = win
            win.show()
        else:
            area = self.home.addTempArea()
        return area

    def floatDock(self, dock):
        """Removes *dock* from this DockArea and places it in a new window."""
        area = self.addTempArea()
        area.win.resize(dock.size())
        area.moveDock(dock, 'top', None)

    def removeTempArea(self, area):
        self.tempAreas.remove(area)
        area.window().close()

    def saveState(self):
        """
        Return a serialized (storable) representation of the state of
        all Docks in this DockArea."""
        if self.topContainer is None:
            main = None
        else:
            main = self.childState(self.topContainer)
        state = {'main':main,  'float':[]}
        for a in self.tempAreas:
            geo = a.win.geometry()
            geo = (geo.x(), geo.y(), geo.width(), geo.height())
            state['float'].append((a.saveState(), geo))

        return state

    def childState(self, obj):
        if isinstance(obj, Dock):
            return ('dock', obj.name(), {})
        childs = []
        for i in range(obj.count()):
            childs.append(self.childState(obj.widget(i)))

        return (obj.type(), childs, obj.saveState())

    def restoreState(self, state):
        """
        Restore Dock configuration as generated by saveState.
        
        Note that this function does not create any Docks--it will only 
        restore the arrangement of an existing set of Docks.
        
        """
        containers, docks = self.findAll()
        oldTemps = self.tempAreas[:]
        if state['main'] is not None:
            self.buildFromState(state['main'], docks, self)
        for s in state['float']:
            a = self.addTempArea()
            a.buildFromState(s[0]['main'], docks, a)
            (a.win.setGeometry)(*s[1])

        for d in docks.values():
            self.moveDock(d, 'below', None)

        for c in containers:
            c.close()

        for a in oldTemps:
            a.apoptose()

    def buildFromState(self, state, docks, root, depth=0):
        typ, contents, state = state
        pfx = '  ' * depth
        if typ == 'dock':
            try:
                obj = docks[contents]
                del docks[contents]
            except KeyError:
                raise Exception('Cannot restore dock state; no dock with name "%s"' % contents)

        else:
            obj = self.makeContainer(typ)
        root.insert(obj, 'after')
        if typ != 'dock':
            for o in contents:
                self.buildFromState(o, docks, obj, depth + 1)

            obj.apoptose(propagate=False)
            obj.restoreState(state)

    def findAll(self, obj=None, c=None, d=None):
        if obj is None:
            obj = self.topContainer
        else:
            if c is None:
                c = []
                d = {}
                for a in self.tempAreas:
                    c1, d1 = a.findAll()
                    c.extend(c1)
                    d.update(d1)

            if isinstance(obj, Dock):
                d[obj.name()] = obj
            elif obj is not None:
                c.append(obj)
                for i in range(obj.count()):
                    o2 = obj.widget(i)
                    c2, d2 = self.findAll(o2)
                    c.extend(c2)
                    d.update(d2)

        return (
         c, d)

    def apoptose(self):
        if self.topContainer.count() == 0:
            self.topContainer = None
            if self.temporary:
                self.home.removeTempArea(self)

    def clear(self):
        docks = self.findAll()[1]
        for dock in docks.values():
            dock.close()

    def dragEnterEvent(self, *args):
        (DockDrop.dragEnterEvent)(self, *args)

    def dragMoveEvent(self, *args):
        (DockDrop.dragMoveEvent)(self, *args)

    def dragLeaveEvent(self, *args):
        (DockDrop.dragLeaveEvent)(self, *args)

    def dropEvent(self, *args):
        (DockDrop.dropEvent)(self, *args)


class TempAreaWindow(QtGui.QMainWindow):

    def __init__(self, area, **kwargs):
        (QtGui.QMainWindow.__init__)(self, **kwargs)
        self.setCentralWidget(area)

    def closeEvent(self, *args, **kwargs):
        self.centralWidget().clear()
        (QtGui.QMainWindow.closeEvent)(self, *args, **kwargs)