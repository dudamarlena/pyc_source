# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/OPKG.py
# Compiled at: 2005-05-28 00:47:35
__doc__ = 'OpenPKG Utilities\n\n$Id: OPKG.py,v 1.4 2005/05/28 04:47:35 csoftmgr Exp $'
__version__ = '$Revision: 1.4 $'[11:-2]
import os, sys, re, glob, curses
from Csys.Curses import *
import signal
from Csys.SysUtils import l_prefix, which
_rcPrefix = os.path.join(l_prefix, 'etc', 'rc.d') + '/rc.'
_rc_conf = os.path.join(l_prefix, 'etc', 'rc.conf')
_shtool = which('shtool')
_rc = os.path.join(l_prefix, 'etc', 'rc')

def packagesInstalled():
    """List of packages installed"""
    packages = map(lambda s: s.replace(_rcPrefix, ''), glob.glob('%s*' % _rcPrefix))
    packages.sort()
    return packages


_rcVals = {'yes': True, 
   'unknown': None, 
   'no': False}

class runControl:
    """OpenPKG run control"""

    def __init__(self, pkgname):
        """Set base attributes"""
        d = self.__dict__
        d['nameOriginal'] = pkgname
        d['name'] = pkgname.replace('-', '_')
        d['enable'] = True
        d['usable'] = None
        d['active'] = True
        return

    def __str__(self):
        return self.name

    def __setattr__(self, attrname, val):
        """Set Attribute"""
        d = self.__dict__
        if attrname in ('enable', 'usable', 'active'):
            try:
                d[attrname] = _rcVals[val.lower()]
            except KeyError:
                d[attrname] = None

        else:
            d[attrname] = val
        return d[attrname]

    def packageEnable(self):
        """Enable Package (remove pkgname_enable) from rc.conf"""
        if not self.enable:
            cmd = "%s subst -e '/\\b%s_enable\\b/d' %s" % (
             _shtool, self.name, _rc_conf)
            os.system(cmd)
            cmd = '%s %s start 2>/dev/null' % (_rc, self.name)
            os.system(cmd)
            self.rcStart()
        self.__dict__['enable'] = True

    def packageDisable(self):
        """Enable Package (remove pkgname_enable) from rc.conf"""
        if self.enable:
            self.rcStop()
            cmd = '%s %s stop 2>/dev/null' % (_rc, self.name)
            os.system(cmd)
            cmd = "%s subst -e '/\\b%s_enable\\b/d' %s 2>/dev/null" % (
             _shtool, self.name, _rc_conf)
            os.system(cmd)
            cmd = '%s subst -e \'$s/$/\\n\\t%s_enable="no"/\' %s' % (
             _shtool, self.name, _rc_conf)
            os.system(cmd)
        self.__dict__['enable'] = False

    def rcStart(self):
        """Start Package"""
        if self.enable:
            cmd = '%s %s start 2>/dev/null' % (_rc, self.nameOriginal)
            os.system(cmd)

    def rcStop(self):
        """Stop Package"""
        if self.enable:
            cmd = '%s %s stop 2>/dev/null' % (_rc, self.nameOriginal)
            os.system(cmd)

    def rcRestart(self):
        """Restart Package"""
        if self.enable:
            cmd = '%s %s restart 2>/dev/null' % (_rc, self.nameOriginal)
            os.system(cmd)

    def rcReload(self):
        """Reload Package"""
        if self.enable:
            cmd = '%s %s reload 2>/dev/null' % (_rc, self.nameOriginal)
            os.system(cmd)

    def Status(self):
        """Get Status from run control"""
        return packageStatus(pkgname=self.name)


_reEnable = re.compile('(.*)_enable=.(.*).$')
_reUsable = re.compile('(.*)_usable=.(.*).$')
_reActive = re.compile('(.*)_active=.(.*).$')
_packagesInstalled = {}

def _loadPackagesInstalled(force):
    """Load _packagesInstalled dictionary"""
    global _packagesInstalled
    if force or not _packagesInstalled:
        if force:
            _packagesInstalled = []
        packages = packagesInstalled()
        for package in packages:
            p = _packagesInstalled[package] = runControl(package)
            _packagesInstalled[p.name] = p

    try:
        _packagesInstalled.pop('openpkg')
    except:
        pass

    return _packagesInstalled


def packageStatus(force=False, pkgname='all'):
    """Build Run Control Display"""
    _packagesInstalled = _loadPackagesInstalled(force)
    fh = os.popen('%s %s status 2>/dev/null' % (_rc, pkgname))
    for line in fh.readlines():
        try:
            re = _reEnable.match(line)
            if re:
                package, val = _packagesInstalled[re.group(1)], re.group(2)
                package.enable = val
                continue
            re = _reUsable.match(line)
            if re:
                package, val = _packagesInstalled[re.group(1)], re.group(2)
                package.usable = val
                continue
            re = _reActive.match(line)
            if re:
                package, val = _packagesInstalled[re.group(1)], re.group(2)
                package.active = val
                continue
        except:
            pass

    fh.close()
    return _packagesInstalled


def pkgKeys():
    """Return list of original package keys (no ``-'' replacement)"""
    keydict = dict(map(lambda k: (_packagesInstalled[k].nameOriginal, 1), _packagesInstalled.keys()))
    keys = keydict.keys()
    keys.sort()
    return keys


_reConfig = re.compile('^(.*)_([^_\\s]*)\\s+"(.*)"\\s+([=!]=)\\s+"(.*)"$')

def packageConfig(force=False):
    """Get Package enabled status from rc --config command"""
    _packagesInstalled = _loadPackagesInstalled(force)
    fh = os.popen('%s/etc/rc --config status 2>/dev/null' % l_prefix)
    for line in fh.readlines():
        re = _reConfig.search(line.rstrip())
        if re:
            name, action, val1, flag, val2 = re.groups()
            try:
                package = _packagesInstalled[name]
                package.__setattr__(action, val1)
                package.__setattr__('flag', flag)
            except KeyError:
                continue

    fh.close()
    return _packagesInstalled


rcNames = ('active', 'inactive', 'disabled')
column_active, column_inactive, column_disabled = range(3)
rcMenuLines = {}
rcMenus = {}
rcwin = ''
rcWindows = {}
rcPrompts = {'active': (
            UserPrompt('s', '[S]top'),
            UserPrompt('r', '[R]estart'),
            UserPrompt('l', 're[L]oad'),
            UserPrompt('d', '[D]isable'),
            UserPrompt('a', '[A]larm')), 
   'inactive': (
              UserPrompt('s', '[S]tart'),
              UserPrompt('d', '[D]isable'),
              UserPrompt('a', '[A]larm')), 
   'disabled': (
              UserPrompt('e', '[E]nable'),
              UserPrompt('a', '[A]larm'))}
_alarmTime = 0
_newTables = False

def _handleAlarm(signum, frame):
    """Alarm Handler"""
    signal.alarm(0)
    signal.signal(signal.SIGALRM, _handleAlarm)
    _rcBuildTables()


def setAlarm():
    """Prompt and set alarm time to seconds (0) is off"""
    global _alarmTime
    while True:
        s = prompt_getstr('Set Alarm Seconds (30 second minimum, 0 is off)')
        if not s:
            return
        try:
            seconds = int(s)
        except:
            unerrs('Invalid input >%s< % s')
            continue

        if seconds < 0:
            unerrs('Negative time not allowed')
            continue
        if seconds > 0:
            seconds = max(30, seconds)
        _alarmTime = seconds
        break

    leftTitle = ''
    if seconds:
        leftTitle = 'Alarm %s seconds' % seconds
    windows_title_set(currentTitle, left=leftTitle, refresh=True)


def _rcBuildTables(pkgname='all'):
    """Build Run Control Columns"""
    global _newTables
    global rcMenuLines
    global rcMenus
    _newTables = True
    pkgtables = {}
    for name in rcNames:
        table = rcMenuLines[name]
        while table:
            table.pop()

        pkgtables[name] = []

    dsp_prmpt('getting package status info...')
    packages = packageStatus(pkgname=pkgname)
    dsp_prmpt('')
    keys = pkgKeys()
    for key in keys:
        pkg = packages[key]
        if not pkg.enable:
            colname = 'disabled'
        elif pkg.active:
            colname = 'active'
        else:
            colname = 'inactive'
        pkgtables[colname].append(pkg)

    for name in rcNames:
        menuLines = rcMenuLines[name]
        seq = 0
        for pkg in pkgtables[name]:
            menuLines.append(MenuLine(pkg.name, seq, data=pkg))
            seq += 1

    for name in rcNames:
        rcMenus[name].reload()

    signal.signal(signal.SIGALRM, _handleAlarm)


def runcontrol():
    """Build Run Control Display"""
    global _newTables
    global currentTitle
    global rcWindows
    global rcwin
    signal.alarm(0)
    currentTitle = 'OpenPKG Run Control'
    windows_title_set(currentTitle, refresh=True)
    if not rcwin:
        rcwin = curses.newwin(term_lines_avail, term_co, term_firsty, 0)
        max_y, max_x = rcwin.getmaxyx()
        offset = 0
        colwidth = int(max_x / 3)
        for name in rcNames:
            win = rcWindows[name] = rcwin.derwin(max_y, colwidth, 0, offset)
            offset += colwidth
            menuLines = rcMenuLines[name] = []
            rcMenus[name] = MenuScroll('', menuLines, hdrLine=name, border=True, win=win, vcenter=False, userPrompts=rcPrompts[name])

    else:
        try:
            windows_body.remove(rcwin)
        except ValueError:
            pass

        windows_body.append(rcwin)
        rcwin.noutrefresh()
        windows_refresh(redraw=True)
        menus = tuple(map(lambda name: rcMenus[name], rcNames))
        n = len(menus) - 1
        column = 0
        column_motion = 0
        pkgname = 'all'
        while True:
            if pkgname:
                _rcBuildTables(pkgname=pkgname)
            pkgname = None
            column += column_motion
            if column < 0:
                column = n
            else:
                if column > n:
                    column = 0
                menu = menus[column]
                if menu.noEntries <= 0:
                    if column_motion == 0:
                        column_motion = 1
                    continue
                column_motion = 0
                _newTables = False
                signal.alarm(_alarmTime)
                try:
                    rc = menu.getSelection()
                except:
                    continue

            signal.alarm(0)
            line = menu.curmenu
            pkg = line.data
            if isinstance(rc, MenuLine):
                continue
            if rc == 'q' or rc == EXIT_NOW:
                break
            if rc == KEY_TAB:
                column_motion = 1
            elif rc == KEY_BTAB:
                column_motion = -1
            elif rc == 'a':
                setAlarm()
            elif column < column_disabled:
                pkgname = pkg.nameOriginal
                if rc == 'd':
                    if yorn('Disable %s' % pkgname):
                        pkg.packageDisable()
                    continue
                if column == column_active:
                    if rc == 's' and yorn('Stop %s' % pkgname):
                        pkg.rcStop()
                    elif rc == 'r' and yorn('Restart %s' % pkgname):
                        pkg.rcRestart()
                    elif rc == 'l' and yorn('Reload %s' % pkgname):
                        pkg.rcReload()
                    else:
                        pkgname = None
                elif column == column_inactive:
                    if rc == 's' and yorn('Start %s' % pkgname):
                        pkg.rcStart()
                    else:
                        pkgname = None
            elif column == column_disabled:
                pkgname = pkg.nameOriginal
                if rc == 'e' and yorn('Enable %s' % pkgname):
                    pkg.packageEnable()
                else:
                    pkgname = None
            else:
                print 'invalid >%s<' % rc
                curses.beep()

        try:
            windows_body.remove(rcwin)
        except ValueError:
            pass

    signal.alarm(0)
    return


if __name__ == '__main__':
    packages = packageConfig()
    uniq = dict(map(lambda p: (p, 1), map(lambda p: packages[p].nameOriginal, packages.keys())))
    keys = uniq.keys()
    keys.sort()
    csbase = packages['csbase']
    print csbase.enable
    csbase.packageDisable()
    print csbase.enable
    csbase.packageEnable()
    print csbase.enable