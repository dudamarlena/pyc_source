# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_autofs_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import autofs_conf
from insights.tests import context_wrap
AUTOFS_CONF = "\n#\n# Define default options for autofs.\n# Heavily edited for brevity by removing most of the useless comments\n#\n[ autofs ]\n#\n# timeout - set the default mount timeout in secons. The internal\n#\t    program default is 10 minutes, but the default installed\n#\t    configuration overrides this and sets the timeout to 5\n#\t    minutes to be consistent with earlier autofs releases.\n#\ntimeout = 300\n#\n# browse_mode - maps are browsable by default.\n#\nbrowse_mode = no\n#\n# mount_nfs_default_protocol - specify the default protocol used by\n# \t\t\t       mount.nfs(8). Since we can't identify\n# \t\t\t       the default automatically we need to\n# \t\t\t       set it in our configuration.\n#\n#mount_nfs_default_protocol = 3\nmount_nfs_default_protocol = 4\n#\n# Define global options for the amd parser within autofs.\n#\n[ amd ]\n#\n# Override the internal default with the same timeout that\n# is used by the override in the autofs configuration, sanity\n# only change.\n#\ndismount_interval = 300\n#\n# map_type = file\n#\n"

class TestAutoFSConf:

    def test_standard_autofs_conf(self):
        cfg = autofs_conf.AutoFSConf(context_wrap(AUTOFS_CONF))
        assert cfg.get(' autofs ', 'timeout') == '300'
        assert cfg.get(' autofs ', 'browse_mode') == 'no'
        assert cfg.get(' autofs ', 'mount_nfs_default_protocol') == '4'
        assert cfg.get(' amd ', 'dismount_interval') == '300'
        assert not cfg.has_option(' amd ', 'map_type')
        assert 'nfs' not in cfg