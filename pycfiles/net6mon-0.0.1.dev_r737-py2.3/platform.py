# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/platform.py
# Compiled at: 2005-10-31 05:04:30
""" This module tries to retrieve as much platform identifying data as
    possible. It makes this information available via function APIs.

    If called from the command line, it prints the platform
    information concatenated as single string to stdout. The output
    format is useable as part of a filename.

"""
__copyright__ = '\n    Copyright (c) 1999-2000, Marc-Andre Lemburg; mailto:mal@lemburg.com\n    Copyright (c) 2000-2003, eGenix.com Software GmbH; mailto:info@egenix.com\n\n    Permission to use, copy, modify, and distribute this software and its\n    documentation for any purpose and without fee or royalty is hereby granted,\n    provided that the above copyright notice appear in all copies and that\n    both that copyright notice and this permission notice appear in\n    supporting documentation or portions thereof, including modifications,\n    that you make.\n\n    EGENIX.COM SOFTWARE GMBH DISCLAIMS ALL WARRANTIES WITH REGARD TO\n    THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND\n    FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,\n    INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING\n    FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,\n    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION\n    WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !\n\n'
__version__ = '1.0.1'
import sys, string, os, re
_libc_search = re.compile('(__libc_init)|(GLIBC_([0-9.]+))|(libc(_\\w+)?\\.so(?:\\.(\\d[0-9.]*))?)')

def libc_ver(executable=sys.executable, lib='', version='', chunksize=2048):
    """ Tries to determine the libc version against which the
        file executable (defaults to the Python interpreter) is linked.

        Returns a tuple of strings (lib,version) which default to the
        given parameters in case the lookup fails.

        Note that the function has intimate knowledge of how different
        libc versions add symbols to the executable is probably only
        useable for executables compiled using gcc. 

        The file is read and scanned in chunks of chunksize bytes.

    """
    f = open(executable, 'rb')
    binary = f.read(chunksize)
    pos = 0
    while 1:
        m = _libc_search.search(binary, pos)
        if not m:
            binary = f.read(chunksize)
            if not binary:
                break
            pos = 0
            continue
        (libcinit, glibc, glibcversion, so, threads, soversion) = m.groups()
        if libcinit and not lib:
            lib = 'libc'
        elif glibc:
            if lib != 'glibc':
                lib = 'glibc'
                version = glibcversion
            elif glibcversion > version:
                version = glibcversion
        elif so:
            if lib != 'glibc':
                lib = 'libc'
                if soversion > version:
                    version = soversion
                if threads and version[-len(threads):] != threads:
                    version = version + threads
        pos = m.end()

    f.close()
    return (lib, version)


def _dist_try_harder(distname, version, id):
    """ Tries some special tricks to get the distribution 
        information in case the default method fails.

        Currently supports older SuSE Linux, Caldera OpenLinux and
        Slackware Linux distributions.

    """
    if os.path.exists('/var/adm/inst-log/info'):
        info = open('/var/adm/inst-log/info').readlines()
        distname = 'SuSE'
        for line in info:
            tv = string.split(line)
            if len(tv) == 2:
                (tag, value) = tv
            else:
                continue
            if tag == 'MIN_DIST_VERSION':
                version = string.strip(value)
            elif tag == 'DIST_IDENT':
                values = string.split(value, '-')
                id = values[2]

        return (
         distname, version, id)
    if os.path.exists('/etc/.installed'):
        info = open('/etc/.installed').readlines()
        for line in info:
            pkg = string.split(line, '-')
            if len(pkg) >= 2 and pkg[0] == 'OpenLinux':
                return (
                 'OpenLinux', pkg[1], id)

    if os.path.isdir('/usr/lib/setup'):
        verfiles = os.listdir('/usr/lib/setup')
        for n in range(len(verfiles) - 1, -1, -1):
            if verfiles[n][:14] != 'slack-version-':
                del verfiles[n]

        if verfiles:
            verfiles.sort()
            distname = 'slackware'
            version = verfiles[(-1)][14:]
            return (distname, version, id)
    return (
     distname, version, id)


_release_filename = re.compile('(\\w+)[-_](release|version)')
_release_version = re.compile('([\\d.]+)[^(]*(?:\\((.+)\\))?')

def dist(distname='', version='', id='', supported_dists=('SuSE', 'debian', 'redhat', 'mandrake')):
    """ Tries to determine the name of the OS distribution name

        The function first looks for a distribution release file in
        /etc and then reverts to _dist_try_harder() in case no
        suitable files are found.

        Returns a tuple distname,version,id which default to the
        args given as parameters.

    """
    try:
        etc = os.listdir('/etc')
    except os.error:
        return (
         distname, version, id)

    for file in etc:
        m = _release_filename.match(file)
        if m:
            (_distname, dummy) = m.groups()
            if _distname in supported_dists:
                distname = _distname
                break
    else:
        return _dist_try_harder(distname, version, id)

    f = open('/etc/' + file, 'r')
    firstline = f.readline()
    f.close()
    m = _release_version.search(firstline)
    if m:
        (_version, _id) = m.groups()
        if _version:
            version = _version
        if _id:
            id = _id
    else:
        l = string.split(string.strip(firstline))
        if l:
            version = l[0]
            if len(l) > 1:
                id = l[1]
    return (
     distname, version, id)


class _popen:
    """ Fairly portable (alternative) popen implementation.

        This is mostly needed in case os.popen() is not available, or
        doesn't work as advertised, e.g. in Win9X GUI programs like
        PythonWin or IDLE.

        Writing to the pipe is currently not supported.

    """
    __module__ = __name__
    tmpfile = ''
    pipe = None
    bufsize = None
    mode = 'r'

    def __init__(self, cmd, mode='r', bufsize=None):
        if mode != 'r':
            raise ValueError, 'popen()-emulation only supports read mode'
        import tempfile
        self.tmpfile = tmpfile = tempfile.mktemp()
        os.system(cmd + ' > %s' % tmpfile)
        self.pipe = open(tmpfile, 'rb')
        self.bufsize = bufsize
        self.mode = mode

    def read(self):
        return self.pipe.read()

    def readlines(self):
        if self.bufsize is not None:
            return self.pipe.readlines()
        return

    def close(self, remove=os.unlink, error=os.error):
        if self.pipe:
            rc = self.pipe.close()
        else:
            rc = 255
        if self.tmpfile:
            try:
                remove(self.tmpfile)
            except error:
                pass

        return rc

    __del__ = close


def popen(cmd, mode='r', bufsize=None):
    """ Portable popen() interface.
    """
    popen = None
    if os.environ.get('OS', '') == 'Windows_NT':
        try:
            import win32pipe
        except ImportError:
            pass
        else:
            popen = win32pipe.popen
    if popen is None:
        if hasattr(os, 'popen'):
            popen = os.popen
            if sys.platform == 'win32':
                try:
                    popen('')
                except os.error:
                    popen = _popen

        else:
            popen = _popen
    if bufsize is None:
        return popen(cmd, mode)
    else:
        return popen(cmd, mode, bufsize)
    return


def _norm_version(version, build=''):
    """ Normalize the version and build strings and return a sinlge
        vesion string using the format major.minor.build (or patchlevel).
    """
    l = string.split(version, '.')
    if build:
        l.append(build)
    try:
        ints = map(int, l)
    except ValueError:
        strings = l
    else:
        strings = map(str, ints)

    version = string.join(strings[:3], '.')
    return version


_ver_output = re.compile('(?:([\\w ]+) ([\\w.]+) .*Version ([\\d.]+))')

def _syscmd_ver(system='', release='', version='', supported_platforms=('win32', 'win16', 'dos', 'os2')):
    """ Tries to figure out the OS version used and returns
        a tuple (system,release,version).
        
        It uses the "ver" shell command for this which is known
        to exists on Windows, DOS and OS/2. XXX Others too ?

        In case this fails, the given parameters are used as
        defaults.

    """
    if sys.platform not in supported_platforms:
        return (
         system, release, version)
    for cmd in ('ver', 'command /c ver', 'cmd /c ver'):
        try:
            pipe = popen(cmd)
            info = pipe.read()
            if pipe.close():
                raise os.error, 'command failed'
        except os.error, why:
            continue
        except IOError, why:
            continue
        else:
            break
    else:
        return (
         system, release, version)

    info = string.strip(info)
    m = _ver_output.match(info)
    if m:
        (system, release, version) = m.groups()
        if release[(-1)] == '.':
            release = release[:-1]
        if version[(-1)] == '.':
            version = version[:-1]
        version = _norm_version(version)
    return (
     system, release, version)


def _win32_getvalue(key, name, default=''):
    """ Read a value for name from the registry key.

        In case this fails, default is returned.

    """
    from win32api import RegQueryValueEx
    try:
        return RegQueryValueEx(key, name)
    except:
        return default


def win32_ver(release='', version='', csd='', ptype=''):
    """ Get additional version information from the Windows Registry
        and return a tuple (version,csd,ptype) referring to version
        number, CSD level and OS type (multi/single
        processor).

        As a hint: ptype returns 'Uniprocessor Free' on single
        processor NT machines and 'Multiprocessor Free' on multi
        processor machines. The 'Free' refers to the OS version being
        free of debugging code. It could also state 'Checked' which
        means the OS version uses debugging code, i.e. code that
        checks arguments, ranges, etc. (Thomas Heller).

        Note: this functions only works if Mark Hammond's win32
        package is installed and obviously only runs on Win32
        compatible platforms.

    """
    try:
        import win32api
    except ImportError:
        return (
         release, version, csd, ptype)

    from win32api import RegQueryValueEx, RegOpenKeyEx, RegCloseKey, GetVersionEx
    from win32con import HKEY_LOCAL_MACHINE, VER_PLATFORM_WIN32_NT, VER_PLATFORM_WIN32_WINDOWS
    (maj, min, buildno, plat, csd) = GetVersionEx()
    version = '%i.%i.%i' % (maj, min, buildno & 65535)
    if csd[:13] == 'Service Pack ':
        csd = 'SP' + csd[13:]
    if plat == VER_PLATFORM_WIN32_WINDOWS:
        regkey = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion'
        if maj == 4:
            if min == 0:
                release = '95'
            else:
                release = '98'
        elif maj == 5:
            release = '2000'
    elif plat == VER_PLATFORM_WIN32_NT:
        regkey = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
        if maj <= 4:
            release = 'NT'
        elif maj == 5:
            release = '2000'
    else:
        if not release:
            release = '%i.%i' % (maj, min)
        return (
         release, version, csd, ptype)
    try:
        keyCurVer = RegOpenKeyEx(HKEY_LOCAL_MACHINE, regkey)
        RegQueryValueEx(keyCurVer, 'SystemRoot')
    except:
        return (
         release, version, csd, ptype)

    build = _win32_getvalue(keyCurVer, 'CurrentBuildNumber', (
     '', 1))[0]
    ptype = _win32_getvalue(keyCurVer, 'CurrentType', (
     ptype, 1))[0]
    version = _norm_version(version, build)
    RegCloseKey(keyCurVer)
    return (release, version, csd, ptype)


def _mac_ver_lookup(selectors, default=None):
    from gestalt import gestalt
    l = []
    append = l.append
    for selector in selectors:
        try:
            append(gestalt(selector))
        except RuntimeError:
            append(default)

    return l


def _bcd2str(bcd):
    return hex(bcd)[2:]


def mac_ver(release='', versioninfo=('', '', ''), machine=''):
    """ Get MacOS version information and return it as tuple (release,
        versioninfo, machine) with versioninfo being a tuple (version,
        dev_stage, non_release_version).

        Entries which cannot be determined are set to ''. All tuple
        entries are strings.

        Thanks to Mark R. Levinson for mailing documentation links and
        code examples for this function. Documentation for the
        gestalt() API is available online at:

           http://www.rgaros.nl/gestalt/

    """
    try:
        import gestalt
    except ImportError:
        return (
         release, versioninfo, machine)

    (sysv, sysu, sysa) = _mac_ver_lookup(('sysv', 'sysu', 'sysa'))
    if sysv:
        major = (sysv & 65280) >> 8
        minor = (sysv & 240) >> 4
        patch = sysv & 15
        release = '%s.%i.%i' % (_bcd2str(major), minor, patch)
    if sysu:
        major = int((sysu & 4278190080) >> 24)
        minor = (sysu & 15728640) >> 20
        bugfix = (sysu & 983040) >> 16
        stage = (sysu & 65280) >> 8
        nonrel = sysu & 255
        version = '%s.%i.%i' % (_bcd2str(major), minor, bugfix)
        nonrel = _bcd2str(nonrel)
        stage = {32: 'development', 64: 'alpha', 96: 'beta', 128: 'final'}.get(stage, '')
        versioninfo = (
         version, stage, nonrel)
    if sysa:
        machine = {1: '68k', 2: 'PowerPC'}.get(sysa, '')
    return (
     release, versioninfo, machine)


def _java_getprop(self, name, default):
    from java.lang import System
    try:
        return System.getProperty(name)
    except:
        return default


def java_ver(release='', vendor='', vminfo=('', '', ''), osinfo=('', '', '')):
    """ Version interface for JPython.

        Returns a tuple (release,vendor,vminfo,osinfo) with vminfo being
        a tuple (vm_name,vm_release,vm_vendor) and osinfo being a
        tuple (os_name,os_version,os_arch).

        Values which cannot be determined are set to the defaults
        given as parameters (which all default to '').

    """
    try:
        import java.lang
    except ImportError:
        return (
         release, vendor, vminfo, osinfo)

    vendor = _java_getprop('java.vendor', vendor)
    release = _java_getprop('java.version', release)
    (vm_name, vm_release, vm_vendor) = vminfo
    vm_name = _java_getprop('java.vm.name', vm_name)
    vm_vendor = _java_getprop('java.vm.vendor', vm_vendor)
    vm_release = _java_getprop('java.vm.version', vm_release)
    vminfo = (vm_name, vm_release, vm_vendor)
    (os_name, os_version, os_arch) = osinfo
    os_arch = _java_getprop('java.os.arch', os_arch)
    os_name = _java_getprop('java.os.name', os_name)
    os_version = _java_getprop('java.os.version', os_version)
    osinfo = (os_name, os_version, os_arch)
    return (
     release, vendor, vminfo, osinfo)


def system_alias(system, release, version):
    """ Returns (system,release,version) aliased to common
        marketing names used for some systems.

        It also does some reordering of the information in some cases
        where it would otherwise cause confusion.

    """
    if system == 'Rhapsody':
        return (
         'MacOS X Server', system + release, version)
    elif system == 'SunOS':
        if release < '5':
            return (system, release, version)
        l = string.split(release, '.')
        if l:
            try:
                major = int(l[0])
            except ValueError:
                pass
            else:
                major = major - 3
                l[0] = str(major)
                release = string.join(l, '.')
        if release < '6':
            system = 'Solaris'
        else:
            system = 'Solaris'
    elif system == 'IRIX64':
        system = 'IRIX'
        if version:
            version = version + ' (64bit)'
        else:
            version = '64bit'
    elif system in ('win32', 'win16'):
        system = 'Windows'
    return (system, release, version)


def _platform(*args):
    """ Helper to format the platform string in a filename
        compatible format e.g. "system-version-machine".
    """
    platform = string.join(map(string.strip, filter(len, args)), '-')
    replace = string.replace
    platform = replace(platform, ' ', '_')
    platform = replace(platform, '/', '-')
    platform = replace(platform, '\\', '-')
    platform = replace(platform, ':', '-')
    platform = replace(platform, ';', '-')
    platform = replace(platform, '"', '-')
    platform = replace(platform, '(', '-')
    platform = replace(platform, ')', '-')
    platform = replace(platform, 'unknown', '')
    while 1:
        cleaned = replace(platform, '--', '-')
        if cleaned == platform:
            break
        platform = cleaned

    while platform[(-1)] == '-':
        platform = platform[:-1]

    return platform


def _node(default=''):
    """ Helper to determine the node name of this machine.
    """
    try:
        import socket
    except ImportError:
        return default

    try:
        return socket.gethostname()
    except socket.error:
        return default


if not hasattr(os.path, 'abspath'):

    def _abspath(path, isabs=os.path.isabs, join=os.path.join, getcwd=os.getcwd, normpath=os.path.normpath):
        if not isabs(path):
            path = join(getcwd(), path)
        return normpath(path)


else:
    _abspath = os.path.abspath

def _follow_symlinks(filepath):
    """ In case filepath is a symlink, follow it until a
        real file is reached.
    """
    filepath = _abspath(filepath)
    while os.path.islink(filepath):
        filepath = os.path.normpath(os.path.join(filepath, os.readlink(filepath)))

    return filepath


def _syscmd_uname(option, default=''):
    """ Interface to the system's uname command.
    """
    if sys.platform in ('dos', 'win32', 'win16', 'os2'):
        return default
    try:
        f = os.popen('uname %s 2> /dev/null' % option)
    except (AttributeError, os.error):
        return default

    output = string.strip(f.read())
    rc = f.close()
    if not output or rc:
        return default
    else:
        return output


def _syscmd_file(target, default=''):
    """ Interface to the system's file command.

        The function uses the -b option of the file command to have it
        ommit the filename in its output and if possible the -L option
        to have the command follow symlinks. It returns default in
        case the command should fail.

    """
    target = _follow_symlinks(target)
    try:
        f = os.popen('file %s 2> /dev/null' % target)
    except (AttributeError, os.error):
        return default

    output = string.strip(f.read())
    rc = f.close()
    if not output or rc:
        return default
    else:
        return output


_default_architecture = {'win32': ('', 'WindowsPE'), 'win16': ('', 'Windows'), 'dos': ('', 'MSDOS')}
_architecture_split = re.compile('[\\s,]').split

def architecture(executable=sys.executable, bits='', linkage=''):
    """ Queries the given executable (defaults to the Python interpreter
        binary) for various architecture informations.

        Returns a tuple (bits,linkage) which contain information about
        the bit architecture and the linkage format used for the
        executable. Both values are returned as strings.

        Values that cannot be determined are returned as given by the
        parameter presets. If bits is given as '', the sizeof(pointer)
        (or sizeof(long) on Python version < 1.5.2) is used as
        indicator for the supported pointer size.

        The function relies on the system's "file" command to do the
        actual work. This is available on most if not all Unix
        platforms. On some non-Unix platforms and then only if the
        executable points to the Python interpreter defaults from
        _default_architecture are used.

    """
    if not bits:
        import struct
        try:
            size = struct.calcsize('P')
        except struct.error:
            size = struct.calcsize('l')
        else:
            bits = str(size * 8) + 'bit'
    output = _syscmd_file(executable, '')
    if not output and executable == sys.executable:
        if _default_architecture.has_key(sys.platform):
            (b, l) = _default_architecture[sys.platform]
            if b:
                bits = b
            if l:
                linkage = l
        return (
         bits, linkage)
    fileout = _architecture_split(output)[1:]
    if 'executable' not in fileout:
        return (bits, linkage)
    if '32-bit' in fileout:
        bits = '32bit'
    elif 'N32' in fileout:
        bits = 'n32bit'
    elif '64-bit' in fileout:
        bits = '64bit'
    if 'ELF' in fileout:
        linkage = 'ELF'
    elif 'PE' in fileout:
        if 'Windows' in fileout:
            linkage = 'WindowsPE'
        else:
            linkage = 'PE'
    elif 'COFF' in fileout:
        linkage = 'COFF'
    elif 'MS-DOS' in fileout:
        linkage = 'MSDOS'
    return (
     bits, linkage)


_uname_cache = None

def uname():
    """ Fairly portable uname interface. Returns a tuple
        of strings (system,node,release,version,machine,processor)
        identifying the underlying platform.

        Note that unlike the os.uname function this also returns
        possible processor information as additional tuple entry.

        Entries which cannot be determined are set to ''.

    """
    global _uname_cache
    if _uname_cache is not None:
        return _uname_cache
    try:
        (system, node, release, version, machine) = os.uname()
    except AttributeError:
        system = sys.platform
        release = ''
        version = ''
        node = _node()
        machine = ''
        processor = ''
        use_syscmd_ver = 1
        if system == 'win32':
            (release, version, csd, ptype) = win32_ver()
            if release and version:
                use_syscmd_ver = 0
        if use_syscmd_ver:
            (system, release, version) = _syscmd_ver(system)
        if system in ('win32', 'win16'):
            if not version:
                if system == 'win32':
                    version = '32bit'
                else:
                    version = '16bit'
            system = 'Windows'
        elif system[:4] == 'java':
            (release, vendor, vminfo, osinfo) = java_ver()
            system = 'Java'
            version = string.join(vminfo, ', ')
            if not version:
                version = vendor
        elif os.name == 'mac':
            (release, (version, stage, nonrel), machine) = mac_ver()
            system = 'MacOS'
    else:
        if system == 'OpenVMS':
            if not release or release == '0':
                release = version
                version = ''
            try:
                import vms_lib
            except ImportError:
                pass
            else:
                (csid, cpu_number) = vms_lib.getsyi('SYI$_CPU', 0)
                if cpu_number >= 128:
                    processor = 'Alpha'
                else:
                    processor = 'VAX'
        else:
            processor = _syscmd_uname('-p', '')

    if system == 'unknown':
        system = ''
    if node == 'unknown':
        node = ''
    if release == 'unknown':
        release = ''
    if version == 'unknown':
        version = ''
    if machine == 'unknown':
        machine = ''
    if processor == 'unknown':
        processor = ''
    _uname_cache = (
     system, node, release, version, machine, processor)
    return _uname_cache
    return


def system():
    """ Returns the system/OS name, e.g. 'Linux', 'Windows' or 'Java'.

        An empty string is returned if the value cannot be determined.

    """
    return uname()[0]


def node():
    """ Returns the computer's network name (may not be fully qualified !)

        An empty string is returned if the value cannot be determined.

    """
    return uname()[1]


def release():
    """ Returns the system's release, e.g. '2.2.0' or 'NT'

        An empty string is returned if the value cannot be determined.

    """
    return uname()[2]


def version():
    """ Returns the system's release version, e.g. '#3 on degas'

        An empty string is returned if the value cannot be determined.

    """
    return uname()[3]


def machine():
    """ Returns the machine type, e.g. 'i386'

        An empty string is returned if the value cannot be determined.

    """
    return uname()[4]


def processor():
    """ Returns the (true) processor name, e.g. 'amdk6'

        An empty string is returned if the value cannot be
        determined. Note that many platforms do not provide this
        information or simply return the same value as for machine(),
        e.g.  NetBSD does this.

    """
    return uname()[5]


_sys_version_parser = re.compile('([\\w.+]+)\\s*\\(#(\\d+),\\s*([\\w ]+),\\s*([\\w :]+)\\)\\s*\\[([^\\]]+)\\]?')
_sys_version_cache = None

def _sys_version():
    """ Returns a parsed version of Python's sys.version as tuple
        (version, buildno, builddate, compiler) referring to the Python
        version, build number, build date/time as string and the compiler
        identification string.

        Note that unlike the Python sys.version, the returned value
        for the Python version will always include the patchlevel (it
        defaults to '.0').

    """
    global _sys_version_cache
    import sys, re, time
    if _sys_version_cache is not None:
        return _sys_version_cache
    (version, buildno, builddate, buildtime, compiler) = _sys_version_parser.match(sys.version).groups()
    buildno = int(buildno)
    builddate = builddate + ' ' + buildtime
    l = string.split(version, '.')
    if len(l) == 2:
        l.append('0')
        version = string.join(l, '.')
    _sys_version_cache = (
     version, buildno, builddate, compiler)
    return _sys_version_cache
    return


def python_version():
    """ Returns the Python version as string 'major.minor.patchlevel'

        Note that unlike the Python sys.version, the returned value
        will always include the patchlevel (it defaults to 0).

    """
    return _sys_version()[0]


def python_version_tuple():
    """ Returns the Python version as tuple (major, minor, patchlevel)
        of strings.

        Note that unlike the Python sys.version, the returned value
        will always include the patchlevel (it defaults to 0).

    """
    return string.split(_sys_version()[0], '.')


def python_build():
    """ Returns a tuple (buildno, builddate) stating the Python
        build number and date as strings.

    """
    return _sys_version()[1:3]


def python_compiler():
    """ Returns a string identifying the compiler used for compiling
        Python.

    """
    return _sys_version()[3]


_platform_cache = None
_platform_aliased_cache = None

def platform(aliased=0, terse=0):
    """ Returns a single string identifying the underlying platform
        with as much useful information as possible (but no more :).
        
        The output is intended to be human readable rather than
        machine parseable. It may look different on different
        platforms and this is intended.

        If "aliased" is true, the function will use aliases for
        various platforms that report system names which differ from
        their common names, e.g. SunOS will be reported as
        Solaris. The system_alias() function is used to implement
        this.

        Setting terse to true causes the function to return only the
        absolute minimum information needed to identify the platform.

    """
    global _platform_aliased_cache
    global _platform_cache
    if not aliased and _platform_cache is not None:
        return _platform_cache
    elif _platform_aliased_cache is not None:
        return _platform_aliased_cache
    (system, node, release, version, machine, processor) = uname()
    if machine == processor:
        processor = ''
    if aliased:
        (system, release, version) = system_alias(system, release, version)
    if system == 'Windows':
        (rel, vers, csd, ptype) = win32_ver(version)
        if terse:
            platform = _platform(system, release)
        else:
            platform = _platform(system, release, version, csd)
    elif system in ('Linux',):
        (distname, distversion, distid) = dist('')
        if distname and not terse:
            platform = _platform(system, release, machine, processor, 'with', distname, distversion, distid)
        else:
            (libcname, libcversion) = libc_ver(sys.executable)
            platform = _platform(system, release, machine, processor, 'with', libcname + libcversion)
    elif system == 'Java':
        (r, v, vminfo, (os_name, os_version, os_arch)) = java_ver()
        if terse:
            platform = _platform(system, release, version)
        else:
            platform = _platform(system, release, version, 'on', os_name, os_version, os_arch)
    elif system == 'MacOS':
        if terse:
            platform = _platform(system, release)
        else:
            platform = _platform(system, release, machine)
    elif terse:
        platform = _platform(system, release)
    else:
        (bits, linkage) = architecture(sys.executable)
        platform = _platform(system, release, machine, processor, bits, linkage)
    if aliased:
        _platform_aliased_cache = platform
    elif terse:
        pass
    else:
        _platform_cache = platform
    return platform
    return


if __name__ == '__main__':
    terse = 'terse' in sys.argv or '--terse' in sys.argv
    aliased = not 'nonaliased' in sys.argv and not '--nonaliased' in sys.argv
    print platform(aliased, terse)
    sys.exit(0)