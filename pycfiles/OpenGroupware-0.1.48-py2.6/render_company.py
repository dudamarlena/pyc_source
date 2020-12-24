# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/vcard/render_company.py
# Compiled at: 2012-10-12 07:02:39
import vobject

def _is_none(v):
    if v is None:
        return ''
    else:
        return str(v)
        return


def render_address(card, addresses, ctx, **params):
    for address in addresses.values():
        if address.kind in ctx.user_agent_description['vcard']['adrTypeMap']:
            kind = ctx.user_agent_description['vcard']['adrTypeMap'][address.kind]['types']
            adr = card.add('adr')
            adr.value = vobject.vcard.Address(street=_is_none(address.street), city=_is_none(address.city), region=_is_none(address.province), code=_is_none(address.postal_code), country=_is_none(address.country), box='', extended=_is_none(address.name1))
            adr.type_paramlist = kind
            if ctx.user_agent_description['vcard']['setCoilsTypeInAdr']:
                adr.x_coils_address_type_param = address.kind


def render_telephones(card, phones, ctx, **params):
    for phone in phones.values():
        if phone.kind in ctx.user_agent_description['vcard']['telTypeMap']:
            kind = ctx.user_agent_description['vcard']['telTypeMap'][phone.kind]['types']
            if ctx.user_agent_description['vcard']['telTypeMap'][phone.kind]['voice'] and ctx.user_agent_description['vcard']['setVoiceAttrInTel']:
                kind.append('voice')
            tel = card.add('tel')
            tel.value = _is_none(phone.number)
            tel.type_paramlist = kind
            if ctx.user_agent_description['vcard']['setCoilsTypeInTel']:
                tel.x_coils_tel_type_param = phone.kind


def render_company_values(card, values, ctx, **params):
    for (name, cv) in values.items():
        if name in ('email1', 'email2', 'email3') and cv.string_value is not None and len(cv.string_value):
            e = card.add('email')
            e.value = cv.string_value
            kind = []
            prop = ctx.property_manager.get_property(cv, 'http://coils.opengroupware.us/logic', 'xattr01')
            if prop is None:
                e.x_evolution_ui_slot_param = '0'
            else:
                xattr = prop.get_value()
                if xattr is not None and len(xattr) > 2 and xattr[0:2] == '1:':
                    slot = xattr.split(':')[1]
                    if slot != '0':
                        e.x_evolution_ui_slot_param = slot
                    kinds = xattr.split(':')[2].split(',')
                    for _kind in kinds:
                        if len(_kind) > 0:
                            kind.append(_kind)

            if len(kind) > 0:
                e.type_param = kind
        elif name == 'job_title' and cv.string_value is not None and len(cv.string_value):
            card.add('title').value = cv.string_value
        elif ctx.user_agent_description['vcard']['includeCompanyValues']:
            value = None
            if cv.string_value is not None:
                if len(cv.string_value) > 0:
                    value = cv.string_value
            elif cv.integer_value is not None:
                value = str(cv.integer_value)
            if value is not None:
                x = card.add('x-coils-company-value-%s' % cv.name)
                x.value = value
                x.x_coils_company_value_widget_param = str(cv.widget)
                if cv.label is not None:
                    x.x_coils_company_value_label_param = cv.label

    return


def render_properties(card, props, **params):
    for prop in props:
        if prop.namespace not in params['exclude_namespace']:
            value = None
            if value is not None:
                x = card.add('x-coils-property-%s' % prop.name)
                x.value = prop.get_value()
                x.x_coils_property_namespace_param = prop.namespace

    return