# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/passcrypt.py
# Compiled at: 2020-03-20 08:07:41
# Size of source mod 2**32: 11739 bytes
__doc__ = 'passcrypt module'
from sys import argv, stdout
from os import path, remove, environ, chmod, stat, makedirs, name as osname
from yaml import load, dump, Loader, Dumper
from colortext import blu, yel, grn, bgre, tabd, error
from system import userfind, filerotate, setfiletime, xgetpass, xmsgok, xinput, xnotify, filerotate, absrelpath, xyesno, random, copy
from secrecy.gpgtools import GPGTool, GPGSMTool, DecryptError, SignatureError
try:
    from atexit import register
except ImportError:
    pass

class PassCrypt(GPGTool):
    """PassCrypt"""
    dbg = None
    vrb = None
    aal = None
    fsy = None
    sho = None
    rnd = None
    out = None
    gsm = None
    sig = True
    dtg = True
    gui = None
    chg = None
    syn = None
    try:
        user = userfind()
        home = userfind(user, 'home')
    except FileNotFoundError:
        user = environ['USERNAME']
        home = path.join(environ['HOMEDRIVE'], environ['HOMEPATH'])

    user = user if user else 'root'
    home = home if home else '/root'
    config = path.join(home, '.config', 'pwclip.cfg')
    plain = path.join(home, '.pwd.yaml')
    crypt = path.join(home, '.passcrypt')
    recvs = []
    keys = {}
    gpgkey = ''
    sslcrt = ''
    sslkey = ''
    sigerr = None
    genpwrex = None
    genpwlen = 24
    _PassCrypt__weaks = {}
    _PassCrypt__oldweaks = {}

    def __init__(self, *args, **kwargs):
        """passcrypt init function"""
        for arg in args:
            if hasattr(self, arg):
                setattr(self, arg, True)

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)

        if self.dbg:
            print(bgre(PassCrypt.__mro__))
            print(bgre(tabd(PassCrypt.__dict__, 2)))
            print(' ', bgre(self.__init__))
            print(bgre(tabd(self.__dict__, 4)))
        else:
            self.cpasmsg = '%s %s%s ' % (
             blu('enter password for'), yel(self.crypt), blu(':'))
            gargs = list(args) + ['sig'] if self.sig else []
            if self.gui:
                gargs = list(args) + ['gui'] + ['sig'] if self.sig else []
                self.cpasmsg = 'enter password for %s: ' % self.crypt
            self.sig = True if 'sig' not in kwargs.keys() else kwargs['sig']
            if self.gsm or self.gsm is None and self.recvs and [r for r in self.recvs if r in GPGSMTool().keylist(True)]:
                (GPGSMTool.__init__)(self, *args, **kwargs)
            else:
                (GPGTool.__init__)(self, *args, **kwargs)
        self.keys = self.findkey()
        if not self.keys:
            self._mkconfkeys()
        self._PassCrypt__weaks = dict(sorted(dict(self._readcrypt()).items()))
        self._PassCrypt__oldweaks = str(self._PassCrypt__weaks)
        if osname != 'nt':
            register(self._cryptpass)

    def __del__(self):
        self._cryptpass()

    def _cryptpass(self):
        chgs = []
        crecvs = []
        if path.isfile(self.crypt):
            erecvs = list(set(self.recvlist(self.crypt)))
            for r in erecvs:
                crecvs.append('0x%s' % r[-16:])

            for r in self.recvs:
                if r not in crecvs:
                    chgs.append('+ %s' % r)

            for r in crecvs:
                if r not in self.recvs:
                    chgs.append('- %s' % r)

        if self._PassCrypt__oldweaks != str(dict(sorted(self._PassCrypt__weaks.items()))) or chgs:
            msg = (
             'recipients have changed:\n',
             '\n'.join(c for c in chgs),
             '\nfrom:\n', ' '.join(erecvs),
             '\nto:\n', ' '.join(self.recvs),
             '\nencryption enforced...')
            if chgs:
                if not self.gui:
                    error(*msg)
                else:
                    xmsgok(' '.join(msg))
            if not self.recvs:
                if not self.findkey():
                    (self.genkeys)(**self._gendefs(self.gui))
            if self._PassCrypt__weaks:
                if self._writecrypt(self._PassCrypt__weaks):
                    if self.vrb:
                        print(blu('file'), yel(self.crypt), blu('encrypted'))

    def _mkconfkeys(self):
        self.gpgkey = '0x%s' % str(self.genkeys())[-16:]
        cfgs = {'gpg': {}}
        override = False
        if path.isfile(self.config):
            override = True
            with open(self.config, 'r') as (cfh):
                cfgs = dict(load((cfh.read()), Loader=Loader))
            if 'gpg' not in cfgs.keys():
                cfgs['gpg'] = {}
        cfgs['gpg']['gpgkey'] = self.gpgkey
        if 'recipients' not in cfgs['gpg'].keys():
            cfgs['gpg']['recipients'] = self.gpgkey
            self.recvs = [self.gpgkey]
        with open(self.config, 'w+') as (cfh):
            cfh.write(str(dump(cfgs, Dumper=Dumper)))

    def _readcrypt(self):
        """read crypt file method"""
        if self.dbg:
            print(bgre(self._readcrypt))
        _PassCrypt__dct = {}
        try:
            _PassCrypt__dct, err = self.decrypt(self.crypt)
        except DecryptError as err:
            error(err)
            exit(1)

        _PassCrypt__dct = dict(load((str(_PassCrypt__dct)), Loader=Loader))
        if err:
            if err == 'SIGERR':
                if self.gui:
                    yesno = xyesno('reencrypt, even though the passcryt signature could not be verified?')
                else:
                    print(grn('reencrypt, even though the passcryt signature could not be verified?'), '[Y/n]')
                    yesno = input()
                    yesno = True if yesno in ('', 'y') else False
                if yesno:
                    if _PassCrypt__dct:
                        self._writecrypt(_PassCrypt__dct)
        return _PassCrypt__dct

    def _writecrypt(self, _PassCrypt__weaks):
        """crypt file writing method"""
        if self.dbg:
            print(bgre(self._writecrypt))
        kwargs = {'output':self.crypt,  'gpgkey':self.gpgkey, 
         'recvs':self.recvs}
        filerotate(self.crypt, 3)
        if self.sig:
            if self.dtg:
                filerotate('%s.sig' % self.crypt, 3)
        isok = self.encrypt((str(dump(_PassCrypt__weaks, Dumper=Dumper))),
          output=(self.crypt))
        chmod(self.crypt, 384)
        return isok

    def __askpwdcom(self, sysuser, usr, pwd, com, opw, ocom):
        if self.rnd:
            pwd = self.rndgetpass()
        if self.gui:
            if not pwd:
                pwd = xgetpass('blank input preserves already set comment/password\nas user %s: enter password for entry %s' % (sysuser, usr))
                pwd = pwd if pwd else opw
                if not pwd:
                    xmsgok('password is needed if adding password')
                    return
            else:
                com = com or xinput('enter comment (optional, "___" deletes the comment)')
            com = ocom if not com else com
            if com == '___':
                com = None
        else:
            if not pwd:
                print((blu('blank input preserves already set comment/password')),
                  (blu('as user ')),
                  (yel(sysuser)), ': ', sep='')
                pwd = pwd if pwd else self.passwd(msg=('%s%s%s%s: ' % (
                 blu('  enter '), yel('password '),
                 blu('for entry '), yel('%s' % usr))))
                pwd = pwd if pwd else opw
                pwd or error('password is needed if adding password')
                return
            else:
                if not com:
                    print((blu('  enter ')),
                      (yel('comment ')), (blu('(optional, ')),
                      (yel('___')), (blu(' deletes the comment)')),
                      ': ', sep='', end='')
                    com = input()
                com = ocom if not com else com
                if com == '___':
                    com = None
                return [p for p in [pwd, com] if p is not None]

    def rndgetpass(self):
        while 1:
            _PassCrypt__pwd = random(self.genpwlen, self.genpwrex)
            yesno = False
            if self.gui:
                yesno = xyesno('use the following password: "%s"?' % _PassCrypt__pwd)
            else:
                print(('%s %s%s [Y/n]' % (
                 grn('use the following password:'),
                 yel(_PassCrypt__pwd), grn('?'))),
                  sep='')
                yesno = input()
                yesno = True if str(yesno).lower() in ('y', '') else False
            if yesno:
                break

        return _PassCrypt__pwd

    def adpw(self, usr, pwd=None, com=None):
        """password adding method"""
        if self.dbg:
            print(bgre(tabd({self.adpw: {'user':self.user,  'entry':usr,  'pwd':pwd, 
                         'comment':com}})))
        elif self.user not in self._PassCrypt__weaks.keys():
            self._PassCrypt__weaks[self.user] = {}
        else:
            if not self.aal:
                if self.user in self._PassCrypt__weaks.keys():
                    if usr in self._PassCrypt__weaks[self.user]:
                        if self.gui:
                            xmsgok('entry %s already exists for user %s' % (
                             usr, self.user))
                        else:
                            error('entry', usr, 'already exists for user', self.user)
                        return self._PassCrypt__weaks
                    else:
                        if self.user not in self._PassCrypt__weaks.keys():
                            self._PassCrypt__weaks[self.user] = {}
                        try:
                            _PassCrypt__opw, _PassCrypt__ocom = self._PassCrypt__weaks[self.user][usr]
                        except KeyError:
                            _PassCrypt__opw, _PassCrypt__ocom = (None, None)

                    pwdcom = self._PassCrypt__askpwdcom(self.user, usr, pwd, com, _PassCrypt__opw, _PassCrypt__ocom)
                    if pwdcom:
                        self._PassCrypt__weaks[self.user][usr] = [p for p in pwdcom if p]
            else:
                for u in self._PassCrypt__weaks.keys():
                    if usr in self._PassCrypt__weaks[u].keys():
                        if self.gui:
                            xmsgok('entry %s already exists for user %s' % (usr, u))
                        else:
                            error('entry', usr, 'already exists for user', u)
                    else:
                        _PassCrypt__opw, _PassCrypt__ocom = self._PassCrypt__weaks[u][usr]
                        pwdcom = self._PassCrypt__askpwdcom(self.user, usr, pwd, com, _PassCrypt__opw, _PassCrypt__ocom)
                        if pwdcom:
                            self._PassCrypt__weaks[u][usr] = [p for p in pwdcom if p]

        return dict(self._PassCrypt__weaks)

    def chpw(self, usr, pwd=None, com=None):
        """change existing password method"""
        if self.dbg:
            print(bgre(tabd({self.chpw: {'user':self.user,  'entry':usr,  'pwd':pwd}})))
        else:
            if not self.aal:
                if self._PassCrypt__weaks:
                    if self.user in self._PassCrypt__weaks.keys():
                        if usr in self._PassCrypt__weaks[self.user].keys():
                            try:
                                _PassCrypt__opw = self._PassCrypt__weaks[self.user][usr][0]
                            except IndexError:
                                return
                            else:
                                try:
                                    _PassCrypt__ocmd = self._PassCrypt__weaks[self.user][usr][1]
                                except IndexError:
                                    _PassCrypt__ocmd = None

                                self._PassCrypt__weaks[self.user][usr] = self._PassCrypt__askpwdcom(self.user, usr, pwd, com, _PassCrypt__opw, _PassCrypt__ocmd)
                else:
                    if self.gui:
                        xmsgok('no entry named %s for user %s' % (usr, self.user))
                    else:
                        error('no entry named', usr, 'for user', self.user)
            else:
                for u in self._PassCrypt__weaks.keys():
                    _PassCrypt__opw = ''
                    _PassCrypt__ocom = None
                    if usr not in self._PassCrypt__weaks[u].keys():
                        self._PassCrypt__weaks[u][usr] = [
                         _PassCrypt__opw, _PassCrypt__ocom]
                    else:
                        if self._PassCrypt__weaks[self.user][usr]:
                            _PassCrypt__opw, _PassCrypt__ocom = self._PassCrypt__weaks[self.user][usr]
                    self._PassCrypt__weaks[u][usr] = self._PassCrypt__askpwdcom(self.user, usr, pwd, com, _PassCrypt__opw, _PassCrypt__ocom)

        return dict(self._PassCrypt__weaks)

    def rmpw(self, usr):
        """remove password method"""
        if self.dbg:
            print(bgre(tabd({self.rmpw: {'user':self.user,  'entry':usr}})))
        else:
            if self.aal:
                _PassCrypt__w = dict(self._PassCrypt__weaks)
                for u in _PassCrypt__w.keys():
                    try:
                        del self._PassCrypt__weaks[u][usr]
                        setattr(self, 'chg', True)
                    except KeyError:
                        if self.gui:
                            xmsgok('entry %s not found as user %s' % (usr, u))
                        else:
                            error('entry', usr, 'not found as user', u)

                    if not self._PassCrypt__weaks[u].keys():
                        del self._PassCrypt__weaks[u]

            elif self.user in self._PassCrypt__weaks.keys():
                if usr in self._PassCrypt__weaks[self.user].keys():
                    del self._PassCrypt__weaks[self.user][usr]
            else:
                if self.gui:
                    xmsgok('entry %s not found as user %s' % (usr, self.user))
                else:
                    error('entry', usr, 'not found as user', self.user)
        if self.user in self._PassCrypt__weaks.keys():
            if not self._PassCrypt__weaks[self.user].keys():
                del self._PassCrypt__weaks[self.user]
        return dict(self._PassCrypt__weaks)

    def lspw(self, usr=None, aal=None):
        """password listing method"""
        if self.dbg:
            if not self.gui:
                print(bgre(tabd({self.lspw: {'user':self.user,  'entry':usr}})))
        aal = True if aal else self.aal
        _PassCrypt__ents = {}
        if self._PassCrypt__weaks:
            if aal:
                _PassCrypt__ents = self._PassCrypt__weaks
                if usr:
                    usrs = [
                     self.user] + [u for u in self._PassCrypt__weaks.keys() if u != self.user]
                    for u in usrs:
                        if u in self._PassCrypt__weaks.keys():
                            if usr in self._PassCrypt__weaks[u].keys():
                                _PassCrypt__ents = {usr: self._PassCrypt__weaks[u][usr]}
                                break

            elif self.user in self._PassCrypt__weaks.keys():
                _PassCrypt__ents = self._PassCrypt__weaks[self.user]
                if usr in _PassCrypt__ents.keys():
                    _PassCrypt__ents = {usr: self._PassCrypt__weaks[self.user][usr]}
        return dict(_PassCrypt__ents)


def lscrypt(usr, dbg=None):
    """passlist wrapper function"""
    if dbg:
        print(bgre(lscrypt))
    __ents = {}
    if usr:
        __ents = PassCrypt().lspw(usr)
    return __ents


if __name__ == '__main__':
    exit(1)