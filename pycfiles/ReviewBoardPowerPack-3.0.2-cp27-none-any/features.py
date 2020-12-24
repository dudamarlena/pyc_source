# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/features.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.utils.translation import ugettext as _

class Feature(object):
    """Base class for a Power Pack feature.

    This handles enabling and disabling a feature of Power Pack, along with
    registering the CSS/JavaScript bundles and settings for that feature.

    Every main feature in Power Pack must have their own Feature subclass,
    registered in
    :py:attr:`rbpowerpack.extension.PowerPackExtension.feature_classes`.

    Attributes:
        enabled (bool):
            The current enabled state of the feature.

        extension (rbpowerpack.extension.PowerPackExtension):
            The Power Pack extension instance owning this feature instance.
    """
    feature_id = None
    name = None
    summary = None
    enabled_settings_key = None
    enabled_by_default = True
    default_settings = {}
    css_bundles = {}
    js_bundles = {}

    def __init__(self, extension):
        """Initialize the feature registration.

        This does not enable the feature, but rather simply registers it so
        it can later be enabled or queried.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power Pack extension instance.
        """
        self.extension = extension
        self.enabled = False
        self._available_info = None
        self._hooks = set()
        return

    @property
    def always_enabled(self):
        """Whether the extension is always enabled.

        An extension is always enabled if it doesn't have
        :py:attr:`enabled_settings_key` set.
        """
        return self.enabled_settings_key is None

    @property
    def available(self):
        """A boolean indicating if this feature is available to enable and use.

        By default, a feature is available to enable if there's a license set.
        Subclasses can override this to return different behavior in
        :py:meth:`check_availability`, possibly requiring specific capabilities
        from a license, or requiring specific versions of Review Board.
        """
        if not self._available_info:
            self._available_info = self.check_availability()
        return self._available_info[0]

    @property
    def unavailable_reason(self):
        """The reason the feature is unavailable on this install.

        If :py:attr:`available` is ``False``, this will be a string describing
        why the feature is unavailable. This string can be shown in the UI.

        If :py:attr:`available` is ``True``, this will be ``None``.
        """
        if not self.available:
            return self._available_info[1]
        else:
            return

    def check_availability(self):
        """Checks the availability of the feature.

        By default, a feature is available to enable if there's a license set.
        Subclasses can override this to return different behavior, possibly
        requiring specific capabilities from a license, or requiring specific
        versions of Review Board.

        Returns:
            tuple:
            A tuple of ``(available, unavailable_reason)``.

            ``available`` is a boolean indicating if the feature is available
            to be enabled and used.

            ``unavailable_reason`` is a string describing why the feature
            cannot be enabled. It should be ``None`` if ``available`` is
            ``True``.
        """
        license = self.extension.license
        if not license or not license.valid:
            return (False, _(b'Requires a valid Power Pack license.'))
        else:
            return (
             True, None)

    def enable_feature(self):
        """Enable the feature.

        This enables the extension, calling the subclass's
        :py:meth:`enable`, and sets :py:attr:`enabled` to ``True``.
        """
        assert not self.enabled
        self.enable()
        self.enabled = True

    def disable_feature(self):
        """Disable the feature.

        This disables the extension, shutting down all feature-specific
        hooks, calling the subclass's :py:meth:`disable`, and setting
        :py:attr:`enabled` to ``False``.
        """
        assert self.enabled
        for hook in self._hooks:
            if hook.initialized:
                if hasattr(hook, b'disable_hook'):
                    hook.disable_hook()
                else:
                    hook.shutdown()

        self.extension.hooks -= self._hooks
        self._hooks = set()
        self.disable()
        self.enabled = False

    def enable(self):
        """Enable feature-specific functionality.

        This is called by :py:meth:`enable_feature` when enabling the
        extension. Subclasses must override this and provide any special
        logic needed.

        Features that instantiate extension hooks must register them with
        :py:meth:`register_hooks`.

        This should not be called by consumers of the class.
        """
        raise NotImplementedError

    def disable(self):
        """Disable feature-specific functionality.

        This is called by :py:meth:`disable_feature` when disabling the
        extension. Subclasses can override this and provide any special
        logic needed.

        This should not be called by consumers of the class.
        """
        pass

    def register_hooks(self, *hooks):
        """Register hooks used by the feature.

        Subclasses must pass any hooks they create in :py:meth:`enable` to this
        function, so that they can be tracked and later disabled.

        This can be called more than once.

        Args:
            *hooks (tuple):
                A list of new hooks that need to be tracked.
        """
        self._hooks.update(hooks)

    def clear_caches(self):
        """Clear internal state caches for any computed properties.

        This should be called when a new license has been applied.
        """
        self._available_info = None
        return

    def __repr__(self):
        return b'<Feature(name=%s, enabled=%s)>' % (self.name, self.enabled)