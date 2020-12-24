# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/user_management.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 3861 bytes


class UserManagement(object):

    def info_user(self, username):
        ret = self.command('userManager.cgi?action=getUserInfo&name={0}'.format(username))
        return ret.content.decode('utf-8')

    @property
    def info_all_users(self):
        ret = self.command('userManager.cgi?action=getUserInfoAll')
        return ret.content.decode('utf-8')

    @property
    def info_all_active_users(self):
        ret = self.command('userManager.cgi?action=getActiveUserInfoAll')
        return ret.content.decode('utf-8')

    def info_group(self, group):
        ret = self.command('userManager.cgi?action=getGroupInfo&name={0}'.format(group))
        return ret.content.decode('utf-8')

    @property
    def info_all_groups(self):
        ret = self.command('userManager.cgi?action=getGroupInfoAll')
        return ret.content.decode('utf-8')

    def delete_user(self, username):
        ret = self.command('userManager.cgi?action=deleteUser&name={0}'.format(username))
        return ret.content.decode('utf-8')

    def add_user(self, username, password, group, sharable=True, reserved=False, memo=None):
        """
        Params:
            username - username for user
            password - password for user
            group - string the range is "admin" and "user". In different group,
                    the user has different authorities.

            sharable - bool, true means allow multi-point login

            reserved - bool, true means this user can't be deleted

            memo - memo to user
        """
        cmd = 'userManager.cgi?action=addUser&user.Name={0}&user.Password={1}&user.Group={2}&user.Sharable={3}&user.Reserved={4}'.format(username, password, group.lower(), sharable.lower(), reserved.lower())
        if memo:
            cmd += '&user.Memo=%s' % memo
        ret = self.command(cmd)
        return ret.content.decode('utf-8')

    def modify_password(self, username, newpwd, oldpwd):
        """
        Params:
            username - user name
            newpwd - new password
            oldpwd - old password
        """
        ret = self.command('userManager.cgi?action=modifyPassword&name={0}&pwd={1}&pwdOld={2}'.format(username, newpwd, oldpwd))
        return ret.content.decode('utf-8')

    def modify_user(self, username, attribute, value):
        """
        Params:
            username - username for user
            attribute - the attribute name that will change:
                        group, sharable, reserved, memo

            value - the new value for attribute
        """
        cmd = 'userManager.cgi?action=modifyUser&name={0}'.format(username)
        if attribute.lower() == 'group':
            cmd += '&user.Group=%s' % value.lower()
        else:
            if attribute.lower() == 'sharable':
                cmd += '&user.Sharable=%s' % value.lower()
            else:
                if attribute.lower() == 'reserved':
                    cmd += '&user.Reserved=%s' % value.lower()
                else:
                    if attribute == 'memo':
                        cmd += '&user.Memo=%s' % value.lower()
        ret = self.command(cmd)
        return ret.content.decode('utf-8')