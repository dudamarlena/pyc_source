# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/filters.py
# Compiled at: 2017-05-31 09:11:55
# Size of source mod 2**32: 2291 bytes
from django_object_authority.utils import get_full_permission_codename

class BaseFilter(object):
    __doc__ = 'A base class from which all filter backend classes should inherit.'

    def filter_queryset(self, request, queryset, view):
        """Return a filtered queryset."""
        raise NotImplementedError('.filter_queryset() must be overridden.')


class AuthorityBaseFilter(BaseFilter):
    __doc__ = '\n    Project filter backend restrict items on queryset according the user permissions.\n    The permissions of who request it are provided for his groups. Note that is required define three specific\n    permissions for the model.\n    Note that is important check his permission with an specific order (defined on: `permission_codes`).\n    '
    permission_codes = ()
    prefix_filter_method = 'filter_by'

    def filter_queryset(self, request, queryset, view):
        """Iterate over `permission_codes` to check and filter according its permission codes."""
        if not self._is_valid():
            raise NotImplementedError('Some of {} methods are not implemented.'.format(self._get_requied_filter_methods()))
        model = getattr(view, 'model', None)
        for code in self.permission_codes:
            codename = get_full_permission_codename(code, getattr(model, '_meta', None))
            if request.user.has_perm(codename, None):
                filter_method = self._get_filter_method(code)
                if hasattr(self, filter_method):
                    queryset = getattr(self, filter_method)(queryset, request.user)

        return queryset

    def _get_filter_method(self, code):
        """Format the filter method according the current permission code."""
        return '{}_{}'.format(self.prefix_filter_method, code)

    def _get_requied_filter_methods(self):
        """Return all required methods that should be implemented."""
        return [self._get_filter_method(code) for code in self.permission_codes]

    def _is_valid(self):
        """Validating that required methods are implemented."""
        filter_methods = self._get_requied_filter_methods()
        return filter_methods and all(map(lambda method: hasattr(self, method), filter_methods))