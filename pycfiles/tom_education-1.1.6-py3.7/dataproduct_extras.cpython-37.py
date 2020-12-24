# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/templatetags/dataproduct_extras.py
# Compiled at: 2020-04-30 08:35:11
# Size of source mod 2**32: 551 bytes
from tom_dataproducts.templatetags import dataproduct_extras

@dataproduct_extras.register.inclusion_tag('tom_dataproducts/partials/dataproduct_list_for_target.html', takes_context=True)
def dataproduct_list_for_target(context, target):
    """
    Override the product list for a target so that included template receives
    the whole current context
    """
    target_ctx = dataproduct_extras.dataproduct_list_for_target(target=target, context=context)
    context.update(target_ctx)
    return context