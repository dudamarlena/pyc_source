# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/Flowchart.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 35886 bytes
from ..Qt import QtCore, QtGui, USE_PYSIDE, USE_PYQT5
from .Node import *
from ..pgcollections import OrderedDict
from ..widgets.TreeWidget import *
from .. import FileDialog, DataTreeWidget
if USE_PYSIDE:
    from . import FlowchartTemplate_pyside as FlowchartTemplate
    from . import FlowchartCtrlTemplate_pyside as FlowchartCtrlTemplate
else:
    if USE_PYQT5:
        from . import FlowchartTemplate_pyqt5 as FlowchartTemplate
        from . import FlowchartCtrlTemplate_pyqt5 as FlowchartCtrlTemplate
    else:
        from . import FlowchartTemplate_pyqt as FlowchartTemplate
        from . import FlowchartCtrlTemplate_pyqt as FlowchartCtrlTemplate
from .Terminal import Terminal
from numpy import ndarray
from .library import LIBRARY
from ..debug import printExc
from .. import configfile
from .. import dockarea
from . import FlowchartGraphicsView
from .. import functions as fn

def strDict(d):
    return dict([(str(k), v) for k, v in d.items()])


class Flowchart(Node):
    sigFileLoaded = QtCore.Signal(object)
    sigFileSaved = QtCore.Signal(object)
    sigChartLoaded = QtCore.Signal()
    sigStateChanged = QtCore.Signal()
    sigChartChanged = QtCore.Signal(object, object, object)

    def __init__(self, terminals=None, name=None, filePath=None, library=None):
        self.library = library or LIBRARY
        if name is None:
            name = 'Flowchart'
        if terminals is None:
            terminals = {}
        self.filePath = filePath
        Node.__init__(self, name, allowAddInput=True, allowAddOutput=True)
        self.inputWasSet = False
        self._nodes = {}
        self.nextZVal = 10
        self._widget = None
        self._scene = None
        self.processing = False
        self.widget()
        self.inputNode = Node('Input', allowRemove=False, allowAddOutput=True)
        self.outputNode = Node('Output', allowRemove=False, allowAddInput=True)
        self.addNode(self.inputNode, 'Input', [-150, 0])
        self.addNode(self.outputNode, 'Output', [300, 0])
        self.outputNode.sigOutputChanged.connect(self.outputChanged)
        self.outputNode.sigTerminalRenamed.connect(self.internalTerminalRenamed)
        self.inputNode.sigTerminalRenamed.connect(self.internalTerminalRenamed)
        self.outputNode.sigTerminalRemoved.connect(self.internalTerminalRemoved)
        self.inputNode.sigTerminalRemoved.connect(self.internalTerminalRemoved)
        self.outputNode.sigTerminalAdded.connect(self.internalTerminalAdded)
        self.inputNode.sigTerminalAdded.connect(self.internalTerminalAdded)
        self.viewBox.autoRange(padding=0.04)
        for name, opts in terminals.items():
            (self.addTerminal)(name, **opts)

    def setLibrary(self, lib):
        self.library = lib
        self.widget().chartWidget.buildMenu()

    def setInput(self, **args):
        """Set the input values of the flowchart. This will automatically propagate
        the new values throughout the flowchart, (possibly) causing the output to change.
        """
        self.inputWasSet = True
        (self.inputNode.setOutput)(**args)

    def outputChanged(self):
        vals = self.outputNode.inputValues()
        self.widget().outputChanged(vals)
        (self.setOutput)(**vals)

    def output(self):
        """Return a dict of the values on the Flowchart's output terminals.
        """
        return self.outputNode.inputValues()

    def nodes(self):
        return self._nodes

    def addTerminal(self, name, **opts):
        term = (Node.addTerminal)(self, name, **opts)
        name = term.name()
        if opts['io'] == 'in':
            opts['io'] = 'out'
            opts['multi'] = False
            self.inputNode.sigTerminalAdded.disconnect(self.internalTerminalAdded)
            try:
                term2 = (self.inputNode.addTerminal)(name, **opts)
            finally:
                self.inputNode.sigTerminalAdded.connect(self.internalTerminalAdded)

        else:
            opts['io'] = 'in'
            self.outputNode.sigTerminalAdded.disconnect(self.internalTerminalAdded)
            try:
                term2 = (self.outputNode.addTerminal)(name, **opts)
            finally:
                self.outputNode.sigTerminalAdded.connect(self.internalTerminalAdded)

        return term

    def removeTerminal(self, name):
        term = self[name]
        inTerm = self.internalTerminal(term)
        Node.removeTerminal(self, name)
        inTerm.node().removeTerminal(inTerm.name())

    def internalTerminalRenamed(self, term, oldName):
        self[oldName].rename(term.name())

    def internalTerminalAdded(self, node, term):
        if term._io == 'in':
            io = 'out'
        else:
            io = 'in'
        Node.addTerminal(self, (term.name()), io=io, renamable=(term.isRenamable()), removable=(term.isRemovable()), multiable=(term.isMultiable()))

    def internalTerminalRemoved(self, node, term):
        try:
            Node.removeTerminal(self, term.name())
        except KeyError:
            pass

    def terminalRenamed(self, term, oldName):
        newName = term.name()
        Node.terminalRenamed(self, self[oldName], oldName)
        for n in [self.inputNode, self.outputNode]:
            if oldName in n.terminals:
                n[oldName].rename(newName)

    def createNode(self, nodeType, name=None, pos=None):
        if name is None:
            n = 0
            while True:
                name = '%s.%d' % (nodeType, n)
                if name not in self._nodes:
                    break
                n += 1

        node = self.library.getNodeType(nodeType)(name)
        self.addNode(node, name, pos)
        return node

    def addNode(self, node, name, pos=None):
        if pos is None:
            pos = [
             0, 0]
        if type(pos) in [QtCore.QPoint, QtCore.QPointF]:
            pos = [
             pos.x(), pos.y()]
        item = node.graphicsItem()
        item.setZValue(self.nextZVal * 2)
        self.nextZVal += 1
        self.viewBox.addItem(item)
        (item.moveBy)(*pos)
        self._nodes[name] = node
        self.widget().addNode(node)
        node.sigClosed.connect(self.nodeClosed)
        node.sigRenamed.connect(self.nodeRenamed)
        node.sigOutputChanged.connect(self.nodeOutputChanged)
        self.sigChartChanged.emit(self, 'add', node)

    def removeNode(self, node):
        node.close()

    def nodeClosed(self, node):
        del self._nodes[node.name()]
        self.widget().removeNode(node)
        for signal in ('sigClosed', 'sigRenamed', 'sigOutputChanged'):
            try:
                getattr(node, signal).disconnect(self.nodeClosed)
            except (TypeError, RuntimeError):
                pass

        self.sigChartChanged.emit(self, 'remove', node)

    def nodeRenamed(self, node, oldName):
        del self._nodes[oldName]
        self._nodes[node.name()] = node
        self.widget().nodeRenamed(node, oldName)
        self.sigChartChanged.emit(self, 'rename', node)

    def arrangeNodes(self):
        pass

    def internalTerminal(self, term):
        """If the terminal belongs to the external Node, return the corresponding internal terminal"""
        if term.node() is self:
            if term.isInput():
                return self.inputNode[term.name()]
            return self.outputNode[term.name()]
        else:
            return term

    def connectTerminals(self, term1, term2):
        """Connect two terminals together within this flowchart."""
        term1 = self.internalTerminal(term1)
        term2 = self.internalTerminal(term2)
        term1.connectTo(term2)

    def process(self, **args):
        """
        Process data through the flowchart, returning the output.
        
        Keyword arguments must be the names of input terminals. 
        The return value is a dict with one key per output terminal.
        
        """
        data = {}
        order = self.processOrder()
        for n, t in self.inputNode.outputs().items():
            if n in args:
                data[t] = args[n]

        ret = {}
        for c, arg in order:
            if c == 'p':
                node = arg
                if node is self.inputNode:
                    continue
                outs = list(node.outputs().values())
                ins = list(node.inputs().values())
                args = {}
                for inp in ins:
                    inputs = inp.inputTerminals()
                    if len(inputs) == 0:
                        continue
                    if inp.isMultiValue():
                        args[inp.name()] = dict([(i, data[i]) for i in inputs if i in data])
                    else:
                        args[inp.name()] = data[inputs[0]]

                if node is self.outputNode:
                    ret = args
                else:
                    try:
                        if node.isBypassed():
                            result = node.processBypassed(args)
                        else:
                            result = (node.process)(display=False, **args)
                    except:
                        print('Error processing node %s. Args are: %s' % (str(node), str(args)))
                        raise

                    for out in outs:
                        try:
                            data[out] = result[out.name()]
                        except KeyError:
                            pass

            elif c == 'd' and arg in data:
                del data[arg]

        return ret

    def processOrder(self):
        """Return the order of operations required to process this chart.
        The order returned should look like [('p', node1), ('p', node2), ('d', terminal1), ...] 
        where each tuple specifies either (p)rocess this node or (d)elete the result from this terminal
        """
        deps = {}
        tdeps = {}
        for name, node in self._nodes.items():
            deps[node] = node.dependentNodes()
            for t in node.outputs().values():
                tdeps[t] = t.dependentNodes()

        order = fn.toposort(deps)
        ops = [('p', n) for n in order]
        dels = []
        for t, nodes in tdeps.items():
            lastInd = 0
            lastNode = None
            for n in nodes:
                if n is self:
                    lastInd = None
                    break
                else:
                    try:
                        ind = order.index(n)
                    except ValueError:
                        continue

                if lastNode is None or ind > lastInd:
                    lastNode = n
                    lastInd = ind

            if lastInd is not None:
                dels.append((lastInd + 1, t))

        dels.sort(key=(lambda a: a[0]), reverse=True)
        for i, t in dels:
            ops.insert(i, ('d', t))

        return ops

    def nodeOutputChanged(self, startNode):
        """Triggered when a node's output values have changed. (NOT called during process())
        Propagates new data forward through network."""
        if self.processing:
            return
        self.processing = True
        try:
            deps = {}
            for name, node in self._nodes.items():
                deps[node] = []
                for t in node.outputs().values():
                    deps[node].extend(t.dependentNodes())

            order = fn.toposort(deps, nodes=[startNode])
            order.reverse()
            terms = set(startNode.outputs().values())
            for node in order[1:]:
                for term in list(node.inputs().values()):
                    deps = list(term.connections().keys())
                    update = False
                    for d in deps:
                        if d in terms:
                            update = True
                            term.inputChanged(d, process=False)

                    if update:
                        node.update()
                        terms |= set(node.outputs().values())

        finally:
            self.processing = False
            if self.inputWasSet:
                self.inputWasSet = False
            else:
                self.sigStateChanged.emit()

    def chartGraphicsItem(self):
        """Return the graphicsItem which displays the internals of this flowchart.
        (graphicsItem() still returns the external-view item)"""
        return self.viewBox

    def widget(self):
        if self._widget is None:
            self._widget = FlowchartCtrlWidget(self)
            self.scene = self._widget.scene()
            self.viewBox = self._widget.viewBox()
        return self._widget

    def listConnections(self):
        conn = set()
        for n in self._nodes.values():
            terms = n.outputs()
            for n, t in terms.items():
                for c in t.connections():
                    conn.add((t, c))

        return conn

    def saveState(self):
        state = Node.saveState(self)
        state['nodes'] = []
        state['connects'] = []
        for name, node in self._nodes.items():
            cls = type(node)
            if hasattr(cls, 'nodeName'):
                clsName = cls.nodeName
                pos = node.graphicsItem().pos()
                ns = {'class':clsName,  'name':name,  'pos':(pos.x(), pos.y()),  'state':node.saveState()}
                state['nodes'].append(ns)

        conn = self.listConnections()
        for a, b in conn:
            state['connects'].append((a.node().name(), a.name(), b.node().name(), b.name()))

        state['inputNode'] = self.inputNode.saveState()
        state['outputNode'] = self.outputNode.saveState()
        return state

    def restoreState(self, state, clear=False):
        self.blockSignals(True)
        try:
            if clear:
                self.clear()
            Node.restoreState(self, state)
            nodes = state['nodes']
            nodes.sort(key=(lambda a: a['pos'][0]))
            for n in nodes:
                if n['name'] in self._nodes:
                    self._nodes[n['name']].restoreState(n['state'])
                    continue
                try:
                    node = self.createNode((n['class']), name=(n['name']))
                    node.restoreState(n['state'])
                except:
                    printExc('Error creating node %s: (continuing anyway)' % n['name'])

            self.inputNode.restoreState(state.get('inputNode', {}))
            self.outputNode.restoreState(state.get('outputNode', {}))
            for n1, t1, n2, t2 in state['connects']:
                try:
                    self.connectTerminals(self._nodes[n1][t1], self._nodes[n2][t2])
                except:
                    print(self._nodes[n1].terminals)
                    print(self._nodes[n2].terminals)
                    printExc('Error connecting terminals %s.%s - %s.%s:' % (n1, t1, n2, t2))

        finally:
            self.blockSignals(False)

        self.sigChartLoaded.emit()
        self.outputChanged()
        self.sigStateChanged.emit()

    def loadFile(self, fileName=None, startDir=None):
        if fileName is None:
            if startDir is None:
                startDir = self.filePath
            if startDir is None:
                startDir = '.'
            self.fileDialog = FileDialog(None, 'Load Flowchart..', startDir, 'Flowchart (*.fc)')
            self.fileDialog.show()
            self.fileDialog.fileSelected.connect(self.loadFile)
            return
        fileName = unicode(fileName)
        state = configfile.readConfigFile(fileName)
        self.restoreState(state, clear=True)
        self.viewBox.autoRange()
        self.sigFileLoaded.emit(fileName)

    def saveFile(self, fileName=None, startDir=None, suggestedFileName='flowchart.fc'):
        if fileName is None:
            if startDir is None:
                startDir = self.filePath
            if startDir is None:
                startDir = '.'
            self.fileDialog = FileDialog(None, 'Save Flowchart..', startDir, 'Flowchart (*.fc)')
            self.fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            self.fileDialog.show()
            self.fileDialog.fileSelected.connect(self.saveFile)
            return
        fileName = unicode(fileName)
        configfile.writeConfigFile(self.saveState(), fileName)
        self.sigFileSaved.emit(fileName)

    def clear(self):
        for n in list(self._nodes.values()):
            if not n is self.inputNode:
                if n is self.outputNode:
                    continue
                n.close()

        self.widget().clear()

    def clearTerminals(self):
        Node.clearTerminals(self)
        self.inputNode.clearTerminals()
        self.outputNode.clearTerminals()


class FlowchartGraphicsItem(GraphicsObject):

    def __init__(self, chart):
        GraphicsObject.__init__(self)
        self.chart = chart
        self.updateTerminals()

    def updateTerminals(self):
        self.terminals = {}
        bounds = self.boundingRect()
        inp = self.chart.inputs()
        dy = bounds.height() / (len(inp) + 1)
        y = dy
        for n, t in inp.items():
            item = t.graphicsItem()
            self.terminals[n] = item
            item.setParentItem(self)
            item.setAnchor(bounds.width(), y)
            y += dy

        out = self.chart.outputs()
        dy = bounds.height() / (len(out) + 1)
        y = dy
        for n, t in out.items():
            item = t.graphicsItem()
            self.terminals[n] = item
            item.setParentItem(self)
            item.setAnchor(0, y)
            y += dy

    def boundingRect(self):
        return QtCore.QRectF()

    def paint(self, p, *args):
        pass


class FlowchartCtrlWidget(QtGui.QWidget):
    __doc__ = 'The widget that contains the list of all the nodes in a flowchart and their controls, as well as buttons for loading/saving flowcharts.'

    def __init__(self, chart):
        self.items = {}
        self.currentFileName = None
        QtGui.QWidget.__init__(self)
        self.chart = chart
        self.ui = FlowchartCtrlTemplate.Ui_Form()
        self.ui.setupUi(self)
        self.ui.ctrlList.setColumnCount(2)
        self.ui.ctrlList.setColumnWidth(1, 20)
        self.ui.ctrlList.setVerticalScrollMode(self.ui.ctrlList.ScrollPerPixel)
        self.ui.ctrlList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.chartWidget = FlowchartWidget(chart, self)
        self.cwWin = QtGui.QMainWindow()
        self.cwWin.setWindowTitle('Flowchart')
        self.cwWin.setCentralWidget(self.chartWidget)
        self.cwWin.resize(1000, 800)
        h = self.ui.ctrlList.header()
        if not USE_PYQT5:
            h.setResizeMode(0, h.Stretch)
        else:
            h.setSectionResizeMode(0, h.Stretch)
        self.ui.ctrlList.itemChanged.connect(self.itemChanged)
        self.ui.loadBtn.clicked.connect(self.loadClicked)
        self.ui.saveBtn.clicked.connect(self.saveClicked)
        self.ui.saveAsBtn.clicked.connect(self.saveAsClicked)
        self.ui.showChartBtn.toggled.connect(self.chartToggled)
        self.chart.sigFileLoaded.connect(self.setCurrentFile)
        self.ui.reloadBtn.clicked.connect(self.reloadClicked)
        self.chart.sigFileSaved.connect(self.fileSaved)

    def chartToggled(self, b):
        if b:
            self.cwWin.show()
        else:
            self.cwWin.hide()

    def reloadClicked(self):
        try:
            self.chartWidget.reloadLibrary()
            self.ui.reloadBtn.success('Reloaded.')
        except:
            self.ui.reloadBtn.success('Error.')
            raise

    def loadClicked(self):
        newFile = self.chart.loadFile()

    def fileSaved(self, fileName):
        self.setCurrentFile(unicode(fileName))
        self.ui.saveBtn.success('Saved.')

    def saveClicked(self):
        if self.currentFileName is None:
            self.saveAsClicked()
        else:
            try:
                self.chart.saveFile(self.currentFileName)
            except:
                self.ui.saveBtn.failure('Error')
                raise

    def saveAsClicked(self):
        try:
            if self.currentFileName is None:
                newFile = self.chart.saveFile()
            else:
                newFile = self.chart.saveFile(suggestedFileName=(self.currentFileName))
        except:
            self.ui.saveBtn.failure('Error')
            raise

    def setCurrentFile(self, fileName):
        self.currentFileName = unicode(fileName)
        if fileName is None:
            self.ui.fileNameLabel.setText('<b>[ new ]</b>')
        else:
            self.ui.fileNameLabel.setText('<b>%s</b>' % os.path.split(self.currentFileName)[1])
        self.resizeEvent(None)

    def itemChanged(self, *args):
        pass

    def scene(self):
        return self.chartWidget.scene()

    def viewBox(self):
        return self.chartWidget.viewBox()

    def nodeRenamed(self, node, oldName):
        self.items[node].setText(0, node.name())

    def addNode(self, node):
        ctrl = node.ctrlWidget()
        item = QtGui.QTreeWidgetItem([node.name(), '', ''])
        self.ui.ctrlList.addTopLevelItem(item)
        byp = QtGui.QPushButton('X')
        byp.setCheckable(True)
        byp.setFixedWidth(20)
        item.bypassBtn = byp
        self.ui.ctrlList.setItemWidget(item, 1, byp)
        byp.node = node
        node.bypassButton = byp
        byp.setChecked(node.isBypassed())
        byp.clicked.connect(self.bypassClicked)
        if ctrl is not None:
            item2 = QtGui.QTreeWidgetItem()
            item.addChild(item2)
            self.ui.ctrlList.setItemWidget(item2, 0, ctrl)
        self.items[node] = item

    def removeNode(self, node):
        if node in self.items:
            item = self.items[node]
            try:
                item.bypassBtn.clicked.disconnect(self.bypassClicked)
            except (TypeError, RuntimeError):
                pass

            self.ui.ctrlList.removeTopLevelItem(item)

    def bypassClicked(self):
        btn = QtCore.QObject.sender(self)
        btn.node.bypass(btn.isChecked())

    def chartWidget(self):
        return self.chartWidget

    def outputChanged(self, data):
        pass

    def clear(self):
        self.chartWidget.clear()

    def select(self, node):
        item = self.items[node]
        self.ui.ctrlList.setCurrentItem(item)


class FlowchartWidget(dockarea.DockArea):
    __doc__ = 'Includes the actual graphical flowchart and debugging interface'

    def __init__(self, chart, ctrl):
        dockarea.DockArea.__init__(self)
        self.chart = chart
        self.ctrl = ctrl
        self.hoverItem = None
        self.view = FlowchartGraphicsView.FlowchartGraphicsView(self)
        self.viewDock = dockarea.Dock('view', size=(1000, 600))
        self.viewDock.addWidget(self.view)
        self.viewDock.hideTitleBar()
        self.addDock(self.viewDock)
        self.hoverText = QtGui.QTextEdit()
        self.hoverText.setReadOnly(True)
        self.hoverDock = dockarea.Dock('Hover Info', size=(1000, 20))
        self.hoverDock.addWidget(self.hoverText)
        self.addDock(self.hoverDock, 'bottom')
        self.selInfo = QtGui.QWidget()
        self.selInfoLayout = QtGui.QGridLayout()
        self.selInfo.setLayout(self.selInfoLayout)
        self.selDescLabel = QtGui.QLabel()
        self.selNameLabel = QtGui.QLabel()
        self.selDescLabel.setWordWrap(True)
        self.selectedTree = DataTreeWidget()
        self.selInfoLayout.addWidget(self.selDescLabel)
        self.selInfoLayout.addWidget(self.selectedTree)
        self.selDock = dockarea.Dock('Selected Node', size=(1000, 200))
        self.selDock.addWidget(self.selInfo)
        self.addDock(self.selDock, 'bottom')
        self._scene = self.view.scene()
        self._viewBox = self.view.viewBox()
        self.buildMenu()
        self._scene.selectionChanged.connect(self.selectionChanged)
        self._scene.sigMouseHover.connect(self.hoverOver)

    def reloadLibrary(self):
        self.nodeMenu.triggered.disconnect(self.nodeMenuTriggered)
        self.nodeMenu = None
        self.subMenus = []
        self.chart.library.reload()
        self.buildMenu()

    def buildMenu(self, pos=None):

        def buildSubMenu(node, rootMenu, subMenus, pos=None):
            for section, node in node.items():
                menu = QtGui.QMenu(section)
                rootMenu.addMenu(menu)
                if isinstance(node, OrderedDict):
                    buildSubMenu(node, menu, subMenus, pos=pos)
                    subMenus.append(menu)
                else:
                    act = rootMenu.addAction(section)
                    act.nodeType = section
                    act.pos = pos

        self.nodeMenu = QtGui.QMenu()
        self.subMenus = []
        buildSubMenu((self.chart.library.getNodeTree()), (self.nodeMenu), (self.subMenus), pos=pos)
        self.nodeMenu.triggered.connect(self.nodeMenuTriggered)
        return self.nodeMenu

    def menuPosChanged(self, pos):
        self.menuPos = pos

    def showViewMenu(self, ev):
        self.buildMenu(ev.scenePos())
        self.nodeMenu.popup(ev.screenPos())

    def scene(self):
        return self._scene

    def viewBox(self):
        return self._viewBox

    def nodeMenuTriggered(self, action):
        nodeType = action.nodeType
        if action.pos is not None:
            pos = action.pos
        else:
            pos = self.menuPos
        pos = self.viewBox().mapSceneToView(pos)
        self.chart.createNode(nodeType, pos=pos)

    def selectionChanged(self):
        items = self._scene.selectedItems()
        if len(items) == 0:
            data = None
        else:
            item = items[0]
            if hasattr(item, 'node') and isinstance(item.node, Node):
                n = item.node
                self.ctrl.select(n)
                data = {'outputs':n.outputValues(),  'inputs':n.inputValues()}
                self.selNameLabel.setText(n.name())
                if hasattr(n, 'nodeName'):
                    self.selDescLabel.setText('<b>%s</b>: %s' % (n.nodeName, n.__class__.__doc__))
                else:
                    self.selDescLabel.setText('')
                if n.exception is not None:
                    data['exception'] = n.exception
            else:
                data = None
        self.selectedTree.setData(data, hideRoot=True)

    def hoverOver(self, items):
        term = None
        for item in items:
            if item is self.hoverItem:
                return
                self.hoverItem = item
                if hasattr(item, 'term') and isinstance(item.term, Terminal):
                    term = item.term
                    break

        if term is None:
            self.hoverText.setPlainText('')
        else:
            val = term.value()
            if isinstance(val, ndarray):
                val = '%s %s %s' % (type(val).__name__, str(val.shape), str(val.dtype))
            else:
                val = str(val)
                if len(val) > 400:
                    val = val[:400] + '...'
            self.hoverText.setPlainText('%s.%s = %s' % (term.node().name(), term.name(), val))

    def clear(self):
        self.selectedTree.setData(None)
        self.hoverText.setPlainText('')
        self.selNameLabel.setText('')
        self.selDescLabel.setText('')


class FlowchartNode(Node):
    pass