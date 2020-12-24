# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dig.py
# Compiled at: 2020-03-25 13:10:41
import doctest, pytest
from insights.parsers import dig, SkipException
from insights.parsers.dig import Dig, DigDnssec, DigEdns, DigNoedns
from insights.tests import context_wrap
SIGNED_DNSSEC = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-2.P3.fc26 <<>> +dnssec nic.cz. SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 58794\n;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version: 0, flags: do; udp: 4096\n;; QUESTION SECTION:\n;nic.cz.                                IN      SOA\n\n;; ANSWER SECTION:\nnic.cz.                 278     IN      SOA     a.ns.nic.cz.\nhostmaster.nic.cz. 1508686803 10800 3600 1209600 7200\nnic.cz.                 278     IN      RRSIG   SOA 13 2 1800\n20171105143612 20171022144003 41758 nic.cz.\nhq3rr8dASRlucMJxu2QZnX6MVaMYsKhmGGxBOwpkeUrGjfo6clzG6MZN\n2Jy78fWYC/uwyIsI3nZMUKv573eCWg==\n\n;; Query time: 22 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Tue Oct 24 14:28:56 CEST 2017\n;; MSG SIZE  rcvd: 189'
NOT_SIGNED_DNSSEC = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-2.P3.fc26 <<>> +dnssec google.com. SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13253\n;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version: 0, flags: do; udp: 4096\n;; QUESTION SECTION:\n;google.com.                    IN      SOA\n\n;; ANSWER SECTION:\ngoogle.com.             60      IN      SOA     ns1.google.com.\ndns-admin.google.com. 173219439 900 900 1800 60\n\n;; Query time: 46 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Tue Oct 24 14:28:20 CEST 2017\n;; MSG SIZE  rcvd: 89'
BAD_DNSSEC = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-2.P3.fc26 <<>> +dnssec google.com. SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 13253\n;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version: 0, flags: do; udp: 4096\n;; QUESTION SECTION:\n;google.com.                    IN      SOA\n\n;; ANSWER SECTION:\ngoogle.com.             60      IN      SOA     ns1.google.com.\ndns-admin.google.com. 173219439 900 900 1800 60\n\n;; Query time: 46 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Tue Oct 24 14:28:20 CEST 2017\n;; MSG SIZE  rcvd: 89'
GOOD_EDNS = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-3.P3.fc26 <<>> +edns=0 . SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 11158\n;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version: 0, flags:; udp: 4096\n;; QUESTION SECTION:\n;.\t\t\t\tIN\tSOA\n\n;; ANSWER SECTION:\n.\t\t\t19766\tIN\tSOA\ta.root-servers.net. nstld.verisign-grs.com. 2017120600 1800 900 604800 86400\n\n;; Query time: 22 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Thu Dec 07 09:38:33 CET 2017\n;; MSG SIZE  rcvd: 103'
BAD_EDNS = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-3.P3.fc26 <<>> +edns=0 . SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 11158\n;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version: 0, flags:; udp: 4096\n;; QUESTION SECTION:\n;.\t\t\t\tIN\tSOA\n\n;; ANSWER SECTION:\n.\t\t\t19766\tIN\tSOA\ta.root-servers.net. nstld.verisign-grs.com. 2017120600 1800 900 604800 86400\n\n;; Query time: 22 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Thu Dec 07 09:38:33 CET 2017\n;; MSG SIZE  rcvd: 103'
GOOD_NOEDNS = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-3.P3.fc26 <<>> +noedns . SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47135\n;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0\n\n;; QUESTION SECTION:\n;.\t\t\t\tIN\tSOA\n\n;; ANSWER SECTION:\n.\t\t\t20195\tIN\tSOA\ta.root-servers.net. nstld.verisign-grs.com. 2017120600 1800 900 604800 86400\n\n;; Query time: 22 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Thu Dec 07 09:31:24 CET 2017\n;; MSG SIZE  rcvd: 92'
BAD_NOEDNS = '; <<>> DiG 9.11.1-P3-RedHat-9.11.1-2.P3.fc26 <<>> +noedns\newf-dwqfwqf-gdsa.com SOA\n;; global options: +cmd\n;; Got answer:\n;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 30634\n;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 0\n\n;; QUESTION SECTION:\n;ewf-dwqfwqf-gdsa.com.          IN      SOA\n\n;; AUTHORITY SECTION:\ncom.                    900     IN      SOA     a.gtld-servers.net.\nnstld.verisign-grs.com. 1508851057 1800 900 604800 86400\n\n;; Query time: 29 msec\n;; SERVER: 10.38.5.26#53(10.38.5.26)\n;; WHEN: Tue Oct 24 15:17:53 CEST 2017\n;; MSG SIZE  rcvd: 111'

def test_dig_no_data():
    with pytest.raises(SkipException):
        Dig(context_wrap(''), '')


def test_dig_dnssec():
    dig_dnssec = DigDnssec(context_wrap(SIGNED_DNSSEC))
    assert dig_dnssec.status == 'NOERROR'
    assert dig_dnssec.has_signature
    dig_dnssec = DigDnssec(context_wrap(NOT_SIGNED_DNSSEC))
    assert dig_dnssec.status == 'NOERROR'
    assert not dig_dnssec.has_signature
    dig_dnssec = DigDnssec(context_wrap(BAD_DNSSEC))
    assert dig_dnssec.status == 'REFUSED'
    assert not dig_dnssec.has_signature


def test_dig_edns():
    dig_edns = DigEdns(context_wrap(GOOD_EDNS))
    assert dig_edns.status == 'NOERROR'
    assert not dig_edns.has_signature
    dig_edns = DigEdns(context_wrap(BAD_EDNS))
    assert dig_edns.status == 'SERVFAIL'
    assert not dig_edns.has_signature


def test_dig_noedns():
    dig_noedns = DigNoedns(context_wrap(GOOD_NOEDNS))
    assert dig_noedns.status == 'NOERROR'
    assert not dig_noedns.has_signature
    dig_noedns = DigNoedns(context_wrap(BAD_NOEDNS))
    assert dig_noedns.status == 'NXDOMAIN'
    assert not dig_noedns.has_signature


def test_doc_examples():
    env = {'dig_dnssec': DigDnssec(context_wrap(SIGNED_DNSSEC)), 
       'dig_edns': DigEdns(context_wrap(GOOD_EDNS)), 
       'dig_noedns': DigNoedns(context_wrap(GOOD_NOEDNS))}
    failed, total = doctest.testmod(dig, globs=env)
    assert failed == 0