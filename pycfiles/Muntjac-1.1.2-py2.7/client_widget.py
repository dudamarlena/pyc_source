# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/client_widget.py
# Compiled at: 2013-04-04 15:36:35


class ClientWidget(object):
    """Annotation defining the default client side counterpart in GWT
    terminal for L{Component}.

    With this annotation server side Muntjac component is marked to have
    a client side counterpart. The value of the annotation is the class
    of client side implementation.

    Note, even though client side implementation is needed during
    development, one may safely remove them from the classpath of the
    production server.
    """

    def __init__(self, widget, loadStyle=None):
        self.widget = widget
        if loadStyle is None:
            self.loadStyle = LoadStyle.DEFERRED
        else:
            self.loadStyle = loadStyle
        return


class LoadStyle(object):
    EAGER = 'EAGER'
    DEFERRED = 'DEFERRED'
    LAZY = 'LAZY'