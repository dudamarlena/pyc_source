# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/client_criterion.py
# Compiled at: 2013-04-04 15:36:37


class ClientCriterion(object):
    """An annotation type used to point the client side counterpart for server
    side a L{AcceptCriterion} class. Usage is pretty similar to L{ClientWidget}
    which is used with Muntjac components that have a specialized client side
    counterpart.

    Annotations are used at GWT compilation phase, so remember to rebuild your
    widgetset if you do changes for L{ClientCriterion} mappings.
    """
    value = None