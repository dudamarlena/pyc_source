# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/accordion.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a component similar to a TabSheet, but with a vertical orientation.
"""
from muntjac.ui.tab_sheet import TabSheet

class Accordion(TabSheet):
    """An accordion is a component similar to a L{TabSheet}, but
    with a vertical orientation and the selected component presented
    between tabs.

    Closable tabs are not supported by the accordion.

    The L{Accordion} can be styled with the .v-accordion, .v-accordion-item,
    .v-accordion-item-first and .v-accordion-item-caption styles.

    @see: L{TabSheet}
    """
    CLIENT_WIDGET = None