# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_irqbalance.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import IrqbalanceSysconfig
from insights.tests import context_wrap
IRQBALANCE_SYSCONF_TEST = ('\n# irqbalance is a daemon process that distributes interrupts across\n# CPUS on SMP systems. The default is to rebalance once every 10\n# seconds. This is the environment file that is specified to systemd via the\n# EnvironmentFile key in the service unit file (or via whatever method the init\n# system you\'re using has.\n#\n# ONESHOT=yes\n# after starting, wait for a minute, then look at the interrupt\n# load and balance it once; after balancing exit and do not change\n# it again.\n#IRQBALANCE_ONESHOT=yes\n\n#\n# IRQBALANCE_BANNED_CPUS\n# 64 bit bitmask which allows you to indicate which cpu\'s should\n# be skipped when reblancing irqs. Cpu numbers which have their\n# corresponding bits set to one in this mask will not have any\n# irq\'s assigned to them on rebalance\n#\nIRQBALANCE_BANNED_CPUS=f8\n\n#\n# IRQBALANCE_ARGS\n# append any args here to the irqbalance daemon as documented in the man page\n#\nIRQBALANCE_ARGS="-d"\n').strip()

def test_irqbalance_conf():
    ret = IrqbalanceSysconfig(context_wrap(IRQBALANCE_SYSCONF_TEST))
    assert ret['IRQBALANCE_BANNED_CPUS'] == 'f8'
    assert 'IRQBALANCE_ARGS' in ret
    assert ret.get('IRQBALANCE_ARGS') == '-d'
    assert 'IRQBALANCE_ONESHOT' not in ret