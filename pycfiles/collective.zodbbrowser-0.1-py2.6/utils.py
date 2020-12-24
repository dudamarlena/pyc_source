# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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