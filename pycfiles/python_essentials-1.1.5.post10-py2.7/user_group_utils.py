# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/user_group_utils.py
# Compiled at: 2014-10-25 21:34:02
import file_line_utils, subprocess, os

def username_by_id(uid):
    if str(type(uid)) != "<type 'int'>":
        raise ValueError('uid has to be an int')
    passwd_lines = file_line_utils.file_lines('/etc/passwd', '#')
    for passwd_line in passwd_lines:
        passwd_line_content = passwd_line.split(':')
        if int(passwd_line_content[2]) == uid:
            return passwd_line_content[0]

    return


def groupname_by_id(gid):
    if str(type(uid)) != "<type 'int'>":
        raise ValueError('uid has to be an int')
    passwd_lines = file_line_utils.file_files('/etc/passwd', '#')
    for passwd_line in passwd_lines:
        passwd_line_content = passwd_line.split(':')
        if passwd_line_content[3] == gid:
            return passwd_line_content[0]

    return


def id_by_username(username):
    if not check_user_exists(username):
        return -1
    ret_value = subprocess.check_output(['id', '-u', username])
    return int(ret_value)


def id_by_groupname(groupname):
    if not check_group_exists(groupname):
        return -1
    else:
        group_lines = file_line_utils.file_lines('/etc/group', comment_symbol='#')
        for group_line in group_lines:
            group_line_content = group_line.split(':')
            if group_line_content[0] == groupname:
                return int(group_line_content[2])

        return


def check_user_exists(username):
    passwd_lines = file_line_utils.file_lines('/etc/passwd', comment_symbol='#')
    for passwd_line in passwd_lines:
        if passwd_line.startswith(username):
            return True

    return False


def check_group_exists(groupname):
    group_lines = file_line_utils.file_lines('/etc/group', comment_symbol='#')
    for group_line in group_lines:
        if group_line.startswith(groupname):
            return True

    return False


def demote_uid(uid):
    return demote_uid_gid(uid, uid)


def demote_uid_gid(uid, gid):

    def ret_value():
        os.setgid(gid)
        os.setuid(uid)

    return ret_value