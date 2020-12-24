# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matthew/Documents/rets/env/lib/python3.8/site-packages/rets/parsers/metadata.py
# Compiled at: 2020-05-12 16:30:24
# Size of source mod 2**32: 4931 bytes
import logging, xmltodict
from rets.exceptions import ParseError
from .base import Base
logger = logging.getLogger('rets')

class CompactMetadata(Base):
    __doc__ = 'Parses COMPCACT-DECODED RETS responses'

    def parse(self, response, metadata_type):
        """
        Parses RETS metadata using the COMPACT-DECODED format
        :param response:
        :param metadata_type:
        :return:
        """
        xml = xmltodict.parse(response.text)
        self.analyze_reply_code(xml_response_dict=xml)
        base = xml.get('RETS', {}).get(metadata_type, {})
        attributes = self.get_attributes(base)
        if base.get('System') or base.get('SYSTEM'):
            system_obj = {}
            if base.get('SYSTEM', {}).get('@SystemDescription'):
                system_obj['system_id'] = str(base['SYSTEM']['@SystemID'])
            if base.get('SYSTEM', {}).get('@SystemDescription'):
                system_obj['system_description'] = str(base['SYSTEM']['@SystemDescription'])
            if base.get('SYSTEM', {}).get('@TimeZoneOffset'):
                system_obj['timezone_offset'] = str(base['SYSTEM']['@TimeZoneOffset'])
            if base.get('SYSTEM', {}).get('Comments'):
                system_obj['comments'] = base['SYSTEM']['Comments']
            if base.get('@Version'):
                system_obj['version'] = base['@Version']
            yield system_obj
        else:
            if 'DATA' in base:
                if not isinstance(base['DATA'], list):
                    base['DATA'] = [base['DATA']]
                for data in base['DATA']:
                    data_dict = self.data_columns_to_dict(columns_string=(base.get('COLUMNS', '')),
                      dict_string=data)
                    data_dict.update(attributes)
                    yield data_dict


class StandardXMLMetadata(Base):
    __doc__ = 'Parses STANDARD-XML RETS responses'

    @staticmethod
    def _identify_key(some_dict, some_key):
        key_cap = None
        for k in some_dict.keys():
            if k.lower() == some_key:
                key_cap = k
            else:
                if some_key == 'lookuptype':
                    if k.lower() == 'lookup':
                        key_cap = k
                    if not key_cap:
                        msg = 'Could not find {0!s} in the response XML'.format(some_key)
                        raise ParseError(msg)
                return key_cap

    def parse(self, response, metadata_type):
        """
        Parses RETS metadata using the STANDARD-XML format
        :param response: requests Response object
        :param metadata_type: string
        :return parsed: list
        """
        xml = xmltodict.parse(response.text)
        self.analyze_reply_code(xml_response_dict=xml)
        base = xml.get('RETS', {}).get('METADATA', {}).get(metadata_type, {})
        if metadata_type == 'METADATA-SYSTEM':
            syst = base.get('System', base.get('SYSTEM'))
            if not syst:
                raise ParseError('Could not get the System key from a METADATA-SYSTEM request.')
            system_obj = {}
            if syst.get('SystemID'):
                system_obj['system_id'] = str(syst['SystemID'])
            if syst.get('SystemDescription'):
                system_obj['system_description'] = str(syst['SystemDescription'])
            if syst.get('Comments'):
                system_obj['comments'] = syst['Comments']
            if base.get('@Version'):
                system_obj['version'] = base['@Version']
            return [
             system_obj]
            if metadata_type == 'METADATA-CLASS':
                key = 'class'
        elif metadata_type == 'METADATA-RESOURCE':
            key = 'resource'
        else:
            if metadata_type == 'METADATA-LOOKUP_TYPE':
                key = 'lookuptype'
            else:
                if metadata_type == 'METADATA-OBJECT':
                    key = 'object'
                else:
                    if metadata_type == 'METADATA-TABLE':
                        key = 'field'
                    else:
                        msg = 'Got an unknown metadata type of {0!s}'.format(metadata_type)
                        raise ParseError(msg)
        if isinstance(base, list):
            res = {}
            for i in base:
                key_cap = self._identify_key(i, key)
                res[i['@Lookup']] = i[key_cap]
            else:
                return res

        key_cap = self._identify_key(base, key)
        if isinstance(base[key_cap], list):
            return base[key_cap]
        return [base[key_cap]]