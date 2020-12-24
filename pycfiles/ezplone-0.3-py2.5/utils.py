# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/ezplone/utils.py
# Compiled at: 2009-04-06 12:06:27
"""
Assorted utilities for working with Plone, mostly from debug prompt.

Note that to sucessfully create content programatically from the debug prompt,
there is a magic preamble that must be called, wrapping the app in a request
and giving you the right permissions::

        from Testing.makerequest import makerequest
        app = makerequest(app)
        from ezplone import utils
        utils.switch_to_admin (app)

"""
__docformat__ = 'restructuredtext en'

def create_obj(par_folder, new_type, new_id, edit={}):
    """
        Creates a new object of the type, edits and returns it.
        
        :Parameters:
                par_folder
                        Folder to create content in.
                new_type : string
                        Name of new object type to create, e.g. 'Document'
                new_id
                        Id to give the new object.
                edit
                        A series of fields and values to change in the new object.
                        
        :Returns:
                The new object.
                        
        Note that 'Pages' are created via 'Document' and that the body of a Page
        is accessed by editing 'text' and 'format' (e.g. 'text/html'). Note also
        that we no checking for id collision.
        
        """
    par_folder.invokeFactory(type_name=new_type, id=new_id)
    new_obj = par_folder[new_id]
    if edit:
        new_obj.edit(**edit)
    new_obj.reindexObject()
    return new_obj


def switch_to_user(app, username):
    """
        Change to this user and their permissions.
        """
    from AccessControl.SecurityManagement import newSecurityManager
    user = context.acl_users.getUserById(username)
    newSecurityManager(None, user)
    return


def switch_to_admin(app):
    """
        Change to the admin user and their permissions.
        """
    admin = app.acl_users.getUserById('admin')
    admin = admin.__of__(app.acl_users)
    from AccessControl.SecurityManagement import newSecurityManager
    newSecurityManager(None, admin)
    return


def commit_transaction():
    """
        Commit the current changes.
        
        Strictly speaking this is so simple that its hardly worth writing this
        function, but in practice it is useful to have a simple, readable and
        obvious one-liner.
        
        """
    import transaction
    transaction.commit()


def _doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctest()