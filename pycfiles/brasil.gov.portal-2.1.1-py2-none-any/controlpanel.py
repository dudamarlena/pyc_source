# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/plone/controlpanel.py
# Compiled at: 2018-10-18 17:35:13
from plone.app.controlpanel.overview import OverviewControlPanel as ControlPanelView
import pkg_resources

class OverviewControlPanel(ControlPanelView):

    def portal_padrao_version(self):
        u"""Retorna versão do Portal Padrão
        """
        get_dist = pkg_resources.get_distribution
        return get_dist('brasil.gov.portal').version

    def version_overview(self):
        u"""Lista versões de produtos instalados
        """
        versions = super(OverviewControlPanel, self).version_overview()
        versions.insert(0, ('Portal Padrão {0}').format(self.portal_padrao_version()))
        return versions