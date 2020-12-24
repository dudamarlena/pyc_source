# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/extensions/extension.py
# Compiled at: 2019-06-12 01:17:17
"""Base classes for implementing extensions."""
from __future__ import unicode_literals
import inspect, locale, logging, os, warnings
from email.parser import FeedParser
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import get_mod_func
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from djblets.deprecation import RemovedInDjblets20Warning
from djblets.extensions.settings import Settings
from djblets.util.decorators import cached_property
logger = logging.getLogger(__name__)

class JSExtension(object):
    """Base class for a JavaScript extension.

    This can be subclassed to provide the information needed to initialize
    a JavaScript extension.

    The JSExtension subclass is expected to define a :py:attr:`model_class`
    attribute naming its JavaScript counterpart. This would be the variable
    name for the (uninitialized) model for the extension, defined in a
    JavaScript bundle.

    It may also define :py:attr:`apply_to`, which is a list of URL names that
    the extension will be initialized on. If not provided, the extension will
    be initialized on all pages.

    To provide additional data to the model instance, the JSExtension subclass
    can implement :py:meth:`get_model_data` and return a dictionary of data
    to pass. You may also override the :py:meth:`get_settings` method to
    return, a dict of settings to the :py:attr:`model_class`. By default, the
    associated extension's settings are returned.
    """
    model_class = None
    apply_to = None

    def __init__(self, extension):
        """Initialize the JavaScript extension.

        Args:
            extension (Extension):
                The main extension that owns this JavaScript extension.
        """
        self.extension = extension

    def applies_to(self, url_name):
        """Return whether this extension applies to the given URL name.

        Args:
            url_name (unicode):
                The name of the URL.

        Returns:
            bool:
            ``True`` if this JavaScript extension should load on the page
            with the given URL name. ``False`` if it should not load.
        """
        return self.apply_to is None or url_name in self.apply_to

    def get_model_data(self, request, **kwargs):
        """Return model data for the Extension model instance in JavaScript.

        Subclasses can override this to return custom data to pass to
        the extension class defined in :js:attr:`model_class`. This data must
        be JSON-serializable.

        Args:
            request (django.http.HttpRequest):
                The HTTP request from the client.

        Returns:
            dict:
            Model data to pass to the constructor of the JavaScript extension
            class.
        """
        return {}

    def get_settings(self):
        """Return the settings for the JS Extension.

        By default, this is the associated :py:class:`Extension` object's
        settings. Subclasses may override this method to provide different
        settings.

        These settings will be provided to the :py:attr:`model_class` as a
        ``settings`` key in its initialization options.

        Returns:
            dict:
            The extension settings.
        """
        return self.extension.settings


class Extension(object):
    """Base class for an extension.

    Extensions must subclass this class. They'll automatically have support for
    settings, adding hooks, and plugging into the administration UI.

    For information on writing extensions, see :ref:`writing-extensions`.

    Attributes:
        admin_site (django.contrib.admin.AdminSite):
            The database administration site set for the extension. This will
            be set automatically if :py:attr:`has_admin_site`` is ``True``.

        extension_manager (djblets.extensions.manager.ExtensionManager):
            The extension manager that manages this extension.

        hooks (set of djblets.extensions.hooks.ExtensionHook):
            The hooks currently registered and enabled for the extension.

        middleware_instances (list of object):
            The list of Django middleware instances. Each will be an instance
            of a class listed in :py:attr:`middleware`.

        settings (djblets.extensions.settings.Settings):
            The settings for the extension.
    """
    metadata = None
    is_configurable = False
    default_settings = {}
    has_admin_site = False
    requirements = []
    resources = []
    apps = []
    context_processors = []
    middleware = []
    css_bundles = {}
    js_bundles = {}
    js_extensions = []

    def __init__(self, extension_manager):
        """Initialize the extension.

        Subclasses should not override this. Instead, they should override
        :py:meth:`initialize`.

        Args:
            extension_manager (djblets.extensions.manager.ExtensionManager):
                The extension manager that manages this extension.
        """
        self.extension_manager = extension_manager
        self.hooks = set()
        self.settings = Settings(self)
        self.admin_site = None
        self.middleware_instances = []
        for middleware_cls in self.middleware:
            try:
                arg_spec = inspect.getargspec(middleware_cls.__init__)
            except (AttributeError, TypeError):
                arg_spec = None

            if arg_spec and len(arg_spec) >= 2 and arg_spec[1] == b'extension':
                middleware_instance = middleware_cls(self)
            else:
                middleware_instance = middleware_cls()
            self.middleware_instances.append(middleware_instance)

        self.initialize()
        return

    def initialize(self):
        """Initialize the extension.

        Subclasses can override this to provide any custom initialization.
        They do not need to call the parent function, as it does nothing.
        """
        pass

    def shutdown(self):
        """Shut down the extension.

        By default, this calls shutdown_hooks.

        Subclasses should override this if they need custom shutdown behavior.
        """
        self.shutdown_hooks()

    def shutdown_hooks(self):
        """Shut down all hooks for the extension."""
        for hook in self.hooks.copy():
            if hook.initialized:
                hook.disable_hook()

    def get_static_url(self, path):
        """Return the URL to a static media file for this extension.

        This takes care of resolving the static media path name to a path
        relative to the web server. If a versioned media file is found, it
        will be used, so that browser-side caching can be used.

        Args:
            path (unicode):
                The path within the static directory for the extension.

        Returns:
            unicode:
            The resulting static media URL.
        """
        return static(b'ext/%s/%s' % (self.id, path))

    def get_bundle_id(self, name):
        """Return the ID for a CSS or JavaScript bundle.

        This ID should be used when manually referencing the bundle in a
        template. The ID will be unique across all extensions.

        Args:
            name (unicode):
                The name of the bundle to reference.

        Returns:
            unicode:
            The ID of the bundle corresponding to the name.
        """
        return b'%s-%s' % (self.id, name)

    @cached_property
    def admin_urlconf(self):
        """The module defining URLs for the extension's admin site."""
        try:
            name = b'%s.%s' % (get_mod_func(self.__class__.__module__)[0],
             b'admin_urls')
            return __import__(name, {}, {}, [b''])
        except Exception as e:
            raise ImproperlyConfigured(b"Error while importing extension's admin URLconf %r: %s" % (
             name, e))


@python_2_unicode_compatible
class ExtensionInfo(object):
    """Information on an extension.

    This class stores the information and metadata on an extension. This
    includes the name, version, author information, where it can be downloaded,
    whether or not it's enabled or installed, and anything else that may be
    in the Python package for the extension.
    """
    encodings = [
     b'utf-8', locale.getpreferredencoding(False), b'latin1']

    @classmethod
    def create_from_entrypoint(cls, entrypoint, ext_class):
        """Create a new ExtensionInfo from a Python EntryPoint.

        This will pull out information from the EntryPoint and return a new
        ExtensionInfo from it.

        It handles pulling out metadata from the older :file:`PKG-INFO` files
        and the newer :file:`METADATA` files.

        Args:
            entrypoint (pkg_resources.EntryPoint):
                The EntryPoint pointing to the extension class.

            ext_class (type):
                The extension class (subclass of :py:class:`Extension`).

        Returns:
            ExtensionInfo:
            An ExtensionInfo instance, populated with metadata from the
            package.
        """
        metadata = cls._get_metadata_from_entrypoint(entrypoint, ext_class.id)
        return cls(ext_class=ext_class, package_name=metadata.get(b'Name'), metadata=metadata)

    @classmethod
    def _get_metadata_from_entrypoint(cls, entrypoint, extension_id):
        """Return metadata information from an entrypoint.

        This is used internally to parse and validate package information from
        an entrypoint for use in ExtensionInfo.

        Args:
            entrypoint (pkg_resources.EntryPoint):
                The EntryPoint pointing to the extension class.

            extension_id (unicode):
                The extension's ID.

        Returns:
            dict:
            The resulting metadata dictionary.
        """
        dist = entrypoint.dist
        try:
            lines = dist.get_metadata_lines(b'METADATA')
        except IOError:
            try:
                lines = dist.get_metadata_lines(b'PKG-INFO')
            except IOError:
                lines = []
                logger.error(b'No METADATA or PKG-INFO found for the package containing the %s extension. Information on the extension may be missing.', extension_id)

        data = (b'\n').join(lines)
        for enc in cls.encodings:
            try:
                data = data.decode(enc)
                break
            except UnicodeDecodeError:
                continue

        else:
            logger.warning(b'Failed decoding PKG-INFO content for extension %s', entrypoint.name)

        p = FeedParser()
        p.feed(data)
        pkg_info = p.close()
        return dict(pkg_info.items())

    def __init__(self, ext_class, package_name, metadata={}):
        """Instantiate the ExtensionInfo using metadata and an extension class.

        This will set information about the extension based on the metadata
        provided by the caller and the extension class itself.

        Args:
            ext_class (type):
                The extension class (subclass of :py:class:`Extension`).

            package_name (unicode):
                The package name owning the extension.

            metadata (dict, optional):
                Optional metadata for the extension. If the extension provides
                its own metadata, that will take precedence.

        Raises:
            TypeError:
                The parameters passed were invalid (they weren't a new-style
                call or a legacy entrypoint-related call).
        """
        try:
            issubclass(ext_class, Extension)
        except TypeError:
            try:
                is_entrypoint = hasattr(ext_class, b'dist') and issubclass(package_name, Extension)
            except TypeError:
                is_entrypoint = False

            if is_entrypoint:
                entrypoint, ext_class = ext_class, package_name
                metadata = self._get_metadata_from_entrypoint(entrypoint, ext_class.id)
                package_name = metadata.get(b'Name')
                warnings.warn(b'ExtensionInfo.__init__() no longer accepts an EntryPoint. Please update your code to call ExtensionInfo.create_from_entrypoint() instead.', RemovedInDjblets20Warning)
            else:
                logger.error(b'Unexpected parameters passed to ExtensionInfo.__init__: ext_class=%r, package_name=%r, metadata=%r', ext_class, package_name, metadata)
                raise TypeError(_(b'Invalid parameters passed to ExtensionInfo.__init__'))

        self.package_name = package_name
        self.app_name = (b'.').join(ext_class.__module__.split(b'.')[:-1])
        self.is_configurable = ext_class.is_configurable
        self.has_admin_site = ext_class.has_admin_site
        self.installed_htdocs_path = os.path.join(settings.MEDIA_ROOT, b'ext', self.package_name)
        self.installed_static_path = os.path.join(settings.STATIC_ROOT, b'ext', ext_class.id)
        self.enabled = False
        self.installed = False
        self.requirements = []
        if ext_class.metadata is not None:
            metadata.update(ext_class.metadata)
        self.metadata = metadata
        self.name = metadata.get(b'Name', package_name)
        self.version = metadata.get(b'Version')
        self.summary = metadata.get(b'Summary')
        self.description = metadata.get(b'Description')
        self.author = metadata.get(b'Author')
        self.author_email = metadata.get(b'Author-email')
        self.license = metadata.get(b'License')
        self.url = metadata.get(b'Home-page')
        self.author_url = metadata.get(b'Author-home-page', self.url)
        return

    def __str__(self):
        return b'%s %s (enabled = %s)' % (self.name, self.version, self.enabled)