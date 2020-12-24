# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/pki/service.py
# Compiled at: 2015-12-29 03:19:15
"""
my_ca = PKI(dirname="/tmp/test")
my_ca.initialize()
my_ca.gen_ca(CertificateEntry("ca.19pouces.net", role=CA))
"""
from __future__ import unicode_literals, with_statement, print_function
import base64, codecs, hashlib, os, datetime, re, shlex, shutil
from subprocess import CalledProcessError
import subprocess, tempfile
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.timezone import utc
from penatesserver.filelocks import Lock
from penatesserver.pki.constants import ROLES, RSA, RESOURCE, USER, ENCIPHERMENT, SIGNATURE, EMAIL, COMPUTER_TEST, COMPUTER, CA
from penatesserver.utils import t61_to_time, ensure_location

def local(command, cwd=None):
    return subprocess.check_output(shlex.split(command), shell=False, cwd=cwd, stderr=subprocess.PIPE)


__author__ = b'Matthieu Gallet'

class CertificateEntry(object):

    def __init__(self, commonName, organizationName=b'', organizationalUnitName=b'', emailAddress=b'', localityName=b'', countryName=b'', stateOrProvinceName=b'', altNames=None, role=RESOURCE, dirname=None):
        self.commonName = commonName
        self.organizationName = organizationName
        self.organizationalUnitName = organizationalUnitName
        self.emailAddress = emailAddress
        self.localityName = localityName
        self.countryName = countryName
        self.stateOrProvinceName = stateOrProvinceName
        self.altNames = altNames or []
        self.role = role
        self.dirname = dirname or settings.PKI_PATH

    @property
    def filename(self):
        basename = b'%s_%s' % (self.role, self.commonName)
        return slugify(basename)

    @property
    def values(self):
        return ROLES[self.role]

    @property
    def key_filename(self):
        return os.path.join(self.dirname, b'private', b'keys', self.filename + b'.key.pem')

    @property
    def pub_filename(self):
        return os.path.join(self.dirname, b'pubkeys', self.filename + b'.pub.pem')

    @property
    def ssh_filename(self):
        return os.path.join(self.dirname, b'pubsshkeys', self.filename + b'.pub')

    @property
    def sshfp_sha1(self):
        with codecs.open(self.ssh_filename, b'r', encoding=b'utf-8') as (fd):
            method, content = fd.read().split(b' ')
        value = hashlib.sha1(base64.b64decode(content)).hexdigest()
        code = {b'ssh-rsa': 1, b'ssh-dss': 2, b'ecdsa-sha2-nistp256': 3, b'ssh-ed25519': 4}.get(method, 0)
        return b'%s 1 %s' % (code, value)

    @property
    def sshfp_sha256(self):
        with codecs.open(self.ssh_filename, b'r', encoding=b'utf-8') as (fd):
            method, content = fd.read().split(b' ')
        value = hashlib.sha256(base64.b64decode(content)).hexdigest()
        code = {b'ssh-rsa': 1, b'ssh-dss': 2, b'ecdsa-sha2-nistp256': 3, b'ssh-ed25519': 4}.get(method, 0)
        return b'%s 2 %s' % (code, value)

    @property
    def crt_filename(self):
        return os.path.join(self.dirname, b'certs', self.filename + b'.crt.pem')

    @property
    def req_filename(self):
        return os.path.join(self.dirname, b'private', b'req', self.filename + b'.req.pem')

    @property
    def ca_filename(self):
        return os.path.join(self.dirname, b'cacert.pem')

    @property
    def crt_sha256(self):
        return self.pem_hash(self.crt_filename, hashlib.sha256)

    @property
    def pub_sha256(self):
        return self.pem_hash(self.pub_filename, hashlib.sha256)

    @property
    def crt_sha512(self):
        return self.pem_hash(self.crt_filename, hashlib.sha512)

    @property
    def pub_sha512(self):
        return self.pem_hash(self.pub_filename, hashlib.sha512)

    @staticmethod
    def pem_hash(filename, hash_cls=None):
        if hash_cls is None:
            hash_cls = hashlib.sha256
        with codecs.open(filename, b'r', encoding=b'utf-8') as (fd):
            content = fd.read()
        b64_der = (b'').join(content.splitlines()[1:-1])
        der = base64.b64decode(b64_der)
        return hash_cls(der).hexdigest()

    def __repr__(self):
        return self.commonName

    def __unicode__(self):
        return self.commonName

    def __str__(self):
        return self.commonName


class PKI(object):

    def __init__(self, dirname=None):
        self.dirname = dirname or settings.PKI_PATH
        self.cacrl_path = os.path.join(self.dirname, b'cacrl.pem')
        self.careq_path = os.path.join(self.dirname, b'private', b'careq.pem')
        self.crt_sources_path = os.path.join(self.dirname, b'crt_sources.txt')
        self.cacrt_path = os.path.join(self.dirname, b'cacert.pem')
        self.users_crt_path = os.path.join(self.dirname, b'users_crt.pem')
        self.hosts_crt_path = os.path.join(self.dirname, b'hosts_crt.pem')
        self.services_crt_path = os.path.join(self.dirname, b'services_crt.pem')
        self.cakey_path = os.path.join(self.dirname, b'private', b'cakey.pem')
        self.users_key_path = os.path.join(self.dirname, b'private', b'users_key.pem')
        self.hosts_key_path = os.path.join(self.dirname, b'private', b'hosts_key.pem')
        self.services_key_path = os.path.join(self.dirname, b'private', b'services_key.pem')

    def get_subca_infos(self, entry):
        assert isinstance(entry, CertificateEntry)
        if entry.role in (USER, EMAIL, SIGNATURE, ENCIPHERMENT):
            return (self.users_crt_path, self.users_key_path)
        if entry.role in (COMPUTER, COMPUTER_TEST):
            return (self.hosts_crt_path, self.hosts_key_path)
        if entry.role == CA:
            return (self.cacrt_path, self.cakey_path)
        return (
         self.services_crt_path, self.services_key_path)

    def initialize(self):
        with Lock(settings.PENATES_LOCKFILE):
            serial = os.path.join(self.dirname, b'serial.txt')
            index = os.path.join(self.dirname, b'index.txt')
            ensure_location(serial)
            if not os.path.isfile(serial):
                with codecs.open(serial, b'w', encoding=b'utf-8') as (fd):
                    fd.write(b'01\n')
            if not os.path.isfile(index):
                with codecs.open(index, b'w', encoding=b'utf-8') as (fd):
                    fd.write(b'')
            ensure_location(os.path.join(self.dirname, b'new_certs', b'0'))

    def ensure_key(self, entry):
        """
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        if not self.__check_key(entry, entry.key_filename):
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_key(entry)
                self.__gen_pub(entry)
                self.__gen_ssh(entry)
        elif not self.__check_pub(entry, entry.pub_filename):
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_pub(entry)
                self.__gen_ssh(entry)
        elif not self.__check_ssh(entry, entry.ssh_filename):
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_ssh(entry)

    def ensure_certificate(self, entry):
        """

        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        if not self.__check_key(entry, entry.key_filename):
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_key(entry)
                self.__gen_pub(entry)
                self.__gen_ssh(entry)
                self.__gen_request(entry)
                self.__gen_certificate(entry)
        elif not self.__check_certificate(entry, entry.crt_filename):
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_request(entry)
                self.__gen_certificate(entry)

    def __gen_openssl_conf(self, entry=None, ca_infos=None):
        """
        principal: used to define values
        ca: used to define issuer values for settings.CA_POINT, settings.CRL_POINT, settings.OCSP_POINT
        temp_object: used to track temporary files and correctly remove them after use
        keyType: used to define issuer values for settings.CA_POINT, settings.CRL_POINT, settings.OCSP_POINT,
            settings.KERBEROS_REALM
        crts: list of revoked Certificate objects

        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        if ca_infos is None:
            ca_crt_path, ca_key_path = self.cacrt_path, self.cakey_path
        else:
            ca_crt_path, ca_key_path = ca_infos
        context = {b'dirname': self.dirname, b'policy_details': [], b'crlPoint': b'', b'caPoint': b'', b'altSection': b'', b'altNamesString': b'', b'krbRealm': b'', b'krbClientName': b'', b'ca_key_path': ca_key_path, b'ca_crt_path': ca_crt_path}
        if entry is not None:
            assert isinstance(entry, CertificateEntry)
            role = ROLES[entry.role]
            for key in ('organizationName', 'organizationalUnitName', 'emailAddress',
                        'localityName', 'stateOrProvinceName', 'countryName', 'commonName'):
                context[key] = getattr(entry, key)

            alt_names = list(entry.altNames)
            for k in ('basicConstraints', 'subjectKeyIdentifier', 'authorityKeyIdentifier'):
                context[b'policy_details'].append((k, role[k]))

            for k in ('keyUsage', 'extendedKeyUsage', 'nsCertType'):
                context[b'policy_details'].append((k, (b', ').join(role[k])))

            if b'1.3.6.1.5.2.3.4' in role[b'extendedKeyUsage'] and settings.PENATES_REALM:
                alt_names.append(('otherName', '1.3.6.1.5.2.2;SEQUENCE:princ_name'))
                context[b'krbRealm'] = settings.PENATES_REALM
                context[b'krbClientName'] = entry.commonName
            if b'1.3.6.1.5.2.3.5' in role[b'extendedKeyUsage'] and settings.PENATES_REALM:
                alt_names.append(('otherName', '1.3.6.1.5.2.2;SEQUENCE:kdc_princ_name'))
                context[b'krbRealm'] = settings.PENATES_REALM
            if alt_names:
                alt_list = [ (b'{0}.{1} = {2}').format(alt[0], i, alt[1]) for i, alt in enumerate(alt_names) ]
                context[b'altNamesString'] = (b'\n').join(alt_list)
                context[b'altSection'] = b'subjectAltName=@alt_section'
                if settings.SERVER_NAME:
                    context[b'crlPoint'] = b'%s://%s%s' % (settings.PROTOCOL, settings.SERVER_NAME, reverse(b'get_crl'))
                    context[b'caPoint'] = b'%s://%s%s' % (settings.PROTOCOL, settings.SERVER_NAME,
                     reverse(b'get_ca_certificate', kwargs={b'kind': b'ca'}))
        conf_content = render_to_string(b'penatesserver/pki/openssl.cnf', context)
        conf_path = os.path.join(self.dirname, b'openssl.cnf')
        with codecs.open(conf_path, b'w', encoding=b'utf-8') as (conf_fd):
            conf_fd.write(conf_content)
        return conf_path

    @staticmethod
    def __gen_key(entry):
        u""" génère la clef privée pour l'entrée fournie
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        role = ROLES[entry.role]
        ensure_location(entry.key_filename)
        if role[b'keyType'] == RSA:
            local((b'"{openssl}" genrsa -out {key} {bits}').format(bits=role[b'rsaBits'], openssl=settings.OPENSSL_PATH, key=entry.key_filename))
        else:
            with tempfile.NamedTemporaryFile() as (fd):
                param = fd.name
            local((b'"{openssl}" dsaparam -rand -genkey {bits} -out "{param}"').format(bits=role[b'dsaBits'], openssl=settings.OPENSSL_PATH, param=param))
            local((b'"{openssl}" gendsa -out "{key}" "{param}"').format(openssl=settings.OPENSSL_PATH, param=param, key=entry.key_filename))
            os.remove(param)
        os.chmod(entry.key_filename, 384)

    @staticmethod
    def __gen_pub(entry):
        u""" génère la clef publique pour l'entrée fournie
        la clef privée doit exister
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        role = ROLES[entry.role]
        ensure_location(entry.pub_filename)
        if role[b'keyType'] == RSA:
            local((b'"{openssl}" rsa -in "{key}" -out "{pub}" -pubout').format(openssl=settings.OPENSSL_PATH, key=entry.key_filename, pub=entry.pub_filename))
        else:
            local((b'"{openssl}" dsa -in "{key}" -out "{pub}" -pubout').format(openssl=settings.OPENSSL_PATH, key=entry.key_filename, pub=entry.pub_filename))

    @staticmethod
    def __gen_ssh(entry):
        u""" génère la clef publique SSH pour l'entrée fournie
        la clef privée doit exister
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        result = local((b'"{ssh_keygen}" -y -f "{inkey}" ').format(inkey=entry.key_filename, ssh_keygen=settings.SSH_KEYGEN_PATH))
        ensure_location(entry.ssh_filename)
        with open(entry.ssh_filename, b'wb') as (ssh_fd):
            ssh_fd.write(result)

    def __gen_request(self, entry):
        u""" génère une demande de certificat pour l'entrée fournie
        la clef privée doit exister
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        conf_path = self.__gen_openssl_conf(entry)
        role = ROLES[entry.role]
        ensure_location(entry.req_filename)
        local((b'"{openssl}" req  -out "{out}" -batch -utf8 -new -key "{inkey}" -{digest} -config "{config}" -extensions role_req').format(openssl=settings.OPENSSL_PATH, inkey=entry.key_filename, digest=role[b'digest'], config=conf_path, out=entry.req_filename))

    def __gen_certificate(self, entry):
        u""" génère un certificat pour l'entrée fournie
        la demande de certificat doit exister, ainsi que la CA
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        ensure_location(entry.crt_filename)
        subca_infos = self.get_subca_infos(entry)
        conf_path = self.__gen_openssl_conf(entry, ca_infos=subca_infos)
        role = ROLES[entry.role]
        local((b'"{openssl}" ca -config "{cfg}" -extensions role_req -in "{req}" -out "{crt}" -notext -days {days} -md {digest} -batch -utf8 ').format(openssl=settings.OPENSSL_PATH, cfg=conf_path, req=entry.req_filename, crt=entry.crt_filename, days=role[b'days'], digest=role[b'digest']))
        serial = self.__get_certificate_serial(entry.crt_filename)
        with codecs.open(self.crt_sources_path, b'a', encoding=b'utf-8') as (fd):
            fd.write(b'%s\t%s\t%s\t%s\n' % (serial, os.path.relpath(entry.key_filename, self.dirname),
             os.path.relpath(entry.req_filename, self.dirname),
             os.path.relpath(entry.crt_filename, self.dirname)))

    def __gen_ca_key(self, entry):
        """
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        role = ROLES[entry.role]
        ensure_location(self.cakey_path)
        if role[b'keyType'] == RSA:
            local((b'"{openssl}" genrsa -out {key} {bits}').format(bits=role[b'rsaBits'], openssl=settings.OPENSSL_PATH, key=self.cakey_path))
        else:
            with tempfile.NamedTemporaryFile() as (fd):
                param = fd.name
            local((b'"{openssl}" dsaparam -rand -genkey {bits} -out "{param}"').format(bits=role[b'dsaBits'], openssl=settings.OPENSSL_PATH, param=param))
            local((b'"{openssl}" gendsa -out "{key}" "{param}"').format(openssl=settings.OPENSSL_PATH, param=param, key=self.cakey_path))
            os.remove(param)
        os.chmod(self.cakey_path, 384)

    def __gen_ca_req(self, entry):
        """
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        role = ROLES[entry.role]
        ensure_location(entry.req_filename)
        conf_path = self.__gen_openssl_conf(entry)
        local((b'"{openssl}" req  -out "{out}" -batch -utf8 -new -key "{inkey}" -{digest} -config "{config}" -extensions role_req').format(openssl=settings.OPENSSL_PATH, inkey=self.cakey_path, digest=role[b'digest'], config=conf_path, out=entry.req_filename))

    def __gen_ca_crt(self, entry):
        """
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        conf_path = self.__gen_openssl_conf(entry)
        role = ROLES[entry.role]
        ensure_location(self.cacrt_path)
        local((b'"{openssl}" ca -config "{cfg}" -selfsign -extensions role_req -in "{req}" -out "{crt}" -notext -days {days} -md {digest} -batch -utf8 ').format(openssl=settings.OPENSSL_PATH, cfg=conf_path, req=entry.req_filename, crt=self.cacrt_path, days=role[b'days'], digest=role[b'digest']))

    def ensure_ca(self, entry):
        u""" si la clef privée de la CA n'existe pas, crée une nouvelle CA
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        """
        if not self.__check_key(entry, self.cakey_path):
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_ca_key(entry)
                self.__gen_ca_req(entry)
                self.__gen_ca_crt(entry)
            for sub_name in ('users', 'services', 'hosts'):
                sub_entry = CertificateEntry(b'%s.%s' % (sub_name, entry.commonName), organizationName=entry.organizationName, organizationalUnitName=entry.organizationalUnitName, emailAddress=entry.emailAddress, localityName=entry.localityName, countryName=entry.countryName, stateOrProvinceName=entry.stateOrProvinceName, dirname=entry.dirname, role=CA)
                self.ensure_certificate(sub_entry)
                shutil.copy(sub_entry.crt_filename, getattr(self, b'%s_crt_path' % sub_name))
                shutil.copy(sub_entry.key_filename, getattr(self, b'%s_key_path' % sub_name))

    @staticmethod
    def __check_pub(entry, path):
        """ vrai si la clef publique est valide
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        :return:
        :rtype: `boolean`
        """
        if not os.path.isfile(path):
            return False
        cmd = b'rsa' if ROLES[entry.role][b'keyType'] == RSA else b'dsa'
        try:
            local((b'"{openssl}" {cmd} -pubout -pubin -in "{path}"').format(openssl=settings.OPENSSL_PATH, cmd=cmd, path=path))
        except CalledProcessError:
            return False

        return True

    @staticmethod
    def __check_key(entry, path):
        u""" vrai si la clef privée est valide
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        :return:
        :rtype: `boolean`
        """
        if not os.path.isfile(path):
            return False
        cmd = b'rsa' if ROLES[entry.role][b'keyType'] == RSA else b'dsa'
        try:
            local((b'"{openssl}" {cmd} -pubout -in "{path}"').format(openssl=settings.OPENSSL_PATH, cmd=cmd, path=path))
        except CalledProcessError:
            return False

        return True

    @staticmethod
    def __check_ssh(entry, path):
        """ vrai si la clef publique SSH est valide
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        :return:
        :rtype: `boolean`
        """
        entry = entry
        if not os.path.isfile(path):
            return False
        return True

    @staticmethod
    def __check_req(entry, path):
        u""" vrai si la requête est valide
        :param entry:
        :type entry: :class:`penatesserver.pki.service.CertificateEntry`
        :return:
        :rtype: `boolean`
        """
        entry = entry
        if not os.path.isfile(path):
            return False
        try:
            local((b'"{openssl}" req -pubkey -noout -in "{path}"').format(openssl=settings.OPENSSL_PATH, path=path))
        except CalledProcessError:
            return False

        return True

    def __check_certificate(self, entry, path):
        entry = entry
        if not os.path.isfile(path):
            return False
        else:
            try:
                stdout = local((b'"{openssl}" x509 -enddate -noout -in "{path}"').format(openssl=settings.OPENSSL_PATH, path=path))
            except CalledProcessError:
                return False

            stdout = stdout.decode(b'utf-8')
            end_date = t61_to_time(stdout.partition(b'=')[2].strip())
            after_now = datetime.datetime.now(tz=utc) + datetime.timedelta(30)
            if end_date is None or end_date < after_now:
                return False
            serial = self.__get_certificate_serial(path)
            if serial is None:
                return False
            if self.__get_index_file()[serial][1] != b'V':
                return False
            return True

    def revoke_certificate(self, crt_content, regen_crl=True):
        with Lock(settings.PENATES_LOCKFILE):
            with tempfile.NamedTemporaryFile() as (fd):
                fd.write(crt_content.encode(b'utf-8'))
                fd.flush()
                serial = self.__get_certificate_serial(fd.name)
                infos = self.__get_index_file()[serial]
                if infos[1] != b'V':
                    return
                conf_path = self.__gen_openssl_conf()
                local((b'"{openssl}" ca -config "{cfg}" -revoke {filename}').format(openssl=settings.OPENSSL_PATH, cfg=conf_path, filename=fd.name))
        key_filename = os.path.join(self.dirname, infos[5])
        if os.path.isfile(key_filename):
            with open(key_filename, b'rb') as (fd):
                content = fd.read()
            os.remove(key_filename)
            with open(key_filename + b'.bak', b'ab') as (fd):
                fd.write(content)
        req_filename = os.path.join(self.dirname, infos[6])
        if os.path.isfile(req_filename):
            os.remove(req_filename)
        crt_filename = os.path.join(self.dirname, infos[7])
        if os.path.isfile(crt_filename):
            os.remove(crt_filename)
        if regen_crl:
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_crl(20)

    @staticmethod
    def __get_certificate_serial(filename):
        cmd = [settings.OPENSSL_PATH, b'x509', b'-serial', b'-noout', b'-in', filename]
        serial_text = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode(b'utf-8')
        matcher = re.match(b'^serial=([\\dA-F]+)$', serial_text.strip())
        if not matcher:
            return None
        else:
            return matcher.group(1)

    def ensure_crl(self):
        if not self.__check_crl():
            with Lock(settings.PENATES_LOCKFILE):
                self.__gen_crl(20)

    def __check_crl(self):
        try:
            content = subprocess.check_output([settings.OPENSSL_PATH, b'crl', b'-noout', b'-nextupdate', b'-in',
             self.cacrl_path], stderr=subprocess.PIPE)
        except CalledProcessError:
            return False

        key, sep, value = content.decode(b'utf-8').partition(b'=')
        if key != b'nextUpdate' or sep != b'=':
            return False
        return t61_to_time(value.strip()) > datetime.datetime.now(utc) + datetime.timedelta(seconds=86400)

    def __gen_crl(self, crldays):
        config = self.__gen_openssl_conf()
        content = subprocess.check_output([settings.OPENSSL_PATH, b'ca', b'-gencrl', b'-utf8', b'-config', config,
         b'-keyfile', self.cakey_path, b'-cert', self.cacrt_path, b'-crldays',
         str(crldays)], stderr=subprocess.PIPE)
        with open(self.cacrl_path, b'wb') as (fd):
            fd.write(content)

    def __get_index_file(self):
        """Return a dict ["serial"] = ["serial", "V|R", "valid_date", "revoke_date", "cn", "key filename",
        "req filename", "crt filename"]
        :return:
        :rtype:
        """
        result = {}
        with codecs.open(os.path.join(self.dirname, b'index.txt'), b'r', encoding=b'utf-8') as (fd):
            for line in fd:
                if not line:
                    continue
                state, valid_date, revoke_date, serial, unused, cn = line.split(b'\t')
                result[serial] = [serial, state, valid_date, revoke_date, cn, None, None, None]

        if os.path.isfile(self.crt_sources_path):
            with codecs.open(self.crt_sources_path, b'r', encoding=b'utf-8') as (fd):
                for line in fd:
                    if not line:
                        continue
                    serial, key, req, crt = line.split(b'\t')
                    result[serial][5] = key
                    result[serial][6] = req
                    result[serial][7] = crt

        return result

    def gen_pkcs12(self, entry, filename, password):
        assert isinstance(entry, CertificateEntry)
        self.ensure_certificate(entry)
        with tempfile.NamedTemporaryFile() as (fd):
            fd.write(password.encode(b'utf-8'))
            fd.flush()
            p = subprocess.Popen([settings.OPENSSL_PATH, b'pkcs12', b'-export', b'-out', filename, b'-passout',
             b'file:%s' % fd.name, b'-aes256', b'-in', entry.crt_filename, b'-inkey',
             entry.key_filename, b'-certfile', self.cacrt_path, b'-name', entry.filename])
            p.communicate()