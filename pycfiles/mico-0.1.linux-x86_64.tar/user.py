# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/lib/core/user.py
# Compiled at: 2013-04-18 09:40:29
"""The user core submodule provide a useful way to create, delete and manage
users in the remote host.
"""
import base64, mico.output
from mico.lib.core.group import group_exists

def user_password(name, password, encrypted_password=False):
    """Sets the given user password.
    """
    encoded_password = base64.b64encode('%s:%s' % (name, password))
    if encrypted_password:
        _x = run("usermod -p '%s' '%s'" % (password, name))
    else:
        _x = run("echo '%s' | openssl base64 -A -d | chpasswd" % encoded_password)
    mico.output.info('set password for user %s' % name)
    return _x


def user_create(name, password=None, home=None, uid=None, gid=None, shell=None, uid_min=None, uid_max=None, encrypted_password=False, fullname=None):
    """Creates the user with the given name, optionally giving a
    specific password/home/uid/gid/shell.
    """
    options = [
     '-m']
    if home:
        options.append("-d '%s'" % home)
    if uid:
        options.append("-u '%s'" % uid)
    if not gid and group_exists(name):
        gid = name
    if gid:
        options.append("-g '%s'" % gid)
    if shell:
        options.append("-s '%s'" % shell)
    if uid_min:
        options.append("-K UID_MIN='%s'" % uid_min)
    if uid_max:
        options.append("-K UID_MAX='%s'" % uid_max)
    if fullname:
        options.append("--gecos='%s'" % fullname)
    _x = run("useradd %s '%s'" % ((' ').join(options), name))
    if password:
        return user_password(name=name, password=password, encrypted_password=encrypted_password)
    else:
        return _x


def user_exists(name=None, uid=None):
    """Checks if there is a user defined with the given name.

    :return: a dictionary with the following fields: name (the name of the
        user), uid (the UID of the user), gid (the GID of the primary group
        of the user), home (the path to home directory) and shell (the shell
        of the user), or None if the user does not exists.
    """
    if name is None and uid is None:
        raise ExecutionError('user_exists require name or uid')
    if name is not None and uid is not None:
        raise ExecutionError('user_exists require name or uid, but not both')
    if name != None:
        d = run("cat /etc/passwd | egrep '^%s:'" % name, force=True)
    else:
        d = run("cat /etc/passwd | egrep '^.*:.*:%s:'" % uid, force=True)
    if not d:
        return False
    else:
        if ':' not in d:
            raise ExecutionError('malformed /etc/passwd, no separator found')
        else:
            d = d.split(':')
            if len(d) < 7:
                raise ExecutionError('malformed /etc/password, 7 fields expected')
            else:
                return dict(zip(('name', 'password', 'uid', 'gid', 'gecos', 'home',
                                 'shell'), d))
        return


def user_ensure(name, password=None, home=None, uid=None, gid=None, shell=None, fullname=None, encrypted_password=False):
    """Ensures that the user exists in the remote host.
    """
    if not user_exists(name):
        return user_create(name, password, home, uid, gid, shell, fullname, encrypted_password)


def user_remove(name, rm_home=False):
    """Removes the user with the given name, optionally
    removing the home directory and mail spool.
    """
    return run("userdel -f %s '%s'" % (rm_home and '-r' or '', name))