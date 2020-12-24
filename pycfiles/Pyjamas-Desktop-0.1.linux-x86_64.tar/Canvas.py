# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/Canvas.py
# Compiled at: 2008-09-03 09:02:13
import DOM
from ui import Image, Widget

class Canvas(Widget):

    def __init__(self, width, height):
        self.context = None
        self.setElement(DOM.createDiv())
        canvas = DOM.createElement('canvas')
        self.setWidth(width)
        self.setHeight(height)
        canvas.width = width
        canvas.height = height
        DOM.appendChild(self.getElement(), canvas)
        self.setStyleName('gwt-Canvas')
        self.init()
        self.context.fillStyle = 'black'
        self.context.strokeStyle = 'black'
        return

    def getContext(self):
        return self.context

    def isEmulation(self):
        JS('\n        return (typeof $wnd.G_vmlCanvasManager != "undefined");\n        ')

    def init(self):
        JS('\n        var el = this.getElement().firstChild;\n        if (typeof $wnd.G_vmlCanvasManager != "undefined") {\n            var parent = el.parent;\n            \n            el = $wnd.G_vmlCanvasManager.fixElement_(el);\n            el.getContext = function () {\n                if (this.context_) {\n                    return this.context_;\n                }\n                return this.context_ = new $wnd.CanvasRenderingContext2D(el);\n            };\n        \n            el.attachEvent("onpropertychange", function (e) {\n                // we need to watch changes to width and height\n                switch (e.propertyName) {\n                    case "width":\n                    case "height":\n                    // coord size changed?\n                    break;\n                }\n            });\n\n            // if style.height is set\n            \n            var attrs = el.attributes;\n            if (attrs.width && attrs.width.specified) {\n                // TODO: use runtimeStyle and coordsize\n                // el.getContext().setWidth_(attrs.width.nodeValue);\n                el.style.width = attrs.width.nodeValue + "px";\n            }\n            if (attrs.height && attrs.height.specified) {\n                // TODO: use runtimeStyle and coordsize\n                // el.getContext().setHeight_(attrs.height.nodeValue);\n                el.style.height = attrs.height.nodeValue + "px";\n            }\n        }\n        var ctx = el.getContext("2d");\n        \n        ctx._createPattern = ctx.createPattern;\n        ctx.createPattern = function(img, rep) {\n            if (!(img instanceof Image)) img = img.getElement(); \n            return this._createPattern(img, rep);\n            }\n\n        ctx._drawImage = ctx.drawImage;\n        ctx.drawImage = function() {\n            var a=arguments;\n            if (!(a[0] instanceof Image)) a[0] = a[0].getElement();\n            if (a.length==9) return this._drawImage(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]);\n            else if (a.length==5) return this._drawImage(a[0], a[1], a[2], a[3], a[4]);\n            return this._drawImage(a[0], a[1], a[2]);\n            }\n        \n        this.context = ctx;\n        ')


class CanvasImage(Image):

    def __init__(self, url='', load_listener=None):
        Image.__init__(self, url)
        if load_listener:
            self.addLoadListener(load_listener)
        self.onAttach()

    def isLoaded(self):
        return self.getElement().complete


class ImageLoadListener:

    def __init__(self, listener=None):
        self.wait_list = []
        self.loadListeners = []
        if listener:
            self.addLoadListener(listener)

    def add(self, sender):
        self.wait_list.append(sender)
        sender.addLoadListener(self)

    def addLoadListener(self, listener):
        self.loadListeners.append(listener)

    def isLoaded(self):
        if len(self.wait_list):
            return False
        return True

    def onError(self, sender):
        for listener in self.loadListeners:
            listener.onError(sender)

    def onLoad(self, sender):
        self.wait_list.remove(sender)
        if self.isLoaded():
            for listener in self.loadListeners:
                listener.onLoad(self)