# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/classes/TestsConfiger.py
# Compiled at: 2018-10-18 06:45:19
from __future__ import absolute_import
import os, copy, sys, logging, inspect, shutil, traceback, time, json
from collections import defaultdict
from raven import Client
from cached_property import cached_property
import inspect
from consolemenu import *
from consolemenu.items import *
from validate_email import validate_email
import urllib2, twitter
from nltk.tokenize import TweetTokenizer
from nose.tools import nottest
from zas_rep_tools_data.utils import path_to_data_folder, path_to_models, path_to_someweta_models, path_to_stop_words
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, MyZODB, transaction, path_to_zas_rep_tools, internet_on, make_zipfile, instance_info, SharedCounterExtern, SharedCounterIntern, Status, function_name, statusesTstring
import zas_rep_tools.src.utils.db_helper as db_helper
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.exporter import Exporter
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.classes.basecontent import BaseContent
from zas_rep_tools.src.utils.configer_helpers import ConfigerData

@nottest
class TestsConfiger(BaseContent, ConfigerData):

    def __init__(self, rewrite=False, stop_if_db_already_exist=True, **kwargs):
        super(type(self), self).__init__(**kwargs)
        self._rewrite = rewrite
        self._stop_if_db_already_exist = stop_if_db_already_exist
        self._path_to_zas_rep_tools = path_to_zas_rep_tools
        self._path_to_user_config_data = os.path.join(self._path_to_zas_rep_tools, 'user_config/user_data.fs')
        self._path_to_zas_rep_tools_data = path_to_data_folder
        self._path_to_zas_rep_tools_someweta_models = path_to_someweta_models
        self._path_to_zas_rep_tools_stop_words = path_to_stop_words
        if not self._check_correctness_of_the_test_data():
            self.logger.error('TestDataCorruption: Please check test data.', exc_info=self._logger_traceback)
            sys.exit()
        self.logger.debug('Intern InstanceAttributes was initialized')
        self.logger.debug(('An instance of {}() was created ').format(self.__class__.__name__))
        attr_to_flag = [
         '_types_folder_names_of_testsets', '_test_dbs', '_init_info_data', '_columns_in_doc_table', '_columns_in_info_tabel', '_columns_in_stats_tables', '_text_elements_collection']
        attr_to_len = False
        self._log_settings(attr_to_flag=attr_to_flag, attr_to_len=attr_to_len)

    def __del__(self):
        pass

    def row_text_elements(self, lang='all'):
        return copy.deepcopy(self._row_text_elements(lang=lang))

    def text_elements(self, token=True, unicode_str=True, lang='all'):
        return copy.deepcopy(self._text_elements(token=token, unicode_str=unicode_str, lang=lang))

    def docs_row_values(self, token=True, unicode_str=True, lang='all'):
        return copy.deepcopy(self._docs_row_values(token=token, unicode_str=unicode_str, lang=lang))

    def docs_row_dict(self, token=True, unicode_str=True, all_values=False, lang='all'):
        """
        just one dict with colums as key and list of all values as values for each columns()key
        """
        return copy.deepcopy(self._docs_row_dict(token=token, unicode_str=unicode_str, all_values=all_values, lang=lang))

    def docs_row_dicts(self, token=True, unicode_str=True, lang='all'):
        """
        list of dicts  with colums and values for each row
        """
        return copy.deepcopy(self._docs_row_dicts(token=token, unicode_str=unicode_str, lang=lang))

    @cached_property
    def path_to_zas_rep_tools(self):
        return copy.deepcopy(self._path_to_zas_rep_tools)

    @cached_property
    def path_to_zas_rep_tools_data(self):
        return copy.deepcopy(self._path_to_zas_rep_tools_data)

    @nottest
    @cached_property
    def path_to_testdbs(self):
        return copy.deepcopy(self._path_to_testdbs)

    @nottest
    @cached_property
    def test_dbs(self):
        return copy.deepcopy(self._test_dbs)

    @cached_property
    def init_info_data(self):
        return copy.deepcopy(self._init_info_data)

    @cached_property
    def columns_in_doc_table(self):
        return copy.deepcopy(self._columns_in_doc_table)

    @cached_property
    def columns_in_info_tabel(self):
        return copy.deepcopy(self._columns_in_info_tabel)

    @cached_property
    def columns_in_stats_tables(self):
        return copy.deepcopy(self._columns_in_stats_tables)

    @nottest
    @cached_property
    def path_to_testsets(self):
        return copy.deepcopy(self._path_to_testsets)

    @cached_property
    def types_folder_names_of_testsets(self):
        return copy.deepcopy(self._types_folder_names_of_testsets)

    @nottest
    def create_test_data(self, abs_path_to_storage_place=False, use_original_classes=True, corp_lang_classification=False, corp_pos_tagger=True, corp_sent_splitter=True, corp_sentiment_analyzer=True, status_bar=True, corp_log_ignored=False, use_test_pos_tagger=False, rewrite=False):
        self.create_testsets(rewrite=rewrite, abs_path_to_storage_place=abs_path_to_storage_place, silent_ignore=True)
        if not self.create_test_dbs(rewrite=rewrite, abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=use_original_classes, corp_lang_classification=corp_lang_classification, corp_log_ignored=corp_log_ignored, corp_pos_tagger=corp_pos_tagger, corp_sent_splitter=corp_sent_splitter, corp_sentiment_analyzer=corp_sentiment_analyzer, status_bar=status_bar, use_test_pos_tagger=use_test_pos_tagger):
            return False
        self.logger.info('Test Data was initialized.')
        return True

    @nottest
    def create_test_dbs(self, rewrite=False, abs_path_to_storage_place=False, corp_log_ignored=False, use_original_classes=True, corp_lang_classification=True, use_test_pos_tagger=False, corp_pos_tagger=True, corp_sent_splitter=True, corp_sentiment_analyzer=True, status_bar=True):
        try:
            if not abs_path_to_storage_place:
                abs_path_to_storage_place = os.path.join(self._path_to_zas_rep_tools, self._path_to_testdbs)
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            exist_fnames_in_dir = [ fname for fname in exist_fnames_in_dir if '.db-journal' in fname ]
            if exist_fnames_in_dir:
                for fname in exist_fnames_in_dir:
                    os.remove(os.path.join(abs_path_to_storage_place, fname))

                msg = ("'{}' '.db-journal' files was deleted. ").format(len(exist_fnames_in_dir))
                self.logger.critical(msg)
            if not rewrite:
                rewrite = self._rewrite
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            num = len(exist_fnames_in_dir)
            exist_fnames_in_dir = [ fname for fname in exist_fnames_in_dir if '.db' in fname and '.db-journal' not in fname ]
            fnames_test_db = [ fname for encr, encr_data in self._test_dbs.items() for template_name, template_name_data in encr_data.items() for lang, lang_data in template_name_data.items() for db_type, fname in lang_data.items() ]
            test_db_num = len(fnames_test_db)
            clean = False
            if len(exist_fnames_in_dir) != len(fnames_test_db):
                clean = True
                self.logger.critical(("Some TestDB are missing. There was found '{}'-DBs. But it should be '{}'. Process of TestDB Creation will be started. ").format(len(exist_fnames_in_dir), len(fnames_test_db)))
            else:
                for fname in fnames_test_db:
                    if fname not in exist_fnames_in_dir:
                        msg = ("Some TestDB are missing. (eg: '{}') Process of TestDB Creation will be started. ").format(fname)
                        self.logger.critical(msg)
                        clean = True
                        break

                if clean:
                    clean = False
                    for fname in exist_fnames_in_dir:
                        os.remove(os.path.join(abs_path_to_storage_place, fname))

                    exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
                    exist_fnames_in_dir = [ fname for fname in exist_fnames_in_dir if '.db-journal' in fname ]
                    for fname in exist_fnames_in_dir:
                        os.remove(os.path.join(abs_path_to_storage_place, fname))

                activ_corp_dbs = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(dict))))
                for template_name, init_data in self._init_info_data.iteritems():
                    for encryption in ['plaintext', 'encrypted']:
                        for dbtype in ['corpus', 'stats']:
                            dbname = self._init_info_data[template_name]['name']
                            visibility = self._init_info_data[template_name]['visibility']
                            platform_name = self._init_info_data[template_name]['platform_name']
                            license = self._init_info_data[template_name]['license']
                            template_name = self._init_info_data[template_name]['template_name']
                            version = self._init_info_data[template_name]['version']
                            source = self._init_info_data[template_name]['source']
                            encryption_key = self._init_info_data[template_name]['encryption_key'][dbtype] if encryption == 'encrypted' else False
                            corpus_id = self._init_info_data[template_name]['id']['corpus']
                            stats_id = self._init_info_data[template_name]['id']['stats']
                            if encryption == 'encrypted':
                                if template_name == 'twitter':
                                    languages = [
                                     'de']
                                elif template_name == 'blogger':
                                    continue
                            else:
                                if encryption == 'plaintext':
                                    if template_name == 'twitter':
                                        continue
                                    elif template_name == 'blogger':
                                        languages = [
                                         'de', 'en', 'test']
                                for language in languages:
                                    try:
                                        path_to_db = os.path.join(abs_path_to_storage_place, self._test_dbs[encryption][template_name][language][dbtype])
                                        if rewrite:
                                            if os.path.isfile(path_to_db):
                                                os.remove(path_to_db)
                                                self.logger.debug(("RewriteOptionIsON: Following DB was deleted from TestDBFolder: '{}'. TestDBCreationScript will try to created this DB.").format(path_to_db))
                                            else:
                                                self.logger.debug(("RewriteOptionIsON: Following DB wasn't found in the TestDBFolder and wasn't deleted: '{}'. TestDBCreationScript will try to created this DB.").format(path_to_db))
                                        elif os.path.isfile(path_to_db):
                                            self.logger.debug(("RewriteOptionIsOFF: '{}'-DB exist and will not be rewrited/recreated.").format(path_to_db))
                                            continue
                                    except KeyError as k:
                                        self.logger.debug(("KeyError: DBName for '{}:{}:{}:{}' is not exist in the 'self._test_dbs'. TestDBCreationScript will try to created this DB. ").format(encryption, template_name, language, dbtype))
                                        continue
                                    except Exception as e:
                                        self.logger.error(("See Exception: '{}'. (line 703). Creation of the TestDBs was aborted.").format(e), exc_info=self._logger_traceback)
                                        sy.exit()

                                    db_id = corpus_id if dbtype == 'corpus' else stats_id
                                    self.logger.info(("TestDBCreationProcess: Was started for DB with following attributes: 'dbtype='{}'; id='{}'; encryption='{}'; template_name='{}'; language='{}'. ").format(dbtype, db_id, encryption, template_name, language))
                                    if dbtype == 'corpus':
                                        if not use_original_classes:
                                            db = DBHandler(logger_level=logging.ERROR, logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, ext_tb=self._ext_tb, stop_if_db_already_exist=self._stop_if_db_already_exist, rewrite=self._rewrite)
                                            was_initialized = db.init(dbtype, abs_path_to_storage_place, dbname, language, visibility, platform_name=platform_name, license=license, template_name=template_name, version=version, source=source, corpus_id=corpus_id, stats_id=stats_id, encryption_key=encryption_key)['status']
                                            if not was_initialized:
                                                if self._stop_if_db_already_exist:
                                                    self.logger.debug(("DBInitialisation: DBName for '{}:{}:{}:{}' wasn't initialized. Since 'self._stop_if_db_already_exist'-Option is on, current Script will ignore current DB and will try to create next one.").format(encryption, template_name, language, dbtype))
                                                    continue
                                                else:
                                                    self.logger.error(("DBInitialisationError: DBName for '{}:{}:{}:{}' wasn't initialized. TestDBCreation was aborted.").format(encryption, template_name, language, dbtype))
                                                    return False
                                            rows_to_insert = self.docs_row_values(token=True, unicode_str=True)[template_name]
                                            path_to_db = db.path()
                                            if not path_to_db:
                                                self.logger.error("Path for current DB wasn't getted. Probably current corpus has InitializationError. TestDBCreation was aborted.")
                                                sys.exit()
                                            db.lazyinsert('documents', rows_to_insert)
                                            if 'Connection' not in str(type(db)):
                                                pass
                                            if len(db.getall('documents')) != len(rows_to_insert):
                                                os.remove(path_to_db)
                                                self.logger.error('TestDBsCreation(InsertionError): Not all rows was correctly inserted into DB. This db was ignored and not created.', exc_info=self._logger_traceback)
                                                sys.exit()
                                                continue
                                            db.commit()
                                            db.close()
                                        else:
                                            corp = Corpus(logger_level=logging.ERROR, logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save, use_test_pos_tagger=use_test_pos_tagger, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, ext_tb=self._ext_tb, stop_if_db_already_exist=self._stop_if_db_already_exist, status_bar=status_bar, rewrite=self._rewrite)
                                            was_initialized = corp.init(abs_path_to_storage_place, dbname, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source, corpus_id=corpus_id, encryption_key=encryption_key, lang_classification=corp_lang_classification, pos_tagger=corp_pos_tagger, sent_splitter=corp_sent_splitter, sentiment_analyzer=corp_sentiment_analyzer)
                                            if not was_initialized:
                                                if self._stop_if_db_already_exist:
                                                    self.logger.debug(("DBInitialisation: DBName for '{}:{}:{}:{}' wasn't initialized. Since 'self._stop_if_db_already_exist'-Option is on, current Script will ignore current DB and will try to create next one.").format(encryption, template_name, language, dbtype))
                                                    continue
                                                else:
                                                    self.logger.error(("DBInitialisationError: DB for '{}:{}:{}:{}' wasn't initialized. TestDBCreation was aborted.").format(encryption, template_name, language, dbtype))
                                                    return False
                                            rows_as_dict_to_insert = self.docs_row_dicts(token=False, unicode_str=True)[template_name]
                                            path_to_db = corp.corpdb.path()
                                            fname_db = corp.corpdb.fname()
                                            if not path_to_db or not fname_db:
                                                self.logger.error(("Path or FileName for current CorpusDB wasn't getted. (lang='{}', dbname='{}', id='{}',platform_name='{}', visibility='{}', encryption_key='{}') Probably current corpus has InitializationError. TestDBCreation was aborted.").format(language, dbname, corpus_id, platform_name, visibility, encryption_key))
                                                sys.exit()
                                            was_inserted = corp.insert(rows_as_dict_to_insert, log_ignored=corp_log_ignored)
                                            if not was_inserted:
                                                os.remove(path_to_db)
                                                msg = ("Rows wasn't inserted into the '{}'-DB. This DB was deleted and script of creating testDBs was aborted.").format(fname_db)
                                                self.logger.error(msg)
                                                raise Exception, msg
                                                sys.exit()
                                                return False
                                            if not corp_lang_classification:
                                                if len(corp.docs()) != len(rows_as_dict_to_insert):
                                                    os.remove(path_to_db)
                                                    msg = 'TestDBsCreation(InsertionError): Not all rows was correctly inserted into DB. This DB was deleted and script of creating testDBs was aborted.'
                                                    self.logger.error(msg, exc_info=self._logger_traceback)
                                                    raise Exception, msg
                                            if corp.total_error_insertion_during_last_insertion_process:
                                                msg = ("TestDBsCreation(InsertionError): '{}'-ErrorInsertion was found!!! Not all rows was correctly inserted into DB. This DB was deleted and script of creating testDBs was aborted.").format(corp.total_error_insertion_during_last_insertion_process)
                                                self.logger.error(msg, exc_info=self._logger_traceback)
                                                raise Exception, msg
                                                return False
                                            self.logger.debug(("'{}'-TestDB was created. Path: '{}'.").format(fname_db, path_to_db))
                                            self.logger.debug(("'{}': Following rows was inserted:\n '{}'. \n\n").format(fname_db, ('\n').join('--->' + str(v) for v in list(corp.docs()))))
                                            activ_corp_dbs[template_name][encryption][dbtype][language] = corp
                                    elif dbtype == 'stats':
                                        if not use_original_classes:
                                            stats = DBHandler(logger_level=logging.ERROR, logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, ext_tb=self._ext_tb, stop_if_db_already_exist=self._stop_if_db_already_exist, rewrite=self._rewrite)
                                            stats.init(dbtype, abs_path_to_storage_place, dbname, language, visibility, platform_name=platform_name, license=license, template_name=template_name, version=version, source=source, corpus_id=corpus_id, stats_id=stats_id, encryption_key=encryption_key)
                                            stats.close()
                                        else:
                                            stats = Stats(logger_level=logging.ERROR, logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, ext_tb=self._ext_tb, stop_if_db_already_exist=self._stop_if_db_already_exist, status_bar=status_bar, rewrite=self._rewrite)
                                            was_initialized = stats.init(abs_path_to_storage_place, dbname, language, visibility, version=version, corpus_id=corpus_id, stats_id=stats_id, encryption_key=encryption_key, case_sensitiv=False, full_repetativ_syntagma=True, baseline_delimiter='++')
                                            corp = activ_corp_dbs[template_name][encryption]['corpus'][language]
                                            if isinstance(corp, Corpus):
                                                stats.compute(corp)
                                                corp.corpdb.commit()
                                                stats.statsdb.commit()
                                                corp.close()
                                                stats.close()
                                            else:
                                                self.logger.error(("Given CorpObj ('{}') is invalid").format(corp))
                                                return False

                exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
                exist_fnames_in_dir = [ fname for fname in exist_fnames_in_dir if '.db' in fname and '.db-journal' not in fname ]
                if len(fnames_test_db) != len(exist_fnames_in_dir):
                    self.logger.error(("TestDBs wasn't initialized correctly. There was found '{}' testDBs in the TestDBFolder, but it should be '{}'. ").format(len(exist_fnames_in_dir), len(fnames_test_db)))
                    return False
                for fname in fnames_test_db:
                    if fname not in exist_fnames_in_dir:
                        self.logger.error(("'{}'-testDB wasn't found in the TestDB-Folder. End with Error.").format(fname))
                        return False

            self.logger.info('TestDBs was initialized.')
            return True
        except KeyboardInterrupt:
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            exist_fnames_in_dir = [ fname for fname in exist_fnames_in_dir if '.db' in fname ]
            for fname in exist_fnames_in_dir:
                os.remove(os.path.join(abs_path_to_storage_place, fname))

            sys.exit()
            return False

    @nottest
    def create_testsets(self, rewrite=False, abs_path_to_storage_place=False, silent_ignore=True):
        return list(self.create_testsets_in_diff_file_formats(rewrite=rewrite, abs_path_to_storage_place=abs_path_to_storage_place, silent_ignore=silent_ignore))

    @nottest
    def create_testsets_in_diff_file_formats(self, rewrite=False, abs_path_to_storage_place=False, silent_ignore=True):
        if not rewrite:
            rewrite = self._rewrite
        if not abs_path_to_storage_place:
            abs_path_to_storage_place = self._path_to_zas_rep_tools
        created_sets = []
        if not abs_path_to_storage_place:
            sys.exit()
        try:
            for file_format, test_sets in self._types_folder_names_of_testsets.iteritems():
                for name_of_test_set, folder_for_test_set in test_sets.iteritems():
                    if file_format == 'txt':
                        continue
                    abs_path_to_current_test_case = os.path.join(abs_path_to_storage_place, self._path_to_testsets['blogger'], folder_for_test_set)
                    if rewrite:
                        if os.path.isdir(abs_path_to_current_test_case):
                            shutil.rmtree(abs_path_to_current_test_case)
                    if not os.path.isdir(abs_path_to_current_test_case):
                        os.makedirs(abs_path_to_current_test_case)
                    path_to_txt_corpus = os.path.join(self.path_to_zas_rep_tools, self._path_to_testsets['blogger'], self._types_folder_names_of_testsets['txt'][name_of_test_set])
                    reader = Reader(path_to_txt_corpus, 'txt', regex_template='blogger', logger_level=self._logger_level, logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, ext_tb=self._ext_tb)
                    exporter = Exporter(reader.getlazy(), rewrite=rewrite, silent_ignore=silent_ignore, logger_level=self._logger_level, logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, ext_tb=self._ext_tb)
                    if file_format == 'csv':
                        if name_of_test_set == 'small':
                            flag = exporter.tocsv(abs_path_to_current_test_case, 'blogger_corpus', self._columns_in_doc_table['blogger'], rows_limit_in_file=5)
                            if not flag:
                                yield False
                            else:
                                created_sets.append('csv')
                                yield True
                        else:
                            flag = exporter.tocsv(abs_path_to_current_test_case, 'blogger_corpus', self._columns_in_doc_table['blogger'], rows_limit_in_file=2)
                            if not flag:
                                yield False
                            else:
                                created_sets.append('csv')
                                yield True
                    elif file_format == 'xml':
                        if name_of_test_set == 'small':
                            flag = exporter.toxml(abs_path_to_current_test_case, 'blogger_corpus', rows_limit_in_file=5)
                            if not flag:
                                yield False
                            else:
                                created_sets.append('xml')
                                yield True
                        else:
                            flag = exporter.toxml(abs_path_to_current_test_case, 'blogger_corpus', rows_limit_in_file=2)
                            if not flag:
                                yield False
                            else:
                                created_sets.append('xml')
                                yield True
                    elif file_format == 'json':
                        if name_of_test_set == 'small':
                            flag = exporter.tojson(abs_path_to_current_test_case, 'blogger_corpus', rows_limit_in_file=5)
                            if not flag:
                                yield False
                            else:
                                created_sets.append('json')
                                yield True
                        else:
                            flag = exporter.tojson(abs_path_to_current_test_case, 'blogger_corpus', rows_limit_in_file=2)
                            if not flag:
                                yield False
                            else:
                                created_sets.append('json')
                                yield True
                    elif file_format == 'sqlite':
                        flag = exporter.tosqlite(abs_path_to_current_test_case, 'blogger_corpus', self._columns_in_doc_table['blogger'])
                        if not flag:
                            yield False
                        else:
                            created_sets.append('sqlite')
                            yield True

            for created_set in set(created_sets):
                path_to_set = os.path.join(abs_path_to_storage_place, self._path_to_testsets['blogger'], created_set)
                make_zipfile(os.path.join(os.path.split(path_to_set)[0], created_set + '.zip'), path_to_set)

            self.logger.info('TestSets (diff file formats) was initialized.')
        except Exception as e:
            print_exc_plus() if self._ext_tb else ''
            self.logger.error(("SubsetsCreaterError: Throw following Exception: '{}'. ").format(e), exc_info=self._logger_traceback)

    def _check_correctness_of_the_test_data(self):
        try:
            for template, data_columns in self._columns_in_doc_table.iteritems():
                for data_values in self.docs_row_values(token=True, unicode_str=True)[template]:
                    if len(data_columns) != len(data_values):
                        self.logger.error('TestDataCorruption: Not same number of columns and values.', exc_info=self._logger_traceback)
                        return False

        except Exception as e:
            self.logger.error(("TestDataCorruption: Test Data in Configer is inconsistent. Probably  - Not same template_names in columns and rows. See Exception: '{}'. ").format(e), exc_info=self._logger_traceback)
            return False

        return True