# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/powerdns/models.py
# Compiled at: 2015-12-29 03:04:14
from __future__ import unicode_literals
import codecs, datetime, re, time
from django.conf import settings
from django.utils.six import text_type
import netaddr
from penatesserver.pki.service import CertificateEntry
from django.db import models
from penatesserver.subnets import get_subnets
__author__ = b'Matthieu Gallet'

class Comment(models.Model):
    domain = models.ForeignKey(b'Domain')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    modified_at = models.IntegerField()
    account = models.CharField(max_length=40, blank=True, null=True)
    comment = models.CharField(max_length=65535)

    class Meta(object):
        managed = False
        db_table = b'comments'


class CryptoKey(models.Model):
    domain = models.ForeignKey(b'Domain', blank=True, null=True)
    flags = models.IntegerField()
    active = models.NullBooleanField()
    content = models.TextField(blank=True, null=True)

    class Meta(object):
        managed = False
        db_table = b'cryptokeys'


class DomainMetadata(models.Model):
    domain = models.ForeignKey(b'Domain', blank=True, null=True)
    kind = models.CharField(max_length=32, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta(object):
        managed = False
        db_table = b'domainMetadata'


class Domain(models.Model):
    name = models.CharField(unique=True, max_length=255)
    master = models.CharField(max_length=128, blank=True, null=True, default=None)
    last_check = models.IntegerField(blank=True, null=True, default=None)
    type = models.CharField(max_length=6, default=b'NATIVE')
    notified_serial = models.IntegerField(blank=True, null=True, default=None)
    account = models.CharField(max_length=40, blank=True, null=True, default=None)

    class Meta(object):
        managed = False
        db_table = b'domains'

    @staticmethod
    def default_record_values(ttl=86400, prio=0, disabled=False, auth=True, change_date=None):
        return {b'ttl': ttl, b'prio': prio, b'disabled': disabled, b'auth': auth, b'change_date': change_date or time.time()}

    def set_extra_records(self, scheme, hostname, port, fqdn, srv_field, entry=None):
        if scheme == b'dns':
            soa_serial = self.get_soa_serial()
            for domain in Domain.objects.filter(name__in=[self.name, b'%s%s' % (settings.PDNS_ADMIN_PREFIX, self.name),
             b'%s%s' % (settings.PDNS_INFRA_PREFIX, self.name)]):
                Record.objects.get_or_create(domain=domain, type=b'NS', name=domain.name, content=hostname)
                if Record.objects.filter(domain=domain, type=b'SOA').count() == 0:
                    content = b'%s %s %s 10800 3600 604800 3600' % (hostname, settings.PENATES_EMAIL_ADDRESS, soa_serial)
                    Record.objects.get_or_create(domain=domain, type=b'SOA', name=domain.name, content=content)

        elif scheme == b'smtp' and port == 25:
            Record.objects.get_or_create(defaults={b'prio': 10}, domain=self, type=b'MX', name=self.name, content=hostname)
            content = b'v=spf1 mx mx:%s -all' % self.name
            if Record.objects.filter(domain=self, type=b'TXT', name=self.name, content__startswith=b'v=spf1').update(content=content) == 0:
                Record(domain=self, type=b'TXT', name=self.name, content=content).save()
        elif scheme == b'dkim' and entry is not None:
            assert isinstance(entry, CertificateEntry)
            with codecs.open(entry.pub_filename, b'r', encoding=b'utf-8') as (fd):
                content = fd.read()
            content = b'v=DKIM1; k=rsa; p=' + content.replace(b'-----END PUBLIC KEY-----', b'').replace(b'-----BEGIN PUBLIC KEY-----', b'').strip()
            name = b'%s._domainkey.%s' % (hostname.partition(b'.')[0], self.name)
            if Record.objects.filter(domain=self, type=b'TXT', name=name, content__startswith=b'v=DKIM1;').update(content=content) == 0:
                Record(domain=self, type=b'TXT', name=name, content=content).save()
            content = b't=n;o=-;r=postmaster@%s' % self.name
            name = b'_domainkey.%s' % self.name
            if Record.objects.filter(domain=self, type=b'TXT', name=name, content=content).count() == 0:
                Record(domain=self, type=b'TXT', name=name, content=content).save()
        if srv_field:
            matcher_full = re.match(b'^(\\w+)/([\\-\\w]+):(\\d+):(\\d+)$', srv_field)
            matcher_protocol = re.match(b'^([\\-\\w]+)/(\\w+)$', srv_field)
            matcher_service = re.match(b'^([\\-\\w]+)$', srv_field)
            if matcher_full:
                self.ensure_srv_record(matcher_full.group(1), matcher_full.group(2), port, int(matcher_full.group(3)), int(matcher_full.group(4)), fqdn)
            elif matcher_protocol:
                self.ensure_srv_record(matcher_protocol.group(1), matcher_protocol.group(2), port, 0, 100, fqdn)
            elif matcher_service:
                self.ensure_srv_record(b'tcp', matcher_service.group(1), port, 0, 100, fqdn)
        return

    def set_certificate_records(self, entry, protocol, hostname, port):
        record_name = b'_%s.%s' % (protocol, hostname)
        Record.objects.get_or_create(name=record_name, domain=self)
        record_name = b'_%d._%s.%s' % (port, protocol, hostname)
        content = b'3 0 1 %s' % entry.crt_sha256
        if Record.objects.filter(name=record_name, domain=self, type=b'TLSA').update(content=content) == 0:
            Record(name=record_name, domain=self, type=b'TLSA', content=content).save()

    @staticmethod
    def get_soa_serial():
        return datetime.datetime.now().strftime(text_type(b'%Y%m%d%H'))

    def update_soa(self):
        records = list(Record.objects.filter(domain=self, type=b'SOA')[0:1])
        if not records:
            return False
        record = records[0]
        values = record.content.split()
        if len(values) != 7:
            return False
        hostname, email, serial, refresh, retry, expire, default_ttl = values
        serial = self.get_soa_serial()
        Record.objects.filter(pk=record.pk).update(content=(b' ').join((hostname, email, serial, refresh, retry, expire, default_ttl)))
        return True

    def ensure_srv_record(self, protocol, service, port, prio, weight, fqdn):
        name = b'_%s.%s' % (protocol, self.name)
        Record.objects.get_or_create(defaults={b'prio': None}, domain=self, type=None, name=name, content=None)
        name = b'_%s._%s.%s' % (service, protocol, self.name)
        content = b'%s %s %s' % (weight, port, fqdn)
        Record.objects.get_or_create(defaults={b'prio': prio}, domain=self, type=b'SRV', name=name, content=content)
        return

    @staticmethod
    def ensure_auto_record(source, target, unique=False, override_reverse=False):
        base, sep, domain_name = target.partition(b'.')
        domain = Domain.objects.get(name=domain_name)
        domain.ensure_record(source, target, unique=unique, override_reverse=override_reverse)
        domain.update_soa()

    def ensure_record(self, source, target, unique=False, override_reverse=True):
        """
        :param source: orignal name (fqdn of the machine, or IP address)
        :param target: DNS alias to create
        :param unique: if True, remove any previous
        :rtype: :class:`penatesserver.powerdns.models.Domain`
        """
        record_name, sep, domain_name = target.partition(b'.')
        if sep != b'.' or domain_name != self.name:
            return False
        if source == target:
            return True
        else:
            try:
                add = netaddr.IPAddress(source)
                record_type = b'A' if add.version == 4 else b'AAAA'
            except netaddr.core.AddrFormatError:
                record_type = b'CNAME'
                add = None

            if not unique and Record.objects.filter(domain=self, name=target, type=record_type, content=source).count() > 0:
                return True
            if record_type == b'A' or record_type == b'AAAA':
                for subnet_obj in get_subnets():
                    if add.version != subnet_obj.network.version or add not in subnet_obj.network:
                        continue
                    reverse_record_name, sep, reverse_domain_name = add.reverse_dns.partition(b'.')
                    reverse_domain_name = reverse_domain_name[:-1]
                    reverse_target = add.reverse_dns[:-1]
                    reverse_domain = self.ensure_subdomain(reverse_domain_name)
                    query = Record.objects.filter(domain=reverse_domain, name=reverse_target, type=b'PTR')
                    if override_reverse and query.update(content=target) == 0 or not override_reverse and query.count() == 0:
                        Record(domain=reverse_domain, name=reverse_target, type=b'PTR', content=target, ttl=3600).save()
                        assert isinstance(reverse_domain, Domain)
                        reverse_domain.update_soa()

            if Record.objects.filter(domain=self, name=target, type__in=[b'A', b'AAAA', b'CNAME']).update(type=record_type, content=source, ttl=3600) == 0:
                Record(domain=self, name=target, type=record_type, content=source, ttl=3600).save()
            return True

    def ensure_subdomain(self, subdomain_name):
        subdomain, created = Domain.objects.get_or_create(name=subdomain_name)
        Record.objects.get_or_create(defaults={b'prio': None}, domain=self, type=None, name=subdomain_name, content=None)
        if Record.objects.filter(domain=subdomain, type=b'SOA').count() == 0:
            soa_records = list(Record.objects.filter(domain=self, type=b'SOA')[0:1])
            if soa_records:
                Record(domain=subdomain, type=b'SOA', name=subdomain_name, content=soa_records[0].content).save()
        return subdomain

    def __repr__(self):
        return b"Domain('%s')" % self.name


class Record(models.Model):
    domain = models.ForeignKey(Domain, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=65535, blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True, default=86400)
    prio = models.IntegerField(blank=True, null=True, default=0)
    change_date = models.IntegerField(blank=True, null=True, default=time.time)
    disabled = models.NullBooleanField(default=False)
    ordername = models.CharField(max_length=255, blank=True, null=True)
    auth = models.NullBooleanField(default=True)

    def __repr__(self):
        if self.type in ('NS', 'SOA', 'MX'):
            return b'Record("%s [%s] -> %s")' % (self.name, self.type, self.content)
        return b'Record("%s [%s] -> %s")' % (self.name, self.type, self.content)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        domain_name = self.domain.name
        self.auth = self.name.endswith(domain_name)
        if self.auth:
            comp = self.name[:-(1 + len(domain_name))].split(text_type(b'.'))
            comp.reverse()
            self.ordername = (b' ').join(comp)
        super(Record, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta(object):
        managed = False
        db_table = b'records'

    @staticmethod
    def local_resolve(name, searched_types=None):
        """ Try to locally resolve a name to A or AAAA record
        :param name:
        :type name:
        :rtype: basestring
        """
        if searched_types is None:
            searched_types = [
             b'A', b'AAAA', b'CNAME']
        try:
            netaddr.IPAddress(name)
            return name
        except netaddr.core.AddrFormatError:
            pass

        to_check = [name]
        excluded = set()
        while to_check:
            new_to_check = []
            for record_data in Record.objects.filter(name__in=to_check, type__in=searched_types).values_list(b'type', b'content'):
                if record_data[0] == b'A' or record_data[0] == b'AAAA':
                    return record_data[1]
                if record_data[1] not in excluded:
                    new_to_check.append(record_data[1])
                excluded.add(record_data[1])

            searched_types = [
             b'A', b'AAAA', b'CNAME']
            to_check = new_to_check

        return


class Supermaster(models.Model):
    ip = models.GenericIPAddressField()
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40)

    class Meta(object):
        managed = False
        db_table = b'supermasters'
        unique_together = (('ip', 'nameserver'), )


class TSIGKey(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)

    class Meta(object):
        managed = False
        db_table = b'tsigkeys'
        unique_together = (('name', 'algorithm'), )