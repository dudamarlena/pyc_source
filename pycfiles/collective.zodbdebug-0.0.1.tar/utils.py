# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/zodbbrowser/utils.py
# Compiled at: 2011-09-30 16:33:48
import transaction
from Products.Five import BrowserView

class DoomedBrowserView(BrowserView):
    """ A browser view that calls transaction.doom() when it is initialized.
    
    This is useful for browser views that shouldn't be able to commit a transaction
    to the database no matter what.
    """

    def __init__(self, context, request):
        transaction.doom()
        super(DoomedBrowserView, self).__init__(context, request)