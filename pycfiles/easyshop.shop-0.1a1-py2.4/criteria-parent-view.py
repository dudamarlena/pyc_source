# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/skins/easyshop_templates/criteria-parent-view.py
# Compiled at: 2008-06-20 09:37:24
url = context.aq_inner.aq_parent.absolute_url()
context.REQUEST.RESPONSE.redirect(url)