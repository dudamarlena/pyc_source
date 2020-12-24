# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_yum_list_installed.py
# Compiled at: 2020-04-16 14:56:28
import pytest, doctest
from insights import SkipComponent
from insights.parsers import yum_list
from insights.parsers.yum_list import YumListInstalled
from insights.tests import context_wrap
EMPTY = ('\nInstalled Packages\n').strip()
EXPIRED_EMPTY = ('\nRepodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast\nInstalled Packages\n').strip()
EXPIRED_WITH_DATA = ('\nRepodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast\nInstalled Packages\nbash.x86_64                               4.4.23-1.fc28                 @updates\n').strip()
SIMPLE = ('\nInstalled Packages\nbash.x86_64                               4.4.23-1.fc28                 @updates\n').strip()
WRAPPED_LINE = ('\nInstalled Packages\nNetworkManager-bluetooth.x86_64           1:1.10.10-1.fc28              @updates\nNetworkManager-config-connectivity-fedora.noarch\n                                          1:1.10.10-1.fc28              @updates\nNetworkManager-glib.x86_64                1:1.10.10-1.fc28              @updates\nNetworkManager-libnm.x86_64               1:1.10.10-1.fc28              @updates\nclucene-contribs-lib.x86_64               2.3.3.4-31.20130812.e8e3d20git.fc28\n                                                                        @fedora\nclucene-core.x86_64                       2.3.3.4-31.20130812.e8e3d20git.fc28\n                                                                        @fedora\n').strip()
COMMANDLINE = '\nInstalled Packages\njdk1.8.0_121.x86_64                       2000:1.8.0_121-fcs            @@commandline\n'
HEADER_FOOTER_JUNK = '\nLoaded plugins: product-id, search-disabled-repos, subscription-manager\nRepodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast\nInstalled Packages\nGConf2.x86_64                    3.2.6-8.el7             @rhel-7-server-rpms\nGeoIP.x86_64                     1.5.0-11.el7            @anaconda/7.3\nImageMagick.x86_64               6.7.8.9-15.el7_2        @rhel-7-server-rpms\nNetworkManager.x86_64            1:1.4.0-17.el7_3        installed\nNetworkManager.x86_64            1:1.8.0-9.el7           installed\nNetworkManager-config-server.noarch\n                                 1:1.8.0-9.el7           installed\nUploading Enabled Repositories Report\nLoaded plugins: priorities, product-id, rhnplugin, rhui-lb, subscription-\n              : manager, versionlock\n'

def test_empty():
    ctx = context_wrap(EMPTY)
    with pytest.raises(SkipComponent):
        YumListInstalled(ctx)


def test_simple():
    ctx = context_wrap(SIMPLE)
    rpms = YumListInstalled(ctx)
    rpm = rpms.newest('bash')
    assert rpm is not None
    assert rpm.epoch == '0'
    assert rpm.version == '4.4.23'
    assert rpm.release == '1.fc28'
    assert rpm.arch == 'x86_64'
    assert rpm.repo == 'updates'
    return


def test_expired_cache_with_data():
    ctx = context_wrap(EXPIRED_WITH_DATA)
    rpms = YumListInstalled(ctx)
    assert rpms.expired_cache is True


def test_expired_cache_no_data():
    ctx = context_wrap(EXPIRED_EMPTY)
    with pytest.raises(SkipComponent):
        YumListInstalled(ctx)


def test_wrapped():
    ctx = context_wrap(WRAPPED_LINE)
    rpms = YumListInstalled(ctx)
    rpm = rpms.newest('NetworkManager-bluetooth')
    assert rpm is not None
    assert rpm.epoch == '1'
    assert rpm.version == '1.10.10'
    assert rpm.release == '1.fc28'
    assert rpm.arch == 'x86_64'
    assert rpm.repo == 'updates'
    rpm = rpms.newest('NetworkManager-config-connectivity-fedora')
    assert rpm is not None
    assert rpm.epoch == '1'
    assert rpm.version == '1.10.10'
    assert rpm.release == '1.fc28'
    assert rpm.arch == 'noarch'
    assert rpm.repo == 'updates'
    rpm = rpms.newest('clucene-contribs-lib')
    assert rpm is not None
    assert rpm.epoch == '0'
    assert rpm.version == '2.3.3.4'
    assert rpm.release == '31.20130812.e8e3d20git.fc28'
    assert rpm.arch == 'x86_64'
    assert rpm.repo == 'fedora'
    rpm = rpms.newest('clucene-core')
    assert rpm is not None
    assert rpm.epoch == '0'
    assert rpm.version == '2.3.3.4'
    assert rpm.release == '31.20130812.e8e3d20git.fc28'
    assert rpm.arch == 'x86_64'
    assert rpm.repo == 'fedora'
    return


def test_commandline():
    ctx = context_wrap(COMMANDLINE)
    rpms = YumListInstalled(ctx)
    rpm = rpms.newest('jdk1.8.0_121')
    assert rpm is not None
    assert rpm.epoch == '2000'
    assert rpm.version == '1.8.0_121'
    assert rpm.release == 'fcs'
    assert rpm.arch == 'x86_64'
    assert rpm.repo == 'commandline'
    return


def test_multiple_stanza():
    ctx = context_wrap(HEADER_FOOTER_JUNK)
    rpms = YumListInstalled(ctx)
    rpm = rpms.newest('GConf2')
    assert rpm is not None
    assert rpm.epoch == '0'
    assert rpm.version == '3.2.6'
    assert rpm.release == '8.el7'
    assert rpm.arch == 'x86_64'
    assert rpm.repo == 'rhel-7-server-rpms'
    rpm = rpms.newest('NetworkManager-config-server')
    assert rpm is not None
    assert rpm.epoch == '1'
    assert rpm.version == '1.8.0'
    assert rpm.release == '9.el7'
    assert rpm.arch == 'noarch'
    assert rpm.repo == 'installed'
    return


def test_doc_examples():
    env = {'installed_rpms': YumListInstalled(context_wrap(HEADER_FOOTER_JUNK))}
    failed, total = doctest.testmod(yum_list, globs=env)
    assert failed == 0