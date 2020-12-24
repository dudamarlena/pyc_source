# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fede/projects/firelet/test/test_remote.py
# Compiled at: 2011-05-29 11:29:43
from json import dumps
from nose.tools import assert_raises, with_setup
from os import listdir
import shutil
from tempfile import mkdtemp
from firelet.flcore import *
from test import debug, string_in_list, assert_equal_line_by_line
import logging
log = logging.getLogger(__name__)
from logging import getLogger
log = logging.getLogger(__name__)
deb = log.debug
from testingutils import *
import testingutils
addrmap = {'10.66.1.2': 'InternalFW', 
   '10.66.2.1': 'InternalFW', 
   '10.66.1.3': 'Smeagol', 
   '10.66.2.2': 'Server001', 
   '172.16.2.223': 'BorderFW', 
   '10.66.1.1': 'BorderFW', 
   '127.0.0.1': 'localhost'}
from firelet.flssh import SSHConnector

def test_SSHConnector_get():
    pass


@with_setup(setup_dir, teardown_dir)
def test_get_confs():
    """Get confs from firewalls
    Check for ip addr show
    Ignore the iptables confs: the current state on the hosts (or emulator) is not known
    """
    d = dict((h, [ip_addr]) for ip_addr, h in addrmap.iteritems())
    sx = SSHConnector(targets=d)
    confs = sx.get_confs()
    assert isinstance(confs, dict)
    for hostname in d:
        assert hostname in confs, '%s missing from the results' % hostname

    for h, conf in confs.iteritems():
        assert 'iptables' in conf
        assert 'ip_a_s' in conf
        assert 'nat' in conf['iptables']
        assert 'filter' in conf['iptables']
        assert 'lo' in conf['ip_a_s']

    for h in ('InternalFW', 'Server001', 'BorderFW', 'Smeagol'):
        assert 'eth0' in confs[h]['ip_a_s'], h + ' has no eth0'

    assert 'eth1' in confs['BorderFW']['ip_a_s']
    assert 'eth1' in confs['InternalFW']['ip_a_s']
    assert 'eth2' in confs['BorderFW']['ip_a_s']


@with_setup(setup_dir, teardown_dir)
def test_get_confs_wrong_username():
    """Try to get confs from firewalls
    using a wrong username
    """
    d = dict((h, [ip_addr]) for ip_addr, h in addrmap.iteritems())
    sx = SSHConnector(targets=d, username='nogcptkiho')
    (assert_raises(Exception, sx.get_confs), 'Tget_confs should fail')


@with_setup(setup_dir, teardown_dir)
def test_get_conf_BorderFW():
    d = {'BorderFW': ['172.16.2.223']}
    for x in xrange(20):
        deb(show('%d run' % x))
        sx = SSHConnector(d)
        confs = sx.get_confs()
        assert isinstance(confs, dict)
        assert 'BorderFW' in confs, 'BorderFW missing from the results'
        assert 'iptables' in confs['BorderFW']
        del sx
        deb(show('Completed run %d' % x))


@with_setup(setup_dir, teardown_dir)
def test_deliver_confs():
    d = dict((h, [ip_addr]) for ip_addr, h in addrmap.iteritems())
    sx = SSHConnector(d)
    confs = dict((h, []) for h in d)
    status = sx.deliver_confs(confs)
    assert status == {'InternalFW': 'ok', 'Server001': 'ok', 'BorderFW': 'ok', 'localhost': 'ok', 'Smeagol': 'ok'}, repr(status)


@with_setup(setup_dir, teardown_dir)
def test_deliver_apply_and_get_confs():
    """Remote conf delivery, apply and get it back
    """
    d = dict((h, [ip_addr]) for ip_addr, h in addrmap.iteritems())
    confs = dict((h, ['# this is an iptables conf test', '# for %s' % h, '-A INPUT -s 3.3.3.3/32 -j ACCEPT']) for h in d)
    log.debug('Delivery...')
    sx = SSHConnector(d)
    status = sx.deliver_confs(confs)
    assert status == {'InternalFW': 'ok', 'Server001': 'ok', 'BorderFW': 'ok', 'localhost': 'ok', 
       'Smeagol': 'ok'}, repr(status)
    log.debug('Applying...')
    sx.apply_remote_confs()
    log.debug('Getting confs...')
    rconfs = sx.get_confs()
    for h, conf in confs.iteritems():
        assert h in rconfs, '%s missing from received confs' % h
        r = rconfs[h]
        assert 'iptables' in r
        assert 'ip_a_s' in r
        assert 'nat' in r['iptables']
        assert 'filter' in r['iptables']
        assert 'lo' in r['ip_a_s']


@with_setup(setup_dir, teardown_dir)
def test_GitFireSet_check():
    """Run diff between complied rules and remote confs using GitFireSet
    Given the test files, the check should be ok and require no deployment"""
    fs = GitFireSet(repodir=testingutils.repodir)
    diff = fs.check()
    assert diff == {}, repr(diff)[:400]


@with_setup(setup_dir, teardown_dir)
def test_GitFireSet_deployment():
    """Deploy confs, then check"""
    fs = GitFireSet(repodir=testingutils.repodir)
    fs.deploy()
    diff = fs.check()
    assert diff == {}, repr(diff)[:400]