# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_dbhandler.py
# Compiled at: 2018-10-19 06:50:52
import unittest, os, logging, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import random, json, time
from zas_rep_tools.src.classes.dbhandler import DBHandler
import zas_rep_tools.src.utils.db_helper as db_helper
from zas_rep_tools.src.utils.helpers import Status
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester

class TestZAScorpusDBHandlerDBHandler(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_dbhandler_initialisation_000(self):
        db = DBHandler(mode=self.mode)
        assert not db.get_db()
        assert not db._attachedDBs_config
        assert not db._tables_dict
        assert not db._attributs_dict
        assert not db.dbnames

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_corpus_with_general_init_as_plaintext_500(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(['info', 'documents']))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['language'].should.be.equal(language)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['platform_name'].should.be.equal(platform_name)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['license'].should.be.equal(license)
        db.get_all_attr()['version'].should.be.equal(version)
        db.get_all_attr()['template_name'].should.be.equal(template_name)
        db.get_all_attr()['source'].should.be.equal(source)
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_corpus_with_additional_columns_and_template_in_documents_501(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        new_additional_columns = [
         ('gender', 'TEXT'),
         ('age', 'TEXT'),
         ('eye_colour', 'TEXT')]
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source, cols_and_types_in_doc=new_additional_columns)
        col_and_types_for_twitter_docs = DBHandler.templates['twitter']
        col_and_types_of_docs_tabel_in_the_current_db = db.colt('documents')
        default_col_and_typ_for_docs = [('blogger_id', 'INTEGER'), ('text', 'BLOB')]
        input_col_and_types = col_and_types_for_twitter_docs + new_additional_columns + default_col_and_typ_for_docs
        copy_of_db_data = copy.deepcopy(col_and_types_of_docs_tabel_in_the_current_db)
        for item_from_db in col_and_types_of_docs_tabel_in_the_current_db:
            for item_from_input in input_col_and_types:
                if item_from_db[0] == item_from_input[0] and item_from_db[1] == item_from_input[1].split(' ')[0]:
                    copy_of_db_data.remove(item_from_db)

        assert copy_of_db_data or True

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_corpus_just_with_additional_columns_in_documents_502(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        new_additional_columns = [
         ('gender', 'TEXT'),
         ('age', 'TEXT'),
         ('eye_colour', 'TEXT')]
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, platform_name, license=license, version=version, source=source, cols_and_types_in_doc=new_additional_columns)
        col_and_types_of_docs_tabel_in_the_current_db = db.colt('documents')
        default_col_and_typ_for_docs = [('blogger_id', 'INTEGER'), ('text', 'BLOB')]
        input_col_and_types = new_additional_columns + default_col_and_typ_for_docs
        copy_of_db_data = copy.deepcopy(col_and_types_of_docs_tabel_in_the_current_db)
        for item_from_db in col_and_types_of_docs_tabel_in_the_current_db:
            for item_from_input in input_col_and_types:
                if item_from_db[0] == item_from_input[0] and item_from_db[1] == item_from_input[1].split(' ')[0]:
                    copy_of_db_data.remove(item_from_db)

        assert copy_of_db_data or True

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_corpus_with_special_init_as_plaintext_503(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(['info', 'documents']))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['language'].should.be.equal(language)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['platform_name'].should.be.equal(platform_name)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['license'].should.be.equal(license)
        db.get_all_attr()['version'].should.be.equal(version)
        db.get_all_attr()['template_name'].should.be.equal(template_name)
        db.get_all_attr()['source'].should.be.equal(source)
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_dbhandler_creation_of_encrypted_empty_corpus_with_general_init_504(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source, encryption_key=encryption_key)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(['info', 'documents']))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['language'].should.be.equal(language)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['platform_name'].should.be.equal(platform_name)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['license'].should.be.equal(license)
        db.get_all_attr()['version'].should.be.equal(version)
        db.get_all_attr()['template_name'].should.be.equal(template_name)
        db.get_all_attr()['source'].should.be.equal(source)
        db.encryption().should.be.equal('encrypted')
        db.is_encrypted.should.be.equal(True)

    @attr(status='stable')
    def test_dbhandler_creation_of_encrypted_empty_corpus_with_special_init_505(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source, encryption_key=encryption_key)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(['info', 'documents']))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['language'].should.be.equal(language)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['platform_name'].should.be.equal(platform_name)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['license'].should.be.equal(license)
        db.get_all_attr()['version'].should.be.equal(version)
        db.get_all_attr()['template_name'].should.be.equal(template_name)
        db.get_all_attr()['source'].should.be.equal(source)
        db.encryption().should.be.equal('encrypted')
        db.is_encrypted.should.be.equal(True)

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_stats_with_general_init_as_plaintext_506(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(db_helper.default_tables['stats'].keys()))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['version'].should.be.equal(version)
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_stats_with_special_init_as_plaintext_507(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.init_stats(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(db_helper.default_tables['stats'].keys()))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['version'].should.be.equal(version)
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_encrypted_stats_with_general_init_508(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        db_helper.default_tables['stats']
        set(db.tables()).should.be.equal(set(db_helper.default_tables['stats'].keys()))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['version'].should.be.equal(version)
        db.encryption().should.be.equal('encrypted')
        db.is_encrypted.should.be.equal(True)

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_encrypted_stats_with_special_init_509(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.init_stats(self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version, encryption_key=encryption_key)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(db_helper.default_tables['stats'].keys()))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['version'].should.be.equal(version)
        db.encryption().should.be.equal('encrypted')
        db.is_encrypted.should.be.equal(True)

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_DB_as_plaintext_510(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = 'testDB'
        db.initempty(self.tempdir_project_folder, name)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        db.tables().should.be.equal([])
        db.dbnames.should.be.equal(['main'])
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_dbhandler_creation_of_empty_DB_as_encrypted_511(self):
        self.prj_folder()
        db = DBHandler(mode=self.mode)
        name = 'testDB'
        encryption_key = 'testDB'
        db.initempty(self.tempdir_project_folder, name, encryption_key=encryption_key)
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        db.tables().should.be.equal([])
        db.dbnames.should.be.equal(['main'])
        db.encryption().should.be.equal('encrypted')
        db.is_encrypted.should.be.equal(True)

    @attr(status='stable')
    def test_connection_with_plain_text_blogger_corpus_plaintext_515(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables()).should.be.equal(set(['info', 'documents']))
        db.dbnames.should.be.equal(['main'])
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['language'].should.be.equal(language)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['platform_name'].should.be.equal(platform_name)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['id'].should.be.equal(corpus_id)
        db.get_all_attr()['license'].should.be.equal(license)
        db.get_all_attr()['version'].should.be.equal(version)
        db.get_all_attr()['template_name'].should.be.equal(template_name)
        db.get_all_attr()['source'].should.be.equal(source)
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_connection_with_plain_text_twitter_corpus_encrypted_516(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key=encryption_key)
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['language'].should.be.equal(language)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['platform_name'].should.be.equal(platform_name)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['id'].should.be.equal(corpus_id)
        db.get_all_attr()['license'].should.be.equal(license)
        db.get_all_attr()['version'].should.be.equal(version)
        db.get_all_attr()['template_name'].should.be.equal(template_name)
        db.get_all_attr()['source'].should.be.equal(source)
        db.encryption().should.be.equal('encrypted')

    @attr(status='stable')
    def test_connection_with_plain_text_blogger_stats_plaintext_517(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        version = self.configer.init_info_data['blogger']['version']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['corpus_id'].should.be.equal(corpus_id)
        db.get_all_attr()['id'].should.be.equal(stats_id)
        db.get_all_attr()['version'].should.be.equal(version)
        db.encryption().should.be.equal('plaintext')

    @attr(status='stable')
    def test_connection_with_plain_text_twitter_stats_encrypted_518(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key=encryption_key)
        db.get_all_attr()['name'].should.be.equal(name)
        db.get_all_attr()['visibility'].should.be.equal(visibility)
        db.get_all_attr()['typ'].should.be.equal(typ)
        db.get_all_attr()['corpus_id'].should.be.equal(corpus_id)
        db.get_all_attr()['id'].should.be.equal(stats_id)
        db.get_all_attr()['version'].should.be.equal(version)
        db.encryption().should.be.equal('encrypted')

    @attr(status='stable')
    def test_attach_plaintext_corpus_db_520(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        db.status().should.be.equal('manyDB')
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))[0])
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        try:
            db._db.cursor
            db.get_db().cursor
            assert True
        except:
            assert False

        set(db.tables(dbname=attached_db_name)).should.be.equal(set(['info', 'documents']))
        db.dbnames.should.be.equal(['main', attached_db_name])
        db.get_all_attr(attached_db_name)['name'].should.be.equal(name)
        db.get_all_attr(attached_db_name)['language'].should.be.equal(language)
        db.get_all_attr(attached_db_name)['visibility'].should.be.equal(visibility)
        db.get_all_attr(attached_db_name)['platform_name'].should.be.equal(platform_name)
        db.get_all_attr(attached_db_name)['typ'].should.be.equal(typ)
        db.get_all_attr(attached_db_name)['id'].should.be.equal(corpus_id)
        db.get_all_attr(attached_db_name)['license'].should.be.equal(license)
        db.get_all_attr(attached_db_name)['version'].should.be.equal(version)
        db.get_all_attr(attached_db_name)['template_name'].should.be.equal(template_name)
        db.get_all_attr(attached_db_name)['source'].should.be.equal(source)

    @attr(status='stable')
    def test_attach_encrypted_corpus_db_521(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        db.status().should.be.equal('manyDB')
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de))[0])
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        platform_name = self.configer.init_info_data['twitter']['platform_name']
        license = self.configer.init_info_data['twitter']['license']
        template_name = self.configer.init_info_data['twitter']['template_name']
        version = self.configer.init_info_data['twitter']['version']
        source = self.configer.init_info_data['twitter']['source']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'corpus'
        db.get_all_attr(attached_db_name)['name'].should.be.equal(name)
        db.get_all_attr(attached_db_name)['language'].should.be.equal(language)
        db.get_all_attr(attached_db_name)['visibility'].should.be.equal(visibility)
        db.get_all_attr(attached_db_name)['platform_name'].should.be.equal(platform_name)
        db.get_all_attr(attached_db_name)['typ'].should.be.equal(typ)
        db.get_all_attr(attached_db_name)['id'].should.be.equal(corpus_id)
        db.get_all_attr(attached_db_name)['license'].should.be.equal(license)
        db.get_all_attr(attached_db_name)['version'].should.be.equal(version)
        db.get_all_attr(attached_db_name)['template_name'].should.be.equal(template_name)
        db.get_all_attr(attached_db_name)['source'].should.be.equal(source)

    @attr(status='stable')
    def test_attach_plaintext_stats_db_522(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        db.status().should.be.equal('manyDB')
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))[0])
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        version = self.configer.init_info_data['blogger']['version']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'stats'
        db.get_all_attr(attached_db_name)['name'].should.be.equal(name)
        db.get_all_attr(attached_db_name)['visibility'].should.be.equal(visibility)
        db.get_all_attr(attached_db_name)['typ'].should.be.equal(typ)
        db.get_all_attr(attached_db_name)['corpus_id'].should.be.equal(corpus_id)
        db.get_all_attr(attached_db_name)['id'].should.be.equal(stats_id)
        db.get_all_attr(attached_db_name)['version'].should.be.equal(version)

    @attr(status='stable')
    def test_attach_encrypted_stats_db_523(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        db.status().should.be.equal('manyDB')
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de))[0])
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.get_all_attr(attached_db_name)['name'].should.be.equal(name)
        db.get_all_attr(attached_db_name)['visibility'].should.be.equal(visibility)
        db.get_all_attr(attached_db_name)['typ'].should.be.equal(typ)
        db.get_all_attr(attached_db_name)['corpus_id'].should.be.equal(corpus_id)
        db.get_all_attr(attached_db_name)['id'].should.be.equal(stats_id)
        db.get_all_attr(attached_db_name)['version'].should.be.equal(version)

    @attr(status='stable')
    def test_reattaching_one_plaintext_db_530(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))[0])
        dbnames = db.dbnames
        db.status().should.be.equal('manyDB')
        db.reattach()
        db.dbnames.should.be.equal(dbnames)
        db.status().should.be.equal('manyDB')
        db.reattach(dbname=attached_db_name)
        db.dbnames.should.be.equal(dbnames)
        db.status().should.be.equal('manyDB')

    @attr(status='stable')
    def test_reattaching_one_encrypted_db_531(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de))[0])
        dbnames = db.dbnames
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False
        db.status().should.be.equal('manyDB')
        db.reattach()
        db.dbnames.should.be.equal(dbnames)
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False
        db.reattach(dbname=attached_db_name)
        db.dbnames.should.be.equal(dbnames)
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False

    @attr(status='stable')
    def test_reattaching_many_attached_dbs_532(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        attached_db_name_1 = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de))[0])
        attached_db_name_2 = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))[0])
        dbnames = db.dbnames
        if len(db._attachedDBs_config) == 2:
            assert True
        else:
            assert False
        db.status().should.be.equal('manyDB')
        db.reattach()
        db.dbnames.should.be.equal(dbnames)
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 2:
            assert True
        else:
            assert False
        db.reattach(dbname=attached_db_name_1)
        db.reattach(dbname=attached_db_name_2)
        db.dbnames.should.be.equal(dbnames)
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 2:
            assert True
        else:
            assert False

    @attr(status='stable')
    def test_detaching_one_encrypted_db_540(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de))[0])
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False
        db.detach()
        db.status().should.be.equal('oneDB')
        if len(db._attachedDBs_config) == 0:
            assert True
        else:
            assert False
        if len(db.dbnames) == 1:
            assert True
        else:
            assert False
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False
        db.detach(dbname=attached_db_name)
        db.status().should.be.equal('oneDB')
        if len(db._attachedDBs_config) == 0:
            assert True
        else:
            assert False
        if len(db.dbnames) == 1:
            assert True
        else:
            assert False

    @attr(status='stable')
    def test_detaching_one_plaintext_db_541(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        attached_db_name = '_' + os.path.basename(os.path.splitext(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))[0])
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False
        db.detach()
        db.status().should.be.equal('oneDB')
        if len(db._attachedDBs_config) == 0:
            assert True
        else:
            assert False
        if len(db.dbnames) == 1:
            assert True
        else:
            assert False
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 1:
            assert True
        else:
            assert False
        db.detach(dbname=attached_db_name)
        db.status().should.be.equal('oneDB')
        if len(db._attachedDBs_config) == 0:
            assert True
        else:
            assert False
        if len(db.dbnames) == 1:
            assert True
        else:
            assert False

    @attr(status='stable')
    def test_detaching_many_attached_dbs_542(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        path_to_db1 = os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en)
        path_to_db2 = os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de)
        path_to_db3 = os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en)
        db.attach(path_to_db1)
        db.attach(path_to_db2, encryption_key='corpus')
        db.attach(path_to_db3)
        attached_db_name_1 = '_' + os.path.basename(os.path.splitext(path_to_db1)[0])
        attached_db_name_2 = '_' + os.path.basename(os.path.splitext(path_to_db2)[0])
        attached_db_name_3 = '_' + os.path.basename(os.path.splitext(path_to_db3)[0])
        if len(db._attachedDBs_config) == 3:
            assert True
        else:
            assert False
        db.detach()
        db.status().should.be.equal('oneDB')
        if len(db._attachedDBs_config) == 0:
            assert True
        else:
            assert False
        if len(db.dbnames) == 1:
            assert True
        else:
            assert False
        db.attach(path_to_db1)
        db.attach(path_to_db2, encryption_key='corpus')
        db.attach(path_to_db3)
        db.status().should.be.equal('manyDB')
        if len(db._attachedDBs_config) == 3:
            assert True
        else:
            assert False
        if len(db.dbnames) == 4:
            assert True
        else:
            assert False
        db.detach(dbname=attached_db_name_1)
        if len(db._attachedDBs_config) == 2:
            assert True
        else:
            assert False
        db.status().should.be.equal('manyDB')
        db.detach(attached_db_name_2)
        db.detach(attached_db_name_3)
        db.status().should.be.equal('oneDB')
        if len(db._attachedDBs_config) == 0:
            assert True
        else:
            assert False
        if len(db.dbnames) == 1:
            assert True
        else:
            assert False

    @attr(status='stable')
    def test_dbhandler_insert_new_column_555(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version)
        columns_before = db.col('replications')
        db.add_col('replications', 'context_L1', 'JSON')
        db.add_col('replications', 'context_R1', 'JSON')
        columns_after = db.col('replications')
        assert 'context_L1' not in columns_after and False
        if 'context_R1' not in columns_after:
            assert False
            assert abs(len(columns_after) - len(columns_before)) != 2 and False

    @attr(status='stable')
    def test_insert_many_values_with_insertdict_560(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        if num_of_insertions != db.rownum('documents'):
            assert False
            assert int(db.all_inserts_counter) != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_insert_dict_with_many_values_with_lazyinsert_561(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.lazyinsert('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_insert_one_value_with_insertdict_562(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=False)['blogger']
        num_of_insertions = 1
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[0]):
            if col != 'text':
                if inp_dict[col] != value:
                    assert False
                else:
                    assert True
            elif value != json.dumps(inp_dict[col]):
                assert False

    @attr(status='stable')
    def test_insert_dict_with_one_value_with_lazyinsert_563(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=False)['blogger']
        num_of_insertions = 1
        db.lazyinsert('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[0]):
            if col != 'text':
                if inp_dict[col] != value:
                    assert False
                else:
                    assert True
            elif value != json.dumps(inp_dict[col]):
                assert False

    @attr(status='stable')
    def test_insert_one_row_with_insert_list_564(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger'][0]
        num_of_insertions = 1
        db.insertlist('documents', inp_list)
        assert num_of_insertions != db.rownum('documents') and False
        for item1, item2 in zip(db.getall('documents')[0], inp_list):
            if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                if not False:
                    raise AssertionError
            elif item1 != json.dumps(item2):
                assert False

    @attr(status='stable')
    def test_insert_one_row_with_insert_lazyinsert_565(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger'][0]
        num_of_insertions = 1
        db.lazyinsert('documents', inp_list)
        assert num_of_insertions != db.rownum('documents') and False
        for item1, item2 in zip(db.getall('documents')[0], inp_list):
            if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                if not False:
                    raise AssertionError
            elif item1 != json.dumps(item2):
                assert False

    @attr(status='stable')
    def test_insert_many_rows_with_insertlist_566(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger']
        num_of_insertions = len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'])
        db.insertlist('documents', inp_list)
        if num_of_insertions != db.rownum('documents'):
            assert False
            for i in xrange(num_of_insertions):
                for item1, item2 in zip(db.getall('documents')[i], inp_list[i]):
                    if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                        if not False:
                            raise AssertionError
                    elif item1 != json.dumps(item2):
                        assert False

            assert int(db.all_inserts_counter) != db.rownum('documents') and False

    @attr(status='stable')
    def test_insert_many_rows_with_lazyinsert_567(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger']
        num_of_insertions = len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'])
        db.lazyinsert('documents', inp_list)
        assert num_of_insertions != db.rownum('documents') and False
        for i in xrange(num_of_insertions):
            for item1, item2 in zip(db.getall('documents')[i], inp_list[i]):
                if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                    if not False:
                        raise AssertionError
                elif item1 != json.dumps(item2):
                    assert False

    @attr(status='stable')
    def test_insert_dict_with_hybrid_number_of_values_with_cashed_lazyinsert_568(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode, use_cash=True)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_dict1 = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions1 = len(random.choice(inp_dict1.values()))
        db.lazyinsert('documents', inp_dict1)
        inp_dict2 = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=False)['blogger']
        num_of_insertions2 = 1
        db.lazyinsert('documents', inp_dict2)
        cash_copy = copy.deepcopy(db._cashed_dict[0]['Thread0']['main']['documents'])
        num_of_insertions = num_of_insertions1 + num_of_insertions2
        for k, v in cash_copy.iteritems():
            assert len(v) == num_of_insertions

        for k, v in inp_dict1.iteritems():
            for item in v:
                cash_copy[k].remove(item)

        for k, v in inp_dict2.iteritems():
            cash_copy[k].remove(v)

        for k, v in cash_copy.iteritems():
            if v:
                assert False

    @attr(status='stable')
    def test_insert_dict_with_many_values_with_cashed_lazyinsert_569(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode, use_cash=True)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.lazyinsert('documents', inp_dict)
        if db._cashed_dict:
            assert True
            db.commit()
            for commit_num, commit_data in db._cashed_dict.iteritems():
                for thread_name, thread_data in commit_data.iteritems():
                    for dbname, dbdata in thread_data.iteritems():
                        for table_name, inp_obj in thread_data.iteritems():
                            if inp_obj:
                                assert False

            assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_insert_dict_with_one_value_with_cashed_lazyinsert_570(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode, use_cash=True)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=False)['blogger']
        num_of_insertions = 1
        db.lazyinsert('documents', inp_dict)
        if db._cashed_dict:
            assert True
            db.commit()
            for commit_num, commit_data in db._cashed_dict.iteritems():
                for thread_name, thread_data in commit_data.iteritems():
                    for dbname, dbdata in thread_data.iteritems():
                        for table_name, inp_obj in thread_data.iteritems():
                            if inp_obj:
                                assert False

            assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[0]):
            if col != 'text':
                if inp_dict[col] != value:
                    assert False
                else:
                    assert True
            elif value != json.dumps(inp_dict[col]):
                assert False

    @attr(status='stable')
    def test_insert_many_rows_with_lazyinsert_aslist_571(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode, use_cash=True)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger']
        num_of_insertions = len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'])
        db.lazyinsert('documents', inp_list)
        if db._cashed_list:
            assert True
            db.commit()
            for commit_num, commit_data in db._cashed_list.iteritems():
                for thread_name, thread_data in commit_data.iteritems():
                    for dbname, dbdata in thread_data.iteritems():
                        for table_name, inp_obj in thread_data.iteritems():
                            if inp_obj:
                                assert False

            assert num_of_insertions != db.rownum('documents') and False
        for i in xrange(num_of_insertions):
            for item1, item2 in zip(db.getall('documents')[i], inp_list[i]):
                if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                    if not False:
                        raise AssertionError
                elif item1 != json.dumps(item2):
                    assert False

    @attr(status='stable')
    def test_insert_one_row_with_insert_lazyinsert_aslist_572(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode, use_cash=True)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger'][0]
        num_of_insertions = 1
        db.lazyinsert('documents', inp_list)
        if db._cashed_list:
            assert True
            db.commit()
            for commit_num, commit_data in db._cashed_list.iteritems():
                for thread_name, thread_data in commit_data.iteritems():
                    for dbname, dbdata in thread_data.iteritems():
                        for table_name, inp_obj in thread_data.iteritems():
                            if inp_obj:
                                assert False

            assert num_of_insertions != db.rownum('documents') and False
        for item1, item2 in zip(db.getall('documents')[0], inp_list):
            if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                if not False:
                    raise AssertionError
            elif item1 != json.dumps(item2):
                assert False

    @attr(status='stable')
    def test_insert_hybrid_number_of_rows_with_lazyinsert_573(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode, use_cash=True)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list1 = self.configer.docs_row_values(token=True, unicode_str=True)['blogger'][0]
        num_of_insertions1 = 1
        db.lazyinsert('documents', inp_list1)
        assert len(db._cashed_list[0]['Thread0']['main']['documents']) == num_of_insertions1
        if db._cashed_dict:
            p(db._cashed_dict, c='m')
        inp_list2 = self.configer.docs_row_values(token=True, unicode_str=True)['blogger']
        num_of_insertions2 = len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'])
        db.lazyinsert('documents', inp_list2)
        assert len(db._cashed_list[0]['Thread0']['main']['documents']) == num_of_insertions1 + num_of_insertions2

    @attr(status='stable')
    def test_work_with_json_list_575(self):
        self.prj_folder()
        self.test_dbs()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        db = DBHandler(mode=self.mode)
        db.init('corpus', self.tempdir_project_folder, 'blogger', 'de', 'extern', platform_name='blogs', license='MIT', template_name='blogger', version='2', source='LanguageGoldMine', corpus_id='7614')
        inp_list = self.configer.docs_row_values(token=True, unicode_str=True)['blogger']
        num_of_insertions = len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'])
        db.insertlist('documents', inp_list)
        assert num_of_insertions != db.rownum('documents') and False
        for i in xrange(num_of_insertions):
            for item1, item2 in zip(db.getall('documents')[i], inp_list[i]):
                if isinstance(item2, (list, dict, tuple)) or item1 != item2:
                    if not False:
                        raise AssertionError
                elif item1 != json.dumps(item2):
                    assert False

        for row in inp_list:
            input_id = row[id_index]
            text_element = row[text_index]
            c = db.execute(('select json_extract("text", "$[0]") from documents WHERE id={};').format(input_id), thread_name='test')

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_580_1(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], db._intern_getter('documents')['out_obj'].fetchall()[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_with_limit_and_offset_580_2(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        cur = db._db.cursor()
        columns = inp_dict.keys()
        rows = inp_dict.values()
        rows_with_intergetter = list(db._intern_getter('documents', limit=3, offset=3)['out_obj'].fetchall())
        if isinstance(db.execute('SELECT * FROM documents LIMIT 3 OFFSET 3;'), Status):
            assert False
            print 'This Execution failed and the Status Object was send'
        rows_with_execute = db.execute('SELECT * FROM documents LIMIT 3 OFFSET 3;').fetchall()
        rows_with_intergetter.should.be.equal(rows_with_execute)

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_with_where_condition_581(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            id_to_search = item[id_index]
            getted_item = db._intern_getter('documents', where=('id = {}').format(id_to_search))['out_obj'].fetchall()[0]
            for i1, i2 in zip(item, getted_item):
                if isinstance(i1, (list, dict, tuple)):
                    i1 = json.dumps(i1)
                if i1 != i2:
                    assert False

        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            id_to_search = item[id_index]
            getted_item = db._intern_getter('documents', where=[('id = {}').format(id_to_search)])['out_obj'].fetchall()[0]
            for i1, i2 in zip(item, getted_item):
                if isinstance(i1, (list, dict, tuple)):
                    i1 = json.dumps(i1)
                if i1 != i2:
                    assert False

        id_collector = []
        items_collector = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            id_to_search = item[id_index]
            if len(id_collector) >= 3:
                where_cond_list = [ ('id={}').format(doc_id) for doc_id in id_collector ]
                getted_item = db._intern_getter('documents', where=where_cond_list, connector_where='OR')['out_obj'].fetchall()
                for item1, item2 in zip(items_collector, getted_item):
                    for i1, i2 in zip(item1, item2):
                        if isinstance(i1, (list, dict, tuple)):
                            i1 = json.dumps(i1)
                        if i1 != i2:
                            assert False

            else:
                id_collector.append(id_to_search)
                items_collector.append(item)

        elem_index_to_use = 0
        index_of_token_in_text_elemen_to_use = 0
        text_token_to_search = ''
        matched_items_to_compare = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            id_to_search = item[id_index]
            getted_item = db._intern_getter('documents', where=[('id = {}').format(id_to_search)])['out_obj'].fetchall()[0]
            text_elem_1 = item[text_index]
            text_elem_2 = json.loads(getted_item[text_index])
            if elem_index_to_use == 0:
                text_token_to_search = text_elem_1[index_of_token_in_text_elemen_to_use]
                item[text_index] = json.dumps(item[text_index]) if isinstance(item[text_index], list) else item[text_index]
                matched_items_to_compare.append(tuple(item))
            elif text_elem_1[index_of_token_in_text_elemen_to_use].lower() == text_token_to_search.lower():
                item[text_index] = json.dumps(item[text_index]) if isinstance(item[text_index], list) else item[text_index]
                matched_items_to_compare.append(tuple(item))
            elem_index_to_use += 1

        if not isinstance(text_token_to_search, unicode):
            print "'text_token_to_search' is not an unicode string."
            assert False
            where_cond = ('json_extract("text", "$[{}]") LIKE "{}" ').format(index_of_token_in_text_elemen_to_use, text_token_to_search.encode('utf-8'))
            extracted_items_from_db = db._intern_getter('documents', where=where_cond)['out_obj'].fetchall()
            assert matched_items_to_compare != extracted_items_from_db and False

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_for_certain_columns_582(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        if num_of_insertions != db.rownum('documents'):
            assert False
            columns = inp_dict.keys()
            rows = inp_dict.values()
            id_index = self.configer.columns_in_doc_table['blogger'].index('id')
            text_index = self.configer.columns_in_doc_table['blogger'].index('text')
            getted_ids_from_db = db._intern_getter('documents', columns='id')['out_obj'].fetchall()
            extracted_ids_from_input_data = []
            for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
                extracted_ids_from_input_data.append((item[id_index],))

            assert getted_ids_from_db != extracted_ids_from_input_data and False
        getted_ids_from_db = db._intern_getter('documents', columns=['id'])['out_obj'].fetchall()
        extracted_ids_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_ids_from_input_data.append((item[id_index],))

        if getted_ids_from_db != extracted_ids_from_input_data:
            assert False
            getted_ids_from_db = db._intern_getter('documents', columns=['id', 'text'])['out_obj'].fetchall()
            extracted_ids_from_input_data = []
            for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
                extracted_ids_from_input_data.append((item[id_index], json.dumps(item[text_index])))

            assert getted_ids_from_db != extracted_ids_from_input_data and False

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_with_additional_select_conditions_on_example_of_json1_583(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        index_of_token_to_extract_from_text_element = 0
        getted_text_tokens_from_db = db._intern_getter('documents', select=('json_extract("text", "$[{}]")').format(index_of_token_to_extract_from_text_element))['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_text_tokens_from_input_data.append((item[text_index][index_of_token_to_extract_from_text_element],))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)
        index_of_token_to_extract_from_text_element = 0
        getted_text_tokens_from_db = db._intern_getter('documents', select=[('json_extract("text", "$[{}]")').format(index_of_token_to_extract_from_text_element)])['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_text_tokens_from_input_data.append((item[text_index][index_of_token_to_extract_from_text_element],))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)
        index_of_1_token_to_extract_from_text_element = 0
        index_of_2_token_to_extract_from_text_element = 1
        getted_text_tokens_from_db = db._intern_getter('documents', select=[('json_extract("text", "$[{}]")').format(index_of_1_token_to_extract_from_text_element), ('json_extract("text", "$[{}]")').format(index_of_2_token_to_extract_from_text_element)])['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item1, item2 in zip(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'], getted_text_tokens_from_db):
            extracted_text_tokens_from_input_data.append((item1[text_index][index_of_1_token_to_extract_from_text_element], item1[text_index][index_of_2_token_to_extract_from_text_element]))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_with_select_and_columns_combined_584(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        gender_index = self.configer.columns_in_doc_table['blogger'].index('gender')
        index_of_token_to_extract_from_text_element = 0
        getted_text_tokens_from_db = db._intern_getter('documents', columns='id', select=('json_extract("text", "$[{}]")').format(index_of_token_to_extract_from_text_element))['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_text_tokens_from_input_data.append((item[id_index], item[text_index][index_of_token_to_extract_from_text_element]))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)
        index_of_1_token_to_extract_from_text_element = 0
        index_of_2_token_to_extract_from_text_element = 1
        getted_text_tokens_from_db = db._intern_getter('documents', columns=['id', 'gender'], select=[('json_extract("text", "$[{}]")').format(index_of_1_token_to_extract_from_text_element), ('json_extract("text", "$[{}]")').format(index_of_2_token_to_extract_from_text_element)])['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_text_tokens_from_input_data.append((item[id_index], item[gender_index], item[text_index][index_of_1_token_to_extract_from_text_element], item[text_index][index_of_2_token_to_extract_from_text_element]))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_with_select_and_columns_combined_585(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        gender_index = self.configer.columns_in_doc_table['blogger'].index('gender')
        index_of_token_to_extract_from_text_element = 0
        getted_text_tokens_from_db = db._intern_getter('documents', columns='id', select=('json_extract("text", "$[{}]")').format(index_of_token_to_extract_from_text_element))['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_text_tokens_from_input_data.append((item[id_index], item[text_index][index_of_token_to_extract_from_text_element]))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)
        index_of_1_token_to_extract_from_text_element = 0
        index_of_2_token_to_extract_from_text_element = 1
        getted_text_tokens_from_db = db._intern_getter('documents', columns=['id', 'gender'], select=[('json_extract("text", "$[{}]")').format(index_of_1_token_to_extract_from_text_element), ('json_extract("text", "$[{}]")').format(index_of_2_token_to_extract_from_text_element)])['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            extracted_text_tokens_from_input_data.append((item[id_index], item[gender_index], item[text_index][index_of_1_token_to_extract_from_text_element], item[text_index][index_of_2_token_to_extract_from_text_element]))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)

    @attr(status='stable')
    def test_get_all_rows_from_db_with_intern_getter_with_columns_and_where_combined_586(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        id_index = self.configer.columns_in_doc_table['blogger'].index('id')
        text_index = self.configer.columns_in_doc_table['blogger'].index('text')
        gender_index = self.configer.columns_in_doc_table['blogger'].index('gender')
        index_of_token_to_extract_from_text_element = 0
        getted_text_tokens_from_db = db._intern_getter('documents', columns='id', where="gender='m'")['out_obj'].fetchall()
        extracted_text_tokens_from_input_data = []
        for item in self.configer.docs_row_values(token=True, unicode_str=True)['blogger']:
            if item[gender_index] == 'm':
                extracted_text_tokens_from_input_data.append((item[id_index],))

        getted_text_tokens_from_db.should.be.equal(extracted_text_tokens_from_input_data)

    @attr(status='stable')
    def test_getall_587(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_getlistlazy_588(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        assert next(db.getlistlazy('documents', just_check_existence=True))
        columns = inp_dict.keys()
        rows = inp_dict.values()
        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], list(db.getlistlazy('documents'))[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_getdictlazy_589(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        assert next(db.getdictlazy('documents', just_check_existence=True))
        getted_output_from_db = list(db.getdictlazy('documents'))
        for i in xrange(num_of_insertions):
            for col in self.configer.columns_in_doc_table['blogger']:
                value_from_input = inp_dict[col][i]
                value_from_output = getted_output_from_db[i][col]
                if col != 'text':
                    if value_from_input != value_from_output:
                        assert False
                    else:
                        assert True
                elif value_from_output != json.dumps(value_from_input):
                    assert False

    @attr(status='stable')
    def test_getdictlazy_for_certain_columns_and_select_590(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        columns_to_get = [
         'id', 'text']
        select_to_get = ['gender']
        getted_output_from_db = list(db.getdictlazy('documents', columns=columns_to_get, select=select_to_get))
        for i in xrange(num_of_insertions):
            for col in columns_to_get + select_to_get:
                value_from_input = inp_dict[col][i]
                value_from_output = getted_output_from_db[i][col]
                if col != 'text':
                    if value_from_input != value_from_output:
                        assert False
                    else:
                        assert True
                elif value_from_output != json.dumps(value_from_input):
                    assert False

    @attr(status='stable')
    def test_getlazy_591(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        assert num_of_insertions != db.rownum('documents') and False
        columns = inp_dict.keys()
        rows = inp_dict.values()
        assert next(db.getdictlazy('documents', just_check_existence=True))
        columns_to_get = [
         'id', 'text']
        select_to_get = ['gender']
        getted_output_from_db = list(db.lazyget('documents', columns=columns_to_get, select=select_to_get, output='dict'))
        for i in xrange(num_of_insertions):
            for col in columns_to_get + select_to_get:
                value_from_input = inp_dict[col][i]
                value_from_output = getted_output_from_db[i][col]
                if col != 'text':
                    if value_from_input != value_from_output:
                        assert False
                    else:
                        assert True
                elif value_from_output != json.dumps(value_from_input):
                    assert False

        for i in xrange(num_of_insertions):
            for col, value in zip(self.configer.columns_in_doc_table['blogger'], list(db.lazyget('documents', output='list'))[i]):
                if col != 'text':
                    if inp_dict[col][i] != value:
                        assert False
                    else:
                        assert True
                elif value != json.dumps(inp_dict[col][i]):
                    assert False

    @attr(status='stable')
    def test_roleback_changes_db_610(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        db.insertdict('documents', inp_dict)
        columns = inp_dict.keys()
        rows = inp_dict.values()
        rowNum_bevore = 0
        if db.rollback() != num_of_insertions:
            assert False
            rowsNum_after_rollback = db.rownum('documents')
            assert rowNum_bevore != rowsNum_after_rollback and False

    @attr(status='stable')
    def test_uniq_DB_encryption_620(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        tables_from_plaintextDB = db.tables()
        assert db.is_encrypted != False and False
        s = db.encrypte('corpus')
        if not s['status']:
            assert False
            assert db.encryption() != 'encrypted' and False
        if db.is_encrypted != True:
            assert False
            tables_from_encryptedDB = db.tables()
            assert tables_from_plaintextDB != tables_from_encryptedDB and False

    @attr(status='stable')
    def test_DB_encryption_with_attachedDBs_621(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        tables_from_plaintextDB = db.tables()
        dbname_bevore_encryption = db.dbnames
        s = db.encrypte('corpus')
        assert s['status'] or False
        if db.encryption() != 'encrypted':
            assert False
            assert db.is_encrypted != True and False
        tables_from_encryptedDB = db.tables()
        dbname_after_encryption = db.dbnames
        if tables_from_plaintextDB != tables_from_encryptedDB:
            assert False
            assert dbname_bevore_encryption != dbname_after_encryption and False

    @attr(status='stable')
    def test_uniq_DB_decryption_622(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        tables_from_plaintextDB = db.tables()
        s = db.decrypte()
        if not s['status']:
            assert False
            assert db.encryption() != 'plaintext' and False
        if db.is_encrypted != False:
            assert False
            tables_from_encryptedDB = db.tables()
            assert tables_from_plaintextDB != tables_from_encryptedDB and False

    @attr(status='stable')
    def test_DB_decryption_with_attachedDBs_623(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_corp_de), encryption_key='corpus')
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        tables_from_plaintextDB = db.tables()
        dbnames_bevore_encryption = db.dbnames
        s = db.decrypte()
        assert s['status'] or False
        if db.encryption() != 'plaintext':
            assert False
            assert db.is_encrypted != False and False
        tables_from_encryptedDB = db.tables()
        dbnames_after_encryption = db.dbnames
        if tables_from_plaintextDB != tables_from_encryptedDB:
            assert False
            assert dbnames_bevore_encryption[0] != dbnames_after_encryption[0] and False

    @attr(status='stable')
    def test_DB_change_encryption_key_624(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_twitter_encrypted_stats_de), encryption_key='stats')
        newkey = 'newkey'
        db.change_key(newkey)
        assert db._encryption_key == newkey

    @attr(status='stable')
    def test_get_attr_from_connected_db_625(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.get_attr('name').should.be.equal(name)
        db.get_attr('language').should.be.equal(language)
        db.get_attr('visibility').should.be.equal(visibility)
        db.get_attr('platform_name').should.be.equal(platform_name)
        db.get_attr('typ').should.be.equal(typ)
        db.get_attr('id').should.be.equal(corpus_id)
        db.get_attr('license').should.be.equal(license)
        db.get_attr('version').should.be.equal(version)
        db.get_attr('template_name').should.be.equal(template_name)
        db.get_attr('source').should.be.equal(source)

    @attr(status='stable')
    def test_get_attr_from_attached_db_626(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        fname = os.path.splitext(os.path.basename(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en)))[0]
        stats_db_name = '_' + fname
        db.attach(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_stats_en))
        db.get_attr('name', stats_db_name).should.be.equal(name)
        db.get_attr('visibility', stats_db_name).should.be.equal(visibility)
        db.get_attr('typ', stats_db_name).should.be.equal('stats')
        db.get_attr('corpus_id', stats_db_name).should.be.equal(corpus_id)
        db.get_attr('id', stats_db_name).should.be.equal(stats_id)
        db.get_attr('version', stats_db_name).should.be.equal(version)

    @attr(status='stable')
    def test_drop_table_from_db_db_700(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        tables_bevore = db.tables()
        db.drop_table('documents')
        tables_after = db.tables()
        if len(tables_bevore) - len(tables_after) != 1:
            assert False
            tables_bevore.remove('documents')
            assert tables_bevore != tables_after and False

    @attr(status='stable')
    def test_update_value_701(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        row1_bevore = db.getall('documents', where='rowid=1')
        db.update('documents', ['gender'], ['unknown'], where='rowid=1')
        row1_after = db.getall('documents', where='rowid=1')
        assert row1_after[0][3] != 'unknown' and False
        db.close()

    @attr(status='stable')
    def test_addNewtable_702(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        newtableName = 'tempTables'
        attributs_names_with_types_as_str = [
         ('text', 'TEXT'),
         ('age', 'TEXT')]
        tables_bevore = db.tables()
        db.addtable(newtableName, attributs_names_with_types_as_str, dbname='main')
        tables_after = db.tables()
        set(db.col(newtableName)).should.be.equal(set(['text', 'age']))
        if tables_bevore == tables_after:
            assert False
            tables_bevore.append(newtableName)
            assert set(tables_bevore) != set(tables_after) and False

    @attr(status='stable')
    def test_init_default_indexes_in_corpus_bevore_insertions_750(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        number_of_indexes_which_should_be_initialized = 0
        for table_name, index_query_list in db_helper.default_indexes['corpus'].iteritems():
            for index_query in index_query_list:
                number_of_indexes_which_should_be_initialized += 1

        number_of_indexes_bevor = len(db.indexes())
        db.init_default_indexes()
        number_of_indexes_after = len(db.indexes())
        assert number_of_indexes_bevor + number_of_indexes_which_should_be_initialized != number_of_indexes_after and False

    @attr(status='stable')
    def test_init_default_indexes_in_corpus_after_insertions_751(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['blogger']['name']
        language = self.configer.init_info_data['blogger']['language']
        visibility = self.configer.init_info_data['blogger']['visibility']
        platform_name = self.configer.init_info_data['blogger']['platform_name']
        license = self.configer.init_info_data['blogger']['license']
        template_name = self.configer.init_info_data['blogger']['template_name']
        version = self.configer.init_info_data['blogger']['version']
        source = self.configer.init_info_data['blogger']['source']
        encryption_key = self.configer.init_info_data['blogger']['encryption_key']['corpus']
        corpus_id = self.configer.init_info_data['blogger']['id']['corpus']
        stats_id = self.configer.init_info_data['blogger']['id']['stats']
        typ = 'corpus'
        db.init_corpus(self.tempdir_project_folder, name, language, visibility, platform_name, license=license, template_name=template_name, version=version, source=source)
        inp_dict = self.configer.docs_row_dict(token=True, unicode_str=True, all_values=True)['blogger']
        num_of_insertions = len(random.choice(inp_dict.values()))
        number_of_indexes_which_should_be_initialized = 0
        for table_name, index_query_list in db_helper.default_indexes['corpus'].iteritems():
            for index_query in index_query_list:
                number_of_indexes_which_should_be_initialized += 1

        number_of_indexes_bevor = len(db.indexes())
        db.insertdict('documents', inp_dict)
        if num_of_insertions != db.rownum('documents'):
            assert False
            columns = inp_dict.keys()
            rows = inp_dict.values()
            for i in xrange(num_of_insertions):
                for col, value in zip(self.configer.columns_in_doc_table['blogger'], db.getall('documents')[i]):
                    if col != 'text':
                        if inp_dict[col][i] != value:
                            assert False
                        else:
                            assert True
                    elif value != json.dumps(inp_dict[col][i]):
                        assert False

            db.init_default_indexes()
            number_of_indexes_after = len(db.indexes())
            assert number_of_indexes_bevor + number_of_indexes_which_should_be_initialized != number_of_indexes_after and False

    @attr(status='stable')
    def test_init_default_indexes_in_stats_bevore_insertions_752(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        name = self.configer.init_info_data['twitter']['name']
        language = self.configer.init_info_data['twitter']['language']
        visibility = self.configer.init_info_data['twitter']['visibility']
        version = self.configer.init_info_data['twitter']['version']
        encryption_key = self.configer.init_info_data['twitter']['encryption_key']['stats']
        corpus_id = self.configer.init_info_data['twitter']['id']['corpus']
        stats_id = self.configer.init_info_data['twitter']['id']['stats']
        typ = 'stats'
        db.init(typ, self.tempdir_project_folder, name, language, visibility, corpus_id=corpus_id, version=version)
        number_of_indexes_which_should_be_initialized = 0
        for table_name, index_query_list in db_helper.default_indexes['stats'].iteritems():
            for index_query in index_query_list:
                number_of_indexes_which_should_be_initialized += 1

        number_of_indexes_bevor = len(db.indexes())
        db.init_default_indexes()
        number_of_indexes_after = len(db.indexes())
        assert number_of_indexes_bevor + number_of_indexes_which_should_be_initialized != number_of_indexes_after and False

    @attr(status='stable')
    def test_backup_routine_800(self):
        self.prj_folder()
        self.test_dbs()
        db = DBHandler(mode=self.mode)
        db.connect(os.path.join(self.tempdir_testdbs, self.db_blogger_plaintext_corp_en))
        dir_num_bevore = len(os.listdir(self.tempdir_testdbs))
        db._backup('main')
        dir_num_after = len(os.listdir(self.tempdir_testdbs))
        assert dir_num_bevore + 1 == dir_num_after
        assert 'main' in db._created_backups