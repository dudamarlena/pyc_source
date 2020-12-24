# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/exporters/SVGExporter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 17241 bytes
from .Exporter import Exporter
from ..python2_3 import asUnicode
from ..parametertree import Parameter
from ..Qt import QtGui, QtCore, QtSvg, USE_PYSIDE
from .. import debug
from .. import functions as fn
import re
import xml.dom.minidom as xml
import numpy as np
__all__ = [
 'SVGExporter']

class SVGExporter(Exporter):
    Name = 'Scalable Vector Graphics (SVG)'
    allowCopy = True

    def __init__(self, item):
        Exporter.__init__(self, item)
        self.params = Parameter(name='params', type='group', children=[])

    def widthChanged(self):
        sr = self.getSourceRect()
        ar = sr.height() / sr.width()
        self.params.param('height').setValue((self.params['width'] * ar), blockSignal=(self.heightChanged))

    def heightChanged(self):
        sr = self.getSourceRect()
        ar = sr.width() / sr.height()
        self.params.param('width').setValue((self.params['height'] * ar), blockSignal=(self.widthChanged))

    def parameters(self):
        return self.params

    def export(self, fileName=None, toBytes=False, copy=False):
        if toBytes is False:
            if copy is False:
                if fileName is None:
                    self.fileSaveDialog(filter='Scalable Vector Graphics (*.svg)')
                    return
        else:
            xml = generateSvg(self.item)
            if toBytes:
                return xml.encode('UTF-8')
                if copy:
                    md = QtCore.QMimeData()
                    md.setData('image/svg+xml', QtCore.QByteArray(xml.encode('UTF-8')))
                    QtGui.QApplication.clipboard().setMimeData(md)
            else:
                with open(fileName, 'wb') as (fh):
                    fh.write(asUnicode(xml).encode('utf-8'))


xmlHeader = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  version="1.2" baseProfile="tiny">\n<title>pyqtgraph SVG export</title>\n<desc>Generated with Qt and pyqtgraph</desc>\n'

def generateSvg(item):
    global xmlHeader
    try:
        node, defs = _generateItemSvg(item)
    finally:
        if isinstance(item, QtGui.QGraphicsScene):
            items = item.items()
        else:
            items = [
             item]
            for i in items:
                items.extend(i.childItems())

        for i in items:
            if hasattr(i, 'setExportMode'):
                i.setExportMode(False)

    cleanXml(node)
    defsXml = '<defs>\n'
    for d in defs:
        defsXml += d.toprettyxml(indent='    ')

    defsXml += '</defs>\n'
    return xmlHeader + defsXml + node.toprettyxml(indent='    ') + '\n</svg>\n'


def _generateItemSvg(item, nodes=None, root=None):
    profiler = debug.Profiler()
    if nodes is None:
        nodes = {}
    if root is None:
        root = item
    if hasattr(item, 'isVisible'):
        if not item.isVisible():
            return
    if hasattr(item, 'generateSvg'):
        return item.generateSvg(nodes)
    tr = QtGui.QTransform()
    if isinstance(item, QtGui.QGraphicsScene):
        xmlStr = '<g>\n</g>\n'
        doc = xml.parseString(xmlStr)
        childs = [i for i in item.items() if i.parentItem() is None]
    elif item.__class__.paint == QtGui.QGraphicsItem.paint:
        xmlStr = '<g>\n</g>\n'
        doc = xml.parseString(xmlStr)
        childs = item.childItems()
    else:
        childs = item.childItems()
        tr = itemTransform(item, item.scene())
        if isinstance(root, QtGui.QGraphicsScene):
            rootPos = QtCore.QPoint(0, 0)
        else:
            rootPos = root.scenePos()
        tr2 = QtGui.QTransform()
        tr2.translate(-rootPos.x(), -rootPos.y())
        tr = tr * tr2
        arr = QtCore.QByteArray()
        buf = QtCore.QBuffer(arr)
        svg = QtSvg.QSvgGenerator()
        svg.setOutputDevice(buf)
        dpi = QtGui.QDesktopWidget().physicalDpiX()
        svg.setResolution(dpi)
        p = QtGui.QPainter()
        p.begin(svg)
        if hasattr(item, 'setExportMode'):
            item.setExportMode(True, {'painter': p})
        else:
            try:
                p.setTransform(tr)
                item.paint(p, QtGui.QStyleOptionGraphicsItem(), None)
            finally:
                p.end()

            if USE_PYSIDE:
                xmlStr = str(arr)
            else:
                xmlStr = bytes(arr).decode('utf-8')
        doc = xml.parseString(xmlStr)
    try:
        g1 = doc.getElementsByTagName('g')[0]
        g2 = [n for n in g1.childNodes if isinstance(n, xml.Element) if n.tagName == 'g']
        defs = doc.getElementsByTagName('defs')
        if len(defs) > 0:
            defs = [n for n in defs[0].childNodes if isinstance(n, xml.Element)]
    except:
        print(doc.toxml())
        raise

    profiler('render')
    correctCoordinates(g1, defs, item)
    profiler('correct')
    baseName = item.__class__.__name__
    i = 1
    while True:
        name = baseName + '_%d' % i
        if name not in nodes:
            break
        i += 1

    nodes[name] = g1
    g1.setAttribute('id', name)
    childGroup = g1
    if not isinstance(item, QtGui.QGraphicsScene):
        if int(item.flags() & item.ItemClipsChildrenToShape) > 0:
            path = QtGui.QGraphicsPathItem(item.mapToScene(item.shape()))
            item.scene().addItem(path)
            try:
                pathNode = _generateItemSvg(path, root=root)[0].getElementsByTagName('path')[0]
            finally:
                item.scene().removeItem(path)

            clip = name + '_clip'
            clipNode = g1.ownerDocument.createElement('clipPath')
            clipNode.setAttribute('id', clip)
            clipNode.appendChild(pathNode)
            g1.appendChild(clipNode)
            childGroup = g1.ownerDocument.createElement('g')
            childGroup.setAttribute('clip-path', 'url(#%s)' % clip)
            g1.appendChild(childGroup)
    profiler('clipping')
    childs.sort(key=(lambda c: c.zValue()))
    for ch in childs:
        csvg = _generateItemSvg(ch, nodes, root)
        if csvg is None:
            continue
        cg, cdefs = csvg
        childGroup.appendChild(cg)
        defs.extend(cdefs)

    profiler('children')
    return (
     g1, defs)


def correctCoordinates(node, defs, item):
    groups = node.getElementsByTagName('g')
    groups2 = []
    for grp in groups:
        subGroups = [
         grp.cloneNode(deep=False)]
        textGroup = None
        for ch in grp.childNodes[:]:
            if isinstance(ch, xml.Element):
                if textGroup is None:
                    textGroup = ch.tagName == 'text'
                elif ch.tagName == 'text':
                    if textGroup is False:
                        subGroups.append(grp.cloneNode(deep=False))
                        textGroup = True
                elif textGroup is True:
                    subGroups.append(grp.cloneNode(deep=False))
                    textGroup = False
            subGroups[(-1)].appendChild(ch)

        groups2.extend(subGroups)
        for sg in subGroups:
            node.insertBefore(sg, grp)

        node.removeChild(grp)

    groups = groups2
    for grp in groups:
        matrix = grp.getAttribute('transform')
        match = re.match('matrix\\((.*)\\)', matrix)
        if match is None:
            vals = [
             1, 0, 0, 1, 0, 0]
        else:
            vals = [float(a) for a in match.groups()[0].split(',')]
        tr = np.array([[vals[0], vals[2], vals[4]], [vals[1], vals[3], vals[5]]])
        removeTransform = False
        for ch in grp.childNodes:
            if not isinstance(ch, xml.Element):
                continue
            if ch.tagName == 'polyline':
                removeTransform = True
                coords = np.array([[float(a) for a in c.split(',')] for c in ch.getAttribute('points').strip().split(' ')])
                coords = fn.transformCoordinates(tr, coords, transpose=True)
                ch.setAttribute('points', ' '.join([','.join([str(a) for a in c]) for c in coords]))
            elif ch.tagName == 'path':
                removeTransform = True
                newCoords = ''
                oldCoords = ch.getAttribute('d').strip()
                if oldCoords == '':
                    continue
                for c in oldCoords.split(' '):
                    x, y = c.split(',')
                    if x[0].isalpha():
                        t = x[0]
                        x = x[1:]
                    else:
                        t = ''
                    nc = fn.transformCoordinates(tr, (np.array([[float(x), float(y)]])), transpose=True)
                    newCoords += t + str(nc[(0, 0)]) + ',' + str(nc[(0, 1)]) + ' '

                ch.setAttribute('d', newCoords)
            elif ch.tagName == 'text':
                removeTransform = False
                families = ch.getAttribute('font-family').split(',')
                if len(families) == 1:
                    font = QtGui.QFont(families[0].strip('" '))
                    if font.style() == font.SansSerif:
                        families.append('sans-serif')
                    elif font.style() == font.Serif:
                        families.append('serif')
                    elif font.style() == font.Courier:
                        families.append('monospace')
                    ch.setAttribute('font-family', ', '.join([f if ' ' not in f else '"%s"' % f for f in families]))
            if removeTransform and ch.getAttribute('vector-effect') != 'non-scaling-stroke':
                w = float(grp.getAttribute('stroke-width'))
                s = fn.transformCoordinates(tr, (np.array([[w, 0], [0, 0]])), transpose=True)
                w = ((s[0] - s[1]) ** 2).sum() ** 0.5
                ch.setAttribute('stroke-width', str(w))

        if removeTransform:
            grp.removeAttribute('transform')


SVGExporter.register()

def itemTransform(item, root):
    if item is root:
        tr = QtGui.QTransform()
        (tr.translate)(*item.pos())
        tr = tr * item.transform()
        return tr
    if int(item.flags() & item.ItemIgnoresTransformations) > 0:
        pos = item.pos()
        parent = item.parentItem()
        if parent is not None:
            pos = itemTransform(parent, root).map(pos)
        tr = QtGui.QTransform()
        tr.translate(pos.x(), pos.y())
        tr = item.transform() * tr
    else:
        nextRoot = item
        while 1:
            nextRoot = nextRoot.parentItem()
            if nextRoot is None:
                nextRoot = root
                break
            if nextRoot is root or int(nextRoot.flags() & nextRoot.ItemIgnoresTransformations) > 0:
                break

        if isinstance(nextRoot, QtGui.QGraphicsScene):
            tr = item.sceneTransform()
        else:
            tr = itemTransform(nextRoot, root) * item.itemTransform(nextRoot)[0]
    return tr


def cleanXml--- This code section failed: ---

 L. 429         0  LOAD_CONST               False
                2  STORE_FAST               'hasElement'

 L. 430         4  BUILD_LIST_0          0 
                6  STORE_FAST               'nonElement'

 L. 431         8  SETUP_LOOP           60  'to 60'
               10  LOAD_FAST                'node'
               12  LOAD_ATTR                childNodes
               14  GET_ITER         
               16  FOR_ITER             58  'to 58'
               18  STORE_FAST               'ch'

 L. 432        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'ch'
               24  LOAD_GLOBAL              xml
               26  LOAD_ATTR                Element
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L. 433        32  LOAD_CONST               True
               34  STORE_FAST               'hasElement'

 L. 434        36  LOAD_GLOBAL              cleanXml
               38  LOAD_FAST                'ch'
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          
               44  JUMP_BACK            16  'to 16'
             46_0  COME_FROM            30  '30'

 L. 436        46  LOAD_FAST                'nonElement'
               48  LOAD_METHOD              append
               50  LOAD_FAST                'ch'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
               56  JUMP_BACK            16  'to 16'
               58  POP_BLOCK        
             60_0  COME_FROM_LOOP        8  '8'

 L. 438        60  LOAD_FAST                'hasElement'
               62  POP_JUMP_IF_FALSE    90  'to 90'

 L. 439        64  SETUP_LOOP          112  'to 112'
               66  LOAD_FAST                'nonElement'
               68  GET_ITER         
               70  FOR_ITER             86  'to 86'
               72  STORE_FAST               'ch'

 L. 440        74  LOAD_FAST                'node'
               76  LOAD_METHOD              removeChild
               78  LOAD_FAST                'ch'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            70  'to 70'
               86  POP_BLOCK        
               88  JUMP_FORWARD        112  'to 112'
             90_0  COME_FROM            62  '62'

 L. 441        90  LOAD_FAST                'node'
               92  LOAD_ATTR                tagName
               94  LOAD_STR                 'g'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   112  'to 112'

 L. 442       100  LOAD_FAST                'node'
              102  LOAD_ATTR                parentNode
              104  LOAD_METHOD              removeChild
              106  LOAD_FAST                'node'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM            98  '98'
            112_1  COME_FROM            88  '88'
            112_2  COME_FROM_LOOP       64  '64'

Parse error at or near `COME_FROM' instruction at offset 112_1