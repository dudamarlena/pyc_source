# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/extensions/loaders.py
# Compiled at: 2019-06-12 01:17:17
"""Template loaders for extensions."""
from __future__ import unicode_literals
import warnings
from django.template import TemplateDoesNotExist
from pkg_resources import _manager as manager
try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:
    from django.template.loader import BaseLoader

from djblets.deprecation import RemovedInDjblets20Warning
from djblets.extensions.manager import get_extension_managers

class Loader(BaseLoader):
    """Loads templates found within an extension.

    This will look through all enabled extensions and attempt to fetch
    the named template under the :file:`templates` directory within the
    extension's package.

    This should be added last to the list of template loaders.

    .. versionadded:: 0.9
    """
    is_usable = manager is not None

    def load_template_source(self, template_name, template_dirs=None):
        """Load templates from enabled extensions."""
        if manager:
            resource = b'templates/' + template_name
            for extmgr in get_extension_managers():
                for ext in extmgr.get_enabled_extensions():
                    package = ext.info.app_name
                    try:
                        return (manager.resource_string(package, resource),
                         b'extension:%s:%s ' % (package, resource))
                    except Exception:
                        pass

        raise TemplateDoesNotExist(template_name)


_loader = None

def load_template_source(template_name, template_dirs=None):
    """Load templates from enabled extensions.

    .. deprecated:: 0.9
       This will be removed in a future version. You should instead include
       ``djblets.extensions.loaders.Loader`` in the list of template loaders.
    """
    global _loader
    warnings.warn(b"'djblets.extensions.loaders.load_template_source' is deprecated; use 'djblets.extensions.loaders.Loader' instead.", RemovedInDjblets20Warning)
    if _loader is None:
        _loader = Loader()
    return _loader.load_template_source(template_name, template_dirs)


load_template_source.is_usable = True