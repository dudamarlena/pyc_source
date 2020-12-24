# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bu_cascade/asset_tools.py
# Compiled at: 2020-04-03 15:18:25
# Size of source mod 2**32: 14758 bytes
from copy import *
import datetime
from xml.etree import ElementTree

def update(search_list, key, value):
    returned_search_list = find(search_list, key, True)
    if type(returned_search_list) == list:
        returned_search_list = returned_search_list[0]
    else:
        if type(value) == list:
            parent_element = __search_for_element__(search_list, key, True)
            if parent_element is not None:
                new_elements = []
                if len(value) == 0:
                    temp_element = deepcopy(find(parent_element, key))
                    temp_element = clear_element_values(temp_element)
                    new_elements.append(temp_element)
                else:
                    for single_value in value:
                        new_elements.append(deepcopy(update(parent_element, key, single_value)))

                indexes_to_remove = []
                for index, element in enumerate(parent_element):
                    if 'name' in element and element['name'] == key:
                        indexes_to_remove.append(index)
                    else:
                        if 'identifier' in element and element['identifier'] == key:
                            indexes_to_remove.append(index)

                for index in reversed(indexes_to_remove):
                    del parent_element[index]

                for new_element in new_elements:
                    parent_element.append(new_element)

            return returned_search_list
        else:
            if returned_search_list is None:
                return
            else:
                if 'name' in returned_search_list:
                    if returned_search_list['name'] == key:
                        new_value_array = []
                        if type(value) is list:
                            for child in value:
                                new_value_array.append({'value': child})

                        else:
                            new_value_array.append({'value': value})
                        if 'fieldValues' in returned_search_list:
                            if 'fieldValue' in returned_search_list['fieldValues']:
                                returned_search_list['fieldValues']['fieldValue'] = new_value_array
                        else:
                            returned_search_list['fieldValues'] = {'fieldValue': new_value_array}
                        return returned_search_list
            if key in returned_search_list:
                returned_search_list[key] = value
                return returned_search_list
        if returned_search_list.get('identifier') == key:
            if returned_search_list['type'] == 'text':
                if '::CONTENT-XML-CHECKBOX::' in str(returned_search_list.get('text', '')):
                    content_xml_type = '::CONTENT-XML-CHECKBOX::'
                else:
                    if '::CONTENT-XML-SELECTOR::' in str(returned_search_list.get('text', '')):
                        content_xml_type = '::CONTENT-XML-SELECTOR::'
                    else:
                        content_xml_type = None
                    if type(value) is list:
                        new_value = ''
                        for item in value:
                            new_value += content_xml_type + item

                    else:
                        if content_xml_type:
                            new_value = content_xml_type + value
                        else:
                            new_value = value
                returned_search_list['text'] = new_value
                return returned_search_list
            else:
                if returned_search_list['type'] == 'group':
                    for subkey, subvalue in value.items():
                        update(returned_search_list, subkey, subvalue)

                    return returned_search_list
                if returned_search_list['type'] == 'asset':
                    if value is None:
                        return
                    else:
                        asset_type = returned_search_list['assetType']
                        returned_search_list[asset_type + 'Id'] = ''
                        returned_search_list[asset_type + 'Path'] = ''
                        if '/' in value:
                            returned_search_list[asset_type + 'Path'] = value
                        else:
                            returned_search_list[asset_type + 'Id'] = value
                        return returned_search_list
                return
        else:
            return


def update_metadata_set(search_list, key, value, default=None):
    returned_search_list = __search_for_element__(search_list, key)
    if returned_search_list is None:
        return
    if 'name' in returned_search_list and returned_search_list['name'] == key and 'fieldType' != 'text':
        new_value_array = []
        if type(value) is list:
            for child in value:
                if child == default:
                    new_value_array.append({'value':child,  'selectedByDefault':True})
                else:
                    new_value_array.append({'value': child})

        else:
            if value == default:
                new_value_array.append({'value':value,  'selectedByDefault':True})
            else:
                new_value_array.append({'value': value})
            if 'possibleValues' in returned_search_list:
                if 'possibleValue' in returned_search_list['possibleValues']:
                    returned_search_list['possibleValues']['possibleValue'] = new_value_array
            returned_search_list['possibleValues'] = {'possibleValue': new_value_array}
        return key
    else:
        if key in returned_search_list:
            returned_search_list[key] = value
            return key
        return


def update_data_definition(search_xml, key, value, default=None):
    return_key = False
    if 'dataDefinition' in search_xml:
        xml = search_xml['dataDefinition']['xml']
    else:
        return
    search_xml_in_json = ElementTree.fromstring(xml)
    for child in search_xml_in_json.findall('.//text'):
        if child.get('identifier') == key:
            if child.get('type') == 'checkbox':
                field_type = 'checkbox-item'
            else:
                if child.get('type') == 'dropdown':
                    field_type = 'dropdown-item'
                else:
                    if child.get('type') == 'radiobutton':
                        field_type = 'radio-item'
                    elif child.get('type') == 'multi-selector':
                        field_type = 'selector-item'
                    else:
                        continue
                indexes_to_remove = []
                for index, element in enumerate(child):
                    indexes_to_remove.append(element)

                for element in indexes_to_remove:
                    child.remove(element)

                for index, single_value in enumerate(value):
                    if single_value == default:
                        child.append(ElementTree.Element(field_type, {'value':single_value.replace(' & ', ' &amp; '),  'selectedByDefault':True}))
                    else:
                        child.append(ElementTree.Element(field_type, {'value': single_value.replace(' & ', ' &amp; ')}))

                return_key = True
                break

    if return_key:
        search_xml['dataDefinition']['xml'] = ElementTree.tostring(search_xml_in_json)
        return key
    else:
        return


def find(search_list, key, return_full_element=True):
    returned_search_list = __search_for_element__(search_list, key)
    if return_full_element:
        return returned_search_list
    else:
        array_to_return = []
        element = returned_search_list
        if hasattr(element, 'keys'):
            if key in element.keys():
                array_to_return.append(element[key])
        try:
            if 'fieldValues' in element:
                temp_array = []
                for item in element['fieldValues']['fieldValue']:
                    temp_array.append(item['value'])

                array_to_return.append(temp_array)
            else:
                if element['type'] == 'text':
                    if '::CONTENT-XML-CHECKBOX::' in str(element['text']):
                        value_of_text = str(element['text']).split('::CONTENT-XML-CHECKBOX::')
                    else:
                        if '::CONTENT-XML-SELECTOR::' in str(element['text']):
                            value_of_text = str(element['text']).split('::CONTENT-XML-SELECTOR::')
                        else:
                            value_of_text = str(element['text'])
                        if len(value_of_text) == 0:
                            pass
                        else:
                            if len(value_of_text) == 1:
                                array_to_return.append(value_of_text[0])
                            else:
                                array_to_return.append(value_of_text)
                else:
                    if element['type'] == 'group':
                        array_to_return.append(element['structuredDataNodes']['structuredDataNode'])
                    else:
                        if element['type'] == 'asset':
                            array_to_return.append(element)
                        else:
                            print('ERROR: need to add more checks here!')
                            print(element)
        except:
            pass

        return __return_formated_array__(array_to_return)


def __search_for_element__(search_list, key, find_parent_element=False):
    if hasattr(search_list, 'keys'):
        if key in search_list.keys():
            return search_list
        if hasattr(search_list, 'keys'):
            if 'name' in search_list.keys():
                if search_list['name'] == key:
                    return search_list
    else:
        if hasattr(search_list, 'get'):
            if search_list.get('identifier') == key:
                return search_list
    found_array = []
    for child in search_list:
        if hasattr(child, 'keys'):
            if key in child.keys():
                if find_parent_element:
                    return search_list
                else:
                    return child
            if hasattr(child, 'keys'):
                if 'name' in child.keys():
                    if child['name'] == key:
                        if find_parent_element:
                            return search_list
                        else:
                            return child
            else:
                if hasattr(child, 'get'):
                    if child.get('identifier') == key:
                        if find_parent_element:
                            return search_list
                        return child
                if hasattr(search_list, 'get'):
                    if type(search_list.get(child)) == dict:
                        found = __search_for_element__(search_list.get(child), key, find_parent_element)
                        if found:
                            if find_parent_element:
                                return found
                            found_array.append(found)
                    elif type(search_list.get(child)) == list:
                        for item in search_list.get(child):
                            found = __search_for_element__(item, key, find_parent_element)
                            if found:
                                if find_parent_element:
                                    return search_list.get(child)
                                found_array.append(found)

    return __return_formated_array__(found_array)


def __return_formated_array__(array):
    if len(array) == 0:
        return
    else:
        if len(array) == 1:
            return array[0]
        return array


def clear_element_values(element):
    if 'type' in element and element.get('type') == 'group':
        parent_element = element['structuredDataNodes']['structuredDataNode']
        for child in parent_element:
            if 'text' in child:
                child['text'] = ''
            elif 'type' in child and child.get('type') == 'asset':
                asset_type = child.get('assetType')
                child[asset_type + 'Id'] = ''
                child[asset_type + 'Path'] = ''
            else:
                if 'type' in child and child.get('type') == 'group':
                    child = clear_element_values(child)

        return element
    else:
        if 'fieldValues' in element:
            element['fieldValues']['fieldValue'] = []
            element['fieldValues']['fieldValue'].append({'value': ''})
            return element
        return


def convert_asset(data):
    if isinstance(data, bytes):
        return data.decode()
    else:
        if isinstance(data, bool) or isinstance(data, datetime.date):
            return data
        else:
            if isinstance(data, (str, int)):
                return str(data)
            else:
                if isinstance(data, dict):
                    return dict(map(convert_asset, data.items()))
                if isinstance(data, tuple):
                    return tuple(map(convert_asset, data))
            if isinstance(data, list):
                return list(map(convert_asset, data))
        if isinstance(data, set):
            return set(map(convert_asset, data))