# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/cms_toolbars.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 1496 bytes
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.toolbar.items import Break

@toolbar_pool.register
class VoucherLinksToolbar(CMSToolbar):
    __doc__ = ' Add vouchers to the financial menu '

    def populate(self):
        if not (self.request.user.has_perm('vouchers.change_voucher') or self.request.user.has_perm('vouchers.change_vouchercategory')):
            return
        else:
            financial_menu = self.toolbar.get_or_create_menu('financial', _('Finances'))
            position = financial_menu.find_first(Break,
              identifier='financial_related_items_break')
            if not position:
                financial_menu.add_break('financial_related_items_break')
                position = financial_menu.find_first(Break,
                  identifier='financial_related_items_break') + 1
            related_menu = financial_menu.get_or_create_menu('financial-related', (_('Related Items')), position=position)
            if self.request.user.has_perm('vouchers.change_vouchercategory'):
                related_menu.add_link_item((_('Voucher Categories')), url=(reverse('admin:vouchers_vouchercategory_changelist')))
            if self.request.user.has_perm('vouchers.change_voucher'):
                related_menu.add_link_item((_('Vouchers')), url=(reverse('admin:vouchers_voucher_changelist')))