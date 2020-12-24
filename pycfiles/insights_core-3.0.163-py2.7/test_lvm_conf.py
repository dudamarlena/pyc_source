# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lvm_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.lvm import LvmConf
from insights.tests import context_wrap
LVM_CONF = ('\nlocking_type = 1\n#locking_type = 2\n# volume_list = [ "vg1", "vg2/lvol1", "@tag1", "@*" ]\nvolume_list = [ "vg2", "vg3/lvol3", "@tag2", "@*" ]\n# filter = [ "a|loop|", "r|/dev/hdc|", "a|/dev/ide|", "r|.*|" ]\n\nfilter = [ "r/sda[0-9]*$/",  "a/sd.*/" ]\nfilter = [ "a/sda[0-9]*$/",  "r/sd.*/" ] #Required for EMC PP - Do Not Modify this Line\nshell {\nhistory_size = 100\n}\n\ntest_bad_json = [ "partial\n').strip()

def test_lvm_conf():
    lvm_conf_output = LvmConf(context_wrap(LVM_CONF))
    assert lvm_conf_output['locking_type'] == 1
    assert lvm_conf_output['volume_list'] == ['vg2', 'vg3/lvol3', '@tag2', '@*']
    assert lvm_conf_output['filter'] == ['a/sda[0-9]*$/', 'r/sd.*/']
    assert lvm_conf_output['test_bad_json'] == '[ "partial'