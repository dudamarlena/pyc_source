# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/authkit/users/postgresql_driver.py
# Compiled at: 2009-10-05 09:07:44
"""An SQLAlchemy driver for Pylons when used directly with PostgreSQL.
"""
import datetime
from authkit.users import *
from paste.util.import_string import eval_import

class UsersDriver(Users):
    """
    Raw SQL Version
    """
    api_version = 0.4

    def __init__(self, environ, data, encrypt=None):
        if encrypt is None:

            def encrypt(password):
                return password

        self.encrypt = encrypt
        if isinstance(data, (str, unicode)):
            data_parts = data.split('\n')
            data = []
            if len(data_parts) == 2:
                data.append(eval_import(data_parts[0].strip()))
                data.append(eval_import(data_parts[1].strip()))
            else:
                raise AuthKitError('Expected two lines in the user configuration, not %s' % len(data_parts))
        (self.get_conn, self.release_conn) = data
        self.environ = environ
        return

    def create_tables(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            -- DROP TABLE groups;\n            -- DROP TABLE roles;\n            -- DROP TABLE users;\n            -- DROP TABLE users_roles;\n\n            CREATE TABLE groups (\n                uid serial UNIQUE NOT NULL,\n                name character varying(255) UNIQUE NOT NULL\n            );\n            \n            CREATE TABLE roles (\n                uid serial UNIQUE NOT NULL,\n                name character varying(255) UNIQUE NOT NULL\n            );\n            \n            CREATE TABLE users (\n                uid serial UNIQUE NOT NULL,\n                username character varying(255) UNIQUE NOT NULL,\n                password character varying(255) NOT NULL,\n                group_uid integer REFERENCES groups (uid) \n            );\n            \n            CREATE TABLE users_roles (\n                uid serial UNIQUE NOT NULL,\n                user_uid integer REFERENCES users (uid),\n                role_uid integer REFERENCES roles (uid)\n            );\n\n        ')
        conn.commit()
        cursor.close()
        self.release_conn(conn)

    def user_create(self, username, password, group=None):
        """
        Create a new user with the username, password and group name specified.
        """
        if ' ' in username:
            raise AuthKitError('Usernames cannot contain space characters')
        if self.user_exists(username):
            raise AuthKitError('User %r already exists' % username)
        if group is not None and not self.group_exists(group):
            raise AuthKitNoSuchGroupError('There is no such group %r' % group)
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT uid FROM groups WHERE name=%s\n            ', (
         group.lower(),))
        group_uid = cursor.fetchall()[0][0]
        cursor.execute('\n            INSERT INTO users (username, password, group_uid) VALUES (%s, %s, %s)\n            ', (
         username, self.encrypt(password), group_uid))
        conn.commit()
        cursor.close()
        self.release_conn(conn)
        return

    def role_create(self, role):
        """
        Add a new role to the system
        """
        if ' ' in role:
            raise AuthKitError('Roles cannot contain space characters')
        if self.role_exists(role):
            raise AuthKitError('Role %r already exists' % role)
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            INSERT INTO roles (name) VALUES (%s)\n            ', (
         role.lower(),))
        conn.commit()
        cursor.close()
        self.release_conn(conn)

    def group_create(self, group):
        """
        Add a new group to the system
        """
        if ' ' in group:
            raise AuthKitError('Groups cannot contain space characters')
        if self.group_exists(group):
            raise AuthKitError('Group %r already exists' % group)
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            INSERT INTO groups (name) VALUES (%s)\n            ', (
         group.lower(),))
        conn.commit()
        cursor.close()
        self.release_conn(conn)

    def user_delete(self, username):
        """
        Remove the user with the specified username 
        """
        if not self.user_exists(username.lower()):
            raise AuthKitError('There is no such user %r' % username)
        else:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute('\n                DELETE FROM users WHERE username=%s\n                ', (
             username.lower(),))
            conn.commit()
            cursor.close()
            self.release_conn(conn)

    def role_delete(self, role):
        """
        Remove the role specified. Rasies an exception if the role is still in use. 
        To delete the role and remove it from all existing users use 
        ``role_delete_cascade()``
        """
        if not self.role_exists(role.lower()):
            raise AuthKitError('There is no such role %r' % role)
        else:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute('\n                SELECT count(name) FROM users_roles\n                LEFT OUTER JOIN roles ON users_roles.role_uid = roles.uid\n                WHERE roles.name=%s\n                ', (
             role.lower(),))
            if cursor.fetchall()[0][0] > 0:
                raise AuthKitError('The role is still being used and therefore cannot be deleted' % role.lower())
            cursor.execute('\n                DELETE FROM roles WHERE name=%s\n                ', (
             role.lower(),))
            conn.commit()
            cursor.close()
            self.release_conn(conn)

    def group_delete(self, group):
        """
        Remove the group specified. Rasies an exception if the group is still in use. 
        To delete the group and remove it from all existing users use ``group_delete_cascade()``
        """
        if not self.group_exists(group.lower()):
            raise AuthKitError('There is no such group %r' % group)
        else:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute('\n                SELECT count(group_uid) FROM users\n                LEFT OUTER JOIN groups ON users.group_uid = groups.uid\n                WHERE groups.name=%s\n                ', (
             group.lower(),))
            if cursor.fetchall()[0][0] > 0:
                raise AuthKitError('The group %r is still being used and therefore cannot be deleted' % group.lower())
            cursor.execute('\n                DELETE FROM groups WHERE name=%s\n                ', (
             group.lower(),))
            conn.commit()
            cursor.close()
            self.release_conn(conn)

    def user_exists(self, username):
        """
        Returns ``True`` if a user exists with the given username, ``False`` 
        otherwise. Usernames are case insensitive.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT count(username) FROM users WHERE username=%s\n            ', (
         username.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0] > 0

    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are
        case insensitive.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT count(name) FROM roles WHERE name=%s\n            ', (
         role.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0] > 0

    def group_exists(self, group):
        """
        Returns ``True`` if the group exists, ``False`` otherwise. Groups 
        are case insensitive.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT count(name) FROM groups WHERE name=%s\n            ', (
         group.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0] > 0

    def list_roles(self):
        """
        Returns a lowercase list of all roll names ordered alphabetically
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT name FROM roles ORDER BY name\n            ')
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return [ row[0] for row in rows ]

    def list_users(self):
        """
        Returns a lowecase list of all usernames ordered alphabetically
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT username FROM users ORDER BY username\n            ')
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return [ row[0] for row in rows ]

    def list_groups(self):
        """
        Returns a lowercase list of all groups ordered alphabetically
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT name FROM groups ORDER BY name\n            ')
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return [ row[0] for row in rows ]

    def user(self, username):
        """
        Returns a dictionary in the following format:

        .. code-block :: Python
        
            {
                'username': username,
                'group':    group,
                'password': password,
                'roles':    [role1,role2,role3... etc]
            }

        Role names are ordered alphabetically
        Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT username, name, password FROM users \n            LEFT OUTER JOIN groups on users.group_uid=groups.uid\n            WHERE users.username=%s\n            ORDER BY username\n            ', (
         username.lower(),))
        rows = cursor.fetchall()[0]
        cursor.close()
        self.release_conn(conn)
        return {'username': rows[0], 
           'group': rows[1], 
           'password': rows[2], 
           'roles': self.user_roles(username)}

    def user_roles(self, username):
        """
        Returns a list of all the role names for the given username ordered 
        alphabetically. Raises an exception if the username doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT roles.name FROM users_roles\n            JOIN users on users.uid = users_roles.user_uid\n            JOIN roles on users_roles.role_uid = roles.uid\n            WHERE users.username=%s\n            ORDER BY roles.name\n            ', (
         username.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return [ x[0] for x in rows ]

    def user_group(self, username):
        """
        Returns the group associated with the user or ``None`` if no group is
        associated. Raises an exception is the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT groups.name FROM groups\n            LEFT OUTER JOIN users on users.group_uid = groups.uid\n            WHERE users.username=%s\n            ORDER BY groups.name\n            ', (
         username.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0]

    def user_password(self, username):
        """
        Returns the password associated with the user or ``None`` if no
        password exists. Raises an exception is the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT password FROM users\n            WHERE username=%s\n            ', (
         username.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0]

    def user_has_role(self, username, role):
        """
        Returns ``True`` if the user has the role specified, ``False`` 
        otherwise. Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        if not self.role_exists(role.lower()):
            raise AuthKitNoSuchRoleError('No such role %r' % role.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT count(users_roles.role_uid) FROM users_roles \n            LEFT OUTER JOIN users on users.uid = users_roles.user_uid\n            LEFT OUTER JOIN roles on users_roles.role_uid = roles.uid\n            WHERE roles.name=%s and users.username = %s\n            ', (
         role.lower(), username.lower()))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0] > 0

    def user_has_group(self, username, group):
        """
        Returns ``True`` if the user has the group specified, ``False`` 
        otherwise. The value for ``group`` can be ``None`` to test that 
        the user doesn't belong to a group. Raises an exception if the 
        user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        if group is not None and not self.group_exists(group.lower()):
            raise AuthKitNoSuchGroupError('No such group %r' % group.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT groups.name FROM users \n            LEFT OUTER JOIN groups on users.group_uid = groups.uid\n            WHERE groups.name=%s and users.username = %s\n            ', (
         group.lower(), username.lower()))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        if rows:
            group_ = rows[0][0]
        else:
            return False
        if group is None:
            if group_ == None:
                return True
        elif group is not None and group_ == group.lower():
            return True
        return False

    def user_has_password(self, username, password):
        """
        Returns ``True`` if the user has the password specified, ``False`` 
        otherwise. Passwords are case sensitive. Raises an exception if the
        user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT password FROM users \n            WHERE username = %s\n            ', (
         username.lower(),))
        rows = cursor.fetchall()
        cursor.close()
        self.release_conn(conn)
        return rows[0][0] == self.encrypt(password)

    def user_set_username(self, username, new_username):
        """
        Sets the user's username to the lowercase of new_username. 
        Raises an exception if the user doesn't exist or if there is already
        a user with the username specified by ``new_username``.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        if self.user_exists(new_username.lower()):
            raise AuthKitError('A user with the username %r already exists' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            UPDATE users SET username=%s WHERE username=%s \n            ', (
         new_username.lower(), username.lower()))
        cursor.close()
        conn.commit()
        self.release_conn(conn)

    def user_set_password(self, username, new_password):
        """
        Sets the user's password. Should be plain text, will be encrypted using self.encrypt
        Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            UPDATE users SET password=%s WHERE username=%s \n            ', (
         self.encrypt(new_password), username.lower()))
        cursor.close()
        conn.commit()
        self.release_conn(conn)

    def user_set_group(self, username, group, auto_add_group=False):
        """
        Sets the user's group to the lowercase of ``group`` or ``None``. If
        the group doesn't exist and ``add_if_necessary`` is ``True`` the 
        group will also be added. Otherwise an ``AuthKitNoSuchGroupError`` 
        will be raised. Raises an exception if the user doesn't exist.
        """
        if group is None:
            return self.user_remove_group(username)
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        if not self.group_exists(group.lower()):
            if auto_add_group:
                self.group_create(group.lower())
            else:
                raise AuthKitNoSuchGroupError('No such group %r' % group.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT uid FROM groups WHERE name=%s \n            ', (
         group.lower(),))
        group_uid = cursor.fetchall()[0][0]
        cursor.execute('\n            UPDATE users SET group_uid=%s WHERE username=%s \n            ', (
         group_uid, username.lower()))
        cursor.close()
        conn.commit()
        self.release_conn(conn)
        return

    def user_add_role(self, username, role, auto_add_role=False):
        """
        Sets the user's role to the lowercase of ``role``. If the role doesn't
        exist and ``add_if_necessary`` is ``True`` the role will also be
        added. Otherwise an ``AuthKitNoSuchRoleError`` will be raised. Raises
        an exception if the user doesn't exist.
        """
        if self.user_has_role(username, role):
            return
        if not self.role_exists(role.lower()):
            if auto_add_role:
                self.role_create(role.lower())
            else:
                raise AuthKitNoSuchRoleError('No such role %r' % role.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT uid FROM users WHERE username=%s \n            ', (
         username.lower(),))
        user_uid = cursor.fetchall()[0][0]
        cursor.execute('\n            SELECT uid FROM roles WHERE name=%s \n            ', (
         role.lower(),))
        role_uid = cursor.fetchall()[0][0]
        cursor.execute('\n            INSERT INTO users_roles (user_uid, role_uid) VALUES (%s, %s); \n            ', (
         user_uid, role_uid))
        cursor.close()
        conn.commit()
        self.release_conn(conn)

    def user_remove_role(self, username, role):
        """
        Removes the role from the user specified by ``username``. Raises 
        an exception if the user doesn't exist.
        """
        if not self.user_has_role(username, role):
            raise AuthKitError('No role %r found for user %r' % (role.lower(), username.lower()))
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            SELECT uid FROM users WHERE username=%s \n            ', (
         username.lower(),))
        user_uid = cursor.fetchall()[0][0]
        cursor.execute('\n            SELECT uid FROM roles WHERE name=%s \n            ', (
         role.lower(),))
        role_uid = cursor.fetchall()[0][0]
        cursor.execute('\n            DELETE FROM users_roles WHERE user_uid=%s and role_uid=%s; \n            ', (
         user_uid, role_uid))
        cursor.close()
        conn.commit()
        self.release_conn(conn)

    def user_remove_group(self, username):
        """
        Sets the group to ``None`` for the user specified by ``username``.
        Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError('No such user %r' % username.lower())
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute('\n            UPDATE users SET group_uid=%s WHERE username=%s \n            ', (
         None, username.lower()))
        cursor.close()
        conn.commit()
        self.release_conn(conn)
        return