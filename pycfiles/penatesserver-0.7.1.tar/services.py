# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/glpi/services.py
# Compiled at: 2015-12-29 03:04:14
from __future__ import unicode_literals
import datetime
from django.core.signing import Signer
from django.utils.six import text_type
from django.utils.translation import ugettext as _
from penatesserver.glpi.models import ShinkenService
from penatesserver.models import Host, Service
__author__ = b'Matthieu Gallet'
signer = Signer()
year_0 = datetime.datetime(1970, 1, 1, 0, 0, 0)
session_duration_in_seconds = 600

def check_session(request, args):
    session = args[0][b'session']
    session = signer.unsign(session)
    end, sep, login_name = session.partition(b':')
    end = int(end)
    if (datetime.datetime.utcnow() - year_0).total_seconds() > end:
        raise ValueError


def get_shinken_services():
    result = []
    for host in Host.objects.all():
        result.append({b'use': b'local-service', b'host_name': host.fqdn, b'service_description': _(b'Check SSH %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_ssh', 
           b'notifications_enabled': b'0'})
        result.append({b'use': b'local-service', b'host_name': host.fqdn, b'service_description': _(b'Ping %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_ping!100.0,20%!500.0,60%', 
           b'icon_set': b'server', b'notifications_enabled': b'0'})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'service_description': _(b'Check all disks on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_all_disk', 
           b'icon_set': b'disk', b'notifications_enabled': b'0'})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'service_description': _(b'Check swap on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_swap', 
           b'notifications_enabled': b'0'})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'service_description': _(b'Check number of processes on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_total_procs', 
           b'icon_set': b'server', b'notifications_enabled': b'0'})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'service_description': _(b'Check number of zombie processes on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_zombie_procs', 
           b'icon_set': b'server', b'notifications_enabled': b'0'})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'service_description': _(b'Check load on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_load', 
           b'icon_set': b'server', b'notifications_enabled': b'0'})
        result.append({b'use': b'local-service', b'host_name': host.fqdn, b'icon_set': b'server', b'service_description': _(b'Check DNS %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'penates_dig_2!%s!%s' % (host.fqdn, host.main_ip_address), 
           b'notifications_enabled': b'0', 
           b'check_interval': text_type(240)})
        result.append({b'use': b'local-service', b'host_name': host.fqdn, b'icon_set': b'server', b'service_description': _(b'Check DNS %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'penates_dig_2!%s!%s' % (host.admin_fqdn, host.admin_ip_address), 
           b'notifications_enabled': b'0', 
           b'check_interval': text_type(240)})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'icon_set': b'server', b'service_description': _(b'Check admin certificate on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_cert_admin', 
           b'notifications_enabled': b'0', 
           b'check_interval': text_type(1440)})
        result.append({b'use': b'generic-service', b'host_name': host.fqdn, b'icon_set': b'server', b'service_description': _(b'Check host certificate on %(fqdn)s') % {b'fqdn': host.fqdn}, 
           b'check_command': b'check_nrpe!check_cert_host', 
           b'notifications_enabled': b'0', 
           b'check_interval': text_type(1440)})

    for service in Service.objects.all():
        if service.scheme in ('http', 'carddav', 'caldav'):
            check = b'penates_http!%s!%s' if service.encryption == b'none' else b'penates_https!%s!%s'
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'HTTP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': check % (service.hostname, service.port), 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'ssh':
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'SSH TCP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': b'check_tcp!%s' % service.port, 
               b'notifications_enabled': b'0'})
            result.append({b'use': b'generic-service', b'host_name': service.fqdn, b'service_description': _(b'SSH process on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': b'check_nrpe!check_sshd', 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'imap':
            check = b'penates_imaps!%s' if service.encryption == b'tls' else b'penates_imap!%s'
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'IMAP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': check % service.port, 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'ldap':
            check = b'penates_ldaps!%s' if service.encryption == b'tls' else b'penates_ldap!%s'
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'LDAP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': check % service.port, 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'krb':
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'Kerberos on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': b'check_tcp!%s' % service.port, 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'dns':
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'DNS on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': b'check_tcp!%s' % service.port, 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'smtp':
            check = b'penates_smtps!%s' if service.encryption == b'tls' else b'penates_smtp!%s'
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'SMTP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': check % service.port, 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'ntp':
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'NTP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': b'penates_ntp!%s' % service.hostname, 
               b'notifications_enabled': b'0'})
        elif service.scheme == b'dkim':
            pass
        elif service.protocol == b'tcp':
            result.append({b'use': b'local-service', b'host_name': service.fqdn, 
               b'service_description': _(b'TCP on %(fqdn)s:%(port)s') % {b'fqdn': service.hostname, b'port': service.port}, 
               b'check_command': b'check_tcp!%s' % service.port, 
               b'notifications_enabled': b'0'})

    for service in ShinkenService.objects.all():
        result.append(service.to_dict())

    return result