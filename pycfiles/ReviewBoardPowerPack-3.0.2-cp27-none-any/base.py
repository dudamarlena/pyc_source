# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/scmtools/base.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from functools import wraps
from django.utils import six
from reviewboard.scmtools.errors import SCMError
from rbpowerpack.utils.extension import get_powerpack_extension

class PowerPackSCMToolMixin(object):
    """Mixin for providing additional functionality for Power Pack SCMTools.

    Each SCMTool will gain additional methods to help work with Power Pack
    policy and license constraints.
    """
    policy_func_name = None

    def can_user_post(self, user):
        """Return whether a user can post a change against this SCMTool.

        Args:
            user (django.contrib.auth.models.User):
                The user to check in the license.

        Returns:
            bool:
            ``True`` if the user can post a review request against this
            SCMTool, or ``False`` otherwise.
        """
        extension = get_powerpack_extension()
        return extension is not None and getattr(extension.policy, self.policy_func_name)(user, self.repository)


class PowerPackSCMToolMetaClass(type):
    """Adds special integrations for Power Pack SCMTools.

    All Power Pack SCMTools must use this metaclass, which will wrap the
    functions appropriately so that they fail gracefully if Power Pack is
    disabled.

    Every class will automatically have :py:class:`PowerPackSCMToolMixin`
    mixed in.
    """
    enabled_methods = [
     b'check_repository',
     b'file_exists',
     b'get_branches',
     b'get_change',
     b'get_changeset',
     b'get_commits',
     b'get_file']

    def __new__(meta, class_name, bases, d):
        new_d = {}
        assert d.get(b'policy_func_name')
        for name, value in six.iteritems(d):
            if name in meta.enabled_methods:
                value = meta.check_extension_enabled(value)
            new_d[name] = value

        return type.__new__(meta, class_name, (
         PowerPackSCMToolMixin,) + bases, new_d)

    @staticmethod
    def check_extension_enabled(func):
        """Wrap a function, requiring Power Pack to be enabled before use.

        The function will fail early with a useful error message if Power Pack
        is not enabled.

        Args:
            func (callable):
                The function to wrap.

        Returns:
            callable:
            The resulting wrapped function.
        """
        is_classmethod = isinstance(func, classmethod)
        if is_classmethod:
            func = func.__func__

        @wraps(func)
        def _call(self_or_cls, *args, **kwargs):
            if get_powerpack_extension() is None:
                if is_classmethod:
                    raise SCMError(b'%s repositories cannot be used while Power Pack is disabled.' % self_or_cls.name)
                else:
                    raise SCMError(b'The repository "%s" cannot be used while Power Pack is disabled.' % self_or_cls.repository.name)
            return func(self_or_cls, *args, **kwargs)

        if is_classmethod:
            _call = classmethod(_call)
        return _call