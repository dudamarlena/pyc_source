# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/RichTextEditor.py
# Compiled at: 2008-09-03 09:02:13
__doc__ = '\n    A rich text editor using FCKeditor.\n    \n    Pass "-j fckeditor/fckeditor.js" to build.py in order to include the FCKeditor\n    javascript.\n'
import Window, DOM
from pyjamas.__pyjamas__ import console
from BoundMethod import BoundMethod
from ui import Widget
from pyjamas.__pyjamas__ import JS

def createFCK(name):
    JS('\n    return new FCKeditor(name);\n    ')


JS('\n    $wnd.FCKeditor_OnComplete = function(editorInstance )\n    {\n        pyjsObject = $doc.getElementById(editorInstance.Name.substr(3)).__listener;\n        console.log("pyjsObject is %o", pyjsObject);\n        if(pyjsObject)\n            pyjsObject.onFCKLoaded(editorInstance);\n    }\n')

class RichTextEditor(Widget):

    def __init__(self, initialValue='', target='', method='POST'):
        Widget.__init__(self)
        self.id = 'rte' + hash(self)
        fck = createFCK('fck' + self.id)
        fck.Height = '600px'
        self.setElement(DOM.createForm())
        DOM.setAttribute(self.element, 'method', 'POST')
        DOM.setAttribute(self.element, 'target', target)
        JS('\n        var rte = this;\n        this.element.onsubmit = function() {\n            $wnd.setTimeout(function() { rte.onSave.call(rte) }, 0);\n            return false;\n        }\n        ')
        self.setID(self.id)
        self.addStyleName('gwt-RichTextEditor')
        fck.Value = initialValue
        fck.BasePath = 'fckeditor/'
        fck.Config.CustomConfigurationsPath = '../../fckconfig.js'
        fck.pyjsObject = self
        self.loaded = False
        self.saveListeners = []
        self.pendingHTML = None
        html = fck.CreateHtml()
        html = html
        DOM.setInnerHTML(self.getElement(), html)
        return

    def addSaveListener(self, listener):
        """
        When the user clicks the save button, your listener will be notified.
        
        Either pass a function (e.g. a BoundMethod) or an object with an onSave()
        method.  Either will be passed the RichtTextEditor instance.
        """
        self.saveListeners.append(listener)

    def removeSaveListener(self, listener):
        """
        Remove a previously added listener
        """
        self.saveListeners.remove(listener)

    def onFCKLoaded(self, fck):
        """
        Called when the FCK editor has loaded, and it is ready for use
        """
        self.loaded = True
        self.fck = fck
        fck.Events.AttachEvent('OnSelectionChange', BoundMethod(self, self.onSelectionChange))
        fck.Events.AttachEvent('OnBlur', BoundMethod(self, self.onBlur))
        fck.Events.AttachEvent('OnFocus', BoundMethod(self, self.onFocus))
        fck.Events.AttachEvent('OnPaste', BoundMethod(self, self.onPaste))
        if self.pendingHTML:
            fck.SetHTML(self.pendingHTML)
            self.pendingHTML = None
        return

    def onSelectionChange(self, sender):
        pass

    def onBlur(self, sender):
        pass

    def onFocus(self, sender):
        pass

    def onPaste(self, sender):
        pass

    def onSave(self):
        """
        Handle the save click and pass it onto the listeners
        """
        console.log('onSave() in %s', Window.getLocation().getHref())
        for listener in self.saveListeners:
            if listener.onSave:
                listener.onSave(self)
            else:
                listener(self)

        return False

    def setHTML(self, html):
        """
        Call this to change the html showing in the editor
        """
        if self.loaded:
            self.fck.SetHTML(html)
        else:
            self.pendingHTML = html

    def getHTML(self):
        """
        Call this to retrieve the HTML showing in the editor (e.g. to save/preview it)
        """
        return self.fck.GetXHTML(True)

    def getDOM(self):
        return self.fck.EditorDocument()

    def getWindow(self):
        return self.fck.EditorWindow()