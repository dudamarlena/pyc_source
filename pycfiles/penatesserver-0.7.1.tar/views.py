# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/views.py
# Compiled at: 2015-12-29 03:04:14
from __future__ import unicode_literals
import base64, hashlib, os, re, tempfile
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
import netaddr
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from penatesserver.forms import PasswordForm
from penatesserver.kerb import add_principal_to_keytab, add_principal, principal_exists
from penatesserver.models import Service, Host, User, Group, MountPoint
from penatesserver.pki.constants import COMPUTER, SERVICE, KERBEROS_DC, PRINTER, TIME_SERVER, SERVICE_1024
from penatesserver.pki.service import CertificateEntry, PKI
from penatesserver.powerdns.models import Domain, Record
from penatesserver.serializers import UserSerializer, GroupSerializer
from penatesserver.subnets import get_subnets
from penatesserver.utils import hostname_from_principal, principal_from_hostname
__author__ = b'flanker'

class KeytabResponse(HttpResponse):

    def __init__(self, principal, **kwargs):
        with tempfile.NamedTemporaryFile() as (fd):
            keytab_filename = fd.name
        add_principal_to_keytab(principal, keytab_filename)
        with open(keytab_filename, b'rb') as (fd):
            keytab_content = bytes(fd.read())
        os.remove(keytab_filename)
        super(KeytabResponse, self).__init__(content=keytab_content, content_type=b'application/keytab', **kwargs)


def entry_from_hostname(hostname):
    return CertificateEntry(hostname, organizationName=settings.PENATES_ORGANIZATION, organizationalUnitName=_(b'Computers'), emailAddress=settings.PENATES_EMAIL_ADDRESS, localityName=settings.PENATES_LOCALITY, countryName=settings.PENATES_COUNTRY, stateOrProvinceName=settings.PENATES_STATE, altNames=[], role=COMPUTER)


def admin_entry_from_hostname(hostname):
    return CertificateEntry(hostname, organizationName=settings.PENATES_ORGANIZATION, organizationalUnitName=_(b'Computers'), emailAddress=settings.PENATES_EMAIL_ADDRESS, localityName=settings.PENATES_LOCALITY, countryName=settings.PENATES_COUNTRY, stateOrProvinceName=settings.PENATES_STATE, altNames=[], role=COMPUTER)


def index(request):
    template_values = {b'protocol': settings.PROTOCOL, b'server_name': settings.SERVER_NAME}
    return render_to_response(b'penatesserver/index.html', template_values, RequestContext(request))


def get_info(request):
    content = b''
    content += b'METHOD:%s\n' % request.method
    content += b'REMOTE_USER:%s\n' % (b'' if request.user.is_anonymous() else request.user.username)
    content += b'REMOTE_ADDR:%s\n' % request.META.get(b'HTTP_X_FORWARDED_FOR', b'')
    content += b'HTTPS?:%s\n' % request.is_secure()
    return HttpResponse(content, status=200, content_type=b'text/plain')


def get_host_keytab(request, hostname):
    """Register a computer:

        - create Kerberos principal
        - create private key
        - create public SSH key
        - create x509 certificate
        - create PTR DNS record
        - create A or AAAA DNS record
        - create SSHFP DNS record
        - return keytab

    :param request:
    :type request:
    :param hostname:
    :type hostname:
    :return:
    :rtype:
    """
    admin_ip_address = request.GET.get(b'ip_address')
    ip_address = request.META.get(b'HTTP_X_FORWARDED_FOR')
    short_hostname = hostname.partition(b'.')[0]
    domain_name = settings.PENATES_DOMAIN
    fqdn = b'%s.%s%s' % (short_hostname, settings.PDNS_INFRA_PREFIX, domain_name)
    principal = principal_from_hostname(fqdn, settings.PENATES_REALM)
    if principal_exists(principal):
        return HttpResponse(b'', status=403)
    add_principal(principal)
    Host.objects.get_or_create(fqdn=fqdn)
    entry = entry_from_hostname(fqdn)
    pki = PKI()
    pki.ensure_certificate(entry)
    if ip_address:
        Domain.ensure_auto_record(ip_address, fqdn, unique=True, override_reverse=True)
        Host.objects.filter(fqdn=fqdn).update(main_ip_address=ip_address)
    if admin_ip_address:
        admin_fqdn = b'%s.%s%s' % (short_hostname, settings.PDNS_ADMIN_PREFIX, domain_name)
        Domain.ensure_auto_record(admin_ip_address, admin_fqdn, unique=True, override_reverse=False)
        Host.objects.filter(fqdn=fqdn).update(admin_ip_address=admin_ip_address)
    if settings.OFFER_HOST_KEYTABS:
        return KeytabResponse(principal)
    return HttpResponse(b'', content_type=b'text/plain', status=201)


def set_dhcp(request, mac_address):
    hostname = hostname_from_principal(request.user.username)
    mac_address = mac_address.replace(b'-', b':').upper()
    remote_addr = request.META.get(b'HTTP_X_FORWARDED_FOR', b'')
    admin_mac_address = request.GET.get(b'mac_address')
    admin_ip_address = request.GET.get(b'ip_address')
    admin_mac_address = admin_mac_address.replace(b'-', b':').upper()
    if remote_addr:
        Host.objects.filter(fqdn=hostname).update(main_ip_address=remote_addr, main_mac_address=mac_address)
        Record.objects.filter(name=hostname).update(content=remote_addr)
    if admin_ip_address and admin_mac_address:
        domain_name = b'%s%s' % (settings.PDNS_ADMIN_PREFIX, settings.PENATES_DOMAIN)
        long_admin_hostname = b'%s.%s' % (hostname.partition(b'.')[0], domain_name)
        Host.objects.filter(fqdn=hostname).update(admin_ip_address=admin_ip_address, admin_mac_address=admin_mac_address)
        Domain.ensure_auto_record(admin_ip_address, long_admin_hostname, unique=True, override_reverse=False)
    return HttpResponse(status=201)


def set_mount_point(request):
    hostname = hostname_from_principal(request.user.username)
    hosts = list(Host.objects.filter(fqdn=hostname)[0:1])
    if not hosts:
        return HttpResponse(status=404)
    host = hosts[0]
    mount_point = request.GET.get(b'mount_point')
    if not mount_point:
        return HttpResponse(b'mount_point GET argument not provided', status=400)
    device = request.GET.get(b'device')
    if not device:
        return HttpResponse(b'device GET argument not provided', status=400)
    fs_type = request.GET.get(b'fs_type')
    if not fs_type:
        return HttpResponse(b'fs_type GET argument not provided', status=400)
    options = request.GET.get(b'options')
    if not options:
        return HttpResponse(b'options GET argument not provided', status=400)
    if MountPoint.objects.filter(host=host, mount_point=mount_point).update(fs_type=fs_type, device=device, options=options) == 1:
        return HttpResponse(b'', status=204)
    MountPoint(host=host, mount_point=mount_point, fs_type=fs_type, device=device, options=options).save()
    return HttpResponse(b'', status=201)


def set_ssh_pub(request):
    fqdn = hostname_from_principal(request.user.username)
    if Host.objects.filter(fqdn=fqdn).count() == 0:
        return HttpResponse(status=404)
    fqdn = b'%s.%s%s' % (fqdn.partition(b'.')[0], settings.PDNS_ADMIN_PREFIX, settings.PENATES_DOMAIN)
    domain_name = b'%s%s' % (settings.PDNS_ADMIN_PREFIX, settings.PENATES_DOMAIN)
    pub_ssh_key = request.body
    matcher = re.match(b'([\\w\\-]+) ([\\w\\+=/]{1,5000})(|\\s.*)$', pub_ssh_key)
    if not matcher:
        return HttpResponse(status=406, content=b'Invalid public SSH key')
    methods = {b'ssh-rsa': 1, b'ssh-dss': 2, b'ecdsa-sha2-nistp256': 3, b'ssh-ed25519': 4}
    if matcher.group(1) not in methods:
        return HttpResponse(status=406, content=b'Unknown SSH key type %s' % matcher.group(1))
    sha1_hash = hashlib.sha1(base64.b64decode(matcher.group(2))).hexdigest()
    sha256_hash = hashlib.sha256(base64.b64decode(matcher.group(2))).hexdigest()
    algorithm_code = methods[matcher.group(1)]
    domain = Domain.objects.get(name=domain_name)
    sha1_value = b'%s 1 %s' % (algorithm_code, sha1_hash)
    sha256_value = b'%s 2 %s' % (algorithm_code, sha256_hash)
    for value in (sha1_value, sha256_value):
        if Record.objects.filter(domain=domain, name=fqdn, type=b'SSHFP', content__startswith=value[:4]).count() == 0:
            Record(domain=domain, name=fqdn, type=b'SSHFP', content=value, ttl=86400).save()
        else:
            Record.objects.filter(domain=domain, name=fqdn, type=b'SSHFP', content__startswith=value[:4]).update(content=value)

    return HttpResponse(status=201)


def set_extra_service(request, hostname):
    ip_address = request.GET.get(b'ip', b'')
    try:
        addr = netaddr.IPAddress(ip_address)
    except ValueError:
        return HttpResponse(status=403, content=b'Invalid IP address ?ip=%s' % ip_address)

    record_type = b'A' if addr.version == 4 else b'AAAA'
    sqdn, sep, domain_name = hostname.partition(b'.')
    if domain_name != settings.PENATES_DOMAIN:
        return HttpResponse(status=403, content=b'Unknown domain %s' % domain_name)
    domain = Domain.objects.get(name=domain_name)
    Record.objects.get_or_create(domain=domain, name=hostname, type=record_type, content=ip_address)
    return HttpResponse(status=201)


def set_service(request, scheme, hostname, port):
    encryption = request.GET.get(b'encryption', b'none')
    srv_field = request.GET.get(b'srv', None)
    kerberos_service = request.GET.get(b'keytab', None)
    role = request.GET.get(b'role', SERVICE)
    protocol = request.GET.get(b'protocol', b'tcp')
    if encryption not in ('none', 'tls', 'starttls'):
        return HttpResponse(b'valid encryption levels are none, tls, or starttls')
    else:
        port = int(port)
        if not 0 <= port <= 65536:
            return HttpResponse(b'Invalid port: %s' % port, status=403, content_type=b'text/plain')
        if protocol not in ('tcp', 'udp', 'socket'):
            return HttpResponse(b'Invalid protocol: %s' % protocol, status=403, content_type=b'text/plain')
        description = request.body
        fqdn = hostname_from_principal(request.user.username)
        if Service.objects.filter(hostname=hostname).exclude(fqdn=fqdn).count() > 0:
            return HttpResponse(status=401, content=b'%s is already registered' % hostname)
        if role not in (SERVICE, KERBEROS_DC, PRINTER, TIME_SERVER, SERVICE_1024):
            return HttpResponse(status=401, content=b'Role %s is not allowed' % role)
        if kerberos_service and kerberos_service not in ('HTTP', 'XMPP', 'smtp', 'IPP',
                                                         'ldap', 'cifs', 'imap',
                                                         'postgres', 'host'):
            return HttpResponse(status=401, content=b'Kerberos service %s is not allowed' % role)
        hosts = list(Host.objects.filter(fqdn=fqdn)[0:1])
        if not hosts:
            return HttpResponse(status=401, content=b'Unknown host %s is not allowed' % fqdn)
        host = hosts[0]
        if scheme == b'ssh' and host.admin_ip_address != host.main_ip_address:
            fqdn = b'%s.%s%s' % (fqdn.partition(b'.')[0], settings.PDNS_ADMIN_PREFIX, settings.PENATES_DOMAIN)
        service, created = Service.objects.get_or_create(fqdn=fqdn, scheme=scheme, hostname=hostname, port=port, protocol=protocol)
        Service.objects.filter(pk=service.pk).update(kerberos_service=kerberos_service, description=description, dns_srv=srv_field, encryption=encryption)
        entry = CertificateEntry(hostname, organizationName=settings.PENATES_ORGANIZATION, organizationalUnitName=_(b'Services'), emailAddress=settings.PENATES_EMAIL_ADDRESS, localityName=settings.PENATES_LOCALITY, countryName=settings.PENATES_COUNTRY, stateOrProvinceName=settings.PENATES_STATE, altNames=[], role=role)
        pki = PKI()
        pki.ensure_certificate(entry)
        if kerberos_service:
            principal_name = b'%s/%s@%s' % (kerberos_service, fqdn, settings.PENATES_REALM)
            add_principal(principal_name)
        record_name, sep, domain_name = hostname.partition(b'.')
        if sep == b'.':
            domains = list(Domain.objects.filter(name=domain_name)[0:1])
            if domains:
                domain = domains[0]
                domain.ensure_record(fqdn, hostname)
                domain.set_extra_records(scheme, hostname, port, fqdn, srv_field, entry=entry)
                domain.update_soa()
        return HttpResponse(status=201, content=b'%s://%s:%s/ created' % (scheme, hostname, port))


def get_service_keytab(request, scheme, hostname, port):
    fqdn = hostname_from_principal(request.user.username)
    protocol = request.GET.get(b'protocol', b'tcp')
    hosts = list(Host.objects.filter(fqdn=fqdn)[0:1])
    if not hosts:
        return HttpResponse(status=401, content=b'Unknown host %s is not allowed' % fqdn)
    host = hosts[0]
    if scheme == b'ssh' and host.admin_ip_address != host.main_ip_address:
        fqdn = b'%s.%s%s' % (fqdn.partition(b'.')[0], settings.PDNS_ADMIN_PREFIX, settings.PENATES_DOMAIN)
    services = list(Service.objects.filter(fqdn=fqdn, scheme=scheme, hostname=hostname, port=port, protocol=protocol)[0:1])
    if not services:
        return HttpResponse(status=404, content=b'%s://%s:%s/ unknown' % (scheme, hostname, port))
    service = services[0]
    principal_name = b'%s/%s@%s' % (service.kerberos_service, fqdn, settings.PENATES_REALM)
    if not principal_exists(principal_name):
        return HttpResponse(status=404, content=b'Principal for %s://%s:%s/ undefined' % (scheme, hostname, port))
    return KeytabResponse(principal_name)


def get_dhcpd_conf(request):

    def get_ip_or_none(scheme):
        values = list(Service.objects.filter(scheme=scheme)[0:1])
        if not values:
            return None
        else:
            return Record.local_resolve(values[0].fqdn) or values[0].hostname

    def get_ip_list(scheme):
        values = list(Service.objects.filter(scheme=scheme))
        return [ Record.local_resolve(x.fqdn) or x.hostname for x in values ]

    template_values = {b'penates_subnets': get_subnets(), 
       b'penates_domain': settings.PENATES_DOMAIN, 
       b'admin_prefix': settings.PDNS_ADMIN_PREFIX, 
       b'infra_prefix': settings.PDNS_INFRA_PREFIX, 
       b'hosts': Host.objects.all(), 
       b'tftp': get_ip_or_none(b'tftp'), 
       b'dns_list': get_ip_list(b'dns'), 
       b'ntp': get_ip_or_none(b'ntp')}
    return render_to_response(b'dhcpd/dhcpd.conf', template_values, status=200, content_type=b'text/plain')


def get_dns_conf(request):
    domains = {}
    for domain in Domain.objects.all():
        domains[domain.id] = (
         domain, [])

    for record in Record.objects.all():
        domains[record.domain_id][1].append(record)

    template_values = {b'domains': domains}
    return render_to_response(b'dns/dns.conf', template_values, status=200, content_type=b'text/plain')


class UserList(ListCreateAPIView):
    """
    List all users, or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = b'name'


class UserDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = b'name'


class GroupList(ListCreateAPIView):
    """
    List all groups, or create a new group.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = b'name'


class GroupDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a group instance.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = b'name'


def change_own_password(request):
    ldap_user = get_object_or_404(User, name=request.user.username)
    if request.method == b'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            ldap_user.set_password(form.cleaned_data[b'password_1'])
            return HttpResponseRedirect(reverse(b'index'))
    else:
        form = PasswordForm()
    template_values = {b'form': form}
    return render_to_response(b'penatesserver/change_password.html', template_values, RequestContext(request))


def get_user_mobileconfig(request):
    user = get_object_or_404(User, name=request.user.username)
    password = request.GET.get(b'password', b'')
    if not password:
        password = user.read_password()
    password = password or b'password'
    pki = PKI()
    p12_certificates = []
    for entry, title in (
     (
      user.user_certificate_entry, _(b'User certificate')),
     (
      user.encipherment_certificate_entry, _(b'Encipherment certificate')),
     (
      user.email_certificate_entry, _(b'Email certificate')),
     (
      user.signature_certificate_entry, _(b'Signature certificate'))):
        with tempfile.NamedTemporaryFile() as (fd):
            filename = fd.name
        pki.ensure_certificate(entry)
        pki.gen_pkcs12(entry, filename, password=password)
        p12_certificates.append((filename, title))

    def f_scheme(y):
        if y in ('caldav', 'carddav'):
            return b'http'
        return y

    kerberos_prefixes = [ b'%s%s://%s/' % (f_scheme(x[0]), b's' if x[2] == b'tls' else b'', x[1]) for x in Service.objects.filter(scheme__in=[b'http', b'smtp', b'imap', b'ldap', b'caldav', b'carddav']).exclude(kerberos_service=None).values_list(b'scheme', b'hostname', b'encryption')
                        ]
    domain_components = settings.PENATES_DOMAIN.split(b'.')
    domain_components.reverse()
    inverted_domain = (b'.').join(domain_components)
    template_values = {b'domain': settings.PENATES_DOMAIN, 
       b'inverted_domain': inverted_domain, 
       b'organization': settings.PENATES_ORGANIZATION, 
       b'realm': settings.PENATES_REALM, 
       b'ldap_servers': [], b'carddav_servers': [], b'caldav_servers': [], b'email_servers': [], b'kerberos_prefixes': kerberos_prefixes, 
       b'vpn_servers': [], b'http_proxies': [], b'password': password, 
       b'username': user.name, 
       b'user': user, 
       b'ldap_base_dn': settings.LDAP_BASE_DN, 
       b'ca_cert_path': pki.cacrt_path, 
       b'hosts_crt_path': pki.hosts_crt_path, 
       b'users_crt_path': pki.users_crt_path, 
       b'services_crt_path': pki.services_crt_path, 
       b'p12_certificates': p12_certificates}
    mail_services = {}
    for service in Service.objects.all():
        if service.scheme == b'ldap':
            template_values[b'ldap_servers'].append(service)
        elif service.scheme == b'carddav':
            template_values[b'carddav_servers'].append(service)
        elif service.scheme == b'caldav':
            template_values[b'caldav_servers'].append(service)
        elif service.scheme == b'imap':
            mail_services.setdefault(service.hostname, {})[b'imap'] = service
        elif service.scheme == b'smtp':
            mail_services.setdefault(service.hostname, {})[b'smtp'] = service
        elif service.scheme == b'proxy_http':
            template_values[b'http_proxies'].append(service)

    template_values[b'email_servers'] = list(mail_services.values())
    response = render_to_response(b'penatesserver/mobileconfig.xml', template_values, content_type=b'application/xml')
    for filename, title in p12_certificates:
        os.remove(filename)

    response[b'Content-Disposition'] = b'attachment; filename=%s.mobileconfig' % request.user.username
    return response