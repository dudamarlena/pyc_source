# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/actions/pull_action.py
# Compiled at: 2020-04-13 16:06:48
# Size of source mod 2**32: 3628 bytes
from ltk.actions.action import *
from ltk.git_auto import Git_Auto
DEFAULT_COMMIT_MESSAGE = 'Translations updated for '

class PullAction(Action):

    def __init__(self, path, download):
        Action.__init__(self, path)
        self.git_auto = Git_Auto(path)
        self.download = download

    def pull_translations(self, locale_code, locale_ext, no_ext, auto_format):
        if auto_format == False:
            if self.auto_format_option == 'on':
                auto_format = True
        first_in_message = True
        documents_added = True
        git_commit_message = DEFAULT_COMMIT_MESSAGE
        try:
            if 'clone' in self.download_option and not locale_ext or no_ext and not locale_ext:
                locale_ext = False
            else:
                locale_ext = True
            entries = self.doc_manager.get_all_entries()
            if not locale_code:
                if entries:
                    for entry in entries:
                        git_commit_message += ('' if first_in_message else '; ') + entry['name'] + ': '
                        first_in_message = False
                        first_locale = True
                        try:
                            locales = entry['locales']
                            for locale in locales:
                                locale = locale.replace('_', '-')
                                git_commit_message += ('' if first_locale else ', ') + locale
                                first_locale = False
                                self.download.download_action((entry['id']), locale, auto_format, locale_ext=locale_ext)

                        except KeyError:
                            self.download.download_action((entry['id']), None, auto_format, locale_ext=locale_ext)
                            git_commit_message = git_commit_message[:-1]

                else:
                    logger.info('No documents have been added')
                    documents_added = False
            else:
                document_ids = self.doc_manager.get_doc_ids()
                if document_ids:
                    for document_id in document_ids:
                        git_commit_message += ('' if first_in_message else '; ') + self.doc_manager.get_doc_by_prop('id', document_id)['name'] + ': ' + locale_code
                        first_in_message = False
                        first_locale = True
                        self.download.download_action(document_id, locale_code, auto_format, locale_ext=locale_ext)

                else:
                    logger.info('No documents have been added')
                    documents_added = False
        except Exception as e:
            log_error(self.error_file_name, e)
            if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                logger.error("Error connecting to Lingotek's TMS")
            else:
                logger.error('Error on pull: ' + str(e))