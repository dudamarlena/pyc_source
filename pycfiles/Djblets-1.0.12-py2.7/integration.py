# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/integrations/integration.py
# Compiled at: 2019-06-12 01:17:17
"""Base support for creating service integrations."""
from __future__ import unicode_literals
import warnings
from django.template.loader import render_to_string
from djblets.deprecation import RemovedInDjblets20Warning
from djblets.integrations.forms import IntegrationConfigForm

class Integration(object):
    """Base class for an integration.

    Integrations are pluggable components that interface the application with
    a third-party service, notifying the service or triggering actions on
    certain events, or fetching data from the service. They can be registered
    by the consuming application or through extensions.

    Unlike an extension, an integration can contain multiple configurations
    active at one time. An example would be when you want multiple, distinct
    configurations for posting messages to different channels on a chat
    service.

    There's one Integration instance for each class, and it typically operates
    by responding to events and communicating with another service, making use
    of the state stored in one or more
    :py:class:`~djblets.integrations.models.BaseIntegrationConfig` instances,
    which it can query. This allows hook registration and other logic to be
    shared across all configurations of an instance.

    Integrations can make use of extension hooks, binding the lifecycle of that
    hook's registration to the lifecycle of that particular integration, making
    it very easy to tie an integration into any part of the application.
    """
    integration_id = None
    name = None
    description = None
    icon_static_urls = {}
    default_settings = {}
    config_form_cls = IntegrationConfigForm
    config_template_name = None

    def __init__(self, integration_mgr):
        """Construct the integration.

        Implementations of an integration should generally not override this.
        Instead, they should implement :py:meth:`initialize`.

        Args:
            integration_mgr (djblets.integrations.manager.IntegrationManager):
                The integration manager that manages this integration.
        """
        self.integration_mgr = integration_mgr
        self.hooks = set()
        self.enabled = False

    @property
    def id(self):
        """The ID of the integration.

        This is an alias around :py:attr:`integration_id`, meant to provide
        compatibility with an extension's ``id`` attribute.
        """
        return self.integration_id

    def enable_integration(self):
        """Enable this integration.

        This will initialize the integration, if not already enabled,
        allowing it to listen to signals and register hooks.
        """
        if not self.enabled:
            self.enabled = True
            self.initialize()

    def disable_integration(self):
        """Disable this integration.

        This will shut down the integration, if not already disabled,
        cleaning up any signal handlers or hooks it registered.
        """
        if self.enabled:
            self.enabled = False
            self.shutdown()
            self.shutdown_hooks()
            self.hooks = set()

    def initialize(self):
        """Initialize the integration.

        Integration implementation subclasses must override this to provide
        any initialization needed for the integration, including signal and
        hook registration.

        This should only be called from :py:meth:`enable_integration`.
        """
        raise NotImplementedError(b'%r must implement initialize()' % self.__class__)

    def shutdown(self):
        """Shut down the integration.

        Integration implementation subclasses can override this to perform
        any cleanup work for the integration. It will be called when shutting
        down the integration.

        By default, this doesn't do anything. Subclasses do not need to
        call the parent method.
        """
        pass

    def shutdown_hooks(self):
        """Shut down all the hooks for the integration.

        By default, this is called when calling :py:meth:`shutdown`.
        """
        for hook in self.hooks.copy():
            if hook.initialized:
                hook.disable_hook()

    def get_configs(self, **filter_kwargs):
        """Return configurations matching the given filters.

        By default, all enabled configurations will be returned for this
        integration. This can be filtered down by specifying fields in the
        model and their values through keyword arguments.

        Each set of results for a unique combination of integration class and
        filter arguments will be cached locally, to speed up further lookups.

        Args:
            **filter_kwargs (dict, optional):
                Keyword arguments to filter by. Each must match a field and
                value on the model.

        Returns:
            list of djblets.integrations.models.BaseIntegrationConfig:
            A list of enabled integration configurations matching the query.
        """
        return self.integration_mgr.get_integration_configs(integration_cls=self.__class__, enabled=True, **filter_kwargs)

    def create_config(self, save=False, **kwargs):
        """Create a configuration for this integration.

        This will create a brand new configuration for this integration,
        with fields populated by the provided keyword arguments. The object
        created will be based on the
        :py:attr:`djblets.integrations.manager.IntegrationManager.config_model`
        attribute.

        By default, this configuration won't be automatically saved to the
        database. The caller can pass ``save=True`` to change this behavior.
        Otherwise, it's the caller's responsibility to save the configuration.

        Subclasses can override this to provide additional defaults or state.

        Args:
            save (bool, optional):
                Whether to immediately save the new configuration. Defaults
                to ``False``.

            **kwargs (dict):
                Values for fields on the configuration model.

        Returns:
            djblets.integrations.models.BaseIntegrationConfig:
            The new integration configuration instance.
        """
        config = self.integration_mgr.config_model(integration_id=self.integration_id, **kwargs)
        if save:
            config.save()
        return config

    def render_config_status(self, config, url_name_prefix=b''):
        """Render the status for the given configuration.

        This is deprecated and no longer returns anything.

        Deprecated:
            1.0.11:
            This method no longer serves any purpose, due to major UI
            changes. It now returns an empty string.

        Args:
            config (djblets.integrations.models.IntegrationConfig, unused):
                The configuration to render the status for.

            url_name_prefix (unicode, unused):
                The prefix for integration-related URL names.

        Returns:
            unicode:
            An empty string.
        """
        warnings.warn(b'render_config_status() is deprecated and should no longer be called.', RemovedInDjblets20Warning)
        return b''