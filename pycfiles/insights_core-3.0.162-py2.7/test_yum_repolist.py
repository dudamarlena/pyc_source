# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_yum_repolist.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import yum
from insights.parsers.yum import YumRepoList
from insights.parsers import SkipException, ParseException
from insights.tests import context_wrap
import doctest, pytest
YUM_REPOLIST_CONTENT = ('\nLoaded plugins: product-id, search-disabled-repos, subscription-manager\nrepo id                                         repo name                status\nrhel-7-server-rpms/7Server/x86_64               Red Hat Enterprise Linux 10415\nrhel-7-server-satellite-6.1-rpms/x86_64         Red Hat Satellite 6.1 (f   660\nrhel-7-server-satellite-capsule-6.1-rpms/x86_64 Red Hat Satellite Capsul   265\nrhel-server-rhscl-7-rpms/7Server/x86_64         Red Hat Software Collect  4571\nrepolist: 15911\n\n').strip()
YUM_REPOLIST_CONTENT_NOPLUGINS = ('\nrepo id                                         repo name                status\nrhel-7-server-rpms/7Server/x86_64               Red Hat Enterprise Linux 10415\nrhel-7-server-satellite-6.1-rpms/x86_64         Red Hat Satellite 6.1 (f   660\nrhel-7-server-satellite-capsule-6.1-rpms/x86_64 Red Hat Satellite Capsul   265\nrhel-server-rhscl-7-rpms/7Server/x86_64         Red Hat Software Collect  4571\nrepolist: 15911\n\n').strip()
YUM_REPOLIST_CONTENT_EUS = ('\nLoaded plugins: product-id, rhnplugin, security, subscription-manager\nUpdating certificate-based repositories.\nrepo id                              repo name                            status\nclone-6u5-server-x86_64              clone-6u5-server-x86_64              3,787\nrhel-x86_64-server-6.2.aus           Red Hot Enterprise Linu              5,509\nrepolist: 3,787\n\n').strip()
YUM_REPOLIST_CONTENT_MISSING_STATUS = '\nLoaded plugins: product-id, rhnplugin, security, subscription-manager\nUpdating certificate-based repositories.\nrepo id                              repo name                            status\nclone-6u5-server-x86_64              clone-6u5-server-x86_64\nrepolist: 3,787\n'
YUM_REPOLIST_CONTENT_OUT_OF_DATE = '\nLoaded plugins: product-id, search-disabled-repos, subscription-manager\nRepodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast\nrepo id                              repo name                                          status\n!rhel-7-server-extras-rpms/x86_64    Red Hat Enterprise Linux 7 Server - Extras (RPMs)  877\n!rhel-7-server-rpms/7Server/x86_64   Red Hat Enterprise Linux 7 Server (RPMs)           20,704\nrepolist: 21,581\n'
YUM_REPOLIST_CONTENT_OUT_OF_DATE_AND_NOT_MATCH_METADATA = '\nLoaded plugins: product-id, search-disabled-repos, subscription-manager\nRepodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast\nrepo id                              repo name                                          status\n!rhel-7-server-extras-rpms/x86_64    Red Hat Enterprise Linux 7 Server - Extras (RPMs)  877\n*rhel-7-server-rpms/7Server/x86_64   Red Hat Enterprise Linux 7 Server (RPMs)           20,704\nrepolist: 21,581\n'
YUM_REPO_NO_REPO_NAME = ('\nLoaded plugins: enabled_repos_upload, package_upload, priorities, product-id,\n              : search-disabled-repos, security, subscription-manager\nrepo id                                                                               status\nLME_EPEL_6_x86_64                                                                     26123\nLME_HP_-_Software_Delivery_Repository_Firmware_Pack_for_ProLiant_-_6Server_-_Current   1163\nLME_HP_-_Software_Delivery_Repository_Scripting_Took_Kit_-_6Server                       17\nLME_HP_-_Software_Delivery_Repository_Service_Pack_for_ProLiant_-_6Server_-_Current    1861\nLME_HP_-_Software_Delivery_Repository_Smart_Update_Manager_-_6Server                     21\nrhel-6-server-optional-rpms                                                           11358\nrhel-6-server-rpms                                                                    19753\nrepolist: 60296\nUploading Enabled Reposistories Report\nPlugin "search-disabled-repos" requires API 2.7. Supported API is 2.6.\nLoaded plugins: priorities, product-id\n').strip()
YUM_REPOLIST_CONTENT_MISSING_END = '\nLoaded plugins: product-id, rhnplugin, security, subscription-manager\nUpdating certificate-based repositories.\nrepo id                              repo name                            status\nclone-6u5-server-x86_64              clone-6u5-server-x86_64              1234\n'
YUM_REPOLIST_CONTENT_EMPTY = '\nrepo id                              repo name                            status\n'
YUM_REPOLIST_DOC = ('\nLoaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager\nrepo id                                             repo name                                                                                                    status\nrhel-7-server-e4s-rpms/x86_64                       Red Hat Enterprise Linux 7 Server - Update Services for SAP Solutions (RPMs)                                 12,250\n!rhel-ha-for-rhel-7-server-e4s-rpms/x86_64          Red Hat Enterprise Linux High Availability (for RHEL 7 Server) Update Services for SAP Solutions (RPMs)         272\n*rhel-sap-hana-for-rhel-7-server-e4s-rpms/x86_64    RHEL for SAP HANA (for RHEL 7 Server) Update Services for SAP Solutions (RPMs)                                   21\nrepolist: 12,768\n').strip()
YUM_REPOLIST_DOC_NO_REPONAME = ('\nLoaded plugins: package_upload, product-id, search-disabled-repos, security, subscription-manager\nrepo id                                                                               status\nLME_EPEL_6_x86_64                                                                        26123\nLME_FSMLabs_Timekeeper_timekeeper                                                            2\nLME_HP_-_Software_Delivery_Repository_Firmware_Pack_for_ProLiant_-_6Server_-_Current      1163\nLME_HP_-_Software_Delivery_Repository_Scripting_Took_Kit_-_6Server                          17\nLME_HP_-_Software_Delivery_Repository_Service_Pack_for_ProLiant_-_6Server_-_Current       1915\nLME_HP_-_Software_Delivery_Repository_Smart_Update_Manager_-_6Server                        30\nLME_LME_Custom_Product_Mellanox_OFED                                                       114\nLME_LME_Custom_Product_OMD_RPMS                                                             14\nLME_LME_Custom_Product_RPMs                                                                  5\nLME_LME_Custom_Product_SNOW_Repository                                                       2\nrhel-6-server-optional-rpms                                                            10400+1\nrhel-6-server-rpms                                                                    18256+12\nrhel-6-server-satellite-tools-6.2-rpms                                                      55\nrepolist: 58096\n').strip()

def test_yum_repolist():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT))
    assert len(repo_list) == 4
    assert repo_list[0] == {'id': 'rhel-7-server-rpms/7Server/x86_64', 'name': 'Red Hat Enterprise Linux', 
       'status': '10415'}
    assert 'rhel-7-server-rpms/7Server/x86_64' in repo_list
    assert repo_list['rhel-7-server-rpms/7Server/x86_64'] == repo_list[0]
    assert repo_list.eus == []


def test_yum_repolist_noplugins():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_NOPLUGINS))
    assert len(repo_list) == 4
    assert repo_list[0] == {'id': 'rhel-7-server-rpms/7Server/x86_64', 'name': 'Red Hat Enterprise Linux', 
       'status': '10415'}
    assert 'rhel-7-server-rpms/7Server/x86_64' in repo_list
    assert repo_list['rhel-7-server-rpms/7Server/x86_64'] == repo_list[0]
    assert repo_list.eus == []


def test_eus():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_EUS))
    assert len(repo_list) == 2
    assert repo_list[0] == {'id': 'clone-6u5-server-x86_64', 'name': 'clone-6u5-server-x86_64', 
       'status': '3,787'}
    assert repo_list.eus == ['6.2.aus']


def test_rhel_repos():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT))
    assert len(repo_list.rhel_repos) == 4
    assert set(repo_list.rhel_repos) == set(['rhel-7-server-rpms',
     'rhel-7-server-satellite-6.1-rpms',
     'rhel-7-server-satellite-capsule-6.1-rpms',
     'rhel-server-rhscl-7-rpms'])


def test_rhel_repos_missing_status():
    with pytest.raises(ParseException) as (se):
        YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_MISSING_STATUS))
    assert 'Incorrect line:' in str(se)


def test_rhel_repos_empty():
    with pytest.raises(SkipException) as (se):
        YumRepoList(context_wrap(''))
    assert 'No repolist.' in str(se)
    with pytest.raises(SkipException) as (se):
        YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_EMPTY))
    assert 'No repolist.' in str(se)


def test_rhel_repos_out_of_date():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_OUT_OF_DATE))
    assert len(repo_list) == 2
    assert set(repo_list.rhel_repos) == set(['rhel-7-server-extras-rpms',
     'rhel-7-server-rpms'])


def test_rhel_repos_out_of_date_and_no_match_metadata():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_OUT_OF_DATE_AND_NOT_MATCH_METADATA))
    assert len(repo_list) == 2
    assert 'rhel-7-server-extras-rpms/x86_64' in repo_list
    assert 'rhel-7-server-rpms/7Server/x86_64' in repo_list
    assert '!rhel-7-server-extras-rpms/x86_64' == repo_list['rhel-7-server-extras-rpms/x86_64']['id']
    assert '*rhel-7-server-rpms/7Server/x86_64' == repo_list['rhel-7-server-rpms/7Server/x86_64']['id']


def test_invalid_get_type():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT))
    assert repo_list[YumRepoList] is None
    return


def test_doc_examples():
    env = {'repolist': YumRepoList(context_wrap(YUM_REPOLIST_DOC)), 
       'repolist_no_reponame': YumRepoList(context_wrap(YUM_REPOLIST_DOC_NO_REPONAME))}
    failed, total = doctest.testmod(yum, globs=env)
    assert failed == 0


def test_repos_without_repo_name():
    repo_list = YumRepoList(context_wrap(YUM_REPO_NO_REPO_NAME))
    assert 7 == len(repo_list)
    assert 2 == len(repo_list.rhel_repos)


def test_repos_without_ends():
    repo_list = YumRepoList(context_wrap(YUM_REPOLIST_CONTENT_MISSING_END))
    assert 1 == len(repo_list)
    assert 0 == len(repo_list.rhel_repos)