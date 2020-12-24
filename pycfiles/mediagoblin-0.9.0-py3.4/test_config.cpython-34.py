# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_config.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 3986 bytes
import pkg_resources
from mediagoblin.init import config
CARROT_CONF_GOOD = pkg_resources.resource_filename('mediagoblin.tests', 'fake_carrot_conf_good.ini')
CARROT_CONF_EMPTY = pkg_resources.resource_filename('mediagoblin.tests', 'fake_carrot_conf_empty.ini')
CARROT_CONF_BAD = pkg_resources.resource_filename('mediagoblin.tests', 'fake_carrot_conf_bad.ini')
FAKE_CONFIG_SPEC = pkg_resources.resource_filename('mediagoblin.tests', 'fake_config_spec.ini')

def test_read_mediagoblin_config():
    this_conf, validation_results = config.read_mediagoblin_config(CARROT_CONF_EMPTY, FAKE_CONFIG_SPEC)
    assert this_conf['carrotapp']['carrotcake'] == False
    assert this_conf['carrotapp']['num_carrots'] == 1
    assert 'encouragement_phrase' not in this_conf['carrotapp']
    assert this_conf['celery']['EAT_CELERY_WITH_CARROTS'] == True
    this_conf, validation_results = config.read_mediagoblin_config(CARROT_CONF_GOOD, FAKE_CONFIG_SPEC)
    assert this_conf['carrotapp']['carrotcake'] == True
    assert this_conf['carrotapp']['num_carrots'] == 88
    assert this_conf['carrotapp']['encouragement_phrase'] == "I'd love it if you eat your carrots!"
    assert this_conf['carrotapp']['blah_blah'] == 'blah!'
    assert this_conf['celery']['EAT_CELERY_WITH_CARROTS'] == False
    this_conf, validation_results = config.read_mediagoblin_config(CARROT_CONF_BAD, FAKE_CONFIG_SPEC)
    assert this_conf['carrotapp']['carrotcake'] == 'slobber'
    assert this_conf['carrotapp']['num_carrots'] == 'GROSS'
    assert this_conf['carrotapp']['encouragement_phrase'] == '586956856856'
    assert this_conf['carrotapp']['blah_blah'] == 'blah!'
    assert this_conf['celery']['EAT_CELERY_WITH_CARROTS'] == 'pants'


def test_generate_validation_report():
    this_conf, validation_results = config.read_mediagoblin_config(CARROT_CONF_EMPTY, FAKE_CONFIG_SPEC)
    report = config.generate_validation_report(this_conf, validation_results)
    assert report is None
    this_conf, validation_results = config.read_mediagoblin_config(CARROT_CONF_GOOD, FAKE_CONFIG_SPEC)
    report = config.generate_validation_report(this_conf, validation_results)
    assert report is None
    this_conf, validation_results = config.read_mediagoblin_config(CARROT_CONF_BAD, FAKE_CONFIG_SPEC)
    report = config.generate_validation_report(this_conf, validation_results)
    assert report.startswith('There were validation problems loading this config file:\n--------------------------------------------------------')
    expected_warnings = [
     'carrotapp:carrotcake = the value "slobber" is of the wrong type.',
     'carrotapp:num_carrots = the value "GROSS" is of the wrong type.',
     'celery:EAT_CELERY_WITH_CARROTS = the value "pants" is of the wrong type.']
    warnings = report.splitlines()[2:]
    assert len(warnings) == 3
    for warning in expected_warnings:
        if not warning in warnings:
            raise AssertionError