# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/security/kerberos.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4547 bytes
import socket, subprocess, sys, time
from airflow import configuration, LoggingMixin
NEED_KRB181_WORKAROUND = None
log = LoggingMixin().log

def renew_from_kt(principal, keytab):
    global NEED_KRB181_WORKAROUND
    renewal_lifetime = '%sm' % configuration.conf.getint('kerberos', 'reinit_frequency')
    cmd_principal = principal or configuration.conf.get('kerberos', 'principal').replace('_HOST', socket.getfqdn())
    cmdv = [
     configuration.conf.get('kerberos', 'kinit_path'),
     '-r', renewal_lifetime,
     '-k',
     '-t', keytab,
     '-c', configuration.conf.get('kerberos', 'ccache'),
     cmd_principal]
    log.info('Reinitting kerberos from keytab: %s', ' '.join(cmdv))
    subp = subprocess.Popen(cmdv, stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      close_fds=True,
      bufsize=(-1),
      universal_newlines=True)
    subp.wait()
    if subp.returncode != 0:
        log.error("Couldn't reinit from keytab! `kinit' exited with %s.\n%s\n%s", subp.returncode, '\n'.join(subp.stdout.readlines()), '\n'.join(subp.stderr.readlines()))
        sys.exit(subp.returncode)
    if NEED_KRB181_WORKAROUND is None:
        NEED_KRB181_WORKAROUND = detect_conf_var()
    if NEED_KRB181_WORKAROUND:
        time.sleep(1.5)
        perform_krb181_workaround(principal)


def perform_krb181_workaround(principal):
    cmdv = [
     configuration.conf.get('kerberos', 'kinit_path'),
     '-c', configuration.conf.get('kerberos', 'ccache'),
     '-R']
    log.info('Renewing kerberos ticket to work around kerberos 1.8.1: %s', ' '.join(cmdv))
    ret = subprocess.call(cmdv, close_fds=True)
    if ret != 0:
        principal = '%s/%s' % (principal or configuration.conf.get('kerberos', 'principal'),
         socket.getfqdn())
        princ = principal
        ccache = configuration.conf.get('kerberos', 'principal')
        log.error("Couldn't renew kerberos ticket in order to work around Kerberos 1.8.1 issue. Please check that the ticket for '%s' is still renewable:\n  $ kinit -f -c %s\nIf the 'renew until' date is the same as the 'valid starting' date, the ticket cannot be renewed. Please check your KDC configuration, and the ticket renewal policy (maxrenewlife) for the '%s' and `krbtgt' principals.", princ, ccache, princ)
        sys.exit(ret)


def detect_conf_var():
    """Return true if the ticket cache contains "conf" information as is found
    in ticket caches of Kerberos 1.8.1 or later. This is incompatible with the
    Sun Java Krb5LoginModule in Java6, so we need to take an action to work
    around it.
    """
    ticket_cache = configuration.conf.get('kerberos', 'ccache')
    with open(ticket_cache, 'rb') as (f):
        return 'X-CACHECONF:' in f.read()


def run(principal, keytab):
    if not keytab:
        log.debug('Keytab renewer not starting, no keytab configured')
        sys.exit(0)
    while True:
        renew_from_kt(principal, keytab)
        time.sleep(configuration.conf.getint('kerberos', 'reinit_frequency'))