# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/xml/render.py
# Compiled at: 2012-10-12 07:02:39
import logging, StringIO
from datetime import datetime, date
from coils.foundation.api import elementflow
from coils.core import *
from coils.core.omphalos import Render as Omphalos

class Render(object):

    @staticmethod
    def render(entity, ctx, detail_level=None, stream=None):
        if detail_level is None:
            detail_level = 65503
        if stream:
            stringify_result = False
        else:
            stream = StringIO.StringIO()
            stringify_result = True
        namespaces = {'': 'http://www.opengroupware.us/model'}
        if isinstance(entity, list):
            with elementflow.xml(stream, 'ResultSet', namespaces=namespaces) as (xml):
                for x in entity:
                    with xml.container('entity', attrs={'entityname': x.__entityName__, 'objectid': unicode(x.object_id)}):
                        Render._render_entity(x, ctx, xml=xml, detail_level=detail_level)

        else:
            with elementflow.xml(stream, 'entity', attrs={'entityname': entity.__entityName__, 'objectid': unicode(entity.object_id)}, namespaces=namespaces) as (xml):
                Render._render_entity(entity, ctx, xml=xml, detail_level=detail_level)
        if stringify_result:
            data = stream.getvalue()
            stream.close()
            return data
        else:
            return
            return

    @staticmethod
    def _render_entity(entity, ctx):
        Render.render(entity, ctx, {})

    @staticmethod
    def _render_entity(entity, ctx, detail_level=65503, xml=None):

        def render_value(xml, value):
            if isinstance(value, list):
                with xml.container('value', attrs={'datatype': 'list'}):
                    for entry in value:
                        with xml.container('item'):
                            render_value(xml, entry)

            elif isinstance(value, dict):
                with xml.container('value', attrs={'datatype': 'dict'}):
                    for (k, v) in value.items():
                        render_key_value(xml, k, v)

            elif isinstance(value, datetime):
                with xml.container('value', attrs={'datatype': 'datetime'}):
                    xml.text(value.strftime('%Y-%m-%dT%H:%M:%s'))
            elif isinstance(value, date):
                with xml.container('value', attrs={'datatype': 'date'}):
                    xml.text(value.strftime('%Y-%m-%d'))
            elif isinstance(value, basestring):
                if value:
                    with xml.container('value', attrs={'datatype': 'string'}):
                        xml.text(unicode(value))
            elif isinstance(value, integer):
                with xml.container('value', attrs={'datatype': 'integer'}):
                    xml.text(unicode(value))
            elif not value:
                pass

        def render_key_value(xml, key, value):
            key = key.lower()
            key = key if not key.isdigit() else ('id{0}').format(key)
            if isinstance(value, list):
                with xml.container(key, attrs={'datatype': 'list'}):
                    for entry in value:
                        with xml.container('item'):
                            render_value(xml, entry)

            elif isinstance(value, dict):
                with xml.container(key):
                    for (k, v) in value.items():
                        render_key_value(xml, k, v)

            elif isinstance(value, basestring):
                xml.element(key, text=unicode(value), attrs={'dataType': 'string'})
            elif isinstance(value, int) or isinstance(value, long):
                xml.element(key, text=unicode(value), attrs={'dataType': 'integer'})
            elif isinstance(value, datetime):
                xml.element(key, text=value.strftime('%Y-%m-%dT%H:%M:%s'), attrs={'dataType': 'datetime'})
            elif isinstance(value, date):
                xml.element(key, text=value.strftime('%Y-%m-%d'), attrs={'dataType': 'date'})
            else:
                raise CoilsException(('Data type "{0}" cannot be encoded for value of {1}').format(type(value), key))

        omphalos = Omphalos.Result(entity, detail_level, ctx)
        if '_PROPERTIES' in omphalos:
            with xml.container('objectproperties'):
                for prop in omphalos['_PROPERTIES']:
                    label = prop['label'] if prop['label'] else prop['attribute']
                    with xml.container('objectproperty', attrs={'attribute': prop['attribute'], 'namespace': prop['namespace'], 
                       'parentid': unicode(prop['parentObjectId'])}):
                        render_value(xml, prop['value'])

        if '_COMPANYVALUES' in omphalos:
            with xml.container('companyvalues'):
                for cv in omphalos['_COMPANYVALUES']:
                    label = cv['label'] if cv['label'] else cv['attribute']
                    if cv['type'] == 1:
                        hint = 'string'
                    elif cv['type'] == 2:
                        hint = 'checkbox'
                    elif cv['type'] == 3:
                        hint = 'email'
                    elif cv['type'] == 9:
                        hint = 'multiselect'
                    else:
                        hint = 'string'
                    with xml.container('companyvalue', attrs={'attribute': cv['attribute'], 'label': label, 
                       'uihint': hint, 
                       'objectId': str(cv['objectId']), 
                       'parentId': str(cv['companyObjectId'])}):
                        render_value(xml, cv['value'])

        if '_PHONES' in omphalos:
            with xml.container('phones'):
                for phone in omphalos['_PHONES']:
                    info = phone['info'] if phone['info'] else ''
                    with xml.container('phone', attrs={'kind': phone['type'], 'info': info, 
                       'objectid': str(phone['objectId']), 
                       'parentid': str(phone['companyObjectId'])}):
                        if phone['number']:
                            xml.text(phone['number'])

        if '_ADDRESSES' in omphalos:
            with xml.container('addresses'):
                for address in omphalos['_ADDRESSES']:
                    with xml.container('addresses', attrs={'kind': address['type'], 'objectId': str(address['objectId']), 
                       'parentId': str(address['companyObjectId'])}):
                        xml.element('city', text=address['city'])
                        xml.element('country', text=address['country'])
                        xml.element('name1', text=address['name1'])
                        xml.element('name2', text=address['name2'])
                        xml.element('name3', text=address['name3'])
                        xml.element('state', text=address['state'])
                        xml.element('street', text=address['street'])
                        xml.element('district', text=address['district'])
                        xml.element('zip', text=address['zip'])

        if '_CONTACTS' in omphalos:
            with xml.container('assignedcontacts'):
                for assignment in omphalos['_CONTACTS']:
                    xml.element('contactid', text=unicode(assignment['targetObjectId']), attrs={'objectid': unicode(assignment['objectId'])})

        if '_ENTERPRISES' in omphalos:
            with xml.container('assignedenterprises'):
                for assignment in omphalos['_ENTERPRISES']:
                    xml.element('enterpriseid', text=unicode(assignment['targetObjectId']), attrs={'objectid': unicode(assignment['objectId'])})

        for (k, v) in omphalos.items():
            if not k[0:1] == '_' and k != 'FLAGS':
                render_key_value(xml, k, v)