# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cstruct/examples/who.py
# Compiled at: 2018-09-18 17:02:25
from cstruct import define, typedef, CStruct
import sys, time
define('UT_NAMESIZE', 32)
define('UT_LINESIZE', 32)
define('UT_HOSTSIZE', 256)
typedef('int', 'pid_t')
typedef('long', 'time_t')

class ExitStatus(CStruct):
    __struct__ = '\n        short   e_termination;      /* Process termination status.  */\n        short   e_exit;             /* Process exit status.  */\n    '


class Timeval(CStruct):
    __struct__ = '\n        int32_t tv_sec;             /* Seconds.  */\n        int32_t tv_usec;            /* Microseconds.  */\n    '


def str_from_c(string):
    return string.decode().split('\x00')[0]


class Utmp(CStruct):
    __struct__ = '\n        short int ut_type;          /* Type of login.  */\n        pid_t ut_pid;               /* Process ID of login process.  */\n        char ut_line[UT_LINESIZE];  /* Devicename.  */\n        char ut_id[4];              /* Inittab ID.  */\n        char ut_user[UT_NAMESIZE];  /* Username.  */\n        char ut_host[UT_HOSTSIZE];  /* Hostname for remote login.  */\n        struct ExitStatus ut_exit;  /* Exit status of a process marked as DEAD_PROCESS.  */\n        int32_t ut_session;         /* Session ID, used for windowing.  */\n        struct Timeval ut_tv;       /* Time entry was made.  */\n        int32_t ut_addr_v6[4];      /* Internet address of remote host.  */\n        char __unused[20];          /* Reserved for future use.  */\n    '

    def print_info(self):
        """andreax  + pts/0        2013-08-21 08:58   .         32341 (l26.box)"""
        print '%-10s %-12s %15s %15s %-8s' % (
         str_from_c(self.ut_user),
         str_from_c(self.ut_line),
         time.strftime('%Y-%m-%d %H:%M', time.gmtime(self.ut_tv.tv_sec)),
         self.ut_pid,
         str_from_c(self.ut_host) and '(%s)' % str_from_c(self.ut_host) or str_from_c(self.ut_id) and 'id=%s' % str_from_c(self.ut_id) or '')


def main():
    utmp = len(sys.argv) > 1 and sys.argv[1] or '/var/run/utmp'
    with open(utmp, 'rb') as (f):
        utmp = Utmp()
        data = f.read(len(utmp))
        while data:
            utmp.unpack(data)
            utmp.print_info()
            data = f.read(len(utmp))


if __name__ == '__main__':
    main()