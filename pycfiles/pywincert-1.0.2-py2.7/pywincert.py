# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywincert\pywincert.py
# Compiled at: 2017-11-27 12:30:27
""":mod:`pywincert` - Create Windows certificates
##################################################

.. module:: pywincert
   :synopsis: Create Windows certificates
.. moduleauthor:: Jim Carroll <jim@carroll.net>

Functions to invoke windows code signing tools. The tools used are:

    +-----------+-----------------------------------+----------------------------+
    | *tool*    | *description*                     | *url*                      |
    +===========+===================================+============================+
    | makecert  | Certificate creation tool.        | http://tinyurl.com/njh7cry |
    +-----------+-----------------------------------+----------------------------+
    | cert2spc  | Convert private key to Software   | http://tinyurl.com/pab4n7q |
    |           | Publish Certificate               |                            |
    +-----------+-----------------------------------+----------------------------+
    | certutil  | Interact with certificate services| http://tinyurl.com/punbfdl |
    |           | on your local machine.            |                            |
    +-----------+-----------------------------------+----------------------------+
    | pvk2pfx   | Combine private key .spc, .cer    | http://tinyurl.com/mu5c6n8 |
    |           | and .pvk to personal information  |                            |
    |           | exchange (.pfx) file.             |                            |
    +-----------+-----------------------------------+----------------------------+

makecert and certutil have popup windows that need to be acknowledge. For the
purpose of automation, these utility functions will handle the details of responding.
Do not hit any keys while these tests are running, or you'll interefere with the
sequence of keystrokes.

NOTE: certutil will sound your system bell when it's windows popup. It's annoying
but you can safely ignore it.

..
   Copyright(c) 2017, Carroll-Net, Inc., All Rights Reserved"""
import datetime, logging, os, re, shutil, subprocess, tempfile, time, _winreg, win32com.client
__version__ = '1.0.1'
__author__ = 'Jim Carroll'
__email__ = 'jim@carroll.net'
__status__ = 'Development'
__copyright__ = 'Copyright(c) 2017, Carroll-Net, Inc., All Rights Reserved'
LOG = logging.getLogger('pywincert')
WINSDK_ERROR = 'Windows SDK may not be installed on this machine. You can read more and (re-)download from https://en.wikipedia.org/wiki/Microsoft_Windows_SDK'

def get_winsdk_path():
    """Retrieve installed path for windows sdk."""
    key = None
    try:
        with _winreg.OpenKeyEx(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Microsoft SDKs\\Windows') as (key):
            pth = _winreg.QueryValueEx(key, 'CurrentInstallFolder')[0]
            return re.sub('\\\\\\\\', '\\\\', pth)
    except (WindowsError, IndexError):
        raise RuntimeError('missing windows sdk registry entry: %s' % WINSDK_ERROR)

    return


def run_makecert_authority(cmd, password):
    """Run *makecert.exe* to create a windows authority (eg: CA). Windows
    requires the user respond to two GUI popup windows. This function using
    WScript.Shell.Run() to provide the appropriate responses. *cmd* is the
    command to pass to WScript.Shell.Run() (assumed to be makecert.exe).
    *password* the password submitted to the popup window.

    Screen 1 Title: Create Private Key Password
    Prompt Field 1: Password
    Prompt Field 2: Confirm Password
    Buttons: [OK]  [None]  [Cancel]

    Screen 2 Title: Enter Private Key Password
    Prompt Field 1: Password
    Buttons: [OK]  [Cancel]
    """
    LOG.debug('run_makecert_authority %s', cmd)
    shell = win32com.client.Dispatch('WScript.Shell')
    shell.Run(cmd, 1, False)
    for _ in xrange(20):
        if shell.AppActivate('Create Private Key Password'):
            break
        time.sleep(0.5)

    if not shell.AppActivate('Create Private Key Password'):
        raise RuntimeError('timeout waiting for makecert popup(1)')
    time.sleep(0.2)
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys('{ENTER}')
    time.sleep(0.5)
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys('{ENTER}')
    time.sleep(0.5)
    shell = None
    return


def run_makecert_enduser(cmd, password):
    """Run *makecert.exe* to create a windows end entity cert. Windows
    requires the user respond to three GUI popup windows. This function using
    WScript.Shell.Run() to provide the appropriate responses. *cmd* is the
    command to pass to WScript.Shell.Run() (assumed to be makecert.exe).
    *password* the password submitted to the popup window.

    Screen 1 Title: Create Private Key Password
    Prompt Field 1: Password
    Prompt Field 2: Confirm Password
    Buttons: [OK]  [None]  [Cancel]

    Screen 2 Title: Enter Private Key Password
    Prompt Field 1: Password
    Buttons: [OK]  [Cancel]

    Screen 3 Title Enter Private Key Password
    Prompt Field 1: Password
    Buttons: [OK]  [Cancel]
    """
    LOG.debug('run_makecert_enduser %s', cmd)
    shell = win32com.client.Dispatch('WScript.Shell')
    shell.Run(cmd, 1, False)
    for _ in xrange(20):
        if shell.AppActivate('Create Private Key Password'):
            break
        time.sleep(0.5)

    if not shell.AppActivate('Create Private Key Password'):
        raise RuntimeError('timeout waiting for makecert popup(1)')
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys('{ENTER}')
    time.sleep(0.5)
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys('{ENTER}')
    time.sleep(0.5)
    shell.SendKeys(password)
    time.sleep(0.2)
    shell.SendKeys('{TAB}')
    time.sleep(0.2)
    shell.SendKeys('{ENTER}')
    time.sleep(0.5)
    shell = None
    return


def make_ca(subject, password, pvk_filename, cer_filename, valid_hours=24):
    """Create self-signed certificate authority that can be used for signing
    and add it to windows cert Root store.  *subject* is the certificate
    subject. *password* is the secret to protect private key.  *pvk_filename*
    is where to create the private key file.  *cer_filename* is where to create
    the public certificate.  *valid_hours* is the number of hours the
    certificate is valid for (defaults to 24-hours).

    For more details, see https://tinyurl.com/yart46ha"""
    mkcert = os.path.join(get_winsdk_path(), 'Bin', 'makecert.exe')
    assert os.path.isfile(mkcert), "missing '%s'" % mkcert
    now = datetime.datetime.now()
    beg_date = now.date() - datetime.timedelta(days=1)
    beg_date = beg_date.strftime('%m/%d/%Y')
    end_date = now.date() + datetime.timedelta(hours=valid_hours)
    end_date = end_date.strftime('%m/%d/%Y')
    cmd = '"%s" -r -a sha1 -pe -b %s -e %s -n "CN=%s" -ss CA -sr LocalMachine -cy authority -sky signature -sv "%s" "%s"' % (
     mkcert, beg_date, end_date, subject, pvk_filename, cer_filename)
    run_makecert_authority(cmd, password)
    for fname in (pvk_filename, cer_filename):
        if not os.path.isfile(fname):
            raise RuntimeError('makecert(CA) did not create %s' % fname)

    subprocess.check_output(['certutil.exe',
     '-addstore', 'Root',
     cer_filename])


def remove_cert_fromstore(certid, store):
    """remove the specified *certid* from the specified *store*.
    The *certid* is the Certificate or CRL match token. This can be a serial
    number, a SHA1-certificate, CRL, CTL or public key hash."""
    output = subprocess.check_output(['certutil.exe',
     '-store', store, certid], shell=True, universal_newlines=True)
    snums = []
    for line in output.split('\n'):
        match = re.match('^Serial Number: ([a-f\\d]+)$', line)
        if match:
            snums.append(match.group(1))

    if not snums:
        raise RuntimeError("no certificate with matching certid '%s'" % certid)
    for snum in snums:
        LOG.debug('delete certificate %s', snum)
        subprocess.check_output(['certutil.exe',
         '-delstore', store, snum])


def remove_ca(certid):
    """Remove *certid* from the Root and CA stores.  The *certid* is the
    Certificate or CRL match token. This can be a serial number, a
    SHA1-certificate, CRL, CTL or public key hash."""
    remove_cert_fromstore(certid, 'Root')
    remove_cert_fromstore(certid, 'CA')


def make_pfx(ca_subject, password, ca_pvk_filename, ca_cer_filename, pfx_filename):
    r"""Create 'personal info exchange' file (\*.pfx). *ca_subject* is the
    subject of certificate authority that was used to create the cert.
    *password* is the secret used to protect the new pfx file. *pfx_filename*
    is where to store the new pfx file. -1 indicates an error, 0 is sucess."""
    sdkpath = os.path.join(get_winsdk_path(), 'Bin')
    mkcert = os.path.join(sdkpath, 'makecert.exe')
    cert2spc = os.path.join(sdkpath, 'cert2spc.exe')
    pvk2pfx = os.path.join(sdkpath, 'pvk2pfx.exe')
    tmpd = tempfile.mkdtemp()
    pvk = os.path.join(tmpd, 'mykey.pvk')
    cer = os.path.join(tmpd, 'mycert.cer')
    spc = os.path.join(tmpd, 'mycert.spc')
    try:
        cmd = '"%s" -pe -n "CN=%s" -cy end -sky signature -ic %s -iv %s -sv "%s" "%s"' % (
         mkcert, ca_subject, ca_cer_filename, ca_pvk_filename, pvk, cer)
        run_makecert_enduser(cmd, password)
        for fname in (pvk, cer):
            if not os.path.isfile(fname):
                raise RuntimeError('makecert(end) did not create %s' % fname)

        try:
            subprocess.check_output([cert2spc, cer, spc], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError('error running %s %s %s: %s' % (
             cert2spc, cer, spc, exc.output))

        try:
            subprocess.check_output([pvk2pfx,
             '-pvk', pvk,
             '-pi', password,
             '-spc', spc,
             '-f',
             '-pfx', pfx_filename,
             '-po', password])
        except subprocess.CalledProcessError as exc:
            raise RuntimeError('error running %s: %s' % (
             pvk2pfx, exc.output))

    finally:
        shutil.rmtree(tmpd, ignore_errors=True)

    return 0


def sign_code(exe, pfx_file, password):
    """Sign *exe* using the *pfx* and *password*"""
    timestamp_urls = ('http://timestamp.comodoca.com/authenticode', 'http://timestamp.verisign.com/scripts/timstamp.dll',
                      'http://timestamp.globalsign.com/scripts/timestamp.dll', 'http://tsa.starfieldtech.com')
    signtool = os.path.join(get_winsdk_path(), 'Bin', 'signtool.exe')
    for turl in timestamp_urls:
        cmd = [
         signtool, 'sign',
         '/f', pfx_file,
         '/p', password,
         '/t', turl,
         exe]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = task.communicate()
        if task.returncode == 2:
            LOG.debug('failed to sign w/ timestamp url %s', turl)
            continue
        if task.returncode:
            LOG.info(stdout)
            LOG.error(stderr)
        LOG.debug(stdout)
        return

    raise RuntimeError('retries exhausted signing %s' % exe)


def is_signed(exe):
    """Return True if *exe* is signed and valid"""
    signtool = os.path.join(get_winsdk_path(), 'Bin', 'signtool.exe')
    try:
        subprocess.check_output([
         signtool, 'verify', '/q', '/pa', exe], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False