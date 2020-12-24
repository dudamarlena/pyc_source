# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/mkUserRsyncConfs.py
# Compiled at: 2009-11-24 20:44:53
import Csys, os, os.path, sys, re
__doc__ = 'Utility to create rsyncd.conf entries for users\n\nusage: %s [username]' % Csys.Config.progname
__doc__ += '\n\n$Id: mkUserRsyncConfs.py,v 1.1 2009/11/25 01:44:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]
allowedCidrs = [
 '192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12']
rsyncFmt = ('\n[%(user)s_upd]\n\tuid = %(user)s\n\tgid = %(gid)s\n\tread only = false\n\t# use chroot = false\n\tpath = %(home)s\n\tcomment = %(home)s\n\thosts allow = %(cidrblocks)s\n\thosts deny = *\n\tlist = no\n').lstrip()
if __name__ == '__main__':

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        return parser


    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    Csys.getoptionsEnvironment(options)
    from Csys.Passwd import read_passwd_shadow
    import Csys.Admin.network, grp
    netcfg = Csys.Admin.network.Config()
    accts = read_passwd_shadow().accts
    users = [ pw.user for pw in accts.values() if not pw.is_admin ]
    if not args:
        args = users
    args.sort()
    if netcfg.publiccidr not in allowedCidrs:
        allowedCidrs.insert(0, netcfg.publiccidr)
    cidrblocks = (', ').join(allowedCidrs)
    rsyncConfigs = {}
    for user in args:
        pw = accts[user]
        home = pw.home
        if home not in rsyncConfigs:
            rsyncConfigs[home] = True
            pw.cidrblocks = cidrblocks
            pw.__dict__['gid'] = grp.getgrgid(pw.gid)[0]
            print rsyncFmt % pw.__dict__