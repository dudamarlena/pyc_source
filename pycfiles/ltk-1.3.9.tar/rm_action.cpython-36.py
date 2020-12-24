# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/actions/rm_action.py
# Compiled at: 2020-04-13 16:03:59
# Size of source mod 2**32: 9790 bytes
from ltk.actions.action import *

class RmAction(Action):

    def __init__(self, path):
        Action.__init__(self, path)
        self.use_delete = False

    def rm_action(self, file_patterns, **kwargs):
        try:
            removed_folder = False
            for pattern in file_patterns:
                if os.path.isdir(pattern):
                    if self.folder_manager.folder_exists(self.norm_path(pattern)):
                        self.folder_manager.remove_element(self.norm_path(pattern))
                        logger.info('Removed folder ' + pattern)
                        removed_folder = True
                    else:
                        logger.warning('Folder ' + str(pattern) + ' has not been added and so can not be removed')

            if 'directory' in kwargs:
                if kwargs['directory']:
                    if not removed_folder:
                        logger.info('No folders to remove at the given path(s)')
                    return
            matched_files = None
            if isinstance(file_patterns, str):
                file_patterns = [
                 file_patterns]
            else:
                if 'force' in kwargs:
                    if kwargs['force']:
                        force = True
                    else:
                        force = False
                    if 'id' in kwargs:
                        if kwargs['id']:
                            useID = True
                    useID = False
                else:
                    if 'remote' in kwargs and kwargs['remote']:
                        self.use_delete = True
                self.use_delete = False
            if 'all' in kwargs and kwargs['all']:
                local = False
                self.folder_manager.clear_all()
                removed_folder = True
                logger.info('Removed all folders.')
                useID = False
                matched_files = self.doc_manager.get_file_names()
            elif 'local' in kwargs and kwargs['local']:
                local = True
                if 'name' in kwargs:
                    if kwargs['name']:
                        matched_files = []
                        for pattern in file_patterns:
                            doc = self.doc_manager.get_doc_by_prop('name', pattern)
                            if doc:
                                matched_files.append(doc['file_name'])

                if len(file_patterns) == 0:
                    self.folder_manager.clear_all()
                    removed_folder = True
                    logger.info('Removed all folders.')
                    useID = False
                    matched_files = self.doc_manager.get_file_names()
            else:
                local = useID or False
            if 'name' in kwargs:
                if kwargs['name']:
                    matched_files = []
                    for pattern in file_patterns:
                        doc = self.doc_manager.get_doc_by_prop('name', pattern)
                        if doc:
                            matched_files.append(doc['file_name'])

                else:
                    matched_files = self.get_doc_filenames_in_path(file_patterns)
            else:
                local = False
                matched_files = file_patterns
            if not matched_files or len(matched_files) == 0:
                if useID:
                    raise exceptions.ResourceNotFound('No documents to remove with the specified id')
                else:
                    if removed_folder:
                        logger.info('No documents to remove')
                    else:
                        if local:
                            raise exceptions.ResourceNotFound('Too many agruments, to specify a document to be removed locally use -l in association with -n')
                        else:
                            if 'all' not in kwargs or not kwargs['all']:
                                raise exceptions.ResourceNotFound('No documents to remove with the specified file path')
                            else:
                                raise exceptions.ResourceNotFound('No documents to remove')
            is_directory = False
            for pattern in file_patterns:
                basename = os.path.basename(pattern)
                if not basename or basename == '':
                    is_directory = True

            for file_name in matched_files:
                self._rm_document(self.norm_path(file_name).replace(self.path, ''), useID, force or local)

        except Exception as e:
            log_error(self.error_file_name, e)
            if 'string indices must be integers' in str(e):
                logger.error("Error connecting to Lingotek's TMS")
            else:
                logger.error('Error on remove: ' + str(e))

    def _rm_clone(self, file_name):
        trans_files = []
        entry = self.doc_manager.get_doc_by_prop('file_name', file_name)
        if entry:
            if 'locales' in entry:
                if entry['locales']:
                    locales = entry['locales']
                    for locale_code in locales:
                        if locale_code in self.locale_folders:
                            download_root = self.locale_folders[locale_code]
                        elif self.download_dir:
                            if len(self.download_dir):
                                download_root = os.path.join(self.download_dir if (self.download_dir and self.download_dir != 'null') else '', locale_code)
                        else:
                            download_root = locale_code
                        download_root = os.path.join(self.path, download_root)
                        source_file_name = entry['file_name']
                        source_path = os.path.join(self.path, os.path.dirname(source_file_name))
                        trans_files.extend(get_translation_files(file_name, download_root, self.download_option, self.doc_manager))

        return trans_files

    def _rm_document(self, file_name, useID, force):
        try:
            doc = None
            if not useID:
                relative_path = self.norm_path(file_name)
                doc = self.doc_manager.get_doc_by_prop('file_name', relative_path)
                title = os.path.basename(self.norm_path(file_name))
                try:
                    document_id = doc['id']
                except TypeError:
                    logger.warning("Document name specified for remove isn't in the local database: {0}".format(relative_path))
                    return

            else:
                document_id = file_name
                doc = self.doc_manager.get_doc_by_prop('id', document_id)
                if doc:
                    file_name = doc['file_name']
                else:
                    if self.use_delete:
                        response = self.api.document_delete(document_id)
                    else:
                        response = self.api.document_cancel(document_id)
                    if response.status_code != 204 and response.status_code != 202:
                        logger.error('Failed to {0} {1} remotely'.format('delete' if self.use_delete else 'cancel', file_name))
                    else:
                        logger.info('{0} has been {1} remotely'.format(file_name, 'deleted' if self.use_delete else 'cancelled'))
                if force:
                    trans_files = []
                    if 'clone' in self.download_option:
                        trans_files = self._rm_clone(file_name)
                    else:
                        if 'folder' in self.download_option:
                            trans_files = self._rm_folder(file_name)
                        else:
                            if 'same' in self.download_option:
                                download_path = self.path
                                trans_files = get_translation_files(file_name, download_path, self.download_option, self.doc_manager)
                    self.delete_local(file_name, document_id)
                self.doc_manager.remove_element(document_id)
        except json.decoder.JSONDecodeError:
            logger.error('JSON error on removing document')
        except KeyboardInterrupt:
            raise_error('', 'Canceled removing document')
            return
        except Exception as e:
            log_error(self.error_file_name, e)
            logger.error('Error on removing document ' + str(file_name) + ': ' + str(e))

    def _rm_folder(self, file_name):
        trans_files = []
        entry = self.doc_manager.get_doc_by_prop('file_name', file_name)
        if entry:
            if 'locales' in entry:
                if entry['locales']:
                    locales = entry['locales']
                    for locale_code in locales:
                        if locale_code in self.locale_folders:
                            if self.locale_folders[locale_code] == 'null':
                                logger.warning('Download failed: folder not specified for ' + locale_code)
                            else:
                                download_path = self.locale_folders[locale_code]
                        else:
                            download_path = self.download_dir
                        download_path = os.path.join(self.path, download_path)
                        trans_files.extend(get_translation_files(file_name, download_path, self.download_option, self.doc_manager))

        return trans_files