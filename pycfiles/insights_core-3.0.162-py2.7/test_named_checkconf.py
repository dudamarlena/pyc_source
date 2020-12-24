# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_named_checkconf.py
# Compiled at: 2020-03-26 13:06:46
import doctest, pytest
from insights.parsers import named_checkconf, SkipException
from insights.parsers.named_checkconf import NamedCheckconf
from insights.tests import context_wrap
CONFIG_DNSSEC_ENABLED = '\noptions {\n    bindkeys-file "/etc/named.iscdlv.key";\n    directory "/var/named";\n    dump-file "/var/named/data/cache_dump.db";\n    listen-on port 53 {\n        127.0.0.1/32;\n    };\n    listen-on-v6 port 53 {\n        ::1/128;\n    };\n    managed-keys-directory "/var/named/dynamic";\n    memstatistics-file "/var/named/data/named_mem_stats.txt";\n    statistics-file "/var/named/data/named_stats.txt";\n    dnssec-enable yes;\n    dnssec-validation yes;\n    recursion yes;\n    allow-query {\n        "localhost";\n    };\n};\n'
CONFIG_DNSSEC_DISABLED = '\noptions {\n    bindkeys-file "/etc/named.iscdlv.key";\n    directory "/var/named";\n    dump-file "/var/named/data/cache_dump.db";\n    listen-on port 53 {\n        127.0.0.1/32;\n    };\n    listen-on-v6 port 53 {\n        ::1/128;\n    };\n    managed-keys-directory "/var/named/dynamic";\n    memstatistics-file "/var/named/data/named_mem_stats.txt";\n    statistics-file "/var/named/data/named_stats.txt";\n    dnssec-enable no;\n    dnssec-validation yes;\n    recursion yes;\n    allow-query {\n        "localhost";\n    };\n};\n'
CONFIG_DNSSEC_DEFAULT = '\noptions {\n    bindkeys-file "/etc/named.iscdlv.key";\n    directory "/var/named";\n    dump-file "/var/named/data/cache_dump.db";\n    listen-on port 53 {\n        127.0.0.1/32;\n    };\n    listen-on-v6 port 53 {\n        ::1/128;\n    };\n    managed-keys-directory "/var/named/dynamic";\n    memstatistics-file "/var/named/data/named_mem_stats.txt";\n    statistics-file "/var/named/data/named_stats.txt";\n    dnssec-validation yes;\n    recursion yes;\n    allow-query {\n        "localhost";\n    };\n};\n'
CONFIG_DISABLED_SECTIONS = '\nlogging {\n    channel "default_debug" {\n        file "data/named.run";\n        severity dynamic;\n    };\n};\noptions {\n    directory "/var/named";\n    dump-file "/var/named/data/cache_dump.db";\n    listen-on port 53 {\n        127.0.0.1/32;\n    };\n    listen-on-v6 port 53 {\n        ::1/128;\n    };\n    managed-keys-directory "/var/named/dynamic";\n    memstatistics-file "/var/named/data/named_mem_stats.txt";\n    pid-file "/run/named/named.pid";\n    recursing-file "/var/named/data/named.recursing";\n    secroots-file "/var/named/data/named.secroots";\n    session-keyfile "/run/named/session.key";\n    statistics-file "/var/named/data/named_stats.txt";\n    disable-algorithms "." {\n        "RSAMD5";\n        "DSA";\n    };\n    disable-ds-digests "." {\n        "GOST";\n    };\n    dnssec-enable yes;\n    dnssec-validation yes;\n    recursion yes;\n    allow-query {\n        "localhost";\n    };\n};\nmanaged-keys {\n    "." initial-key 257 3 8 "AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW0O8gcCjF\n                FVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoX\n                bfDaUeVPQuYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaD\n                X6RS6CXpoY68LsvPVjR0ZSwzz1apAzvN9dlzEheX7ICJBBtuA6G3LQpz\n                W5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7OyQdXfZ57relS\n                Qageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulq\n                QxA+Uk1ihz0=";\n    "." initial-key 257 3 8 "AwEAAaz/tAm8yTn4Mfeh5eyI96WSVexTBAvkMgJzkKTOiW1vkIbzxeF3\n                +/4RgWOq7HrxRixHlFlExOLAJr5emLvN7SWXgnLh4+B5xQlNVz8Og8kv\n                ArMtNROxVQuCaSnIDdD5LKyWbRd2n9WGe2R8PzgCmr3EgVLrjyBxWezF\n                0jLHwVN8efS3rCj/EWgvIWgb9tarpVUDK/b58Da+sqqls3eNbuv7pr+e\n                oZG+SrDK6nWeL3c6H5Apxz7LjVc1uTIdsIXxuOLYA4/ilBmSVIzuDWfd\n                RUfhHdY6+cn8HFRm+2hM8AnXGXws9555KrUB5qihylGa8subX2Nn6UwN\n                R1AkUTV74bU=";\n};\nzone "." IN {\n    type hint;\n    file "named.ca";\n};\nzone "localhost.localdomain" IN {\n    type master;\n    file "named.localhost";\n    allow-update {\n        "none";\n    };\n};\nzone "localhost" IN {\n    type master;\n    file "named.localhost";\n    allow-update {\n        "none";\n    };\n};\nzone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {\n    type master;\n    file "named.loopback";\n    allow-update {\n        "none";\n    };\n};\nzone "1.0.0.127.in-addr.arpa" IN {\n    type master;\n    file "named.loopback";\n    allow-update {\n        "none";\n    };\n};\nzone "0.in-addr.arpa" IN {\n    type master;\n    file "named.empty";\n    allow-update {\n        "none";\n    };\n};\n'

def test_config_no_data():
    with pytest.raises(SkipException):
        NamedCheckconf(context_wrap(''))


def test_config_dnssec():
    dnssec_disabled = NamedCheckconf(context_wrap(CONFIG_DNSSEC_DISABLED))
    assert dnssec_disabled.is_dnssec_disabled
    assert dnssec_disabled.dnssec_line == 'dnssec-enable no;'
    assert dnssec_disabled.disable_algorithms == {}
    assert dnssec_disabled.disable_ds_digests == {}
    dnssec_enabled = NamedCheckconf(context_wrap(CONFIG_DNSSEC_ENABLED))
    assert not dnssec_enabled.is_dnssec_disabled
    assert dnssec_enabled.dnssec_line is None
    assert dnssec_enabled.disable_algorithms == {}
    assert dnssec_enabled.disable_ds_digests == {}
    dnssec_default = NamedCheckconf(context_wrap(CONFIG_DNSSEC_DEFAULT))
    assert not dnssec_default.is_dnssec_disabled
    assert dnssec_default.dnssec_line is None
    assert dnssec_default.disable_algorithms == {}
    assert dnssec_default.disable_ds_digests == {}
    return


def test_config_disabled_sections():
    disabled_sections = NamedCheckconf(context_wrap(CONFIG_DISABLED_SECTIONS))
    assert not disabled_sections.is_dnssec_disabled
    assert disabled_sections.dnssec_line is None
    assert disabled_sections.disable_algorithms == {'.': ['RSAMD5', 'DSA']}
    assert disabled_sections.disable_ds_digests == {'.': ['GOST']}
    return


def test_doc_examples():
    env = {'named_checkconf': NamedCheckconf(context_wrap(CONFIG_DISABLED_SECTIONS))}
    failed, total = doctest.testmod(named_checkconf, globs=env)
    assert failed == 0