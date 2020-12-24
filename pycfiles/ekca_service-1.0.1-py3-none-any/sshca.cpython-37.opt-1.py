# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_service/sshca.py
# Compiled at: 2020-03-08 15:45:52
# Size of source mod 2**32: 5071 bytes
"""
mainly ssh-keygen actions
"""
import datetime, logging, os, os.path, subprocess, sys, uuid
from io import StringIO
from random import SystemRandom
import paramiko
from .cmd import ShellCommand
SSH_PERMS = {
 'pty',
 'X11-forwarding',
 'agent-forwarding',
 'port-forwarding',
 'user-rc'}

def ssh_passphrase(alphabet, length):
    """
    Returns a random password byte string consisting of `length' bytes of
    chars found in `alphabet'.
    """
    sys_rand = SystemRandom()
    random_upper_bound = len(alphabet) - 1
    return ''.join([alphabet[sys_rand.randint(0, random_upper_bound)] for _ in range(length)])


class SSHCAException(Exception):
    __doc__ = '\n    errors specific to SSH-CA instances\n    '


class SSHCertAuthority:
    __doc__ = '\n    SSH Certificate Authority\n    '
    cert_subdir = 'certs'
    userkey_comment = '{user}@{ip} signed by {ca} (keyid={kid}, time={time:%Y-%m-%d %H:%M:%S})'
    logger = logging.getLogger('SSHCertAuthority')

    def __init__(self, cfg, ca_name, ca_dir, logger=None):
        self._cfg = cfg
        self.ca_name = ca_name
        self.ca_dir = ca_dir
        self.ca_certdir = os.path.join(ca_dir, self.cert_subdir)
        self.ca_pub = os.path.join(ca_dir, ca_name + '.pub')
        if logger is not None:
            self.logger = logger
        self._check_files()

    def _check_files(self):
        """
        check whether CA's private and public key files are in place
        """
        if not os.path.isfile(self.ca_pub):
            raise SSHCAException('public key file %r of %s does not exist' % (
             self.ca_pub,
             self.ca_name))

    def get_pubkey(self):
        """
        returns CA's public key (trust anchor) read from file
        """
        with open(self.ca_pub, 'rb') as (pub_file):
            pub_key = pub_file.read().decode(sys.stdin.encoding)
        return pub_key

    def user_cert(self, user_name, from_ip, req_id, cert_perms, validity, remove_files=False):
        """
        generate user key pair and cert
        """
        key_id = str(uuid.uuid4())
        user_pass_phrase = ssh_passphrase(self._cfg['SSH_PASSPHRASE_ALPHABET'], self._cfg['SSH_PASSPHRASE_LENGTH']).encode('utf-8')
        priv_key = paramiko.rsakey.RSAKey.generate(2048)
        with StringIO() as (priv_key_filobj):
            priv_key.write_private_key(priv_key_filobj, password=user_pass_phrase)
            priv_key_str = priv_key_filobj.getvalue()
        pub_key_filename = os.path.join(self.ca_certdir, key_id + '.pub')
        with open(pub_key_filename, 'wb') as (pub_key_fileobj):
            pub_key_fileobj.write(bytes(' '.join((priv_key.get_name(), priv_key.get_base64())), 'ascii'))
        now = datetime.datetime.utcnow()
        key_comment = self.userkey_comment.format(user=user_name,
          ca=(self.ca_name),
          ip=(','.join(from_ip or [])),
          kid=key_id,
          time=now)
        serial_no = str(SystemRandom().randint(0, 18446744073709551616))
        sign_args = ShellCommand(self._cfg['SSH_KEYGEN_CMD'], [
         '-Us', self.ca_pub,
         '-n', user_name,
         '-C', key_comment,
         '-I', key_id,
         '-z', serial_no,
         '-V', validity,
         '-q'])
        if cert_perms:
            sign_args.extend([
             '-O', 'clear'])
            cert_perms = ['permit-' + opt for opt in cert_perms if opt in SSH_PERMS]
            for opt in cert_perms:
                sign_args.extend([
                 '-O', opt])

        if from_ip:
            sign_args.extend([
             '-O', 'source-address={ip}'.format(ip=(','.join(from_ip)))])
        sign_args.append(pub_key_filename)
        self.logger.info('SSH-CA %r signs cert no. %r for user %r (keyid %s) with command %r (request ID %s)', self.ca_name, serial_no, user_name, key_id, str(sign_args), req_id)
        subprocess.check_call(sign_args, shell=False)
        cert_filename = os.path.join(self.ca_certdir, key_id + '-cert.pub')
        with open(cert_filename, 'rb') as (cert_fileobj):
            user_cert = cert_fileobj.read()
        if remove_files:
            os.remove(pub_key_filename)
            os.remove(cert_filename)
        return (
         user_pass_phrase, priv_key_str, user_cert)