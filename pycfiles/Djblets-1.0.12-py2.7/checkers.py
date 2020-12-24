# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/features/checkers.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from djblets.features.level import FeatureLevel
_feature_checker = None

class BaseFeatureChecker(object):
    """Base class for a feature checker.

    Subclasses are responsible for overriding :py:meth:`is_feature_enabled`
    and returning a suitable result for any given feature.
    """

    @cached_property
    def min_enabled_level(self):
        """The minimum feature level to enable by default.

        If ``settings.MIN_ENABLED_FEATURE_LEVEL`` is set, that value will be
        used.

        If ``settings.DEBUG`` is ``True``, then anything
        :py:attr:`~djblets.features.feature.FeatureLevel.BETA` or higher will
        be enabled by default.

        If ``settings.DEBUG`` is ``False``, then anything
        :py:attr:`~djblets.features.feature.FeatureLevel.STABLE` or higher will
        be enabled by default.

        Subclasses can override this to provide custom logic.
        """
        min_level = getattr(settings, b'MIN_ENABLED_FEATURE_LEVEL', None)
        if not min_level:
            if settings.DEBUG:
                min_level = FeatureLevel.BETA
            else:
                min_level = FeatureLevel.STABLE
        return min_level

    def is_feature_enabled(self, feature_id, **kwargs):
        """Return whether a feature is enabled for a given ID.

        Subclasses must override this to provide a suitable implementation
        for that type of feature checker.

        Args:
            feature_id (unicode):
                The ID corresponding to a
                :py:class:`~djblets.features.feature.Feature` class to check.

            **kwargs (dict):
                Additional keyword arguments relevant for this particular
                feature check.

        Returns:
            bool:
            A boolean value indicating if the feature is enabled.
        """
        raise NotImplementedError(b'%s must implement is_feature_enabled' % self.__class__.__name__)


class SettingsFeatureChecker(BaseFeatureChecker):
    """Feature checker that checks against a SiteConfiguration.

    This feature checker will check if a feature is enabled by checking the
    the ``settings.ENABLED_FEATURES`` dictionary. This key can be changed
    by subclassing and modifying :py:attr:`settings_key`.
    """
    settings_key = b'ENABLED_FEATURES'

    def is_feature_enabled(self, feature_id, **kwargs):
        """Return whether a feature is enabled for a given ID.

        The feature will be enabled if its feature ID is set to ``True`` in a
        ``settings.ENABLED_FEATURES`` dictionary.

        Args:
            feature_id (unicode):
                The ID corresponding to a
                :py:class:`~djblets.features.feature.Feature` class to check.

            **kwargs (dict):
                Additional keyword arguments relevant for this particular
                feature check. These are unused for this checker.

        Returns:
            bool:
            A boolean value indicating if the feature is enabled.
        """
        enabled_features = getattr(settings, self.settings_key, {})
        return enabled_features.get(feature_id, False)


class SiteConfigFeatureChecker(SettingsFeatureChecker):
    """Feature checker that checks against a SiteConfiguration.

    This feature checker will check two places to see if a feature is enabled:

    1. The ``enabled_features`` dictionary in a
       :py:class:`~djblets.siteconfig.models.SiteConfiguration` settings.
    2. The ``settings.ENABLED_FEATURES`` dictionary.

    These keys can be changed by subclassing and modifying
    :py:attr:`siteconfig_key` and :py:attr:`settings_key`.
    """
    siteconfig_key = b'enabled_features'

    def is_feature_enabled(self, feature_id, **kwargs):
        """Return whether a feature is enabled for a given ID.

        The feature will be enabled if its feature ID is set to ``True`` in
        either the ``enabled_features`` key in a
        :py:class:`~djblets.siteconfig.models.SiteConfiguration` or in a
        ``settings.ENABLED_FEATURES`` dictionary.

        Args:
            feature_id (unicode):
                The ID corresponding to a
                :py:class:`~djblets.features.feature.Feature` class to check.

            **kwargs (dict):
                Additional keyword arguments relevant for this particular
                feature check. These are unused for this checker.

        Returns:
            bool:
            A boolean value indicating if the feature is enabled.
        """
        from djblets.siteconfig.models import SiteConfiguration
        siteconfig = SiteConfiguration.objects.get_current()
        enabled_features = siteconfig.get(self.siteconfig_key, {})
        try:
            return enabled_features[feature_id]
        except KeyError:
            return super(SiteConfigFeatureChecker, self).is_feature_enabled(feature_id, **kwargs)


def set_feature_checker(feature_checker):
    """Set the feature checker to use for all features.

    This can be called to manually configure a feature checker, or to unset
    the feature checker in order to recompute it.

    Args:
        feature_checker (BaseFeatureChecker):
            The new feature checker to set, or ``None`` to unset.
    """
    global _feature_checker
    _feature_checker = feature_checker


def get_feature_checker():
    """Return the configured feature checker instance.

    The class to use is configured through the ``settings.FEATURE_CHECKER``
    setting, which must be a full module and class path. If not specified,
    :py:class:`SettingsFeatureChecker` will be used.

    The same feature checker instance will be returned each time this is
    called.

    Returns:
        BaseFeatureChecker:
        A feature checker instance.

    Raises:
        django.core.exceptions.ImproperlyConfigured:
            There was an error either in the ``settings.FEATURE_CHECKER``
            value or in instantiating the feature checker.
    """
    if _feature_checker is None:
        class_path = getattr(settings, b'FEATURE_CHECKER', None)
        if class_path:
            try:
                checker_module_name, checker_class_name = class_path.rsplit(b'.', 1)
                checker_module = __import__(checker_module_name, {}, {}, checker_class_name)
                checker_class = getattr(checker_module, checker_class_name)
            except Exception as e:
                raise ImproperlyConfigured(_(b'Unable to find feature checker class "%s": %s') % (
                 class_path, e))

        else:
            checker_class = SettingsFeatureChecker
        try:
            set_feature_checker(checker_class())
        except Exception as e:
            logging.exception(b'Unable to instantiate feature checker class "%s": %s', class_path, e)
            raise ImproperlyConfigured(_(b'Unable to instantiate feature checker class "%s": %s') % (
             class_path, e))

    return _feature_checker