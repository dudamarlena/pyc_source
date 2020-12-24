# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/vcard/render_contact.py
# Compiled at: 2012-10-12 07:02:39
import vobject
from render_company import *

def render_contact(contact, ctx, **params):
    if contact.last_name is None or contact.first_name is None:
        return
    else:
        card = vobject.vCard()
        card.add('n')
        card.n.value = vobject.vcard.Name(family=contact.last_name, given=contact.first_name)
        if contact.file_as is None:
            file_as = '%s, %s' % (contact.last_name, contact.first_name)
        else:
            file_as = contact.file_as
        card.add('fn').value = file_as
        card.add('x-evolution-file-as').value = file_as
        if contact.display_name is not None:
            card.add('nickname').value = contact.display_name
        if contact.im_address is not None:
            card.add('x-jabber').value = contact.im_address
        card.add('uid').value = 'coils://Contact/%d' % contact.object_id
        if contact.associated_company is not None and len(contact.associated_company) > 0 or contact.department is not None and len(contact.department) > 0 or contact.office is not None and len(contact.office) > 0:
            card.add('org').value = [
             contact.associated_company if contact.associated_company is not None else '',
             contact.department if contact.department is not None else '',
             contact.office if contact.office is not None else '']
        if contact.occupation is not None:
            if len(contact.occupation) > 0:
                card.add('role').value = contact.occupation
        if contact.assistant_name is not None:
            if len(contact.assistant_name) > 0:
                card.add('x-assistant').value = contact.assistant_name
                card.add('x-evolution-assistant').value = contact.assistant_name
        if contact.boss_name is not None:
            if len(contact.boss_name) > 0:
                card.add('x-manager').value = contact.boss_name
                card.add('x-evolution-manager').value = contact.boss_name
        if contact.partner_name is not None:
            if len(contact.partner_name) > 0:
                card.add('x-spouse').value = contact.partner_name
                card.add('x-evolution-spouse').value = contact.partner_name
        card.add('x-mozilla-html').value = 'FALSE'
        if contact.keywords is not None:
            if len(contact.keywords) > 0:
                card.add('categories').value = contact.keywords
        card.add('class').value = 'PUBLIC'
        x = card.add('x-coils-account')
        if contact.is_account == 1:
            x.value = 'YES'
            x.x_coils_account_id_param = str(contact.object_id)
            x.x_coils_account_login_param = str(contact.login)
        else:
            x.value = 'NO'
        render_address(card, contact.addresses, ctx)
        render_telephones(card, contact.telephones, ctx)
        render_company_values(card, contact.company_values, ctx)
        pm = ctx.property_manager
        render_properties(card, pm.get_properties(contact), exclude_namespace=[
         'http://coils.opengroupware.us/admin'])
        return str(card.serialize(lineLength=5096))