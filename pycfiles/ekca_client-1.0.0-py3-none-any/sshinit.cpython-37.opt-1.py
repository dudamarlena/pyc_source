# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_client/sshinit.py
# Compiled at: 2020-02-24 08:59:40
# Size of source mod 2**32: 8432 bytes
"""
ekca_client.sshinit - the command-line client for EKCA service
"""
import sys, os, re, getpass, subprocess, uuid, json, time, nacl.utils, nacl.encoding, nacl.public
if sys.platform == 'win32':
    import win32com.client
else:
    import ptyprocess
from .cmd import SSH_ADD_WAIT
from .cfg import read_config, check_ca_certs
from .req import EKCAUserCertRequest
if sys.platform == 'win32':
    TMPFS_LOCATIONS = []
else:
    TMPFS_LOCATIONS = [
     os.path.join('/run/user', str(os.getuid()))]
TMPFS_LOCATIONS.extend([
 '/tmp',
 os.environ.get('TMP', os.environ.get('TEMP', os.path.expanduser('~')))])

def remove_file(path):
    """
    overwrite file before removing it
    """
    old_size = os.stat(path).st_size
    with open(path, 'ab') as (fileobj):
        fileobj.seek(0)
        fileobj.write(os.urandom(old_size))
    os.remove(path)
    print('Removed file', path)


def remove_temp_files(ssh_init_path, ssh_key_filename, ssh_cert_filename):
    """
    Remove temporary cert/key files
    """
    if sys.platform != 'win32':
        remove_file(ssh_key_filename)
        remove_file(ssh_cert_filename)
    current_time = time.time()
    with os.scandir(ssh_init_path) as (stale_files):
        for dir_entry in stale_files:
            if dir_entry.stat().st_mtime <= current_time - 86400:
                remove_file(os.path.join(ssh_init_path, dir_entry.name))


def prepare_ssh_init_path():
    """
    search for temporary storage directory and create extra directory within
    """
    for ssh_init_tmpfs in TMPFS_LOCATIONS:
        if os.path.isdir(ssh_init_tmpfs):
            break

    ssh_init_path = os.path.join(ssh_init_tmpfs, '.ekca-ssh-init')
    if not os.path.exists(ssh_init_path):
        os.mkdir(ssh_init_path, mode=448)
    else:
        os.chmod(ssh_init_path, 448)
    return ssh_init_path


def ask_password_and_otp(cfg, user_name):
    """
    interactively get the user's password and OTP
    """
    try:
        while True:
            password = getpass.getpass('Password for user %r' % user_name)
            if password:
                break
            sys.stdout.write('Empty password, please repeat...\n')

        while True:
            otp_value = getpass.getpass('OTP for user %r' % user_name)
            if otp_value:
                if re.fullmatch((cfg['otp_regex']), otp_value, flags=0):
                    break
            if not otp_value:
                sys.stdout.write('Empty OTP, please repeat...\n')
            else:
                sys.stdout.write('Malformed OTP did not match %r, please repeat...\n' % cfg['otp_regex'])

    except KeyboardInterrupt:
        print('\nAborted by user -> exiting...')
        sys.exit(0)

    return (password, otp_value)


def ssh_add(cfg, ssh_cert_filename, ssh_key_filename, passphrase, validity):
    """
    Invoke ssh-add command to load user cert and private key into ssh-agent.
    """
    subprocess.check_call([cfg['ssh_keygen'], '-L', '-f', ssh_cert_filename])
    subprocess.check_call([cfg['ssh_add'], '-D'])
    ssh_add_cmd = [
     cfg['ssh_add']]
    if sys.platform != 'win32':
        ssh_add_cmd.extend(['-t', validity])
    else:
        ssh_add_cmd.append(ssh_key_filename)
        print('Adding new key with following command:', repr(ssh_add_cmd))
        if sys.platform == 'win32':
            proc = win32com.client.Dispatch('WScript.Shell')
            proc.run(' '.join(ssh_add_cmd))
            proc.AppActivate('ssh-add to agent')
            time.sleep(SSH_ADD_WAIT)
            proc.SendKeys(passphrase.decode('ascii') + '{ENTER}')
        else:
            proc = ptyprocess.PtyProcess.spawn(ssh_add_cmd)
            pw_prompt = proc.read(3000)
            print('-->', pw_prompt.decode('ascii'))
            proc.waitnoecho()
            print('--> echo disabled')
            print('<-- send decrypted passphrase')
            proc.write(passphrase + proc.crlf)
            _ = proc.read(3000)
            proc.sendeof()
            time.sleep(SSH_ADD_WAIT)
            proc.close()
    try:
        subprocess.check_call([cfg['ssh_add'], '-l'])
    except subprocess.CalledProcessError:
        pass
    else:
        print('Successfully added key and cert to SSH key agent.')


def sshinit():
    """
    the main CLI function
    """
    cfg = read_config()
    check_ca_certs(cfg)
    if sys.platform == 'win32':
        pass
    else:
        if 'SSH_AUTH_SOCK' not in os.environ:
            print('No SSH key agent found!')
            sys.exit(1)
        else:
            try:
                user_name = sys.argv[1]
            except IndexError:
                user_name = getpass.getuser()

        ssh_init_path = prepare_ssh_init_path()
        password, otp_value = ask_password_and_otp(cfg, user_name)
        req_id = str(uuid.uuid4())
        enroll_key = nacl.public.PrivateKey.generate()
        err = None
        print('Sending signing request...')
        try:
            resp = EKCAUserCertRequest((cfg['baseurl']),
              (cfg['sshca_name']),
              username=user_name,
              password=password,
              reqid=req_id,
              otp=otp_value,
              epubkey=(enroll_key.public_key.encode(encoder=(nacl.encoding.URLSafeBase64Encoder)).decode('ascii'))).req(cafile=(cfg['ca_certs']))
            resp_body = resp.read().decode('utf-8')
            resp_data = json.loads(resp_body)
            resp_msg = resp_data.get('message', '')
            if resp.status != 200:
                print('{0}: {1}'.format(resp.status, resp_msg))
                sys.exit(1)
            if req_id != resp_data['reqid']:
                print('Expected request ID {0} but received {1}'.format(req_id, resp_data['reqid']))
                sys.exit(1)
        except Exception as err:
            try:
                print('Exception: ', str(err))
                sys.exit(1)
            finally:
                err = None
                del err

        ssh_key_filename = os.path.join(ssh_init_path, req_id)
        ssh_cert_filename = ssh_key_filename + '-cert.pub'
        with open(ssh_key_filename, mode='wt', encoding='utf-8') as (fileobj):
            fileobj.write(resp_data['key'])
        os.chmod(ssh_key_filename, mode=384)
        with open(ssh_cert_filename, mode='wt', encoding='utf-8') as (fileobj):
            fileobj.write(resp_data['cert'])
        os.chmod(ssh_cert_filename, mode=384)
        unseal_box = nacl.public.SealedBox(enroll_key)
        passphrase = unseal_box.decrypt(resp_data['passphrase'], nacl.encoding.URLSafeBase64Encoder)
        try:
            ssh_add(cfg, ssh_cert_filename, ssh_key_filename, passphrase, resp_data['validity'])
        finally:
            remove_temp_files(ssh_init_path, ssh_key_filename, ssh_cert_filename)


if __name__ == '__main__':
    sshinit()