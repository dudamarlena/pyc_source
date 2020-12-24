# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/cycle_templates/cycle.py
# Compiled at: 2011-10-12 13:31:11
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from ageliaco.rd import ICycle, IAttribution, ICycles
import datetime

class CycleForm(grok.AddForm):
    grok.context(ICycles)
    form_fields = grok.AutoFields(Cycle)
    label = "Création d'un cycle annuel d'administration"
    grok.require('zope2.View')

    @grok.action("Ajout d'un cycle")
    def add(self, **data):
        cycle = Cycle()
        nb_cycles = len(self.context)
        projet = self.context.ac_parent
        cycle.year = str(datetime.datetime.today().year)
        cycle.id = cycle.year
        if nb_cycle == 0:
            cycle.title = 'Initial'
            cycle.contributors = projet.contributors
        self.context[cycle.id] = cycle
        return self.redirect(self.url(self.context[cycle.id]))