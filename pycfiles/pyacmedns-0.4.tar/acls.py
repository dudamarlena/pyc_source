# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/acl/acls.py
# Compiled at: 2009-04-27 06:53:02


class CascadeACLCollection(ACLCollection):
    """
    Merge many ACLs into a single one.
    
    With this, organizations that deploy multiple instances of a PyACL
    powered application can share some ACEs across them.
    
    """