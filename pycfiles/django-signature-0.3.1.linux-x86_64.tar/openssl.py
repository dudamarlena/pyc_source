# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cyberj/src/python/vtenv2.6/lib/python2.6/site-packages/signature/openssl.py
# Compiled at: 2011-06-14 07:22:27
"""
From django-pki - Copyright (C) 2010 Daniel Kerwin <django-pki@linuxaddicted.de>
    http://github.com/dkerwin/django-pki

                - Copyright (C) 2010 Johan Charpentier <jcharpentier@bearstech.com>

This program and entire repository is free software; you can
redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software
Foundation; either version 2 of the License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; If not, see <http://www.gnu.org/licenses/>.
"""
import os, re, sys, datetime, string, random
from signature.settings import PKI_OPENSSL_BIN, PKI_OPENSSL_CONF, PKI_DIR, PKI_OPENSSL_TEMPLATE, PKI_SELF_SIGNED_SERIAL
from subprocess import Popen, PIPE, STDOUT
import shutil
from logging import getLogger
from tempfile import NamedTemporaryFile, TemporaryFile, mkdtemp
try:
    from hashlib import md5 as md5_constructor
except ImportError:
    from md5 import new as md5_constructor

from django.template.loader import render_to_string
from django.utils.encoding import smart_str, smart_unicode
logger = getLogger('pki')

def refresh_pki_metadata(ca_list):
    """Refresh pki metadata (PKI storage directories and openssl configuration files)

    Each ca_list element is a dictionary:
    'name': CA name
    'subcas_allowed': sub CAs allowed (boolean)
    """
    status = True
    dirs = {'certs': 493, 'private': 448, 
       'crl': 493}
    try:
        if not os.path.exists(PKI_DIR):
            logger.info('Creating base PKI directory')
            os.mkdir(PKI_DIR, 448)
        purge_dirs = set([ os.path.join(PKI_DIR, d) for d in os.listdir(PKI_DIR) if os.path.isdir(os.path.join(PKI_DIR, d))
                         ])
        for ca in ca_list:
            ca_dir = os.path.join(PKI_DIR, ca.name)
            if ca_dir not in purge_dirs:
                logger.info('Creating base directory for CA %s' % ca.name)
                os.mkdir(ca_dir)
                for (d, m) in dirs.items():
                    os.mkdir(os.path.join(ca_dir, d), m)

                initial_serial = 1
                try:
                    if not ca.parent and int(PKI_SELF_SIGNED_SERIAL) > 0:
                        initial_serial = PKI_SELF_SIGNED_SERIAL + 1
                except ValueError:
                    logger.error('PKI_SELF_SIGNED_SERIAL failed conversion to int!')
                else:
                    h2s = '%X' % initial_serial
                    if len(h2s) % 2 == 1:
                        h2s = '0' + h2s
                    s = open(os.path.join(ca_dir, 'serial'), 'wb')
                    s.write(h2s)
                    s.close()
                    s = open(os.path.join(ca_dir, 'crlnumber'), 'wb')
                    s.write('01')
                    s.close()
                    open(os.path.join(ca_dir, 'index.txt'), 'wb').close()
            purge_dirs.discard(ca_dir)

        for d in purge_dirs:
            if os.path.isdir(d):
                if os.path.isfile(os.path.join(d, 'crlnumber')):
                    logger.debug('Purging CA directory tree %s' % d)
                    shutil.rmtree(d)
                else:
                    logger.warning('Directory %s does not contain any metadata, preserving it' % d)

    except OSError, e:
        status = False
        logger.error('Refreshing directory structure failed: %s' % e)

    ctx = {'ca_list': ca_list}
    try:
        conf = render_to_string(PKI_OPENSSL_TEMPLATE, ctx)
        f = open(PKI_OPENSSL_CONF, 'wb')
        f.write(conf)
        f.close()
    except:
        raise Exception('Failed to render OpenSSL template')
        status = False

    return status


def in_temp_dir(func):
    """Create a temp dir and clean them on end of function
    """

    def new_func(*args, **kwargs):
        if args[0].tmpdir:
            return func(*args, **kwargs)
        tmpdir = mkdtemp()
        oldvalue = args[0].tmpdir
        args[0].tmpdir = tmpdir
        try:
            result = func(*args, **kwargs)
        finally:
            shutil.rmtree(tmpdir)
            args[0].tmpdir = oldvalue

        return result

    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


class Openssl:
    """Do the real openssl work - Generate keys, csr, sign"""

    def __init__(self, tmpdir=''):
        """Class constructor"""
        self.env_pw = ('').join(random.sample(string.letters + string.digits, 10))
        self.tmpdir = tmpdir

    class VerifyError(Exception):
        """Openssl verify fails
        """
        pass

    def exec_rehash(directory):
        """call c_rehash on directory
        """
        proc = Popen('/usr/bin/c_rehash %s' % directory, shell=False, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        (stdout_value, stderr_value) = proc.communicate()
        if proc.returncode != 0:
            raise self.VerifyError(stdout_value)
        else:
            return stdout_value

    def exec_openssl(self, command, stdin=None, env_vars=None, cwd=None):
        """Run openssl command. PKI_OPENSSL_BIN doesn't need to be specified"""
        command = [ smart_str(x) for x in command ]
        stdin = smart_str(stdin)
        c = [
         PKI_OPENSSL_BIN]
        c.extend(command)
        if env_vars:
            env_vars.setdefault('PKI_DIR', PKI_DIR)
        else:
            env_vars = {'PKI_DIR': PKI_DIR}
        proc = Popen(c, shell=False, env=env_vars, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd)
        (stdout_value, stderr_value) = proc.communicate(stdin)
        if proc.returncode != 0:
            raise self.VerifyError(stdout_value)
        else:
            return stdout_value

    def generate_self_signed_cert(self, days, subj, key, passphrase=None):
        """Generate a self signed root certificate
        """
        key_f = NamedTemporaryFile()
        key_f.write(key)
        key_f.seek(0)
        logger.info('Generating self-signed root certificate')
        command = [
         'req', '-batch', '-sha1', '-new', '-x509', '-subj', subj, '-days', str(days),
         '-extensions', 'v3_ca', '-key', key_f.name, '-passin', 'stdin']
        pem = self.exec_openssl(command, stdin=passphrase)
        return pem

    def generate_der_encoded(self):
        """Generate a DER encoded version of a given certificate"""
        logger.info('Generating DER encoded certificate for %s' % self.i.name)
        command = 'x509 -in %s -out %s -outform DER' % (self.crt, self.der)
        self.exec_openssl(command.split())
        return True

    @in_temp_dir
    def sign_csr(self, csr, cakey, cacrt, serial, days, passphrase=None, ca_capable=False):
        """Sign the CSR with given CA
        """
        shutil.copy(PKI_OPENSSL_CONF, self.tmpdir)
        confpath = os.path.join(self.tmpdir, os.path.split(PKI_OPENSSL_CONF)[(-1)])
        logger.info('Signing CSR')
        if ca_capable:
            extension = 'v3_ca'
        else:
            extension = 'usr_cert'
        csrfile = NamedTemporaryFile()
        csrfile.write(csr)
        csrfile.seek(0)
        cafile = NamedTemporaryFile()
        cafile.write(cacrt)
        cafile.seek(0)
        cakeyfile = NamedTemporaryFile()
        cakeyfile.write(cakey)
        cakeyfile.seek(0)
        serialfile = NamedTemporaryFile()
        serial = '%X' % serial
        serial = serial.rjust(2, '0')
        serialfile.write(serial)
        serialfile.seek(0)
        certfile = NamedTemporaryFile()
        command = [
         'x509', '-req', '-CAserial', serialfile.name, '-extfile', confpath, '-sha1', '-days', str(days), '-in', csrfile.name, '-CA', cafile.name, '-CAkey', cakeyfile.name, '-passin', 'stdin', '-extensions', extension, '-out', certfile.name]
        self.exec_openssl(command, stdin=passphrase)
        pem = certfile.read()
        return pem

    def _revoke_certificate(self, ppf):
        """Revoke a given certificate"""
        if self.get_revoke_status_from_cert():
            logger.info('Skipping revoke as it already happened')
            return True
        logger.info('Revoking certificate %s' % self.i.name)
        command = 'ca -config %s -name %s -batch -revoke %s -passin env:%s' % (PKI_OPENSSL_CONF, self.i.parent, self.crt, self.env_pw)
        self.exec_openssl(command.split(), env_vars={self.env_pw: str(ppf)})

    def renew_certificate(self):
        """Renew/Reissue a given certificate"""
        logger.info('Renewing certificate %s' % self.i.name)
        if os.path.exists(self.csr):
            self.sign_csr()
        else:
            raise Exception('Failed to renew certificate %s! CSR is missing!' % self.i.name)

    @in_temp_dir
    def verify_ca_chain(self, chain):
        """Verify the the CA chain
        """
        trusted_chain = [ crt for crt in chain if crt.trust ]
        certs = ('').join([ crt.pem for crt in chain ])
        for c in trusted_chain:
            filepath = os.path.join(self.tmpdir, '%s.0' % c.certhash)
            w = open(filepath, 'w')
            w.write(c.pem)
            w.close()

        command = [
         'verify', '-CApath', self.tmpdir]
        result = self.exec_openssl(command, stdin=certs)
        if result == 'stdin: OK\n':
            return True
        raise self.VerifyError(result)

    def get_hash_from_cert(self, cert):
        """Use openssl to get the hash value of a given certificate
        """
        command = 'x509 -hash -noout'
        output = self.exec_openssl(command.split(), cert)
        return output.rstrip('\n')

    def get_subject_from_cert(self, cert):
        """Get the subject form a given CA certificate
        """
        command = [
         'x509', '-noout', '-subject']
        output = self.exec_openssl(command, stdin=cert.pem)
        return output.rstrip('\n').lstrip('subject= ')

    def get_revoke_status_from_cert(self, cert, crl):
        """Is the given certificate already revoked? True=yes, False=no

        Beware : that don't check cert <-> crl signature
        """
        serial = cert.serial
        command = 'crl -text -noout'
        output = self.exec_openssl(command.split(), stdin=crl)
        serial_re = re.compile('^\\s+Serial\\sNumber\\:\\s+(\\w+)')
        lines = output.split('\n')
        serial = serial.rjust(2, '0')
        for l in lines:
            if serial_re.match(l):
                if serial_re.match(l).group(1) == serial:
                    return True

        return False

    def generate_index(self, ca, issued):
        r"""Generate Index
        http://www.mail-archive.com/openssl-users@openssl.org/msg45982.html

        The columns are defined as 
        #define DB_type         0 /* Status of the certificate */
        #define DB_exp_date     1 /* Expiry date */
        #define DB_rev_date     2 /* Revocation date */
        #define DB_serial       3       /* Serial No., index - unique */
        #define DB_file         4      
        #define DB_name         5       /* DN, index - unique when active and not disabled */

        DB_type is defined as
        #define DB_TYPE_REV    'R' /* Revoked */
        #define DB_TYPE_EXP    'E' /* Expired */
        #define DB_TYPE_VAL    'V' /* Valid */

        /!\ Only revoked for now ...

        """
        raise NotImplementedError()
        from M2Crypto.ASN1 import ASN1_UTCTIME
        index = ''
        for cert in issued:
            if cert.revoked:
                subject = self.get_subject_from_cert(cert)
                asn1 = ASN1_UTCTIME()
                asn1.set_datetime(cert)

    @in_temp_dir
    def generate_crl(self, ca, cakey, crlnumber, crlchain=[], issued=[], passphrase=None):
        """Generate CRL: When a CA is modified
        """
        certdir = os.path.join(self.tmpdir, 'certs')
        os.mkdir(certdir, 448)
        privdir = os.path.join(self.tmpdir, 'private')
        os.mkdir(privdir, 448)
        crldir = os.path.join(self.tmpdir, 'crl')
        os.mkdir(crldir, 448)
        for c in issued:
            filepath = os.path.join(certdir, '%s.0' % c.certhash)
            w = open(filepath, 'w')
            w.write(c.pem)
            w.close()

        filepath = os.path.join(self.tmpdir, 'cacert.pem')
        w = open(filepath, 'w')
        w.write(ca.pem)
        w.close()
        filepath = os.path.join(privdir, 'cakey.pem')
        w = open(filepath, 'w')
        w.write(cakey)
        w.close()
        shutil.copy(PKI_OPENSSL_CONF, self.tmpdir)
        confpath = os.path.join(self.tmpdir, os.path.split(PKI_OPENSSL_CONF)[(-1)])
        open(os.path.join(self.tmpdir, 'index.txt'), 'w').write(ca.index)
        serial = '%X' % ca.ca_serial
        serial = serial.rjust(2, '0')
        open(os.path.join(self.tmpdir, 'serial'), 'w').write(serial)
        crlnumber = '%X' % crlnumber
        crlnumber = crlnumber.rjust(2, '0')
        open(os.path.join(self.tmpdir, 'crlnumber'), 'w').write(crlnumber)
        crlpath = os.path.join(self.tmpdir, '%s.r0' % ca.certhash)
        if ca.crl:
            w = open(crlpath, 'w')
            w.write(ca.crl)
            w.close()
        logger.info('CRL generation for CA %s' % ca)
        command = ['ca', '-config', confpath, '-gencrl', '-crldays', '1', '-passin', 'stdin', '-out', crlpath]
        result = self.exec_openssl(command, stdin=passphrase, cwd=self.tmpdir)
        crlpem = open(crlpath, 'r').read()
        return crlpem

    @in_temp_dir
    def revoke_cert(self, ca, cakey, crlnumber, crl, cert, issued=[], passphrase=None):
        """Generate CRL: When a CA is modified
        """
        certdir = os.path.join(self.tmpdir, 'certs')
        os.mkdir(certdir, 448)
        privdir = os.path.join(self.tmpdir, 'private')
        os.mkdir(privdir, 448)
        crldir = os.path.join(self.tmpdir, 'crl')
        os.mkdir(crldir, 448)
        for c in issued:
            filepath = os.path.join(certdir, '%s.0' % c.certhash)
            if c == cert:
                torevoke = filepath
            w = open(filepath, 'w')
            w.write(c.pem)
            w.close()

        filepath = os.path.join(self.tmpdir, 'cacert.pem')
        w = open(filepath, 'w')
        w.write(ca.pem)
        w.close()
        filepath = os.path.join(privdir, 'cakey.pem')
        keyfile = filepath
        w = open(filepath, 'w')
        w.write(cakey)
        w.close()
        shutil.copy(PKI_OPENSSL_CONF, self.tmpdir)
        confpath = os.path.join(self.tmpdir, os.path.split(PKI_OPENSSL_CONF)[(-1)])
        open(os.path.join(self.tmpdir, 'index.txt'), 'w').write(ca.index)
        serial = '%X' % ca.ca_serial
        serial = serial.rjust(2, '0')
        open(os.path.join(self.tmpdir, 'serial'), 'w').write(serial)
        crlnumber = '%X' % crlnumber
        crlnumber = crlnumber.rjust(2, '0')
        open(os.path.join(self.tmpdir, 'crlnumber'), 'w').write(crlnumber)
        crlpath = os.path.join(self.tmpdir, 'crl.pem')
        if crl:
            w = open(crlpath, 'w')
            w.write(crl)
            w.close()
        command = [
         'ca', '-config', confpath, '-batch', '-revoke', torevoke, '-passin', 'stdin']
        result = self.exec_openssl(command, stdin=passphrase, cwd=self.tmpdir)
        command = ['ca', '-config', confpath, '-gencrl', '-crldays', '1', '-passin', 'stdin', '-out', crlpath]
        result = self.exec_openssl(command, stdin=passphrase, cwd=self.tmpdir)
        crlpem = open(crlpath, 'r').read()
        index = open(os.path.join(self.tmpdir, 'index.txt'), 'r').read()
        return (crlpem, index)

    @in_temp_dir
    def sign_pkcs7(self, cert, text, key, certs=[], passphrase=None):
        """Make pkcs7 with smime
        """
        textpath = os.path.join(self.tmpdir, 'in.txt')
        f = open(textpath, 'w')
        f.write(text)
        f.close()
        certpath = os.path.join(self.tmpdir, 'cert.pem')
        f = open(certpath, 'w')
        f.write(cert)
        f.close()
        keypath = os.path.join(self.tmpdir, 'key.pem')
        f = open(keypath, 'w')
        f.write(key)
        f.close()
        outpath = os.path.join(self.tmpdir, 'out.pkcs7')
        command = [
         'smime', '-sign', '-text',
         '-in', textpath,
         '-out', outpath,
         '-signer', certpath,
         '-inkey', keypath,
         '-passin', 'stdin']
        result = self.exec_openssl(command, stdin=certs)
        f = open(outpath, 'r')
        return f.read()

    @in_temp_dir
    def verify_pkcs7(self, cert, smime, certs=[]):
        """Verify pcks7 smime
        """
        textpath = os.path.join(self.tmpdir, 'in.pkcs7')
        f = open(textpath, 'w')
        f.write(smime)
        f.close()
        certpath = os.path.join(self.tmpdir, 'cert.pem')
        f = open(certpath, 'w')
        f.write(cert)
        f.close()
        outpath = os.path.join(self.tmpdir, 'out.text')
        command = [
         'smime', '-verify',
         '-in', textpath,
         '-out', outpath,
         '-signer', certpath,
         '-noverify', certpath]
        result = self.exec_openssl(command, stdin=certs)
        f = open(outpath, 'r')
        data = f.read()
        header = 'Content-Type: text/plain\r\n\r\n'
        return data[len(header):]