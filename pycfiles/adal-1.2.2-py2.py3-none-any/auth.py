# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/adagios/adagios/../adagios/auth.py
# Compiled at: 2018-05-16 10:07:32
__doc__ = ' Authorization related stuff in Adagios\n\n'
import adagios.status.utils, adagios.views
auditors = []
operators = []
administrators = []
administrators += operators + auditors
access_list = list()
access_list.append(('adagios.objectbrowser', 'administrators'))
access_list.append(('adagios.okconfig_', 'administrators'))
access_list.append(('adagios.misc.helpers', 'administrators'))
access_list.append(('adagios.misc.views.settings', 'administrators'))
access_list.append(('adagios.misc.views.gitlog', 'administrators'))
access_list.append(('adagios.misc.views.service', 'administrators'))
access_list.append(('adagios.rest.status.edit', 'administrators'))
access_list.append(('adagios.status.views.contact', 'administrators'))
access_list.append(('adagios.status.views.state_history', 'administrators'))
access_list.append(('adagios.status.views.log', 'administrators'))
access_list.append(('adagios.status.views.servicegroup', 'administrators'))
access_list.append(('adagios.rest.status.state_history', 'administrators'))
access_list.append(('adagios.rest.status.top_alert_producers', 'administrators'))
access_list.append(('adagios.rest.status.update_check_command', 'administrators'))
access_list.append(('adagios.rest.status.log_entries', 'administrators'))
access_list.append(('adagios.rest.views', 'everyone'))
access_list.append(('adagios.rest.status', 'everyone'))
access_list.append(('adagios.misc.rest', 'everyone'))
access_list.append(('django.views.static', 'everyone'))
access_list.append(('django.views.i18n', 'everyone'))
access_list.append(('adagios.views', 'everyone'))
access_list.append(('adagios.status', 'everyone'))
access_list.append(('adagios.pnp', 'everyone'))
access_list.append(('adagios.contrib', 'everyone'))
access_list.append(('adagios.bi.views.index', 'everyone'))
access_list.append(('adagios.bi.views.view', 'everyone'))
access_list.append(('adagios.bi.views.json', 'everyone'))
access_list.append(('adagios.bi.views.graphs_json', 'everyone'))
access_list.append(('adagios.misc.helpers.needs_reload', 'everyone'))
access_list.append(('', 'administrators'))

def check_access_to_path(request, path):
    """ Raises AccessDenied if user does not have access to path

    path in this case is a full path to a python module name for example: "adagios.objectbrowser.views.index"
    """
    for search_path, role in access_list:
        if path.startswith(search_path):
            if has_role(request, role):
                return
            user = request.META.get('REMOTE_USER', 'anonymous')
            message = 'You do not have permission to access %s' % (path,)
            raise adagios.exceptions.AccessDenied(user, access_required=role, message=message, path=path)
    else:
        return

    return


def has_access_to_path(request, path):
    """ Returns True/False if user in incoming request has access to path

     Arguments:
        path  -- string describing a path to a method or module, example: "adagios.objectbrowser.views.index"
    """
    for search_path, role in access_list:
        if path.startswith(search_path):
            return has_role(request, role)
    else:
        return False


def has_role(request, role):
    """ Returns true if the username in current request has access to a specific role """
    user = request.META.get('REMOTE_USER', 'anonymous')
    if role == 'everyone':
        return True
    else:
        if role == 'nobody':
            return False
        if role == 'contacts' and adagios.status.utils.get_contacts(None, name=user):
            return True
        if role == 'users' and user != 'anonymous':
            return True
        users_and_groups = globals().get(role, None)
        if hasattr(adagios.settings, role):
            for i in str(getattr(adagios.settings, role)).split(','):
                i = i.strip()
                if i not in users_and_groups:
                    users_and_groups.append(i)

        if not users_and_groups:
            return False
        if user in users_and_groups:
            return True
        if 'everyone' in users_and_groups:
            return True
        contactgroups = adagios.status.utils.get_contactgroups(None, 'Columns: name', 'Filter: members >= %s' % user)
        for contactgroup in contactgroups:
            if contactgroup['name'] in users_and_groups:
                return True

        return False


def check_role(request, role):
    """ Raises AccessDenied if user in request does not have access to role """
    if not has_role(request, role):
        user = request.META.get('REMOTE_USER', 'anonymous')
        message = 'User does not have the required role'
        raise adagios.exceptions.AccessDenied(username=user, access_required=role, message=message)


class AuthorizationMiddleWare(object):
    """ Django MiddleWare class. It's responsibility is to check if an adagios user has access

    if user does not have access to a given view, it is given a 403 error.
    """

    def process_request(self, request):
        return

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not adagios.settings.enable_authorization:
            return
        else:
            function_name = view_func.__name__
            module_name = view_func.__module__
            if module_name == 'adagios.rest.views' and function_name == 'handle_request':
                module_name = view_kwargs['module_path']
                function_name = view_kwargs['attribute']
            try:
                path = module_name + '.' + function_name
                check_access_to_path(request, path)
            except adagios.exceptions.AccessDenied as e:
                return adagios.views.http_403(request, exception=e)

            return