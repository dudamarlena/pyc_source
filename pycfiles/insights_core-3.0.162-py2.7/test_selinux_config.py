# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_selinux_config.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.selinux_config import SelinuxConfig
from insights.tests import context_wrap
SELINUX_CONFIG = '\n# This file controls the state of SELinux on the system.\n# SELINUX= can take one of these three values:\n#     enforcing - SELinux security policy is enforced.\n#     permissive - SELinux prints warnings instead of enforcing.\n#     disabled - No SELinux policy is loaded.\nSELINUX=enforcing\n\n # SELINUXTYPE= can take one of three two values:\n #     targeted - Targeted processes are protected,\n #     minimum - Modification of targeted policy. Only selected processes are protected.\n #     mls - Multi Level Security protection.\nSELINUXTYPE=targeted\n\n'

def test_selinux_config():
    selinux_config = SelinuxConfig(context_wrap(SELINUX_CONFIG)).data
    assert selinux_config['SELINUX'] == 'enforcing'
    assert selinux_config.get('SELINUXTYPE') == 'targeted'
    assert len(selinux_config) == 2