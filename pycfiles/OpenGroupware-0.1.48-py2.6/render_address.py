# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_address.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *

def render_addresses(entity, ctx):
    """'
        {'city': '',
         'companyObjectId': 10160,
         'country': '',
         'entityName': 'address',
         'name1': '',
         'name2': '',
         'name3': '',
         'objectId': 10210,
         'state': '',
         'street': '',
         'type': 'location',
         'district': '9',
         'zip': ''}
    """
    if ctx.user_agent_description['omphalos']['associativeLists']:
        result = {}
    else:
        result = []
    if hasattr(entity, 'addresses'):
        for address in entity.addresses.values():
            tmp = {'entityName': 'address', 'objectId': address.object_id, 
               'city': as_string(address.city), 
               'name1': as_string(address.name1), 
               'name2': as_string(address.name2), 
               'name3': as_string(address.name3), 
               'street': as_string(address.street), 
               'companyObjectId': as_integer(entity.object_id), 
               'state': as_string(address.province), 
               'country': as_string(address.country), 
               'type': as_string(address.kind), 
               'district': as_string(address.district), 
               'zip': as_string(address.postal_code)}
            if ctx.user_agent_description['omphalos']['associativeLists']:
                result[address.kind] = tmp
            else:
                result.append(tmp)

    return result


def render_telephones(entity, ctx):
    """""
    {'companyObjectId': 10100,
                      'entityName': 'telephone',
                      'info': '',
                      'number': '',
                      'objectId': 10170,
                      'realNumber': '',
                      'type': '02_tel',
                      'url': ''}
    """
    if ctx.user_agent_description['omphalos']['associativeLists']:
        result = {}
    else:
        result = []
    for telephone in entity.telephones.values():
        tmp = {'entityName': 'telephone', 'objectId': telephone.object_id, 
           'info': as_string(telephone.info), 
           'companyObjectId': as_integer(entity.object_id), 
           'number': as_string(telephone.number), 
           'realNumber': '', 
           'type': telephone.kind, 
           'url': ''}
        if ctx.user_agent_description['omphalos']['associativeLists']:
            result[telephone.kind] = tmp
        else:
            result.append(tmp)

    return result


def render_projects(entity, ctx):
    """
        {'entityName': 'assignment',
         'objectId': 11400,
         'sourceEntityName': 'Contact',
         'sourceObjectId': 10100,
         'targetEntityName': 'Project',
         'targetObjectId': 11360}
    """
    result = []
    if hasattr(entity, 'projects'):
        tm = ctx.type_manager
        for assignment in entity.projects:
            result.append({'objectId': assignment.object_id, 'sourceEntityName': entity.__entityName__, 
               'sourceObjectId': entity.object_id, 
               'targetEntityName': 'Project', 
               'targetObjectId': assignment.parent_id, 
               'entityName': 'assignment'})

    return result


def render_enterprises(entity, ctx):
    """
        {'entityName': 'assignment',
         'objectId': 11400,
         'sourceEntityName': 'Contact',
         'sourceObjectId': 10100,
         'targetEntityName': 'Project',
         'targetObjectId': 11360}
    """
    result = []
    if hasattr(entity, 'enterprises'):
        tm = ctx.type_manager
        for assignment in entity.enterprises:
            if tm.get_type(assignment.parent_id) == 'Enterprise':
                result.append({'entityName': 'assignment', 'objectId': assignment.object_id, 
                   'sourceEntityName': 'Enterprise', 
                   'sourceObjectId': assignment.parent_id, 
                   'targetEntityName': 'Contact', 
                   'targetObjectId': assignment.child_id})

    return result


def render_contacts(entity, ctx):
    """
        {'entityName': 'assignment',
         'objectId': 11400,
         'sourceEntityName': 'Contact',
         'sourceObjectId': 10100,
         'targetEntityName': 'Project',
         'targetObjectId': 11360}
    """
    result = []
    if hasattr(entity, 'contacts'):
        tm = ctx.type_manager
        for assignment in entity.contacts:
            if tm.get_type(assignment.child_id) == 'Contact':
                result.append({'objectId': assignment.object_id, 'entityName': 'assignment', 
                   'sourceEntityName': entity.__entityName__, 
                   'sourceObjectId': assignment.parent_id, 
                   'targetEntityName': 'Contact', 
                   'targetObjectId': assignment.child_id})

    return result


def render_company_values(entity, ctx):
    """""
    {'attribute': 'receive_mail',
                     'companyObjectId': 10100,
                     'entityName': 'companyValue',
                     'label': 'Willing To Recieve Mail',
                     'objectId': 4937930,
                     'type': 2,
                     'uid': '',
                     'value': 'YES'}
    """
    values = {}
    for company_value in entity.company_values.values():
        if company_value.uid is None:
            uid = ''
        else:
            uid = company_value.uid
        if company_value.widget == 9:
            if company_value.string_value is None:
                c_value = []
            else:
                c_value = company_value.string_value.split(',')
        else:
            c_value = as_string(company_value.string_value)
        values[company_value.name] = {'entityName': 'companyValue', 'objectId': company_value.object_id, 
           'companyObjectId': entity.object_id, 
           'label': as_string(company_value.label), 
           'type': as_integer(company_value.widget), 
           'uid': uid, 
           'value': c_value, 
           'attribute': as_string(company_value.name)}

    sd = ServerDefaultsManager()
    if isinstance(entity, Enterprise):
        attr_list = sd.default_as_list('SkyPublicExtendedEnterpriseAttributes')
        attr_list.extend(sd.default_as_list('SkyPrivateExtendedEnterpriseAttributes'))
    elif isinstance(entity, Contact):
        attr_list = sd.default_as_list('SkyPublicExtendedPersonAttributes')
        attr_list.extend(sd.default_as_list('SkyPrivateExtendedPersonAttributes'))
    else:
        raise CoilsException('Cannot render company values on a non-company entity.')
    if ctx.user_agent_description['omphalos']['associativeLists']:
        result = {}
    else:
        result = []
    for attr in attr_list:
        if attr['key'] in values:
            if len(values[attr['key']]['label']) == 0:
                values[attr['key']]['label'] = attr.get('label', '')
            if ctx.user_agent_description['omphalos']['associativeLists']:
                result[values[attr['key']]['attribute']] = values[attr['key']]
            else:
                result.append(values[attr['key']])

    return result