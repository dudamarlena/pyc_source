# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/secrecy/gpgtools.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 19540 bytes
"""
gpgtool module
"""
from os import path, environ, remove, walk, name as osname
try:
    from os import uname
except ImportError:

    def uname():
        return [
         0][environ['COMPUTERNAME']]


try:
    from os import chmod
except ImportError:

    def chmod(*_):
        pass


from shutil import move
from re import search
from getpass import getpass
from tkinter import TclError
from gnupg import GPG
import wget
try:
    import readline
except ImportError:
    pass

from colortext import blu, yel, grn, bgre, tabd, abort, error, fatal
from system import xyesno, xgetpass, xmsgok, xinput, xnotify, userfind, which
from executor import Command

class DecryptError(Exception):
    pass


class EncryptionError(Exception):
    pass


class SignatureError(Exception):
    pass


class GPGTool(Command):
    __doc__ = '\n\tgnupg wrapper-wrapper :P\n\talthough the gnupg module is quite handy and the functions are pretty and\n\tuseable i need some modificated easing functions to be able to make the\n\tmain code more easy to understand by wrapping multiple gnupg functions to\n\tone - also i can prepare some program related stuff in here\n\t'
    sh_ = True
    dbg = None
    dtg = True
    vrb = None
    gui = None
    frc = None
    iac = None
    sig = True
    dtg = True
    _GPGTool__c = 0
    _GPGTool__ppw = None
    homedir = path.join(path.expanduser('~'), '.gnupg')
    if 'GNUPGHOME' in environ.keys():
        homedir = environ['GNUPGHOME'].strip()
    _GPGTool__bin = 'gpg'
    if osname == 'nt':
        homedir = path.join(path.expanduser('~'), 'AppData', 'Roaming', 'gnupg')
        _GPGTool__bin = 'gpg.exe'
    _binary = which(_GPGTool__bin)
    _gpgselfcheck = None
    _keyserver = ''
    _gpgselfcheck = None
    kginput = {}
    recvs = []
    environ['LC_MESSAGES'] = 'C'
    if 'RECIPIENTS' in environ.keys():
        recvs = environ['RECIPIENTS'].split(' ')
    gpgkey = ''
    if 'GPGKEY' in environ.keys():
        gpgkey = environ['GPGKEY']
    cardkey = ''
    if 'CARDKEY' in environ.keys():
        cardkey = environ['CARDKEY']
    pwdmsg = 'enter passphrase: '

    def __init__(self, *args, **kwargs):
        """gpgtool init function"""
        args = [
         'sh_'] + [a for a in args]
        for arg in args:
            setattr(self, arg, True)

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)

        if self.dbg:
            print(bgre(GPGTool.__mro__))
            print(bgre(tabd(GPGTool.__dict__, 2)))
            print(' ', bgre(self.__init__))
            print(bgre(tabd(self.__dict__, 4)))
        (Command.__init__)(self, *args, **kwargs)
        if osname == 'nt' and not which('gpg.exe'):
            if not xyesno('mandatory gpg4win not found! Install it?'):
                raise RuntimeError('cannot continue without gpg4win')
            import wget
            src = 'https://files.gpg4win.org/gpg4win-latest.exe'
            trg = path.join(environ['TEMP'], 'gpg4win.exe')
            wget.download(src, out=trg)
            self.call(trg)
            remove(trg)

    @property
    def keyring(self):
        """pubring getter (read-only)"""
        if self.binary.endswith('.exe'):
            return path.join(self.homedir, 'pubring.gpg')
        else:
            if self.binary.endswith('2'):
                return path.join(self.homedir, 'pubring.kbx')
            return path.join(self.homedir, 'pubring.gpg')

    @property
    def secring(self):
        """secring getter (read-only)"""
        if self.binary.endswith('.exe'):
            return path.join(self.homedir, 'secring.gpg')
        else:
            if self.binary.endswith('2'):
                if self.keyring.endswith('gpg'):
                    return path.join(self.homedir, 'secring.gpg')
            return path.join(self.homedir, 'secring.kbx')

    @property
    def binary(self):
        """binary path getter"""
        return self._binary

    @binary.setter
    def binary(self, val):
        """binary path setter"""
        self._binary = val

    @property
    def _gpg_(self):
        """gpg wrapper property"""
        opts = [
         '--batch']
        if osname != 'nt':
            opts = [
             '--pinentry-mode=loopback']
        if self._GPGTool__c >= 1:
            if not self._GPGTool__ppw:
                self._GPGTool__ppw = self.passwd(False, self.gui, self.pwdmsg)
        _GPGTool__g = GPG(gnupghome=(self.homedir),
          gpgbinary=(self.binary),
          use_agent=True,
          options=opts,
          verbose=(1 if self.dbg else 0))
        if osname != 'nt':
            _GPGTool__g.encoding = 'utf-8'
        return _GPGTool__g

    @staticmethod
    def passwd(rpt=False, gui=None, msg='enter passphrase: ', rptmsg='repeat that passphrase: '):
        """password questioning method"""
        pas = getpass
        err = error
        if gui:
            pas = xgetpass
            err = xmsgok
        else:
            msg = blu(msg)
            rptmsg = blu(rptmsg)
        while True:
            if not rpt:
                return pas(msg)
            _GPGTool__pwd = pas(msg)
            if _GPGTool__pwd == pas(rptmsg):
                return _GPGTool__pwd
            err('passwords do not match')

        return False

    @staticmethod
    def __find(pattern, *vals):
        """pattern matching method"""
        if not isinstance(pattern, str):
            raise error('pattern must be type string, got', '%s %s' % (
             type(pattern), pattern))
        for val in vals:
            if isinstance(val, (list, tuple)):
                if [v for v in val if pattern in v]:
                    return True
                else:
                    if isinstance(val, dict):
                        if pattern in val.values():
                            return True
                    if pattern in val:
                        return True

        return False

    @staticmethod
    def _gendefs(gui=False):
        user = environ['USERNAME'] if osname == 'nt' else environ['USER']
        host = environ['COMPUTERNAME'] if osname == 'nt' else uname()[1]
        kginput = {'name_real':user if len(user) >= 5 else '%s key' % user, 
         'name_comment':'', 
         'name_email':'%s@%s' % (user, host), 
         'expire_date':0, 
         'key_type':'RSA', 
         'key_length':4096, 
         'subkey_type':'RSA', 
         'subkey_length':4096}
        bea = False
        while 1:
            echo = print
            ynq = ask = input
            _m = '%s\n%s\n%s [Y/n]\n'
            _g = grn('generating keys using:')
            _d = yel(tabd(kginput, 2))
            _o = grn('Is that OK?')
            if gui:
                echo = xmsgok
                ynq = xyesno
                ask = xinput
                _g = 'generating keys using:'
                _d = tabd(kginput, 2)
                _o = 'Is that OK?'
            msg = _m % (_g, _d, _o)
            try:
                yna = ynq(msg)
            except TclError as err:
                print(err)
                break

            if yna in ('n', False, None):
                msg = '%s [Y/n]' % grn('continue editing?')
                if gui:
                    msg = 'abort editing?'
                yna = ynq(msg)
                if yna in ('n', False, None):
                    break
                if yna in ('n', False, None):
                    while True:
                        for k, v in sorted(kginput.items()):
                            nv = ask('enter new value for: "%s"\ncurrent value: "%s"\nenter "_" to unset or leave blank to use the  preset value above\n' % (
                             k, v))
                            if nv == '_':
                                del kginput[k]
                                continue
                            nv = v if not nv else nv
                            kginput[k] = nv

                        msg = _m % (_g, yel(tabd(kginput, 2)), _o)
                        bea = ynq(msg)
                        if bea is True or bea in ('n', ''):
                            break

                else:
                    if yna in ('y', '', True):
                        break
                    if bea is not False:
                        break

        return kginput

    def _listsecs(self, kllis, pattern=None):
        ksdics = {}
        kdic = {}
        for kl in kllis:
            t, dat = kl.split(':')[0], ':'.join(kl.split(':')[1:])
            if t == 'sec':
                if kdic:
                    uid = kdic['uid']
                    del kdic['uid']
                    ksdics[uid] = kdic
                    kdic = {}
                kdic[t] = dat
            else:
                kdic[t] = dat

        return ksdics

    def _listpubs(self, kllis, pattern=None):
        trust = kllis[0]
        del kllis[0]
        kls = []
        kdic = {'trust': trust}
        for kl in kllis:
            if kl.startswith('pub'):
                if kls:
                    kdic[kl.strip()] = [k for k in kls]
                    kls = []
                    continue
                    kls.append(kl)

        return kdic

    def gpglistkeys(self, pattern=None, secrets=None):
        opt = ' -k'
        lister = self._listpubs
        if secrets:
            lister = self._listsecs
            opt = ' -K'
        klstr = self.stdo('%s --with-colons --status-fd 2 --fixed-list-mode%s' % (
         self.binary, opt))
        kdic = lister(klstr.split('\n'), pattern)
        if pattern:
            retdic = {}
            for k, vs in kdic.items():
                if pattern in k:
                    retdic[k] = vs
                else:
                    hit = False
                    for v in vs:
                        if pattern in v:
                            hi = True
                            break

                    if hit:
                        retdic[k] = vs

        return kdic

    def _gpgcheck(self):
        if self._gpgselfcheck:
            return
        else:
            gpgkey = self.cardkey if self.cardkey else self.gpgkey
            if not gpgkey:
                o = self.smcstatus()
                if o:
                    for l in o.split('\n'):
                        if l.startswith('sec'):
                            gpgkey = str(l.split()[1]).split('/')[1]

            gpgkey = gpgkey if gpgkey else self.gpgkey
            recvs = self.recvs
            if gpgkey:
                if recvs:
                    recvs = [
                     gpgkey] + [r for r in recvs if r != gpgkey]
            if gpgkey:
                recvs = [
                 gpgkey]
            self.sh_ = True
            getin = input
            quest = '%s [y/n]' % grn('could not authenticate, retry?')
            cmd = '%s --batch --always-trust' % self.binary
            if self.gui:
                getin = xyesno
                quest = 'could not authenticate, retry?'
            enc = self.stdo(('%s %s -e' % (cmd, ' -r '.join(k for k in recvs))),
              inputs='')
            rtn = self.call(('%s -d' % cmd), inputs=(enc.encode()), stderr=False)
            if rtn == 0:
                self._gpgselfcheck = True
                return True
            yesno = getin(quest)
            if str(yesno) not in ('true', 'y'):
                self._GPGTool__c += 1
                return
            return self._gpgcheck()

    def recvlist(self, crypt):
        keys = []
        out = self.stde('%s --list-only -v -d %s' % (
         self.binary, crypt)).strip()
        _ks = []
        if out:
            _ks = [l.split(' ')[(-1)].strip() for l in out.split('\n') if l]
        for k in _ks:
            kv = self.findkey(k, typ='c')
            if not kv:
                pass
            else:
                keys.append('0x%s' % str(list(kv[0].keys())[0])[-16:])

        return keys

    def genkeys(self, **kginput):
        """key-pair generator method"""
        if self.dbg:
            print(bgre(self.genkeys))
        else:
            kginput = kginput if kginput else self._gendefs(self.gui)
            kgmsg = '%s %s%s ' % (
             blu('enter new password for'), yel(kginput['name_real']), blu(':'))
            if self.gui:
                echo = xmsgok
                kgmsg = 'enter new password for %s' % kginput['name_real']
            if 'passphrase' not in kginput.keys():
                kginput['passphrase'] = self.passwd(True, self.gui, kgmsg)
        return self._gpg_.gen_key((self._gpg_.gen_key_input)(**kginput))

    def findkey(self, pattern='', **kwargs):
        """key finder method"""
        typ = 'A' if 'typ' not in kwargs.keys() else kwargs['typ']
        sec = False if 'secret' not in kwargs.keys() else kwargs['secret']
        keys = []
        pattern = pattern if not pattern.startswith('0x') else pattern[2:]
        for key in self._gpg_.list_keys(secret=sec):
            if pattern:
                if not (self._GPGTool__find)(pattern, *key.values()):
                    continue
            finger = key['fingerprint']
            subs = {}
            for k, _ in key.items():
                if k == 'subkeys':
                    for sub in key[k]:
                        _, typs, fin = sub
                        if typ == 'A' or typ in typs:
                            if typs not in subs.keys():
                                subs[typs] = []
                            subs[typs].append(fin)

            keys.append({finger: subs})

        return keys

    def smcstatus(self):
        if self.dbg:
            print(bgre(self.smcstatus))
        return self.stdo('%s --card-status' % self.binary)

    def smcfetch(self, urls):
        if self.dbg:
            print(bgre(self.smcfetch))
        if not urls:
            o = self.smcstatus()
            urls = []
            if o:
                for l in o.split('\n'):
                    if l.startswith('URL of public key :'):
                        urls = [
                         ':'.join(l.split(':')[1:])]

        eno = 0
        for url in urls:
            cmd = '%s --fetch-key %s' % (self.binary, url)
            e, o, n = self.oerc(cmd)
            if n != 0:
                eno = n

        return eno

    def keyimport(self, key):
        """key from string import method"""
        if self.dbg:
            print(bgre('%s %s' % (self.keyimport, key)))
        return self._gpg_.import_keys(key)

    def _encryptwithkeystr(self, data, keystr, output):
        """encrypt using given keystring method"""
        fingers = [r['fingerprint'] for r in self._gpg_.import_keys(keystr).results]
        return self._gpg_.encrypt(data,
          fingers, output=output)

    def _fingered(self, keys, typ='e'):
        fingers = []
        if not keys:
            return error('no keys received', keys, 'mode', typ)
        else:
            for key in keys:
                for hsh, tyks in key.items():
                    if typ == 'c':
                        fingers.append(hsh)
                    else:
                        for t in tyks.keys():
                            if typ in t:
                                fingers = fingers + tyks[t]

            return fingers

    def _signfromfile(self, path, finger, out):
        with open(path, 'rb') as (cfh):
            return self._gpg_.sign_file(cfh,
              keyid=finger, detach=(self.dtg), output=out)

    def sign(self, data, out=None):
        """text encrypting method"""
        if self.dbg:
            print(bgre(self.sign))
        if not self.gpgkey:
            return error('key is needed for signing')
        else:
            if self.vrb:
                if out:
                    print(blu('signing to'), yel(out))
            else:
                gpgkey = self.gpgkey
                if self.gpgkey:
                    if self.cardkey:
                        if self.gpgkey != self.cardkey:
                            if self.vrb:
                                error('card-key',
                                  (self.cardkey), 'superseeds key set by config', (self.gpgkey),
                                  buzzword='WARNING')
                            gpgkey = self.cardkey
                finger = self._fingered(self.findkey(gpgkey, typ='s'), 's')[0]
                if path.isfile(data):
                    sign = self._signfromfile(str(data), finger, out)
                else:
                    sign = self._gpg_.sign((str(data)),
                      keyid=finger, detach=(self.dtg), output=out)
            if path.isfile(out):
                chmod(out, 384)
            return sign

    def verify(self, sign, data=None):
        sig = False
        c = 0
        while c < 3:
            if path.isfile(sign):
                with open(data, 'rb') as (sfh):
                    sig = self._gpg_.verify_data(sign, sfh.read())
            else:
                sig = self._gpg_.verify(sign)
            if hasattr(sig, 'valid'):
                if sig.valid:
                    sig = True
            if sig:
                break
            c += 1

        return sig

    def encrypt(self, data, **kwargs):
        """text encrypting method"""
        if self.dbg:
            print(bgre(self.encrypt))
        else:
            out = None if 'output' not in kwargs.keys() else kwargs['output']
            message = data
            if path.isfile(str(data)):
                with open(data, 'r') as (cfh):
                    message = str(cfh.read())
            recvs = self.recvs
            if 'recvs' in kwargs.keys():
                recvs = kwargs['recvs']
            if 'recipients' in kwargs.keys():
                recvs = kwargs['recipients']
            if self.vrb:
                if out:
                    print(blu('encrypting to'), yel(out))
            fingers = []
            for rec in recvs:
                fins = self._fingered(self.findkey(rec, typ='e'), 'e')
                fingers = fingers + fins if fins else []

            crypt = self._gpg_.encrypt((str(message)), fingers, output=out)
            if not crypt.ok:
                raise EncryptionError('no valid encrypted object was returned')
            crypt = str(crypt)
            sign = False
            if self.sig:
                sig = '%s.sig' % out if out else None
                crypt = crypt if crypt else out
                sign = self.sign(crypt, sig)
            if out:
                if path.isfile(out):
                    chmod(out, 384)
        return (
         crypt, sign)

    def decrypt(self, data, **kwargs):
        """text decrypting method"""
        if self.dbg:
            print(bgre(self.decrypt))
        else:
            out = None if 'output' not in kwargs.keys() else kwargs['output']
            sig = self.sig if 'sign' not in kwargs.keys() else kwargs['sign']
            message = data
            if path.isfile(data):
                with open(data, 'r') as (cfh):
                    message = str(cfh.read())
            sigerr = False
            if sig:
                sign = '%s.sig' % data
                if self.vrb:
                    print(blu('validating'), yel(sign))
                signed = self.verify(sign, data)
                if not signed:
                    sigerr = True
                    yesno = False
                    yesno = self.iac or True
                    sigerr = False
                else:
                    if self.gui:
                        yesno = xyesno('ERROR: signature could not be verified\ncontinue anyways?')
                    else:
                        error('signature could not be verified')
                        print(grn('continue anyways?'), '[y/N]')
                        yesno = input()
                        if yesno.lower() == 'y':
                            yesno = True
                        if not yesno:
                            raise SignatureError('signature verification failed')
            _GPGTool__plain = None
            if self.vrb:
                print(blu('decrypting from'), yel(data))
        while self._GPGTool__c < 4:
            _GPGTool__plain = self._gpg_.decrypt(message,
              output=out, always_trust=True, passphrase=(self._GPGTool__ppw))
            if _GPGTool__plain.ok:
                if sigerr:
                    return [
                     _GPGTool__plain, 'SIGERR']
                return [_GPGTool__plain, None]
            yesno = True
            if self._GPGTool__c > 3:
                yesno = False
                if self.gui:
                    xnotify('too many wrong attempts')
                else:
                    error('too many wrong attempts')
                raise DecryptError('cannot decrypt - too many wrong attempts')
            else:
                if self._GPGTool__c >= 1:
                    yesno = False
                    if self.gui:
                        yesno = xyesno('decryption failed - try again?')
                    else:
                        yesno = True if str(input('decryption failed - retry? [Y/n]')).lower() in ('y',
                                                                                                   '') else False
            if yesno:
                mss = message.split('\n')
                raise DecryptError('%s failed to decrypt %s\n...\n%s' % (
                 self.decrypt, '\n'.join(mss[:3]), '\n'.join(mss[3:])))

        return [
         _GPGTool__plain, 'KEYINTERRUPT']


class GPGSMTool(GPGTool):
    __doc__ = 'GPGSMTool class for compatibility to SSL keys/certificates'
    dbg = False
    homedir = path.join(path.expanduser('~'), '.gnupg')
    _GPGSMTool__gsm = 'gpgsm'
    _GPGSMTool__ssl = 'openssl'
    if osname == 'nt':
        homedir = path.join(path.expanduser('~'), 'AppData', 'Roaming', 'gnupg')
        _GPGSMTool__gsm = 'gpgsm.exe'
        _GPGSMTool__ssl = 'openssl.exe'
    _gsmbin = which(_GPGSMTool__gsm)
    _sslbin = which(_GPGSMTool__ssl)
    sslcrt = ''
    sslkey = ''
    sslca = ''
    recvs = []

    def __init__(self, *args, **kwargs):
        for arg in args:
            if hasattr(self, arg):
                setattr(self, arg, True)

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)

        if not self.recvs:
            if 'GPGKEYS' in environ.keys():
                self.recvs = environ['GPGKEYS'].split(' ')
            elif 'GPGKEY' in environ.keys():
                self.recvs = [
                 environ['GPGKEY']]
        if self.sslcrt:
            if self.sslkey:
                if osname == 'nt':
                    raise RuntimeError('ssl import is currently not available for windows')
                self.sslimport(self.sslkey, self.sslcrt, self.sslca)
        if self.dbg:
            print(bgre(GPGSMTool.__mro__))
            print(bgre(tabd(GPGSMTool.__dict__, 2)))
            print(' ', bgre(self.__init__))
            print(bgre(tabd(self.__dict__, 4)))
        (GPGTool.__init__)(self, *args, **kwargs)

    def sslimport(self, key, crt, ca):
        """ssl key/cert importing method"""
        if self.dbg:
            print(bgre('%s key=%s crt=%s' % (self.sslimport, key, crt)))
        self.stdo(('%s --import' % self._gsmbin), inputs=self.stdo(('%s pkcs12 -export -chain -CAfile %s -in %s -inkey %s' % (
         self._sslbin, ca, crt, key)),
          b2s=False),
          b2s=False)

    def keylist(self, secret=False):
        """key listing function"""
        if self.dbg:
            print(bgre(self.keylist))
        else:
            gsc = 'gpgsm -k'
            if secret:
                gsc = 'gpgsm -K'
            strs = self.stdo(gsc)
            keys = []
            if strs:
                strs = str('\n'.join(strs.split('\n')[2:])).split('\n\n')
                for ks in strs:
                    if not ks:
                        pass
                    else:
                        kid = str(ks.split('\n')[0].strip()).split(': ')[1]
                        inf = [i.strip() for i in ks.split('\n')[1:]]
                        key = {kid: {}}
                        for i in inf:
                            key[kid][i.split(': ')[0]] = i.split(': ')[1]

                        keys.append(key)

        return keys

    def findkey(self, pattern=''):
        return self.keylist()

    def encrypt(self, message, **kwargs):
        """text encrypting method"""
        if self.dbg:
            print(bgre(self.encrypt))
        recvs = self.recvs if 'recvs' not in kwargs.keys() else kwargs['recvs']
        if 'recipients' in kwargs.keys():
            recvs = kwargs['recipients']
        recvs = ''.join(['-r %s' % r for r in recvs])
        out = '' if 'output' not in kwargs.keys() else '-o %s' % kwargs['output']
        gsc = '%s -e --armor --disable-policy-checks --disable-crl-checks %s %s' % (
         self._gsmbin, out, recvs)
        _GPGSMTool__crypt = self.stdo(gsc, inputs=(message.encode()))
        if _GPGSMTool__crypt:
            return _GPGSMTool__crypt.decode()
        else:
            return False

    def decrypt(self, message, output=None):
        """text decrypting method"""
        if self.dbg:
            print(bgre(self.decrypt))
        out = '' if not output else '-o %s' % 'output'
        gsc = '%s -d %s' % (self._gsmbin, out)
        _GPGSMTool__plain = self.stdo(gsc, inputs=message)
        if _GPGSMTool__plain:
            return _GPGSMTool__plain
        else:
            return False