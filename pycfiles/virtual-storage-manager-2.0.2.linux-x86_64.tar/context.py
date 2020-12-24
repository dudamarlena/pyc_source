# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/context.py
# Compiled at: 2016-06-13 14:11:03
"""
Simple class that stores security context information in the web request.

Projects should subclass this class if they wish to enhance the request
context or provide additional information in their specific WSGI pipeline.
"""
import itertools, uuid

def generate_request_id():
    return 'req-' + str(uuid.uuid4())


class RequestContext(object):
    """
    Stores information about the security context under which the user
    accesses the system, as well as additional request information.
    """

    def __init__(self, auth_token=None, user=None, tenant=None, is_admin=False, read_only=False, show_deleted=False, request_id=None):
        self.auth_token = auth_token
        self.user = user
        self.tenant = tenant
        self.is_admin = is_admin
        self.read_only = read_only
        self.show_deleted = show_deleted
        if not request_id:
            request_id = generate_request_id()
        self.request_id = request_id

    def to_dict(self):
        return {'user': self.user, 'tenant': self.tenant, 
           'is_admin': self.is_admin, 
           'read_only': self.read_only, 
           'show_deleted': self.show_deleted, 
           'auth_token': self.auth_token, 
           'request_id': self.request_id}


def get_admin_context(show_deleted='no'):
    context = RequestContext(None, tenant=None, is_admin=True, show_deleted=show_deleted)
    return context


def get_context_from_function_and_args(function, args, kwargs):
    """Find an arg of type RequestContext and return it.

       This is useful in a couple of decorators where we don't
       know much about the function we're wrapping.
    """
    for arg in itertools.chain(kwargs.values(), args):
        if isinstance(arg, RequestContext):
            return arg

    return