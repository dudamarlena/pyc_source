# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/kerb.py
# Compiled at: 2015-10-19 03:33:47
from __future__ import unicode_literals
import codecs, subprocess
from django.conf import settings
__author__ = b'Matthieu Gallet'

def heimdal_command(*args):
    args_list = [
     b'kadmin', b'-p', settings.PENATES_PRINCIPAL, b'-K', settings.PENATES_KEYTAB] + list(args)
    p = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    return p


def mit_command(*args):
    arg_list = [
     b'kadmin', b'-p', settings.PENATES_PRINCIPAL, b'-k', b'-t', settings.PENATES_KEYTAB, b'-q'] + list(args)
    p = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    return p


def add_principal_to_keytab(principal, filename):
    if settings.RUNNING_TESTS:
        from penatesserver.models import PrincipalTest
        PrincipalTest.objects.get(name=principal)
        with codecs.open(filename, b'a', encoding=b'utf-8') as (fd):
            fd.write(principal)
            fd.write(b'\n')
        return
    if settings.KERBEROS_IMPL == b'mit':
        mit_command(b'ktadd -k %s %s' % (filename, principal))
    else:
        heimdal_command(b'ext_keytab', b'-k', filename, principal)


def change_password(principal, password):
    if settings.RUNNING_TESTS:
        from penatesserver.models import PrincipalTest
        PrincipalTest.objects.get(name=principal)
        return
    if settings.KERBEROS_IMPL == b'mit':
        mit_command(b'change_password -pw %s %s' % (password, principal))
    else:
        heimdal_command(b'passwd', b'--password=%s' % password, principal)


def keytab_has_principal(principal, keytab_filename):
    if settings.RUNNING_TESTS:
        with codecs.open(keytab_filename, b'r', encoding=b'utf-8') as (fd):
            content = fd.read()
        return principal in content.splitlines()
    if settings.KERBEROS_IMPL == b'mit':
        p = subprocess.Popen([b'ktutil'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(b'rkt %s\nlist' % keytab_filename)
    else:
        p = subprocess.Popen([b'ktutil', b'-k', keytab_filename, b'list'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
    if stderr:
        raise ValueError(b'Invalid keytab file %s' % keytab_filename)
    stdout_text = stdout.decode(b'utf-8')
    for line in stdout_text.splitlines():
        if line.strip().endswith(principal):
            return True

    return False


def add_principal(principal):
    if settings.RUNNING_TESTS:
        from penatesserver.models import PrincipalTest
        PrincipalTest.objects.get_or_create(name=principal)
        return
    from penatesserver.models import Principal
    if principal_exists(principal):
        return
    if settings.KERBEROS_IMPL == b'mit':
        Principal(name=principal).save()
    else:
        heimdal_command(b'add', b'--random-key', b'--max-ticket-life=1d', b'--max-renewable-life=1w', b'--attributes=', b'--expiration-time=never', b'--pw-expiration-time=never', b'--policy=default', principal)


def principal_exists(principal_name):
    if settings.RUNNING_TESTS:
        from penatesserver.models import PrincipalTest
        return PrincipalTest.objects.filter(name=principal_name).count() > 0
    else:
        from penatesserver.models import Principal
        if settings.KERBEROS_IMPL == b'mit':
            return bool(list(Principal.objects.filter(name=principal_name)[0:1]))
        p = heimdal_command(b'get', b'-s', b'-o', b'principal', principal_name)
        return p.returncode == 0


def delete_principal(principal):
    if settings.RUNNING_TESTS:
        from penatesserver.models import PrincipalTest
        PrincipalTest.objects.filter(name=principal).delete()
        return
    from penatesserver.models import Principal
    if settings.KERBEROS_IMPL == b'mit':
        Principal.objects.filter(name=principal).delete()
    else:
        heimdal_command(b'delete', principal)