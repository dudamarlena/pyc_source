# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Passwd.py
# Compiled at: 2011-10-05 18:47:45
"""Celestial Software Password Utitilities

These routines get and maintain password and shadow files.

import Csys.Passwd

accts = Csys.Passws.read_password_shadow()

$Id: Passwd.py,v 1.12 2011/10/05 22:47:45 csoftmgr Exp $"""
__version__ = '$Revision: 1.12 $'[11:-2]
import os, sys, re, email, copy, Csys
myHostname = Csys.Config.hostname

class Error(Exception):
    """Base class for Csys.Passwd exceptions"""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class NoOStype(Error):
    """Raised on unknown OK type (sys.platform)"""

    def __init__(self, osname):
        Error.__init__(self, 'Unknown Platform: %s' % osname)
        self.osname = osname


class ReadOnly(Error):
    """Raised on attempt to change read only field"""

    def __init__(self, field):
        Error.__init__(self, 'Cannot change read-only field %s: %s' % (
         field, self.__dict__[field]))


from Csys.LockFile import lockFile
lockedFiles = {}
_saltchars = ('.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
              'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
              'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
              's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

def mksalt(size=2):
    """Return salt string from _saltchars set"""
    from random import randint
    if size < 2:
        raise Error('mksalt: size %d < 2' % size)
    n = len(_saltchars) - 1
    salt = ''
    while size > 0:
        salt += _saltchars[randint(0, n)]
        size -= 1

    return salt


from crypt import crypt

def mkpasswd(passwd, salt=mksalt()):
    """Create encrypted password"""
    return crypt(passwd, salt)


def chkpasswd(plaintext, cryptpw):
    """Check plaintext password against encrypted version"""
    return cryptpw == crypt(plaintext, cryptpw)


class _OSTable(Csys.CSClass):
    """Operating specific parameters"""
    _attributes = {'osname': None, 
       'passwd_fields': ('user', 'pwd', 'uid', 'gid', 'gcos', 'home', 'shell'), 
       'passwd_default': '/etc/passwd', 
       'shadow_default': '/etc/shadow', 
       'group_default': '/etc/group', 
       'useradd_fmt': "cspw.py useradd -u %(uid)s -g %(gid)s -c '%(gcos)s' -d '%(home)s' -s %(shell)s -p'%(pwd)s' '%(user)s'", 
       'useradd_fmt1': "useradd -m -c '%(gcos)s' -d '%(home)s' -s %(shell)s '%(user)s'", 
       'use_master_passwd': False, 
       'pw_uid': 0, 
       'pw_gid': 0, 
       'pw_mode': 420, 
       'sh_uid': 0, 
       'sh_gid': 0, 
       'sh_mode': 384, 
       'max_admin': 100, 
       'nouser': 'nobody', 
       'nouser_uid': 65534, 
       'nouser_gid': 65533, 
       'nogroup': 'nobody', 
       'nogroup_gid': 65534, 
       'shadow_fields': ('user', 'pwd', 'lastChanged', 'minChangeDays', 'maxChangeDays', 'warnBefore', 'disableAfter',
 'expirationDate', 'shadowFlags')}

    def __init__(self, osname, **kwflags):
        Csys.CSClass.__init__(self, **kwflags)
        self.osname = osname


osTable = {re.compile('^linux', re.IGNORECASE): 'linux', 
   re.compile('^freebsd', re.IGNORECASE): 'freebsd', 
   re.compile('^sco_sv', re.IGNORECASE): 'sco_sv', 
   re.compile('^darwin', re.IGNORECASE): 'darwin', 
   re.compile('^sunos5', re.IGNORECASE): 'sunos5'}
osname = sys.platform
for p, t in osTable.items():
    if p.search(osname):
        osname = t
        break
else:
    raise NoOStype(osname)

_OSTables = {'default': _OSTable('default'), 
   'freebsd': _OSTable('freebsd', passwd_fields=('user', 'pwd', 'uid', 'gid', 'bsd_change', 'bsd_class',
                                   'bsd_expire', 'gcos', 'home', 'shell'), passwd_default='/etc/master.passwd', shadow_default=None, pw_mode=384, useradd_fmt="pw useradd -m -u %(uid)s -g %(gid)s -c '%(gcos)s' -d '%(home)s' -s %(shell)s -n '%(user)s'", useradd_fmt1="pw useradd -m -c '%(gcos)s' -d '%(home)s' -s %(shell)s -n '%(user)s'"), 
   'sco_sv': _OSTable('sco_sv', max_admin=200, nouser='nouser', nouser_uid=28, nouser_gid=28, nogroup_gid=28, shadow_fields=('user',
                                                                                                                'pwd',
                                                                                                                'lastChanged',
                                                                                                                'minChangeDays',
                                                                                                                'sp_max'))}
OSTable = _OSTables[{'linux': 'default', 
   'freebsd': 'freebsd', 
   'sco_sv': 'sco_sv', 
   'darwin': 'freebsd', 
   'sunos5': 'default'}[osname]]
nogroup = OSTable.nogroup
nogroup_gid = OSTable.nogroup_gid
nouser = OSTable.nouser
nobody = nouser
nouser_gid = OSTable.nouser_gid
nouser_uid = OSTable.nouser_uid
skipNoUserGids = set((nogroup_gid, nouser_gid))
if OSTable.osname != osname:
    _OSTables[osname] = OSTable
adminAccounts = set([
 'amanda',
 'at',
 'bin',
 'bind',
 'csoft',
 'csoftdev',
 'csoftmgr',
 'cvs',
 'daemon',
 'dhcpd',
 'distcc',
 'dnscache',
 'dnslog',
 'ftp',
 'games',
 'gdm',
 'hacluster',
 'irc',
 'kmem',
 'ldap',
 'lp',
 'mail',
 'mailnull',
 'man',
 'mdom',
 'mysql',
 'netdump',
 'news',
 'nobody',
 'nouser',
 'ntp',
 'operator',
 'pop',
 'postfix',
 'postgres',
 'privoxy',
 'pwrchute',
 'quagga',
 'radiusd',
 'root',
 'smmsp',
 'squid',
 'sshd',
 'stunnel',
 'tinydns',
 'tomcat',
 'toor',
 'tty',
 'uucp',
 'vdr',
 'www',
 'wwwrun',
 'xten'])
nobodyAccounts = set([
 'nobody',
 'nouser',
 'nfsnobody'])
_write_passwd_or_shadow_kwargs = {'no_admin': False, 
   'delim': ':', 
   'with_pwd': False, 
   'inplace': False, 
   'overwrite': False, 
   'passwd': None, 
   'shadow': None, 
   'osname': 'default'}
_read_passwd_shadow_opts = {'hostname': myHostname, 
   'passwd': None, 
   'shadow': None, 
   'group': None, 
   'forcechange': False, 
   'osname': osname, 
   'ssh': None, 
   'lockupdate': False}

class Passwd(Csys.CSClass):
    _attributes = {'user': '', 
       'pwd': '', 
       'uid': 0, 
       'gid': 0, 
       'gcos': '', 
       'home': '', 
       'shell': '', 
       'is_changed': '', 
       'lastChanged': 10869, 
       'minChangeDays': -1, 
       'maxChangeDays': -1, 
       'maxChangeDays': -1, 
       'warnBefore': -1, 
       'sp_max': '', 
       'disableAfter': -1, 
       'expirationDate': -1, 
       'shadowFlags': '', 
       'bsd_change': '', 
       'bsd_class': '', 
       'bsd_expire': '', 
       '_osname': 'default', 
       '_parent': None, 
       '_intAttrs': ('uid', 'gid', 'seq', 'lastChanged'), 
       '_seq': 0}

    def __init__(self, parent, pwline, forcechange=False, seq=0, osname=osname, **kwargs):
        Csys.CSClass.__init__(self, False, **kwargs)
        cols = self.__dict__
        cols['_osname'] = osname
        OS = self._ostype = _OSTables[self._osname]
        incols = dict(zip(OS.passwd_fields, pwline.split(':')))
        self._convertInts(incols)
        cols.update(incols)
        self.pwline = pwline
        self.finishInit(seq, forcechange)

    def finishInit(self, seq, forcechange):
        if not self.gcos:
            self.gcos = 'unknown'
        OS = self._ostype = _OSTables[self._osname]
        P = self._parent
        uid = self.uid
        if P:
            if uid != OS.nouser_uid and uid > P.max_uid:
                P.max_uid = uid
            if not seq:
                P.max_seq += 1
                seq = P.max_seq
        self._seq = int(seq)
        self.disabled = self.pwd.startswith('*')
        cols = self.__dict__
        cols['_is_changed'] = forcechange
        cols['is_admin'] = self.user in adminAccounts or self.uid < OS.max_admin
        cols['deleted'] = False
        cols['sortkey'] = '%08d%s' % (self._seq, self.user)
        lastChanged = int(self.lastChanged)
        if P and lastChanged > P.max_lastChanged:
            P.max_lastChanged = lastChanged

    def _convertInts(self, dict):
        """Convert dictionary fields to int where necessary"""
        _intAttrs = self._attributes['_intAttrs']
        for k, v in dict.items():
            try:
                if k in _intAttrs:
                    dict[k] = int(v)
            except:
                pass

    def useradd(self):
        """Return useradd shell command"""
        OS = self._ostype = _OSTables[self._osname]
        return OS.useradd_fmt % self.__dict__

    def __setattr__(self, attr, val):
        """Set attributes"""
        cols = self.__dict__
        if attr == '_parent':
            cols[attr] = val
            return
        _intAttrs = self._attributes['_intAttrs']
        if attr in _intAttrs:
            val = int(val)
        P = self._parent
        try:
            if val != cols[attr]:
                if attr in ('user', ):
                    raise ReadOnly(attr)
                if not attr.startswith('_') and attr != '_is_changed' and attr in self._attributes:
                    cols['_is_changed'] = True
                    if P:
                        P.changes += 1
                if attr == 'pwd':
                    if not val:
                        val = '*'
                    self.disabled = val.startswith('*')
                elif attr == 'uid':
                    if P and val != OS.nouser_uid and val > P.max_uid:
                        P.max_uid = val
                    cols['is_admin'] = int(val) < max_admin
                elif attr == 'lastChanged':
                    if P and int(val) > P.max_lastChanged:
                        P.max_lastChanged = val
        except:
            pass

        cols[attr] = val

    def disable(self):
        """Disable accounting by setting first character of pwd to '*' """
        if not self.disabled:
            self.pwd = '*' + self.pwd
            self.disabled = True

    def enable(self):
        """Enable account by removing leading '*' from password"""
        if self.pwd.startswith('*') and len(self.pwd > 1):
            self.pwd = self.pwd[1:]

    def get_shadow(self, shadow_line, setUpdate=False):
        """Get shadow info from shadow file line without changing is_changed"""
        shadow = dict(zip(self._ostype.shadow_fields, shadow_line.split(':')))
        user = shadow['user']
        if user != self.user:
            raise Error('Shadow User %s != %s' % (user, self.user))
        self._convertInts(shadow)
        P = self._parent
        if P and self.lastChanged > P.max_lastChanged:
            P.max_lastChanged = self.lastChanged
        if setUpdate:
            for k, v in shadow.items():
                self.__setattr__(k, v)

        else:
            cols = self.__dict__
            cols.update(shadow)
        self.disabled = self.pwd.startswith('*')

    def upd_shadow(self, shadow_line):
        """Get shadow info from shadow file line without changing is_changed"""
        self.set_shadow(shadow_line, setUpdate=True)

    def upd_passwd(self, pwline, setPwd=False):
        """Update from password line"""
        password = dict(zip(self._ostype.passwd_fields, pwline.split(':')))
        if not setPwd:
            password.pop('pwd')
        for k, v in password.items():
            self.__setattr__(k, v)

        return 'OK'

    def print_passwd_val(self, with_pwd=False, delim=':', with_user=True, ostype=None):
        """Return password string

                If with_pwd is False, substitute 'x' for encrypted password
                if with_user is False, drop the first field (uname)
                """
        if ostype:
            OS = _OSTables[ostype]
        else:
            OS = self._ostype
        dict = self.__dict__.copy()
        fields = list(OS.passwd_fields[:])
        if not with_pwd:
            dict['pwd'] = 'x'
        if not with_user:
            fields.pop(0)
        output = []
        for field in fields:
            output.append(str(dict[field]))

        return delim.join(output)

    def print_passwd(self, with_pwd=False, delim=':', ostype=None):
        """Print entire password line"""
        if ostype:
            OS = _OSTables[ostype]
        else:
            OS = self._ostype
        if OS.use_master_passwd:
            with_pwd = True
        return self.print_passwd_val(with_pwd, delim, with_user=True, ostype=ostype)

    def print_shadow_val(self, delim=':', ostype=None):
        """Get shadow line without username"""
        if ostype:
            OS = _OSTables[ostype]
        else:
            OS = self._ostype
        d = self.__dict__
        output = [ str(d.get(x, '')) for x in OS.shadow_fields[1:] ]
        for i in range(0, len(output)):
            if output[i] == '0':
                output[i] = ''

        s = delim.join(output)
        return s

    def print_compare_string(self, with_pwd=False, delim=':', with_user=True, ostype=None):
        """generate string for comparison"""
        return delim.join((
         self.print_passwd_val(with_pwd=with_pwd, delim=delim, with_user=with_user, ostype=ostype),
         self.print_shadow_val(delim=delim, ostype=ostype)))

    def __str__(self):
        return self.print_compare_string()

    def __cmp__(self, other):
        return cmp((self._seq, self.user), (other._seq, other.user))

    def print_shadow(self, delim=':', ostype=None):
        """Get entire shadow line with username"""
        if ostype:
            OS = _OSTables[ostype]
        else:
            OS = self._ostype
        d = self.__dict__
        output = [ str(d[x]) for x in OS.shadow_fields ]
        return delim.join(output)

    def printldif(self, base):
        """LDAP user output"""
        raise Error('printldif not implemented yet')

    def dumpldifs(self, base):
        """LDAP user output"""
        raise Error('dumpldifs not implemented yet')

    def cryptw(self, plaintext, nullok=False):
        if not (plaintext or nullok):
            raise Error('cryptpw: null password not allowed %s' % self.user)
        if plaintext:
            self.pwd = mkpasswd(plaintext)
        else:
            self.pwd = ''
        return self.pwd

    def checkpw(self, plaintext):
        """Check plain text password"""
        return chkpasswd(plaintext, self.pwd)


class PasswdAccounts(Csys.CSClass):
    _attributes = {'hostname': myHostname, 
       'passwd': None, 
       'shadow': None, 
       'group': None, 
       'osname': osname, 
       'accts': {}, 'origaccts': {}, 'max_seq': 0, 
       'max_uid': 0, 
       'max_lastChanged': 10869, 
       'changes': 0, 
       'OSinput': OSTable, 
       'OSoutput': OSTable, 
       'forcechange': False, 
       'lockupdate': False, 
       'ssh': None, 
       '_readaccounts': True, 
       '_lastline': '', 
       'groups': None}

    def __init__(self, **kwargs):
        cols = self.__dict__
        Csys.CSClass.__init__(self, **kwargs)
        OS = self.OSinput = _OSTables[self.osname]
        if self.passwd is None:
            self.passwd = OS.passwd_default
        if self.shadow is None:
            self.shadow = OS.shadow_default
        if self.group is None:
            self.group = OS.group_default
        lockupdate = self.lockupdate
        ssh = self.ssh
        hostname = self.hostname
        if hostname != myHostname:
            self.lockupdate = lockupdate = False
            if not ssh:
                self.ssh = ssh = 'ssh %s cat ' % hostname
        if lockupdate:
            lock = lockedFiles[passwd] = lockFile(passwd)
            if not lock.is_locked:
                raise Error('read_passwd_shadow: failed to lock %s' % passwd)
        if hasattr(self.passwd, 'readlines'):
            fh = self.passwd
        elif ssh:
            fh = Csys.popen(ssh + self.passwd)
        else:
            fh = open(self.passwd)
        accts = self.accts
        if self._readaccounts:
            seq = 0
            for pwline in fh:
                pwline = pwline.rstrip()
                if pwline.startswith('+::::::'):
                    self._lastline = pwline
                    continue
                try:
                    seq += 1
                    pw = Passwd(self, pwline, seq=seq, **cols)
                    accts[pw.user] = pw
                except:
                    sys.stderr.write('bad pw >%s<\n' % pwline)

            fh.close()
            if not OS.use_master_passwd and self.shadow and not self.forcechange:
                if hasattr(self.shadow, 'readlines'):
                    fh = self.shadow
                else:
                    if ssh:
                        fh = Csys.popen(ssh + self.shadow)
                    else:
                        fh = open(self.shadow)
                    for shadowline in fh:
                        shadowline = shadowline.rstrip()
                        user, rest = shadowline.split(':', 1)
                        try:
                            acct = accts[user]
                            acct.get_shadow(shadowline)
                        except:
                            sys.stderr.write('acct >%s< missing from passwd\n' % user)

            self.origaccts = copy.deepcopy(accts)
            self.groups = readGroupFile(self.group, **kwargs)
        return

    def _OSoutput(self, ostype=None):
        """Return OS object for output"""
        if ostype is None:
            OS = self.OSoutput
        else:
            OS = _OSTables[ostype]
        return OS

    def write_passwd_or_shadow(self, ftype, fname=None, ostype=None, **kwargs):
        """Lock and write password or shadow files"""
        accts = self.accts
        ftype = ftype.lower()
        if ftype not in ('passwd', 'shadow'):
            raise Error('write_passwd_or_shadow: %s must be passwd or shadow' % ftype)
        kw = Csys.KWArgs(_write_passwd_or_shadow_kwargs, False, **kwargs)
        OS = self._OSoutput(ostype)
        if fname is None:
            fname = kw.__dict__[ftype]
            if fname is None:
                attr = ftype + '_default'
                fname = OS.__dict__[attr]
        if fname is None:
            return True
        if kw.inplace:
            lock = lockedFiles[fname] = lockFile(fname)
            if not lock.is_locked:
                raise Error('write_passwd_or_shadow: failed to lock %s' % fname)
            fwrite = fname + '.new'
            if os.access(fwrite):
                os.unlink(fwrite)
        else:
            fwrite = fname
            if os.access(fwrite, os.F_OK):
                if not kw.overwrite:
                    raise Error('write_passwd_or_shadow: file %s exists' % fwrite)
                os.unlink(fwrite)
            fh = open(fwrite, 'w')
            writingPasswdFile = ftype == 'passwd'
            if writingPasswdFile:
                os.chown(fwrite, OS.pw_uid, OS.pw_gid)
                os.chmod(fwrite, OS.pw_mode)
            else:
                os.chown(fwrite, OS.sh_uid, OS.sh_gid)
                os.chmod(fwrite, OS.sh_mode)
            sort_accts = []
            no_admin = kw.no_admin
            for k, acct in accts.items():
                if acct.deleted:
                    continue
                if not (no_admin and (acct.disabled or acct.is_admin or acct.user == OS.nobody)):
                    sort_accts.append(acct)

            sort_accts.sort()
            with_pwd, delim = kw.with_pwd, kw.delim
            for acct in sort_accts:
                if writingPasswdFile:
                    fh.write('%s\n' % acct.print_passwd_val(with_pwd, delim, ostype=ostype))
                else:
                    fh.write('%s\n' % acct.print_shadow(delim, ostype=ostype))

        if writingPasswdFile and self._lastline:
            fh.write('%s\n' % self._lastline)
        fh.close()
        if fwrite != fname and lock.is_locked:
            os.rename(fwrite, fname)
            lock.unlock()
        return True

    def write_passwd(self, passwd=None, ostype=None, **kwargs):
        kw = Csys.KWArgs(_write_passwd_or_shadow_kwargs, **kwargs)
        if passwd is None:
            passwd = kw.passwd
        if passwd is None:
            passwd = self._OSoutput(ostype).passwd_default + '.new'
        return self.write_passwd_or_shadow('passwd', passwd, ostype=ostype, **kwargs)

    def write_shadow(self, shadow=None, ostype=None, **kwargs):
        kw = Csys.KWArgs(_write_passwd_or_shadow_kwargs, **kwargs)
        if shadow is None:
            shadow = kw.shadow
        if shadow is None:
            shadow = self._OSoutput(ostype).shadow_default + '.new'
        return self.write_passwd_or_shadow('shadow', shadow, ostype=ostype, **kwargs)

    def write_passwd_shadow(self, passwd=None, shadow=None, ostype=None, **kwargs):
        if not (self.write_passwd(passwd, ostype=ostype, **kwargs) and self.write_shadow(shadow, ostype=ostype, **kwargs)):
            raise Error('write_passwd_shadow: Failed')

    def deletedaccts(self):
        """Return deleted account objects"""
        accts = self.accts
        deleted = {}
        for k, v in self.origaccts.items():
            if k not in accts:
                deleted[k] = v

        return deleted

    def changedaccts(self):
        """Return dictionary of accounts with changes"""
        changed = {}
        if self.changes:
            for k, v in self.accts.items():
                if v.is_changed:
                    changed[k] = v

        return changed


_currentAccounts = None

def read_passwd_shadow(passwd=None, shadow=None, hostname=None, **kwargs):
    """Set up argument and return PasswdAccounts object"""
    global _currentAccounts
    kw = Csys.KWArgs(_read_passwd_shadow_opts, **kwargs)
    OS = _OSTables[kw.osname]
    if passwd is not None:
        kw.passwd = passwd
    if shadow is not None:
        kw.shadow = shadow
    if hostname is not None:
        kw.hostname = hostname
    _currentAccounts = PasswdAccounts(**kw.__dict__)
    return _currentAccounts


def origpasswds():
    """Return dictionary of original accounts"""
    return _currentAccounts.origaccts


def deletedaccts():
    """Return deleted account objects"""
    return _currentAccounts.deletedaccts()


def changedaccts():
    """Return dictionary of accounts with changes"""
    return _currentAccounts.changedaccts()


def write_passwd(passwd=None, ostype=None, **kwargs):
    return _currentAccounts.write_passwd(passwd, ostype, **kwargs)


def write_shadow(shadow=None, ostype=None, **kwargs):
    return _currentAccounts.write_shadow(shadow, ostype, **kwargs)


def write_passwd_shadow(passwd=None, shadow=None, ostype=None, **kwargs):
    return _currentAccounts.write_passwd_shadow(passwd, shadow, ostype, **kwargs)


def getpwnam(user):
    """Shortcut to get info from system getpwd command"""
    from pwd import getpwnam
    return Passwd(None, (':').join([ str(x) for x in getpwnam(user) ]), osname='default')


reQUOTES = re.compile('[\'"]')

def genPassword(n=1):
    """Generate pronounceable password using "apg" """
    while True:
        fh = Csys.popen('%s -Mnc -n %d' % (os.path.join(Csys.prefix, 'bin/apg'), n * 2))
        output = []
        for line in fh:
            pw = line.rstrip()
            if not reQUOTES.search(pw):
                output.append(line.rstrip())

        fh.close()
        if len(output) >= n:
            break

    if n == 1:
        return output[0]
    else:
        return output


def getSinglePasswd(user):
    """Quick way to get one user from passwd and shadow files"""
    assert user is not None, 'getPasswd: user must be specified'
    accts = read_passwd_shadow(Csys.popen('grep "^%s:" /etc/passwd' % user), Csys.popen('grep "^%s:" /etc/shadow' % user)).accts
    return accts.get(user)


actions = {'add': 1, 
   'modify': 0, 
   'delete': -1, 
   'enable': 2, 
   'disable': 3}
ADD = actions['add']
MODIFY = actions['modify']
DELETE = actions['delete']
ENABLE = actions['enable']
DISABLE = actions['disable']
shells = dict([ (s, s) for s in ('/bin/sh', '/bin/bash', '/bin/ksh')
              ])
try:
    fh = open('/etc/shells')
    for line in fh:
        line = line.rstrip()
        shells[os.path.basename(line)] = line

    fh.close()
except IOError as e:
    pass

class UserAddMod(Csys.CSClass):
    """Utility class to generate useradd and usermod commands"""
    _attributes = {'user': '', 
       'pwd': '*Not Set*', 
       'pwdPlain': '', 
       'uid': '', 
       'gid': '', 
       'gcos': 'unknown', 
       'home': '', 
       'shell': '/bin/false', 
       'error': '', 
       'newuser': ''}

    def __init__(self, user, **kwargs):
        Csys.CSClass.__init__(self, raiseError=False, **kwargs)
        self.user = user
        if self.pwdPlain:
            self.pwd = mkpasswd(self.pwdPlain)
        shell = self.shell
        if shell and shell[0] != '/':
            self.shell = shells.get(shell, '/bin/false')

    def _runcmd(self, execute, name, cmd):
        """Run system command returning result and setting error"""
        if not execute:
            return execute
        rc = Csys.system(cmd)
        if rc:
            self.error = '%s: FAILED %s' % (name, cmd)
        return rc

    def useradd(self, execute=False, adminOK=False):
        """Generate useradd command"""
        user = self.user
        if getSinglePasswd(user):
            self.error = 'useradd: Duplicate User >%s<' % user
            return None
        else:
            self.error = ''
            if not self.home:
                self.home = '/home/' + self.user
            cmd = '/usr/sbin/useradd -m -d %s -c %s' % (
             repr(self.home), repr(self.gcos))
            if self.pwd:
                cmd = cmd + ' -p %s' % repr(self.pwd)
            if self.uid:
                OS = _currentAccounts._OSoutput()
                if not adminOK and int(self.uid) < OS.max_admin:
                    self.error = 'useradd: cannot add admin user >%s< uid %s' % (
                     user, self.uid)
                    return None
                cmd = cmd + ' -u %s' % self.uid
            if self.gid:
                cmd = cmd + ' -g %s' % self.gid
            if self.shell:
                cmd = cmd + ' -s %s' % repr(self.shell)
            cmd = cmd + ' ' + user
            self.cmd = cmd
            if self._runcmd(execute, 'useradd', cmd):
                return None
            return getSinglePasswd(self.user)

    def usermod(self, execute=False, adminOK=False):
        user = self.user
        pw = getSinglePasswd(user)
        if not pw:
            self.error = 'usermod: No User >%s<' % user
            return None
        else:
            if not adminOK and pw.is_admin:
                self.error = 'usermod: Cannot modify admin user >%s<' % user
                return None
            self.error = ''
            if self.newuser and self.newuser != user:
                newpw = getSinglePasswd(self.newuser)
                if newpw:
                    self.error = 'usermod: newuser %s exists cannot change %s' % (
                     self.newuser, user)
                    return None
                self.user = self.newuser
                self.pwd = pw.pwd
                self.gcos = pw.gcos
                self.shell = pw.shell
                self.home = pw.home.replace(user, newuser)
                self.adduser(execute, adminOK)
                newpw = getSinglePasswd(self.newuser)
                if not newpw:
                    self.error = 'usermod: change %s to %s failed' % (
                     pw.user, self.user)
                    return None
                cmd = os.path.join(Csys.prefix, 'bin/grm') + ' -r ' + newpw.home
                if self._runcmd(execute, 'usermod', cmd):
                    return None
                cmd = os.path.join(Csys.prefix, 'bin/gmv') + ' %s %s' % (
                 pw.home, newpw.home)
                if self._runcmd(execute, 'usermod', cmd):
                    return None
                cmd = os.path.join(Csys.prefix, 'bin/gchown') + ' -R %s: %s' % (newpw.user, newpw.user)
                if self._runcmd(execute, 'usermod', cmd):
                    return None
                self.user = pw.user
                self.userdel(action, adminOK)
                self.user = newpw.user
                return newpw
            cmd = '/usr/sbin/usermod'
            if self.home:
                cmd = cmd + ' -d %s' % repr(self.home)
            if self.gcos:
                cmd = cmd + ' -c %s' % repr(self.gcos)
            if self.pwd:
                cmd = cmd + ' -p %s' % repr(self.pwd)
            if self.uid:
                cmd = cmd + ' -u %s' % self.uid
            if self.gid:
                cmd = cmd + ' -g %s' % self.gid
            if self.shell:
                cmd = cmd + ' -s %s' % repr(self.shell)
            cmd = cmd + ' ' + self.user
            self.cmd = cmd
            if self._runcmd(execute, 'usermod', cmd):
                return None
            return getSinglePasswd(self.user)

    def userdel(self, execute=False, adminOK=False):
        user = self.user
        pw = getSinglePasswd(user)
        if not pw:
            self.error = 'userdel: No User >%s<' % user
            return None
        else:
            if not adminOK and pw.is_admin:
                self.error = 'userdel: Cannot delete admin user >%s<' % user
                return None
            self.error = ''
            self.cmd = '/usr/sbin/userdel -r 2>/dev/null ' + user
            if self._runcmd(execute, 'userdel', self.cmd):
                return None
            return pw

    def userEnableDisable(self, action, execute=False, adminOK=False):
        """Enable by removing leading '*' from encrypted password"""
        if action not in (ENABLE, DISABLE):
            self.error = 'userEnableDisable: invalid action = %s' % action
            return None
        else:
            user = self.user
            pw = getSinglePasswd(user)
            if not pw:
                self.error = 'userenable: No User >%s<' % user
                return None
            if not adminOK and pw.is_admin:
                self.error = 'userenable: Cannot enable admin user >%s<' % user
                return None
            self.error = ''
            pwd = pw.pwd
            if action == ENABLE and pwd.startswith('*'):
                pwd = pwd[1:]
            elif action == DISABLE and not pwd.startswith('*'):
                pwd = '*' + pwd
            if pwd != pw.pwd:
                pw.pwd = pwd
                self.cmd = cmd = '/usr/sbin/usermod -p %s %s' % (repr(pwd), user)
                if self._runcmd(execute, 'userEnableDisable', cmd):
                    return None
                getSinglePasswd(self.user)
            return pw

    def userenable(self, execute=False, adminOK=False):
        return self.userEnableDisable(ENABLE, execute, adminOK)

    def userdisable(self, execute=False, adminOK=False):
        return self.userEnableDisable(DISABLE, execute, adminOK)

    def userupdate(self, action, execute=False, adminOK=False):
        """Select the appropriate function based on action"""
        self.action = action
        if action == MODIFY:
            pw = self.usermod(execute, adminOK)
        elif action == ADD:
            pw = self.useradd(execute, adminOK)
        elif action == DELETE:
            pw = self.userdel(execute, adminOK)
        elif action == ENABLE:
            pw = self.userenable(execute, adminOK)
        elif action == DISABLE:
            pw = self.userdisable(execute, adminOK)
        else:
            pw = None
        return pw


class Group(Csys.CSClass):
    _attributes = dict(gname='', pwd='x', gid=100, members=set(), _seq=0)
    _groupSeq = 0

    @classmethod
    def groupSeq(klass):
        return klass._groupSeq

    @classmethod
    def setGroupSeq(klass, val):
        klass._groupSeq = int(val)

    _maxGid = 0

    @classmethod
    def maxGid(klass):
        return klass._maxGid

    @classmethod
    def setMaxGid(klass, val):
        klass._maxGid = int(val)

    def __init__(self, line=None, **kwargs):
        if line:
            kwargs = dict(zip(('gname', 'pwd', 'gid', 'members'), line.strip().split(':')))
        kwargs['gid'] = int(kwargs.get('gid') or 100)
        kwargs['members'] = set(Csys.COMMA_SPACES.split(kwargs.get('members', '')))
        Csys.CSClass.__init__(self, True, **kwargs)
        Group._groupSeq += 1
        if self.gid not in skipNoUserGids:
            Group._maxGid = max(Group._maxGid, self.gid)
        self._seq = Group._groupSeq

    @classmethod
    def readGroupFile(klass, groupFile=None, **kwargs):
        """Read group file or open file handle"""
        kw = Csys.KWArgs(_read_passwd_shadow_opts, **kwargs)
        groupFile = groupFile or kw.group or '/etc/group'
        hostname = kw.hostname
        if hostname != myHostname:
            groupFile = '%s:%s' % (hostname, groupFile)
        if hasattr(groupFile, '__iter__'):
            fhinput = groupfile
        else:
            if groupFile.find(':') != -1:
                host, fname = groupFile.split(':', 1)
                cmd = 'ssh %s cat %s' % (host, fname)
                fhinput = Csys.popen(cmd)
            else:
                fhinput = open(groupFile)
            groupsDicts = Csys.CSClassDict(dict(groupsByName={}, groupsByGid={}))
            for line in fhinput:
                group = klass(line)
                groupsDicts.groupsByName[group.gname] = group
                groupsDicts.groupsByGid[group.gid] = group

        return groupsDicts

    def __cmp__(self, othr):
        return cmp(self._seq, othr._seq)

    def __str__(self):
        s = (':').join((
         self.gname,
         self.pwd,
         str(self.gid),
         (',').join(sorted(self.members))))
        return s

    def addMember(self, username):
        """Add user to members using sets automatically takes care of
                possible duplicates"""
        self.members.add(username)

    def delMember(self, username):
        """Remove user from members"""
        self.members.discard(username)


readGroupFile = Group.readGroupFile
groupSeq = Group.groupSeq
setGroupSeq = Group.setGroupSeq
maxGid = Group.maxGid
setMaxGid = Group.setMaxGid

def writeGroupFile(groups, fname='/etc/group.new', force=False):
    """Write new group file from dictionary containing members
        of the Group Class or from a list of Groups"""
    if hasattr(groups, 'values'):
        groups = sorted(groups.values())
    if os.path.exists(fname) and not force:
        raise Error('%s exists' % fname)
    fhout = Csys.openOut(fname, mode=420)
    for group in groups:
        fhout.write('%s\n' % group)

    fhout.close()


if __name__ == '__main__':
    print 'OK'
    groupDicts = readGroupFile()
    groups = sorted(groupDicts.groupsByName.values())
    for group in groups:
        print str(group)

    accts = read_passwd_shadow(None, '/dev/null').accts
    gidMap = groupDicts.groupsByGid
    sys.exit(0)
    print OSTable.useradd_fmt
    t = UserAddMod('testuser', shell='shell')
    print 'home=>%s< shell=>%s<' % (t.home, t.shell)
    print getpwnam('bill')