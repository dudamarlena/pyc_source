# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_freeipa_healthcheck_log.py
# Compiled at: 2020-03-25 13:10:41
import doctest
from insights.parsers import freeipa_healthcheck_log
from insights.parsers.freeipa_healthcheck_log import FreeIPAHealthCheckLog
from insights.tests import context_wrap
LONG_FREEIPA_HEALTHCHECK_LOG_OK = ('\n[{"source": "ipahealthcheck.ipa.roles", "check": "IPACRLManagerCheck",\n"result": "SUCCESS", "uuid": "1f4177a4-0ddb-4e4d-8258-a5cd5f4638fc",\n"when": "20191203122317Z", "duration": "0.002254",\n"kw": {"key": "crl_manager", "crlgen_enabled": true}}]\n').strip()
LONG_FREEIPA_HEALTHCHECK_LOG_FAILURES = ('\n[{"source": "ipahealthcheck.system.filesystemspace",\n"check": "FileSystemSpaceCheck",\n"result": "ERROR", "uuid": "90ed8765-6ad7-425c-abbd-b07a652649cb",\n"when": "20191203122221Z", "duration": "0.000474", "kw": {\n"msg": "/var/log/audit/: free space under threshold: 14 MiB < 512 MiB",\n"store": "/var/log/audit/", "free_space": 14, "threshold": 512}}]\n').strip()
FREEIPA_HEALTHCHECK_LOG_DOCS_EXAMPLE = ('\n    [\n      {\n        "source": "ipahealthcheck.ipa.roles",\n        "check": "IPACRLManagerCheck",\n        "result": "SUCCESS",\n        "uuid": "1f4177a4-0ddb-4e4d-8258-a5cd5f4638fc",\n        "when": "20191203122317Z",\n        "duration": "0.002254",\n        "kw": {\n          "key": "crl_manager",\n          "crlgen_enabled": true\n        }\n      },\n      {\n        "source": "ipahealthcheck.ipa.roles",\n        "check": "IPARenewalMasterCheck",\n        "result": "SUCCESS",\n        "uuid": "1feb7f99-2e98-4e37-bb52-686896972022",\n        "when": "20191203122317Z",\n        "duration": "0.018330",\n        "kw": {\n          "key": "renewal_master",\n          "master": true\n        }\n      },\n      {\n        "source": "ipahealthcheck.system.filesystemspace",\n        "check": "FileSystemSpaceCheck",\n        "result": "ERROR",\n        "uuid": "90ed8765-6ad7-425c-abbd-b07a652649cb",\n        "when": "20191203122221Z",\n        "duration": "0.000474",\n        "kw": {\n          "msg": "/var/log/audit/: free space under threshold: 14 MiB < 512 MiB",\n          "store": "/var/log/audit/",\n          "free_space": 14,\n          "threshold": 512\n         }\n       }\n    ]\n').strip()
FREEIPA_HEALTHCHECK_LOG_OK = ('').join(LONG_FREEIPA_HEALTHCHECK_LOG_OK.splitlines())
FREEIPA_HEALTHCHECK_LOG_FAILURES = ('').join(LONG_FREEIPA_HEALTHCHECK_LOG_FAILURES.splitlines())

def test_freeipa_healthcheck_log_ok():
    log_obj = FreeIPAHealthCheckLog(context_wrap(FREEIPA_HEALTHCHECK_LOG_OK))
    assert len(log_obj.issues) == 0


def test_freeipa_healthcheck_log_not_ok():
    log_obj = FreeIPAHealthCheckLog(context_wrap(FREEIPA_HEALTHCHECK_LOG_FAILURES))
    assert len(log_obj.issues) > 0
    for issue in log_obj.issues:
        assert issue['check'] == 'FileSystemSpaceCheck'
        assert issue['source'] == 'ipahealthcheck.system.filesystemspace'


def test_freeipa_healthcheck_get_results_ok():
    log_obj = FreeIPAHealthCheckLog(context_wrap(FREEIPA_HEALTHCHECK_LOG_OK))
    results = log_obj.get_results('ipahealthcheck.system.filesystemspace', 'FileSystemSpaceCheck')
    assert len(results) == 0


def test_freeipa_healthcheck_get_results_not_ok():
    log_obj = FreeIPAHealthCheckLog(context_wrap(FREEIPA_HEALTHCHECK_LOG_FAILURES))
    results = log_obj.get_results('ipahealthcheck.system.filesystemspace', 'FileSystemSpaceCheck')
    assert len(results) == 1
    for result in results:
        assert result['result'] in ('ERROR', 'CRITICAL')
        assert result['check'] == 'FileSystemSpaceCheck'
        assert result['source'] == 'ipahealthcheck.system.filesystemspace'


def test_freeipa_healthcheck_log__documentation():
    env = {'healthcheck': FreeIPAHealthCheckLog(context_wrap(FREEIPA_HEALTHCHECK_LOG_DOCS_EXAMPLE))}
    failed, total = doctest.testmod(freeipa_healthcheck_log, globs=env)
    assert failed == 0