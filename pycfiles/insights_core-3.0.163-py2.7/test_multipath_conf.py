# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_multipath_conf.py
# Compiled at: 2019-11-14 13:57:46
import pytest
from insights.parsers import SkipException
from insights.parsers import multipath_conf
from insights.parsr.query import first, last
from insights.tests import context_wrap
CONF = ('\nblacklist {\n       device {\n               vendor  "IBM"\n               product "3S42"       #DS4200 Product 10\n       }\n       device {\n               vendor  "HP"\n               product "*"\n       }\n}').strip()
MULTIPATH_CONF_INFO = ('\ndefaults {\n       udev_dir                /dev\n       path_selector           "round-robin 0"\n       user_friendly_names     yes\n}\n\nmultipaths {\n       multipath {\n               alias                   yellow\n               path_grouping_policy    multibus\n       }\n       multipath {\n               wwid                    1DEC_____321816758474\n               alias                   red\n       }\n}\n\ndevices {\n       device {\n               path_selector           "round-robin 0"\n               no_path_retry           queue\n       }\n       device {\n               vendor                  "COMPAQ  "\n               path_grouping_policy    multibus\n       }\n}\n\nblacklist {\n       wwid 26353900f02796769\n       devnode "^hd[a-z]"\n}\n\n').strip()
INPUT_EMPTY = ''

def test_multipath_conf():
    multipath_conf_info = multipath_conf.MultipathConf(context_wrap(MULTIPATH_CONF_INFO))
    assert multipath_conf_info.get('defaults').get('udev_dir') == '/dev'
    assert multipath_conf_info.get('defaults').get('path_selector') == 'round-robin 0'
    assert multipath_conf_info.get('multipaths')[1].get('alias') == 'red'
    assert multipath_conf_info.get('devices')[0].get('no_path_retry') == 'queue'
    assert multipath_conf_info.get('blacklist').get('devnode') == '^hd[a-z]'


def test_multipath_conf_initramfs():
    multipath_conf_initramfs = multipath_conf.MultipathConfInitramfs(context_wrap(MULTIPATH_CONF_INFO))
    assert multipath_conf_initramfs.get('defaults').get('udev_dir') == '/dev'
    assert multipath_conf_initramfs.get('defaults').get('path_selector') == 'round-robin 0'
    assert multipath_conf_initramfs.get('multipaths')[1].get('alias') == 'red'
    assert multipath_conf_initramfs.get('devices')[0].get('no_path_retry') == 'queue'
    assert multipath_conf_initramfs.get('blacklist').get('devnode') == '^hd[a-z]'


def test_multipath_conf_trees():
    for c in (multipath_conf.MultipathConfTree,
     multipath_conf.MultipathConfTreeInitramfs):
        conf = c(context_wrap(CONF))
        assert len(conf['blacklist']) == 1
        assert len(conf['blacklist']['device']) == 2
        assert len(conf['blacklist']['device']['vendor']) == 2
        assert len(conf['blacklist']['device']['product']) == 2
        assert conf['blacklist']['device']['vendor'][first].value == 'IBM'
        assert conf['blacklist']['device']['vendor'][last].value == 'HP'
        assert conf['blacklist']['device']['product'][first].value == '3S42'
        assert conf['blacklist']['device']['product'][last].value == '*'


def test_empty_multipath_conf_tree():
    with pytest.raises(SkipException) as (e_info):
        multipath_conf.MultipathConfTree(context_wrap(INPUT_EMPTY))
    assert 'Empty content.' in str(e_info.value)
    with pytest.raises(SkipException) as (e_info):
        multipath_conf.MultipathConfTreeInitramfs(context_wrap(INPUT_EMPTY))
    assert 'Empty content.' in str(e_info.value)


def test_empty_multipath_conf():
    with pytest.raises(SkipException) as (e_info):
        multipath_conf.MultipathConfParser(context_wrap(INPUT_EMPTY))
    assert 'Empty content.' in str(e_info.value)