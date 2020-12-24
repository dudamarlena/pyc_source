# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/History.py
# Compiled at: 2008-09-03 09:02:13
from pyjamas.__pyjamas__ import JS, doc, get_main_frame
historyToken = ''

def init():
    global __historyToken
    print 'history: TODO'
    __historyToken = ''
    return
    JS("\n    $wnd.__historyToken = '';\n\n    // Get the initial token from the url's hash component.\n    var hash = $wnd.location.hash;\n    if (hash.length > 0)\n        $wnd.__historyToken = decodeURIComponent(hash.substring(1));\n\n    // Create the timer that checks the browser's url hash every 1/4 s.\n    $wnd.__checkHistory = function() {\n        var token = '', hash = $wnd.location.hash;\n        if (hash.length > 0)\n            token = decodeURIComponent(hash.substring(1));\n\n        if (token != $wnd.__historyToken) {\n            $wnd.__historyToken = token;\n            // TODO - move init back into History\n            // this.onHistoryChanged(token);\n            var h = new __History_History();\n            h.onHistoryChanged(token);\n        }\n\n        $wnd.setTimeout('__checkHistory()', 250);\n    };\n\n    // Kick off the timer.\n    $wnd.__checkHistory();\n\n    return true;\n    ")


historyListeners = []
init()

class History:
    """
        Simple History management class for back/forward button support.
        
        This class allows your AJAX application to use a history.  Each time you
        call newItem(), a new item is added to the history and the history
        listeners are notified.  If the user clicks the browser's forward or back 
        buttons, the appropriate item (a string passed to newItem) is fetched
        from the history and the history listeners are notified.
        
        The address bar of the browser contains the current token, using 
        the "#" seperator (for implementation reasons, not because we love 
        the # mark).
        
        You may want to check whether the hash already contains a history
        token when the page loads and use that to show appropriate content;
        this allows users of the site to store direct links in their
        bookmarks or send them in emails.
        
        To make this work properly in all browsers, you must add a specially
        named iframe to your html page, like this:
        
        <iframe id='__pygwt_historyFrame' style='width:0;height:0;border:0'></iframe>
    """

    def addHistoryListener(self, listener):
        global historyListeners
        historyListeners.append(listener)

    def back(self):
        JS('\n        $wnd.history.back();\n        ')

    def forward(self):
        JS('\n        $wnd.history.forward();\n        ')

    def getToken(self):
        global historyToken
        return historyToken
        JS('\n        return $wnd.__historyToken;\n        ')

    def newItem(self, historyToken):
        print 'History - new item', historyToken
        self.onHistoryChanged(historyToken)
        return
        JS('\n        if(historyToken == "" || historyToken == null){\n            historyToken = "#";\n        }\n        $wnd.location.hash = encodeURIComponent(historyToken);\n        ')

    def onHistoryChanged(self, historyToken):
        self.fireHistoryChangedImpl(historyToken)

    def fireHistoryChangedAndCatch(self):
        pass

    def fireHistoryChangedImpl(self, historyToken):
        for listener in historyListeners:
            listener.onHistoryChanged(historyToken)

    def removeHistoryListener(self, listener):
        historyListeners.remove(listener)