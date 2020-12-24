# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bu_cascade/cascade_connector.py
# Compiled at: 2019-11-06 14:43:10
# Size of source mod 2**32: 8582 bytes
from suds.client import Client
from suds.sudsobject import asdict
from suds.transport import TransportError
import copy, html
from bs4 import BeautifulStoneSoup
import cgi
from bu_cascade.asset_tools import convert_asset

class Cascade(object):

    def __init__(self, service_url, login, site_id, staging_destination_id):
        self.service_url = service_url
        self.login = login
        self.site_id = site_id
        self.client = self.get_client()
        self.staging_destination_id = staging_destination_id

    def get_client(self):
        try:
            client = Client(url=(self.service_url + '?wsdl'), location=(self.service_url))
            return client
        except TransportError:
            return

    def read(self, path_or_id, asset_type):
        identifier = self.create_identifier(path_or_id, asset_type)
        response = self.client.service.read(self.login, identifier)
        return self.build_asset_structure(response)

    def create(self, asset):
        asset = convert_asset(asset)
        response = self.client.service.create(self.login, asset)
        return response

    def edit(self, asset):
        asset = convert_asset(asset)
        response = self.client.service.edit(self.login, asset)
        return response

    def delete(self, path_or_id, asset_type):
        identifier = self.create_identifier(path_or_id, asset_type)
        response = self.client.service.delete(self.login, identifier)
        return response

    def build_asset_structure(self, asset):
        asset = self.recursive_asdict(asset)
        asset = convert_asset(asset)
        return asset

    def HTMLEntitiesToUnicode(self, text):
        """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
        text = str(BeautifulStoneSoup(text, convertEntities=(BeautifulStoneSoup.ALL_ENTITIES)), 'utf-8')
        return text

    def unicodeToHTMLEntities(self, text):
        """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
        text = html.escape(text).encode('ascii', 'xmlcharrefreplace')
        return text

    def recursive_asdict(self, d):
        from suds.sudsobject import asdict
        out = {}
        if type(d) is not dict:
            d = asdict(d)
        for k, v in d.items():
            if hasattr(v, '__keylist__'):
                out[k] = self.recursive_asdict(v)
            else:
                if isinstance(v, list):
                    out[k] = []
                    for item in v:
                        if hasattr(item, '__keylist__'):
                            out[k].append(self.recursive_asdict(item))
                        else:
                            out[k].append(item)

                else:
                    if v:
                        try:
                            out[k] = v.encode('ascii', 'xmlcharrefreplace')
                        except:
                            out[k] = v

        return out

    def create_identifier(self, path_or_id, asset_type):
        if path_or_id is None:
            return
        else:
            if path_or_id[0] == '/':
                identifier = {'type':asset_type,  'path':{'path':path_or_id, 
                  'siteId':self.site_id}}
            else:
                identifier = {'id':path_or_id, 
                 'type':asset_type}
            return identifier

    def publish(self, path_or_id, asset_type, destination=''):
        identifier = self.create_identifier(path_or_id, asset_type)
        identifier = {'identifier':identifier, 
         'destinations':self.get_destinations_for_string(destination)}
        response = self.client.service.publish(self.login, identifier)
        return response

    def get_groups_for_user(self, username=None):
        if username is None:
            return {}
        else:
            try:
                user = self.read(username, 'user')
                allowed_groups = user['asset']['user']['groups'].decode('utf-8')
            except AttributeError:
                allowed_groups = ''

            return allowed_groups.split(';')

    def unpublish(self, path_or_id, asset_type):
        identifier = self.create_identifier(path_or_id, asset_type)
        identifier = {'identifier':identifier, 
         'unpublish':True}
        response = self.client.service.publish(self.login, identifier)
        return response

    def move(self, old_path_or_id, new_folder_path_or_id, asset_type):
        identifier = self.create_identifier(old_path_or_id, asset_type)
        new_identifier = self.create_identifier(new_folder_path_or_id, 'folder')
        moveParameters = {'destinationContainerIdentifier':new_identifier, 
         'doWorkflow':False, 
         'newName':None}
        response = self.client.service.move(self.login, identifier, moveParameters)
        return response

    def copy(self, old_path_or_id, asset_type, destination_path_or_id, new_name):
        old_identifier = self.create_identifier(old_path_or_id, asset_type)
        destination = self.create_identifier(destination_path_or_id, 'folder')
        copyParameters = {'destinationContainerIdentifier':destination, 
         'doWorkflow':False, 
         'newName':new_name}
        response = self.client.service.copy(self.login, old_identifier, copyParameters)
        return response

    def rename(self, path_or_id, new_name, asset_type):
        identifier = self.create_identifier(path_or_id, asset_type)
        renameParameters = {'doWorkflow':False, 
         'newName':new_name}
        response = self.client.service.move(self.login, identifier, renameParameters)
        return response

    def is_in_workflow(self, path_or_id, asset_type):
        identifier = self.create_identifier(path_or_id, asset_type)
        response = self.client.service.readWorkflowInformation(self.login, identifier)
        if response.workflow is not None:
            if str(response.workflow.currentStep) != 'finish':
                return True
        return False

    def load_base_asset_by_id(self, id, asset_type):
        asset = self.read(id, asset_type)
        if asset_type == 'page':
            asset_specific_key = 'page'
        else:
            if asset_type == 'block':
                asset_specific_key = 'xhtmlDataDefinitionBlock'
            else:
                return
        new_asset = self.build_asset_structure(copy.deepcopy(asset)['asset'])
        new_asset[asset_specific_key]['id'] = None
        new_asset[asset_specific_key]['parentFolderId'] = None
        new_asset[asset_specific_key]['parentFolderPath'] = None
        new_asset[asset_specific_key]['path'] = None
        new_asset[asset_specific_key]['metadata']['author'] = None
        new_asset[asset_specific_key]['metadata']['metaDescription'] = None
        new_asset_md = new_asset[asset_specific_key]['metadata']
        new_asset_sd = new_asset[asset_specific_key]['structuredData']
        return (
         new_asset, new_asset_md, new_asset_sd)

    def get_destinations_for_string(self, destination):
        if destination == 'staging':
            identifier = {'assetIdentifier': {'id':self.staging_destination_id, 
                                 'type':'destination'}}
            return identifier
        else:
            return ''

    def search(self, search_information):
        response = self.client.service.search(self.login, search_information)
        return response

    def list_relationships(self, path_or_id, asset_type):
        identifier = self.create_identifier(path_or_id, asset_type)
        response = self.client.service.listSubscribers(self.login, identifier)
        return response