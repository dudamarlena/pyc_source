# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/qtui2mj.py
# Compiled at: 2013-04-04 15:36:35
from decimal import Decimal
import sys, re, os, xml.sax.handler, traceback
from muntjac.api import *
from mjextras import *

class TreeBuilder(xml.sax.handler.ContentHandler):

    def __init__(self, parent):
        self.stack = []
        self.root = DataNode()
        self.current = self.root
        self.text_parts = []
        self.parent = parent

    def startElement(self, name, attrs):
        self.stack.append((self.current, self.text_parts))
        self.current = DataNode()
        self.text_parts = []
        for k, v in attrs.items():
            self.current._add_xml_attr(self.parent._name_mangle(k), v)

    def endElement(self, name):
        text = ('').join(self.text_parts).strip()
        if text:
            self.current.data = text
        if self.current._attrs:
            obj = self.current
        else:
            obj = text or ''
        self.current, self.text_parts = self.stack.pop()
        self.current._add_xml_attr(self.parent._name_mangle(name), obj)

    def characters(self, content):
        self.text_parts.append(content)


class DataNode(object):

    def __init__(self):
        self._attrs = {}
        self.data = None
        return

    def __len__(self):
        return 1

    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self._attrs.get(key, None)
        else:
            return [
             self][key]
            return

    def __contains__(self, name):
        return self._attrs.has_key(name)

    def __nonzero__(self):
        return bool(self._attrs or self.data)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)
        return self._attrs.get(name, None)

    def _add_xml_attr(self, name, value):
        if name in self._attrs:
            children = self._attrs[name]
            if not isinstance(children, list):
                children = [
                 children]
                self._attrs[name] = children
            children.append(value)
        else:
            self._attrs[name] = value

    def __str__(self):
        return self.data or ''

    def __repr__(self):
        items = sorted(self._attrs.items())
        if self.data:
            items.append(('data', self.data))
        return '{%s}' % (', ').join([ '%s:%s' % (k, repr(v)) for k, v in items ])


class xml2obj(object):

    def __init__(self, src):
        self.src = src
        self.non_id_char = re.compile('[^_0-9a-zA-Z]')

    def _name_mangle(self, name):
        return self.non_id_char.sub('_', name)

    def build(self):
        builder = TreeBuilder(self)
        if isinstance(self.src, basestring):
            xml.sax.parseString(self.src, builder)
        else:
            xml.sax.parse(self.src, builder)
        return builder.root._attrs.values()[0]


def cfkey(theobj, thevar):
    try:
        e = getattr(theobj, thevar)
        if e == '':
            return False
        return True
    except:
        return False


class MuntJacWindow(object):

    def __init__(self):
        pass


class QT2Muntjac(object):

    def __init__(self):
        pass

    def translateUI(self, filename):
        IN = open(filename, 'r').read()
        g = xml2obj(IN).build()
        centralwidget = g.widget
        mainWidget = aWidget(None, centralwidget, None, True)
        self.window = mainWidget.mainwidget
        self.ui = mainWidget.mainUI
        return


class aWidget(object):

    def __init__(self, parent, widget, mainUI=None, main=False):
        if mainUI == None:
            self.mainUI = MuntJacWindow()
        else:
            self.mainUI = mainUI
        self.main = main
        self.parent = parent
        self.widget = widget
        self.cls = widget['class']
        self.mainwidget = None
        self.isLayout = False
        if self.main == False:
            if self.parent.wHandleSize == False:
                self.wHandleSize = False
            else:
                self.wHandleSize = True
        else:
            self.wHandleSize = False
        found, geometry = self.getProperty('geometry')
        if found:
            self.geometry = geometry
        else:
            self.geometry = None
        self.makeWidget()
        self.makeChildren()
        return

    def makeWidget(self):
        if not self.main:
            if self.widget['class'] == 'QWidget':
                if self.widget.layout != None:
                    if self.widget.layout['class'] == 'QVBoxLayout':
                        self.mainUI.__dict__[self.widget.layout.name] = VerticalLayout()
                        self.thiswidget = self.mainUI.__dict__[self.widget.layout.name]
                        self.wHandleSize = False
                        self.isLayout = True
                    elif self.widget.layout['class'] == 'QHBoxLayout':
                        self.mainUI.__dict__[self.widget.layout.name] = HorizontalLayout()
                        self.thiswidget = self.mainUI.__dict__[self.widget.layout.name]
                        self.wHandleSize = False
                        self.isLayout = True
                elif self.widget.layout == None:
                    self.mainUI.__dict__[self.widget.name] = AbsoluteLayout()
                    self.thiswidget = self.mainUI.__dict__[self.widget.name]
                    self.wHandleSize = True
                if self.parent.widget['class'] == 'QMainWindow':
                    self.parent.mainwidget = self.thiswidget
                    self.mainUI.width = self.parent.geometry.rect.width
                    self.mainUI.height = self.parent.geometry.rect.height
            elif self.widget['class'] == 'QStackedWidget':
                self.mainUI.__dict__[self.widget.name] = StackedSheet()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
            elif self.widget['class'] == 'QGroupBox':
                title = str(self.getTitle())
                self.mainUI.__dict__[self.widget.name + 'Panel'] = Panel(title)
                self.thiswidget = self.mainUI.__dict__[(self.widget.name + 'Panel')]
                self.mainUI.__dict__[self.widget.name] = AbsoluteLayout()
                self.thiswidget.setContent(self.mainUI.__dict__[self.widget.name])
            elif self.widget['class'] == 'QLabel':
                text = str(self.getText())
                self.mainUI.__dict__[self.widget.name] = Label(text)
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
            elif self.widget['class'] == 'QLineEdit':
                text = str(self.getText())
                self.mainUI.__dict__[self.widget.name] = TextField('')
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
                self.thiswidget.setValue(text)
            elif self.widget['class'] == 'QPushButton':
                text = str(self.getText())
                self.mainUI.__dict__[self.widget.name] = Button(text)
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
            elif self.widget['class'] == 'QTextEdit':
                html = str(self.getHtml())
                self.mainUI.__dict__[self.widget.name] = TextArea()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
                self.thiswidget.setValue(html)
            elif self.widget['class'] == 'QTabWidget':
                self.mainUI.__dict__[self.widget.name] = TabSheet()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
            elif self.widget['class'] == 'QTableView' or self.widget['class'] == 'QTableWidget':
                self.mainUI.__dict__[self.widget.name] = Table()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
            elif self.widget['class'] == 'QCheckBox':
                self.mainUI.__dict__[self.widget.name] = CheckBox()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
            else:
                print 'could not handle ', self.widget['class']
                self.wHandleSize = False
                return
            if self.wHandleSize:
                self.handleSize()
            if self.parent.widget['class'] == 'QWidget':
                if self.parent.widget.layout != None:
                    pnname = self.parent.widget.layout.name
                    pnclass = self.parent.widget.layout['class']
                else:
                    pnname = self.parent.widget.name
                    pnclass = self.parent.widget['class']
                if self.widget.layout != None:
                    thname = self.widget.layout.name
                    thclass = self.widget.layout['class']
                else:
                    thname = self.widget.name
                    thclass = self.widget['class']
            else:
                pnname = self.parent.widget.name
                pnclass = self.parent.widget['class']
                thname = self.widget.name
                thclass = self.widget['class']
            if pnclass == 'QVBoxLayout' or pnclass == 'QHBoxLayout' or pnclass == 'QTabWidget' or pnclass == 'QStackedWidget':
                if pnclass != 'QMainWindow':
                    if self.parent.widget['class'] == 'QStackedWidget' or self.parent.widget['class'] == 'QTabWidget':
                        self.parent.thiswidget.addTab(self.thiswidget)
                        if thclass == 'QGroupBox':
                            self.thiswidget = self.mainUI.__dict__[thname]
                    else:
                        self.parent.thiswidget.addComponent(self.thiswidget)
                        if thclass == 'QGroupBox':
                            self.thiswidget = self.mainUI.__dict__[thname]
            elif pnclass != 'QMainWindow' and pnclass != 'QVBoxLayout' and pnclass != 'QHBoxLayout':
                if self.parent.geometry != None:
                    print 'adding', thname, 'to', pnname, 'is a', pnclass, 'is a', type(self.parent.thiswidget)
                    xpos = '%.2f' % ((float(self.geometry.rect.x) + 0.001) / (float(self.parent.geometry.rect.width) + 0.001) * 100)
                    ypos = '%.2f' % ((float(self.geometry.rect.y) + 0.001) / (float(self.parent.geometry.rect.height) + 0.001) * 100)
                    self.parent.thiswidget.addComponent(self.thiswidget, 'top:' + str(ypos) + '%;left:' + str(xpos) + '%')
                else:
                    print 'adding', thname, 'to', pnname, 'is a', pnclass, 'is a', type(self.parent.thiswidget)
                    self.parent.thiswidget.addComponent(self.thiswidget, 'top:' + str(self.geometry.rect.y) + '%;left:' + str(self.geometry.rect.x) + '%')
                if thclass == 'QGroupBox':
                    self.thiswidget = self.mainUI.__dict__[thname]
        return

    def handleSize(self):
        if self.geometry == None:
            self.geometry = self.parent.geometry
            wdth = '%.2f' % (float(self.parent.geometry.rect.width) / float(self.parent.geometry.rect.width) * 100)
            hgth = '%.2f' % (float(self.parent.geometry.rect.height) / float(self.parent.geometry.rect.height) * 100)
            if self.widget.name == 'gbValidation':
                print self.widget.name, wdth, hgth
            if self.widget['class'] != 'QPanel':
                self.thiswidget.setHeight(str(hgth) + '%')
            else:
                self.thiswidget.setHeight(str(self.parent.geometry.rect.height) + 'px')
            self.thiswidget.setWidth(str(wdth) + '%')
        else:
            wdth = '%.2f' % (float(self.geometry.rect.width) / (float(self.parent.geometry.rect.width) - float(self.geometry.rect.x)) * 100)
            hgth = '%.2f' % (float(self.geometry.rect.height) / (float(self.parent.geometry.rect.height) - float(self.geometry.rect.y)) * 100)
            if self.widget.name == 'gbValidation':
                print self.widget.name, wdth, hgth
            if self.widget['class'] != 'QLineEdit':
                self.thiswidget.setHeight(str(hgth) + '%')
            self.thiswidget.setWidth(str(wdth) + '%')
        return

    def getTitle(self):
        found, title = self.getProperty('title')
        if found:
            title = title.string
        else:
            title = ''
        return title

    def getText(self):
        found, thetext = self.getProperty('text')
        if found:
            thetext = thetext.string
        else:
            thetext = ''
        return thetext

    def getHtml(self):
        found, html = self.getProperty('html')
        if found:
            html = html.string
        else:
            html = ''
        return html

    def makeChildren(self):
        if self.isLayout:
            if self.widget.layout.item is not None:
                for awidget in self.widget.layout.item:
                    aWidget(self, awidget.widget, self.mainUI)

        elif self.widget.widget is not None:
            for awidget in self.widget.widget:
                aWidget(self, awidget, self.mainUI)

        if self.main:
            pass
        return

    def getProperty(self, name, ref='string'):
        widget = self.widget
        if cfkey(widget, 'property'):
            if type(widget.property) is list:
                for prop in widget.property:
                    if prop.name == name:
                        return (True, prop)

                return (
                 False, '')
            try:
                if widget.property.name == name:
                    return (True, widget.property)
                else:
                    return (
                     False, '')

            except:
                return (
                 False, '')

        else:
            return (
             False, '')

    def getSProperty(self, widget, name, ref='string'):
        if cfkey(widget, 'property'):
            if type(widget.property) is list:
                for prop in widget.property:
                    if prop.name == name:
                        ret = str(getattr(prop, ref))
                        return ret

                return ''
            try:
                if widget.property.name == name:
                    ret = str(getattr(widget.property, ref))
                    return ret
                else:
                    return ''

            except:
                return ''

        else:
            return ''


if __name__ == '__main__':
    conv = QT2Muntjac()
    conv.translateUI('DEMO.ui')