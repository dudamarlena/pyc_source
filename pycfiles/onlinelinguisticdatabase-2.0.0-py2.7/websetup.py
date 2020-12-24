# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/websetup.py
# Compiled at: 2016-09-19 13:27:02
"""Setup the old application"""
import logging, os
from shutil import copyfile
import pylons.test
from onlinelinguisticdatabase.config.environment import load_environment
from onlinelinguisticdatabase.model.meta import Base, Session
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Commands to setup onlinelinguisticdatabase."""
    config = load_environment(conf.global_conf, conf.local_conf)
    log.info('Environment loaded.')
    Base.metadata.create_all(bind=Session.bind)
    filename = os.path.split(conf.filename)[(-1)]
    h.create_OLD_directories(config=config)
    log.info('Retrieving ISO-639-3 languages data.')
    languages = h.get_language_objects(filename, config)
    log.info('Creating a default administrator, contributor and viewer.')
    administrator = h.generate_default_administrator(config_filename=filename)
    contributor = h.generate_default_contributor(config_filename=filename)
    viewer = h.generate_default_viewer(config_filename=filename)
    if filename == 'test.ini':
        Base.metadata.drop_all(bind=Session.bind, checkfirst=True)
        log.info('Existing tables dropped.')
        Base.metadata.create_all(bind=Session.bind, checkfirst=True)
        log.info('Tables created.')
        Session.add_all(languages + [administrator, contributor, viewer])
        Session.commit()
    else:
        requests_tests_path = os.path.join(config['pylons.paths']['root'], 'tests', 'scripts', '_requests_tests.py')
        Base.metadata.create_all(bind=Session.bind, checkfirst=True)
        log.info('Tables created.')
        log.info('Creating default home and help pages.')
        homepage = h.generate_default_home_page()
        helppage = h.generate_default_help_page()
        log.info('Generating default application settings.')
        application_settings = h.generate_default_application_settings()
        log.info('Creating some useful tags and categories.')
        restricted_tag = h.generate_restricted_tag()
        foreign_word_tag = h.generate_foreign_word_tag()
        S = h.generate_s_syntactic_category()
        N = h.generate_n_syntactic_category()
        V = h.generate_v_syntactic_category()
        log.info('Adding defaults.')
        data = [administrator, contributor, viewer, homepage, helppage,
         application_settings, restricted_tag, foreign_word_tag]
        if config['add_language_data'] != '0':
            data += languages
        if config['empty_database'] == '0':
            Session.add_all(data)
            Session.commit()
        log.info('OLD successfully set up.')