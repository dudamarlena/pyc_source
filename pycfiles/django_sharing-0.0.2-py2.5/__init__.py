# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sharing/__init__.py
# Compiled at: 2010-09-29 05:29:28
import inspect

def admin_mixin_share():
    """
    Apply ShareAdminMixin class to registered admin classes, thus automatically enabling 
    sharing on for all models in admin.
    """
    from django.contrib import admin
    from sharing.admin import ShareAdminMixin
    for (model_class, admin_options) in admin.site._registry.items():
        admin_class = admin_options.__class__
        if ShareAdminMixin in inspect.getmro(admin_class):
            continue
        admin.site.unregister(model_class)
        mixin_admin_class = type('%sShareMixin' % admin_class.__name__, (ShareAdminMixin, admin_class), {'inlines': admin_class.inlines + ShareAdminMixin.inlines})
        admin.site.register(model_class, mixin_admin_class)