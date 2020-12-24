# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/cms_plugins.py
# Compiled at: 2018-03-26 19:55:32
# Size of source mod 2**32: 384 bytes
from django.utils.translation import ugettext_lazy as _
from danceschool.core.registries import plugin_templates_registry, PluginTemplateBase

@plugin_templates_registry.register
class VoucherStatsTemplate(PluginTemplateBase):
    template_name = 'stats/schoolstats_voucherusage.html'
    plugin = 'StatsGraphPlugin'
    description = _('Statistics on Usage of Vouchers')