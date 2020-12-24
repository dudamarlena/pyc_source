# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yakonfig/tests/test_yakonfig.py
# Compiled at: 2015-07-07 22:00:14
from __future__ import absolute_import, division, print_function
import argparse, logging, os, tempfile, pytest
from six import StringIO
from yakonfig import set_global_config, get_global_config, clear_global_config
import yakonfig.yakonfig as yakonfig_internals
logger = logging.getLogger(__name__)

@pytest.fixture
def reset_globals(request):
    """
    for fixture that makes each test run as if it were the first call
    to yakonfig
    """
    clear_global_config()


def test_yakonfig_simple(reset_globals):
    YAML_TEXT_ONE = StringIO('\npipeline_property1: run_fast\npipeline_property2: no_errors\n')
    config = set_global_config(YAML_TEXT_ONE)
    assert get_global_config() is config
    assert config['pipeline_property1'] == 'run_fast'
    assert config['pipeline_property2'] == 'no_errors'


@pytest.fixture
def monkeypatch_open(request):

    def other_open(*args, **kwargs):
        fh = StringIO('\nk1: v1\nk2: \n - v21\n')
        fh.__exit__ = lambda x, y, z: None
        fh.__enter__ = lambda : fh
        return fh

    real_open = yakonfig_internals.Loader.open
    yakonfig_internals.Loader.open = other_open

    def fin():
        yakonfig_internals.Loader.open = real_open

    request.addfinalizer(fin)


def test_include_yaml_abstract(reset_globals, monkeypatch_open):
    YAML_TEXT_TWO = StringIO('\napp_one:\n  one: car\n\napp_two:\n  bad: [cat, horse]\n  good: !include_yaml /some-path-that-will-not-be-used\n')
    config = set_global_config(YAML_TEXT_TWO)
    assert get_global_config() is config
    sub_config = get_global_config('app_two')
    assert sub_config is config['app_two']
    assert sub_config['good'] == dict(k1='v1', k2=['v21'])


def test_include_abstract(reset_globals, monkeypatch_open):
    YAML_TEXT_TWO = StringIO('\napp_one:\n  one: car\n\napp_two:\n  bad: [cat, horse]\n  good: !include /some-path-that-will-not-be-used\n')
    config = set_global_config(YAML_TEXT_TWO)
    assert get_global_config() is config
    sub_config = get_global_config('app_two')
    assert sub_config is config['app_two']
    assert sub_config['good'] == dict(k1='v1', k2=['v21'])


def test_include_real_paths(reset_globals):
    t1 = tempfile.NamedTemporaryFile()
    t2 = tempfile.NamedTemporaryFile()
    t3 = tempfile.NamedTemporaryFile()
    y1 = '\nt1:\n  k3: !include_yaml %s\n  k4: !include_yaml %s\n' % (t2.name, os.path.basename(t3.name))
    print(y1)
    y2 = 'dog'
    y3 = 'two'
    t1.write(y1.encode('utf-8'))
    t2.write(y2.encode('utf-8'))
    t3.write(y3.encode('utf-8'))
    t1.flush()
    t2.flush()
    t3.flush()
    config = set_global_config(t1.name)
    assert get_global_config() is config
    print(config)
    sub_config = get_global_config('t1')
    assert sub_config is config['t1']
    assert sub_config['k3'] == y2
    assert sub_config['k4'] == y3