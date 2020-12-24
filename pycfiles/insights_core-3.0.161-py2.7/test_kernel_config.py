# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_kernel_config.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import kernel_config, SkipException
from insights.parsers.kernel_config import KernelConf
from insights.tests import context_wrap
KERNEL_CONFIG = ('\n#\n# Automatically generated file; DO NOT EDIT.\n# Linux/x86_64 3.10.0-693.el7.x86_64 Kernel Configuration\n#\nCONFIG_64BIT=y\nCONFIG_X86_64=y\nCONFIG_X86=y\nCONFIG_INSTRUCTION_DECODER=y\nCONFIG_OUTPUT_FORMAT="elf64-x86-64"\nCONFIG_ARCH_DEFCONFIG="arch/x86/configs/x86_64_defconfig"\nCONFIG_ARCH_MMAP_RND_COMPAT_BITS_MIN=8\nCONFIG_PREEMPT_RT_FULL=y\n').strip()
KERNEL_CONFIG_2 = ('\n#\n# Automatically generated file; DO NOT EDIT.\n# Linux/x86_64 3.10.0-693.el7.x86_64 Kernel Configuration\n#\nCONFIG_64BIT=y\nCONFIG_X86_64=y\nCONFIG_X86=y\nCONFIG_INSTRUCTION_DECODER=y\nCONFIG_OUTPUT_FORMAT="elf64-x86-64"\nCONFIG_ARCH_DEFCONFIG="arch/x86/configs/x86_64_defconfig"\nCONFIG_ARCH_MMAP_RND_COMPAT_BITS_MIN=8\n# CONFIG_PREEMPT_RT_FULL is not set\n# CONFIG_IRQ_DOMAIN_DEBUG is not set\n').strip()
KCONFIG_FILE_PATH = '/boot/config-3.10.0-327.28.3.rt56.235.el7.x86_64'
KERNEL_CONFIG_NO = ('\n').strip()
KERNEL_CONFIG_NO_2 = ('\n#\n# Automatically generated file; DO NOT EDIT.\n# Linux/x86_64 3.10.0-693.el7.x86_64 Kernel Configuration\n#\n').strip()
KCONFIG_FILE_PATH_NO = ''

def test_kernel_config():
    r = KernelConf(context_wrap(KERNEL_CONFIG, KCONFIG_FILE_PATH))
    assert r.get('CONFIG_PREEMPT_RT_FULL') == 'y'
    assert len(r) == 8
    assert r.kconf_file == 'config-3.10.0-327.28.3.rt56.235.el7.x86_64'
    r = KernelConf(context_wrap(KERNEL_CONFIG_2, KCONFIG_FILE_PATH))
    assert len(r) == 7
    with pytest.raises(SkipException) as (exc):
        r = KernelConf(context_wrap(KERNEL_CONFIG_NO, KCONFIG_FILE_PATH))
    assert 'No Contents' in str(exc)


def test_docs():
    env = {'kconfig': KernelConf(context_wrap(KERNEL_CONFIG, KCONFIG_FILE_PATH))}
    failed, total = doctest.testmod(kernel_config, globs=env)
    assert failed == 0