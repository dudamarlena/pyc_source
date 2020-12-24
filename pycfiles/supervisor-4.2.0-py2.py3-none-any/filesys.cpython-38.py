# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/filesys.py
# Compiled at: 2019-09-16 13:23:31
# Size of source mod 2**32: 11368 bytes
from supervisor.compat import long

class abstract_filesystem:

    def __init__(self):
        pass

    def current_directory(self):
        """Return a string representing the current directory."""
        pass

    def listdir(self, path, long=0):
        """Return a listing of the directory at 'path' The empty string
        indicates the current directory.  If 'long' is set, instead
        return a list of (name, stat_info) tuples
        """
        pass

    def open(self, path, mode):
        """Return an open file object"""
        pass

    def stat(self, path):
        """Return the equivalent of os.stat() on the given path."""
        pass

    def isdir(self, path):
        """Does the path represent a directory?"""
        pass

    def isfile(self, path):
        """Does the path represent a plain file?"""
        pass

    def cwd(self, path):
        """Change the working directory."""
        pass

    def cdup(self):
        """Change to the parent of the current directory."""
        pass

    def longify(self, path):
        """Return a 'long' representation of the filename
        [for the output of the LIST command]"""
        pass


import os, stat, re

def safe_stat--- This code section failed: ---

 L.  79         0  SETUP_FINALLY        18  'to 18'

 L.  80         2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              os
                6  LOAD_METHOD              stat
                8  LOAD_FAST                'path'
               10  CALL_METHOD_1         1  ''
               12  BUILD_TUPLE_2         2 
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  81        18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  82        24  POP_EXCEPT       
               26  LOAD_CONST               None
               28  RETURN_VALUE     
               30  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 24


class os_filesystem:
    path_module = os.path
    do_globbing = 1

    def __init__(self, root, wd='/'):
        self.root = root
        self.wd = wd

    def current_directory(self):
        return self.wd

    def isfile(self, path):
        p = self.normalizeself.path_module.join(self.wd, path)
        return self.path_module.isfileself.translatep

    def isdir(self, path):
        p = self.normalizeself.path_module.join(self.wd, path)
        return self.path_module.isdirself.translatep

    def cwd(self, path):
        p = self.normalizeself.path_module.join(self.wd, path)
        translated_path = self.translatep
        if not self.path_module.isdirtranslated_path:
            return 0
        old_dir = os.getcwd()
        can = 0
        try:
            try:
                os.chdirtranslated_path
                can = 1
                self.wd = p
            except:
                pass

        finally:
            if can:
                os.chdirold_dir

        return can

    def cdup(self):
        return self.cwd'..'

    def listdir(self, path, long=0):
        p = self.translatepath
        ld = os.listdirp
        if not long:
            return list_producer(ld, None)
        old_dir = os.getcwd()
        try:
            os.chdirp
            result = [_f for _f in map(safe_stat, ld) if _f]
        finally:
            os.chdirold_dir

        return list_producer(result, self.longify)

    def stat(self, path):
        p = self.translatepath
        return os.statp

    def open(self, path, mode):
        p = self.translatepath
        return open(p, mode)

    def unlink(self, path):
        p = self.translatepath
        return os.unlinkp

    def mkdir(self, path):
        p = self.translatepath
        return os.mkdirp

    def rmdir(self, path):
        p = self.translatepath
        return os.rmdirp

    def rename(self, src, dst):
        return os.rename(self.translatesrc, self.translatedst)

    def normalize(self, path):
        path = re.sub('/+', '/', path)
        p = self.path_module.normpathpath
        if len(p) > 2:
            if p[:3] == '/..':
                p = '/'
        return p

    def translate(self, path):
        path = os.sep.joinpath.split'/'
        p = self.normalizeself.path_module.join(self.wd, path)
        p = self.normalizeself.path_module.join(self.root, p[1:])
        return p

    def longify(self, path_stat_info_tuple):
        path, stat_info = path_stat_info_tuple
        return unix_longify(path, stat_info)

    def __repr__(self):
        return '<unix-style fs root:%s wd:%s>' % (
         self.root,
         self.wd)


if os.name == 'posix':

    class unix_filesystem(os_filesystem):
        pass


    class schizophrenic_unix_filesystem(os_filesystem):
        PROCESS_UID = os.getuid()
        PROCESS_EUID = os.geteuid()
        PROCESS_GID = os.getgid()
        PROCESS_EGID = os.getegid()

        def __init__(self, root, wd='/', persona=(None, None)):
            os_filesystem.__init__(self, root, wd)
            self.persona = persona

        def become_persona(self):
            if self.persona != (None, None):
                uid, gid = self.persona
                os.setegidgid
                os.seteuiduid

        def become_nobody(self):
            if self.persona != (None, None):
                os.seteuidself.PROCESS_UID
                os.setegidself.PROCESS_GID

        def cwd--- This code section failed: ---

 L. 231         0  SETUP_FINALLY        26  'to 26'

 L. 232         2  LOAD_FAST                'self'
                4  LOAD_METHOD              become_persona
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 233        10  LOAD_GLOBAL              os_filesystem
               12  LOAD_METHOD              cwd
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'path'
               18  CALL_METHOD_2         2  ''
               20  POP_BLOCK        
               22  CALL_FINALLY         26  'to 26'
               24  RETURN_VALUE     
             26_0  COME_FROM            22  '22'
             26_1  COME_FROM_FINALLY     0  '0'

 L. 235        26  LOAD_FAST                'self'
               28  LOAD_METHOD              become_nobody
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          
               34  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 22

        def cdup--- This code section failed: ---

 L. 238         0  SETUP_FINALLY        24  'to 24'

 L. 239         2  LOAD_FAST                'self'
                4  LOAD_METHOD              become_persona
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 240        10  LOAD_GLOBAL              os_filesystem
               12  LOAD_METHOD              cdup
               14  LOAD_FAST                'self'
               16  CALL_METHOD_1         1  ''
               18  POP_BLOCK        
               20  CALL_FINALLY         24  'to 24'
               22  RETURN_VALUE     
             24_0  COME_FROM            20  '20'
             24_1  COME_FROM_FINALLY     0  '0'

 L. 242        24  LOAD_FAST                'self'
               26  LOAD_METHOD              become_nobody
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          
               32  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 20

        def open--- This code section failed: ---

 L. 245         0  SETUP_FINALLY        28  'to 28'

 L. 246         2  LOAD_FAST                'self'
                4  LOAD_METHOD              become_persona
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 247        10  LOAD_GLOBAL              os_filesystem
               12  LOAD_METHOD              open
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'filename'
               18  LOAD_FAST                'mode'
               20  CALL_METHOD_3         3  ''
               22  POP_BLOCK        
               24  CALL_FINALLY         28  'to 28'
               26  RETURN_VALUE     
             28_0  COME_FROM            24  '24'
             28_1  COME_FROM_FINALLY     0  '0'

 L. 249        28  LOAD_FAST                'self'
               30  LOAD_METHOD              become_nobody
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          
               36  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 24

        def listdir--- This code section failed: ---

 L. 252         0  SETUP_FINALLY        28  'to 28'

 L. 253         2  LOAD_FAST                'self'
                4  LOAD_METHOD              become_persona
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 254        10  LOAD_GLOBAL              os_filesystem
               12  LOAD_METHOD              listdir
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'path'
               18  LOAD_FAST                'long'
               20  CALL_METHOD_3         3  ''
               22  POP_BLOCK        
               24  CALL_FINALLY         28  'to 28'
               26  RETURN_VALUE     
             28_0  COME_FROM            24  '24'
             28_1  COME_FROM_FINALLY     0  '0'

 L. 256        28  LOAD_FAST                'self'
               30  LOAD_METHOD              become_nobody
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          
               36  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 24


class msdos_filesystem(os_filesystem):

    def longify(self, path_stat_info_tuple):
        path, stat_info = path_stat_info_tuple
        return msdos_longify(path, stat_info)


class merged_filesystem:

    def __init__(self, *fsys):
        pass


def msdos_longify(file, stat_info):
    if stat.S_ISDIRstat_info[stat.ST_MODE]:
        dir = '<DIR>'
    else:
        dir = '     '
    date = msdos_date(stat_info[stat.ST_MTIME])
    return '%s       %s %8d %s' % (
     date,
     dir,
     stat_info[stat.ST_SIZE],
     file)


def msdos_date(t):
    try:
        info = time.gmtimet
    except:
        info = time.gmtime0
    else:
        hour = info[3]
        if hour > 11:
            merid = 'PM'
            hour -= 12
        else:
            merid = 'AM'
        return '%02d-%02d-%02d  %02d:%02d%s' % (
         info[1],
         info[2],
         info[0] % 100,
         hour,
         info[4],
         merid)


months = [
 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mode_table = {'0':'---', 
 '1':'--x', 
 '2':'-w-', 
 '3':'-wx', 
 '4':'r--', 
 '5':'r-x', 
 '6':'rw-', 
 '7':'rwx'}
import time

def unix_longify(file, stat_info):
    mode = ('%o' % stat_info[stat.ST_MODE])[-3:]
    mode = ''.join[mode_table[x] for x in mode]
    if stat.S_ISDIRstat_info[stat.ST_MODE]:
        dirchar = 'd'
    else:
        dirchar = '-'
    date = ls_date(long(time.time()), stat_info[stat.ST_MTIME])
    return '%s%s %3d %-8d %-8d %8d %s %s' % (
     dirchar,
     mode,
     stat_info[stat.ST_NLINK],
     stat_info[stat.ST_UID],
     stat_info[stat.ST_GID],
     stat_info[stat.ST_SIZE],
     date,
     file)


def ls_date(now, t):
    try:
        info = time.gmtimet
    except:
        info = time.gmtime0
    else:
        if now - t > 15600000:
            return '%s %2d  %d' % (
             months[(info[1] - 1)],
             info[2],
             info[0])
        return '%s %2d %02d:%02d' % (
         months[(info[1] - 1)],
         info[2],
         info[3],
         info[4])


class list_producer:

    def __init__(self, list, func=None):
        self.list = list
        self.func = func

    def more(self):
        if not self.list:
            return ''
        bunch = self.list[:50]
        if self.func is not None:
            bunch = map(self.func, bunch)
        self.list = self.list[50:]
        return '\r\n'.joinbunch + '\r\n'