# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/vcard/parse_vcard.py
# Compiled at: 2012-10-12 07:02:39
import datetime, re, vobject
from utility import determine_ogo_tel_type_from_caldav_type

def take_integer_value(values, key, name, vcard, default=None):
    key = key.replace('-', '_')
    if hasattr(vcard.key):
        try:
            values[name] = int(getattr(vcard, key).value)
        except:
            values[name] = default


def take_string_value(values, key, name, vcard, default=None):
    key = key.replace('-', '_')
    if hasattr(vcard.key):
        try:
            values[name] = str(getattr(vcard, key).value)
        except:
            values[name] = default


def determine_adr_type(attributes, **params):
    entity_name = params.get('entity_name', 'Contact')
    if 'X-COILS-ADDRESS-TYPE' in attributes:
        return attributes['X-COILS-ADDRESS-TYPE'][0]
    else:
        if 'TYPE' in attributes:
            if entity_name == 'Contact':
                if 'home' in attributes:
                    return 'private'
                else:
                    if 'work' in attributes:
                        return 'mailing'
                    return 'location'
            elif entity_name == 'Enterprise':
                raise NotImplementedException()
            else:
                if entity_name == 'Team':
                    return
                raise CoilException('Unknown vCard to entity correspondence')
        else:
            raise CoilsException('Cannot parse vCard; address with no type')
        return


def parse_vcard(card, ctx, log, **params):
    entity_name = params.get('entity_name', 'Contact')
    if entity_name not in ('Contact', 'Enterprise'):
        raise CoilsException('Parsing to this kind of entity not supported.')
    values = {}
    emails = []
    for line in card.lines():
        if line.name == 'UID':
            if line.value[:8] == 'coils://':
                if entity_name == 'Contact' and line.value[:16] == 'coils://Contact/' and line.value[16:].isdigit():
                    values['objectId'] = int(line.value[16:])
                elif entity_name == 'Enterprise' and line.value[:19] == 'coils://Enterprise/' and line.value[19:].isdigit():
                    values['objectId'] = int(line.value[19:])
                elif entity_name == 'Team' and line.value[:13] == 'coils://Team/' and line.value[13:].isdigit():
                    values['objectId'] = int(line.value[13:])
                else:
                    log.warn(('Corrupted COILS UID String: {0}').format(line.value))
            else:
                log.debug(('vCard UID not a COILS id: {0}').format(line.value))
        elif line.name == 'ADR':
            kind = determine_adr_type(line.params, **params)
            if kind is not None:
                if '_ADDRESSES' not in values:
                    values['_ADDRESSES'] = []
                address = {'type': kind}
                address['name1'] = line.value.extended
                address['city'] = line.value.city
                address['postalCode'] = line.value.code
                address['country'] = line.value.country
                address['state'] = line.value.region
                address['street'] = line.value.street
                values['_ADDRESSES'].append(address)
        elif line.name == 'X-JABBER':
            values['imAddress'] = line.value
        elif line.name == 'TITLE':
            if '_COMPANYVALUES' not in values:
                values['_COMPANYVALUES'] = []
            values['_COMPANYVALUES'].append({'attribute': 'job_title', 'value': line.value})
        elif line.name == 'TEL':
            if '_PHONES' not in values:
                values['_PHONES'] = []
            telephone = {'type': None}
            if 'TYPE' in line.params:
                telephone['caldav_types'] = [ x.upper() for x in line.params['TYPE'] ]
            if 'X-COILS-TEL-TYPE' in line.params:
                telephone['type'] = line.params['X-COILS-TEL-TYPE'][0]
            elif 'caldav_types' in telephone:
                telephone['type'] = determine_ogo_tel_type_from_caldav_type(telephone)
            if not telephone['type']:
                raise CoilsException('Cannot parse vCard; telephone with no type')
            telephone['number'] = line.value
            values['_PHONES'].append(telephone)
        elif line.name == 'N':
            values['lastName'] = line.value.family
            values['firstName'] = line.value.given
        elif line.name == 'NICKNAME':
            values['descripion'] = line.value
        elif line.name == 'X-EVOLUTION-FILE-AS':
            values['fileAs'] = line.value
        elif line.name == 'X-EVOLUTION-MANAGER':
            values['managersname'] = line.value
        elif line.name == 'X-EVOLUTION-ASSISTANT':
            values['assistantName'] = line.value
        elif line.name == 'X-EVOLUTION-SPOUSE':
            pass
        elif line.name == 'X-EVOLUTION-ANNIVERSARY':
            pass
        elif line.name == 'ROLE':
            values['occupation'] = line.value
        elif line.name == 'BDAY':
            pass
        elif line.name == 'CALURL':
            pass
        elif line.name == 'FBURL':
            values['comment'] = line.value
        elif line.name == 'NOTE':
            pass
        elif line.name == 'CATEGORIES':
            pass
        elif line.name == 'CLASS':
            pass
        elif line.name == 'ORG':
            values['associatedcompany'] = line.value[0]
            if len(line.value) > 1:
                values['department'] = line.value[1]
            if len(line.value) > 2:
                values['office'] = line.value[2]
        elif line.name == 'EMAIL':
            emails.append({'value': line.value, 'slot': int(line.params.get('X-EVOLUTION-UI-SLOT', [0])[0]), 
               'types': line.params.get('TYPE', [])})
        elif line.name == 'FN':
            pass
        elif line.name[:22] == 'X-COILS-COMPANY-VALUE-':
            attribute = line.name[22:].lower().replace('-', '_')
            if len(attribute) > 0:
                if '_COMPANYVALUES' not in values:
                    values['_COMPANYVALUES'] = []
                values['_COMPANYVALUES'].append({'attribute': attribute, 'value': line.value})
        else:
            log.debug(('unprocessed vcard attribute {0}').format(line.name))

    if len(emails) > 0:
        if '_COMPANYVALUES' not in values:
            values['_COMPANYVALUES'] = []
        count = 1
        for email in emails:
            values['_COMPANYVALUES'].append({'attribute': ('email{0}').format(count), 'value': email['value'], 
               'xattr': ('1:{0}:{1}:').format(email['slot'], (',').join(email['types']))})
            count += 1
            if count == 4:
                break

    if 'objectId' not in values:
        if len(emails) == 0:
            log.debug('No e-mail address provided in vCard, cannot attempt identification via e-mail search')
        else:
            for email in emails:
                x = ctx.run_command('contact::search', criteria=[
                 {'key': 'email1', 'value': email['value']}])
                if len(x) == 0:
                    log.debug('Unable to identify contact via e-mail search: no candidates')
                elif len(x) == 1:
                    object_id = x[0].object_id
                    log.debug(('Identified vCard via e-mail search result; objectId = {0}').format(object_id))
                    values['objectId'] = object_id
                    break
                else:
                    log.debug('Unable to identify contact via e-mail search: too many candidates')
            else:
                log.debug('Identification of vCard via e-mail search failed.')
    return values