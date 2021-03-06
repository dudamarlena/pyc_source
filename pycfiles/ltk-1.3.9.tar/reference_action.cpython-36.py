# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/actions/reference_action.py
# Compiled at: 2020-04-13 16:05:54
# Size of source mod 2**32: 11318 bytes
from ltk.actions.action import *

class ReferenceAction(Action):

    def __init__(self, path):
        Action.__init__(self, path)

    def reference_add_action(self, filename, doc_id):
        if self._check_filename(filename, doc_id):
            material = []
            while 1:
                while True:
                    prompt_message = 'Reference Material file: '
                    file_input = input(prompt_message)
                    file_input or logger.warning('You must enter a path to reference material')
                    continue
                    ref_file = os.path.abspath(os.path.expanduser(file_input))
                    if os.path.isfile(ref_file):
                        break
                    else:
                        logger.error(ref_file + ' could not be found')

                prompt_message = 'Reference Material Name: '
                name_input = input(prompt_message)
                prompt_message = 'Reference Material Description: '
                desc_input = input(prompt_message)
                reference = {'file': ref_file}
                if name_input:
                    reference['name'] = name_input
                else:
                    reference['name'] = os.path.basename(ref_file)
                if desc_input:
                    reference['description'] = desc_input
                material.append(reference)
                if not yes_no_prompt('Would you like to add another reference material?', default_yes=False):
                    break

            if doc_id:
                document_id = filename
            else:
                doc_entity = self.doc_manager.get_doc_by_prop('file_name', self.norm_path(filename))
                if not doc_entity:
                    logger.error('{0} could not be found in local database'.format(self.norm_path(filename)))
                    return
                document_id = doc_entity['id']
            for reference in material:
                response = self.api.document_add_reference(document_id, reference)
                if response.status_code == 404:
                    logger.warning('The reference material could not be added because the document could not be found in Lingotek.  The document may still be in the process of uploading.')
                else:
                    if response.status_code != 202:
                        logger.info('The reference material could not be added')
                        logger.error(response.json()['messages'])
                    else:
                        logger.info('{0} ({1}) has been added to the document'.format(reference['name'], response.json()['properties']['id']))

    def reference_list_action(self, filename, doc_id):
        if self._check_filename(filename, doc_id):
            if doc_id:
                document_id = filename
            else:
                doc_entity = self.doc_manager.get_doc_by_prop('file_name', self.norm_path(filename))
                if not doc_entity:
                    logger.error('{0} could not be found in local database'.format(self.norm_path(filename)))
                    return
                document_id = doc_entity['id']
            self._list_reference_material(document_id)

    def reference_download_action(self, filename, doc_id, get_all, path):
        if not path:
            path = self.path
        if self._check_filename(filename, doc_id):
            if doc_id:
                document_id = filename
            else:
                doc_entity = self.doc_manager.get_doc_by_prop('file_name', self.norm_path(filename))
                if not doc_entity:
                    logger.error('{0} could not be found in local database'.format(self.norm_path(filename)))
                    return
                document_id = doc_entity['id']
            table = self._list_reference_material(document_id)
            tablemap = {}
            for row in table:
                tablemap.update({row[0]: {'name':row[1],  'id':row[2]}})

            if len(tablemap) > 0:
                chosen_list = []
                if get_all:
                    chosen_list = tablemap.values()
                while not len(chosen_list) > 0:
                    prompt_message = 'Reference materials to download: (Separate indices by comma) '
                    choice = input(prompt_message)
                    try:
                        choices = choice.replace(', ', ',').split(',')
                        for index in choices:
                            chosen_list.append(tablemap[int(index)])

                    except ValueError:
                        logger.error('Some unexpected, non-integer value was included')
                        chosen_list = []
                    except KeyError:
                        logger.error('An index not in the list was included')
                        chosen_list = []

                for reference in chosen_list:
                    response = self.api.document_download_reference(document_id, reference['id'])
                    if response.status_code == 404:
                        logger.error('{0} ({1}) not found'.format(reference['name'], reference['id']))
                    else:
                        if response.status_code == 200:
                            self._download_reference(response, path, reference['name'])
                        else:
                            logger.info('{0} ({1}) could not be downloaded'.format(reference['name'], reference['id']))
                            logger.error(response.json()['messages'])

    def reference_remove_action(self, filename, doc_id, remove_all):
        if self._check_filename(filename, doc_id):
            if doc_id:
                document_id = filename
            else:
                doc_entity = self.doc_manager.get_doc_by_prop('file_name', self.norm_path(filename))
                if not doc_entity:
                    logger.error('{0} could not be found in local database'.format(self.norm_path(filename)))
                    return
                document_id = doc_entity['id']
            table = self._list_reference_material(document_id)
            tablemap = {}
            for row in table:
                tablemap.update({row[0]: {'name':row[1],  'id':row[2]}})

            if len(tablemap) > 0:
                chosen_list = []
                if remove_all:
                    chosen_list = tablemap.values()
                while not len(chosen_list) > 0:
                    prompt_message = 'Reference materials to remove: (Separate indices by comma) '
                    choice = input(prompt_message)
                    try:
                        choices = choice.replace(', ', ',').split(',')
                        for index in choices:
                            chosen_list.append(tablemap[int(index)])

                    except ValueError:
                        logger.error('Some unexpected, non-integer value was included')
                        chosen_list = []
                    except KeyError:
                        logger.error('An index not in the list was included')
                        chosen_list = []

                for reference in chosen_list:
                    response = self.api.document_remove_reference(document_id, reference['id'])
                    if response.status_code == 404:
                        logger.error('{0} ({1}) not found'.format(reference['name'], reference['id']))
                    else:
                        if response.status_code == 204:
                            logger.info('{0} ({1}) deleted'.format(reference['name'], reference['id']))
                        else:
                            logger.info('{0} ({1}) could not be deleted'.format(reference['name'], reference['id']))
                            logger.error(response.json()['messages'])

    def _check_filename(self, filename, doc_id):
        if doc_id:
            return True
        else:
            if os.path.isfile(filename):
                foundfile = self.get_doc_filenames_in_path(filename)
                if len(foundfile) == 0:
                    logger.warning(filename + ' has not been added yet.')
                    return False
                else:
                    if len(foundfile) == 1:
                        return True
                    logger.warning('Only manage reference material on one file at a time')
                    return False
            else:
                if os.path.isdir(filename):
                    logger.error(filename + ' is not a file')
                    return False
                logger.error(filename + ' could not be found')
            return False

    def _list_reference_material(self, document_id):
        response = self.api.document_list_reference(document_id)
        if response.status_code == 404:
            logger.warning('The document could not be found in Lingotek.')
            return []
        if response.status_code != 200:
            logger.info('The reference material list could not be retrieved')
            logger.error(response.json()['messages'])
            return []
        else:
            if response.json()['properties']['size'] > 0:
                materials = response.json()['entities']
                index = 0
                table = []
                for material in materials:
                    row = [
                     index, material['properties']['name'], material['properties']['id']]
                    if 'description' in material['properties']:
                        if material['properties']['description']:
                            row.append(material['properties']['description'])
                    table.append(row)
                    index += 1

                print(tabulate(table, headers=['', 'Name', 'ID', 'Description']))
                return table
            print('There is no reference material attached to this document')
            return []

    def _download_reference(self, response, path, name):
        filepath = os.path.join(path, name)
        if os.path.isfile(filepath):
            if not yes_no_prompt(('There is already a file {0}.  Would you like to overwrite it?'.format(filepath)), default_yes=False):
                return
        try:
            with open(filepath, 'wb') as (file):
                for chunk in response.iter_content(1024):
                    file.write(chunk)

        except IOError as e:
            print(e.errno)
            print(e)
            return

        logger.info('Downloaded {0}'.format(filepath))