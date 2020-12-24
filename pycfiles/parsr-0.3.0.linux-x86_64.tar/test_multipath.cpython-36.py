# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/tests/test_multipath.py
# Compiled at: 2019-05-28 16:54:46
# Size of source mod 2**32: 3957 bytes
from parsr.examples.multipath_conf import loads
EXAMPLE = '\n# This is a basic configuration file with some examples, for device mapper\n# multipath.\n#\n# For a complete list of the default configuration values, run either\n# multipath -t\n# or\n# multipathd show config\n#\n# For a list of configuration options with descriptions, see the multipath.conf\n# man page\n\n## By default, devices with vendor = "IBM" and product = "S/390.*" are\n## blacklisted. To enable mulitpathing on these devies, uncomment the\n## following lines.\n#blacklist_exceptions {\n#\tdevice {\n#\t\tvendor\t"IBM"\n#\t\tproduct\t"S/390.*"\n#\t}\n#}\n\n## Use user friendly names, instead of using WWIDs as names.\ndefaults {\n    user_friendly_names yes\n    find_multipaths yes\n}\n##\n## Here is an example of how to configure some standard options.\n##\n#\n#defaults {\n#\tudev_dir\t\t/dev\n#\tpolling_interval \t10\n#\tselector\t\t"round-robin 0"\n#\tpath_grouping_policy\tmultibus\n#\tprio\t\t\talua\n#\tpath_checker\t\treadsector0\n#\trr_min_io\t\t100\n#\tmax_fds\t\t\t8192\n#\trr_weight\t\tpriorities\n#\tfailback\t\timmediate\n#\tno_path_retry\t\tfail\n#\tuser_friendly_names\tyes\n#}\n##\n## The wwid line in the following blacklist section is shown as an example\n## of how to blacklist devices by wwid.  The 2 devnode lines are the\n## compiled in default blacklist. If you want to blacklist entire types\n## of devices, such as all scsi devices, you should use a devnode line.\n## However, if you want to blacklist specific devices, you should use\n## a wwid line.  Since there is no guarantee that a specific device will\n## not change names on reboot (from /dev/sda to /dev/sdb for example)\n## devnode lines are not recommended for blacklisting specific devices.\n##\n#blacklist {\n#       wwid 26353900f02796769\n#\tdevnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"\n#\tdevnode "^hd[a-z]"\n#}\n#multipaths {\n#\tmultipath {\n#\t\twwid\t\t\t3600508b4000156d700012000000b0000\n#\t\talias\t\t\tyellow\n#\t\tpath_grouping_policy\tmultibus\n#\t\tpath_checker\t\treadsector0\n#\t\tpath_selector\t\t"round-robin 0"\n#\t\tfailback\t\tmanual\n#\t\trr_weight\t\tpriorities\n#\t\tno_path_retry\t\t5\n#\t}\n#\tmultipath {\n#\t\twwid\t\t\t1DEC_____321816758474\n#\t\talias\t\t\tred\n#\t}\n#}\n#devices {\n#\tdevice {\n#\t\tvendor\t\t\t"COMPAQ  "\n#\t\tproduct\t\t\t"HSV110 (C)COMPAQ"\n#\t\tpath_grouping_policy\tmultibus\n#\t\tpath_checker\t\treadsector0\n#\t\tpath_selector\t\t"round-robin 0"\n#\t\thardware_handler\t"0"\n#\t\tfailback\t\t15\n#\t\trr_weight\t\tpriorities\n#\t\tno_path_retry\t\tqueue\n#\t}\n#\tdevice {\n#\t\tvendor\t\t\t"COMPAQ  "\n#\t\tproduct\t\t\t"MSA1000         "\n#\t\tpath_grouping_policy\tmultibus\n#\t}\n#}\n#'
CONF = '\nblacklist {\n       device {\n               vendor  "IBM"\n               product "3S42"       #DS4200 Product 10\n       }\n       device {\n               vendor  "HP"\n               product "*"\n       }\n}'.strip()
MULTIPATH_CONF_INFO = '\ndefaults {\n       udev_dir                /dev\n       path_selector           "round-robin 0"\n       user_friendly_names     yes\n}\n\nmultipaths {\n       multipath {\n               alias                   yellow\n               path_grouping_policy    multibus\n       }\n       multipath {\n               wwid                    1DEC_____321816758474\n               alias                   red\n       }\n}\n\ndevices {\n       device {\n               path_selector           "round-robin 0"\n               no_path_retry           queue\n       }\n       device {\n               vendor                  "COMPAQ  "\n               path_grouping_policy    multibus\n       }\n}\n\nblacklist {\n       wwid 26353900f02796769\n       devnode "^hd[a-z]"\n}\n\n'.strip()

def test_multipath_example():
    res = loads(EXAMPLE)
    assert res['defaults']['user_friendly_names'].value == 'yes'


def test_multipath_conf():
    res = loads(CONF)
    assert res['blacklist']['device'][0]['product'].value == '3S42'


def xtest_multipath_conf_info():
    res = loads(MULTIPATH_CONF_INFO)
    if not res['defaults']['path_selector'].value == 'round-robin 0':
        raise AssertionError
    elif not res['multipaths']['multipath'][1]['wwid'].value == '1DEC_____321816758474':
        raise AssertionError