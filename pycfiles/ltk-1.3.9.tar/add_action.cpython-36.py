# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/actions/add_action.py
# Compiled at: 2020-01-30 14:00:13
# Size of source mod 2**32: 6536 bytes
from ltk.actions.action import *
import ctypes, socket, ltk.check_connection

class AddAction(Action):

    def __init__(self, path):
        Action.__init__(self, path)

    def add_action(self, file_patterns, **kwargs):
        try:
            added_folder = self.add_folders(file_patterns)
            if 'directory' in kwargs:
                if kwargs['directory']:
                    if not added_folder:
                        logger.info('No folders to add at the given path(s).')
                    return
            matched_files = get_files(file_patterns)
            if not matched_files:
                if added_folder:
                    return
                raise exceptions.ResourceNotFound('Could not find the specified file/pattern.')
            (self.add_documents)(matched_files, **kwargs)
        except Exception as e:
            log_error(self.error_file_name, e)
            if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                logger.error("Error connecting to Lingotek's TMS")
            else:
                logger.error('Error on add: ' + str(e))

    def add_documents(self, matched_files, **kwargs):
        """ adds new documents to the lingotek cloud and, after prompting user, overwrites changed documents that
                have already been added """
        metadata = copy.deepcopy(self.default_metadata)
        if 'metadata' in kwargs:
            if kwargs['metadata']:
                metadata = self.metadata_wizard()
        if self.metadata_prompt:
            if yes_no_prompt('Would you like to launch the metadata wizard?', default_yes=True):
                metadata = self.metadata_wizard()
        confirmed = False
        for file_name in matched_files:
            try:
                relative_path = self.norm_path(file_name)
                title = os.path.basename(relative_path)
                try:
                    if os.stat(os.path.join(self.path, relative_path)).st_size == 0:
                        logger.info('This document is empty and was not added: {0}\n'.format(title))
                        continue
                except FileNotFoundError:
                    logger.warning('Warning: could not verify that {0} is not empty'.format(relative_path))
                except Exception as e:
                    raise e

                if not self.doc_manager.is_doc_new(relative_path):
                    if self.doc_manager.is_doc_modified(relative_path, self.path) or len(metadata) > 0:
                        if 'overwrite' in kwargs:
                            if kwargs['overwrite']:
                                confirmed = True
                    else:
                        try:
                            if not confirmed:
                                option = yes_no_prompt(("Document '{0}' already exists. Would you like to overwrite it?".format(title)), default_yes=False)
                            else:
                                option = True
                            if option:
                                logger.info("Overwriting document '{0}' in Lingotek Cloud...\n".format(title))
                                (self.update_document_action)(file_name, title, doc_metadata=metadata, **kwargs)
                                continue
                            else:
                                logger.info("Will not overwrite document '{0}' in Lingotek Cloud\n".format(title))
                                continue
                        except KeyboardInterrupt:
                            logger.error('Canceled adding the document')
                            return

                else:
                    logger.error('This document has already been added and no metadata is being sent: {0}\n'.format(title))
                    continue
            except json.decoder.JSONDecodeError:
                logger.error('JSON error on adding document.')
            except Exception:
                logger.error('Error adding document')
            else:
                (self.add_document)(file_name, title, doc_metadata=metadata, **kwargs)

    def add_folders(self, file_patterns):
        """ checks each file pattern for a directory and adds matching patterns to the db """
        added_folder = False
        for pattern in file_patterns:
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    if self.is_hidden_file(pattern):
                        logger.warning('Folder is hidden')
                    else:
                        if not self._is_folder_added(pattern):
                            self.folder_manager.add_folder(self.norm_path(pattern.rstrip(os.sep)))
                            logger.info('Added folder ' + str(pattern))
                        else:
                            logger.warning('Folder ' + str(pattern) + ' has already been added.\n')
                    added_folder = True
            else:
                logger.warning('Path "' + str(pattern) + '" doesn\'t exist.\n')

        return added_folder

    def _is_folder_added(self, file_name):
        """ checks if a folder has been added or is a subfolder of an added folder """
        folder_names = self.folder_manager.get_file_names()
        for folder in folder_names:
            if os.path.join(self.path, folder) in os.path.abspath(file_name):
                return True

        return False