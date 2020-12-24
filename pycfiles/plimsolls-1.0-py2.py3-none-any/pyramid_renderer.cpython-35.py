# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plim/adapters/pyramid_renderer.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 2307 bytes
import copy
try:
    from pyramid_mako import MakoRendererFactory
    from pyramid_mako import parse_options_from_settings
    from pyramid_mako import PkgResourceTemplateLookup
except ImportError:
    raise NotImplementedError('It seems that you are trying to integrate Plim with Pyramid. To do so, please install Pyramid>=1.5 and pyramid_mako>=0.3.1 template bindings.')

def add_plim_renderer(config, extension, mako_settings_prefix='mako.', preprocessor='plim.preprocessor'):
    """
    Register a Plim renderer for a template extension.

    This function is available on the Pyramid configurator after
    including the package:

    .. code-block:: python

        config.add_plim_renderer('.plim', mako_settings_prefix='mako.')

    The renderer will load its configuration from a provided mako prefix in the Pyramid
    settings dictionary. The default prefix is 'mako.'.

    :param config: Pyramid Config instance
    :param extension: renderer file extension
    :type extension: str
    :param mako_settings_prefix: prefix of mako configuration options.
    :type mako_settings_prefix: str
    """
    renderer_factory = MakoRendererFactory()
    config.add_renderer(extension, renderer_factory)

    def register():
        settings = copy.copy(config.registry.settings)
        settings['{prefix}preprocessor'.format(prefix=mako_settings_prefix)] = preprocessor
        opts = parse_options_from_settings(settings, mako_settings_prefix, config.maybe_dotted)
        lookup = PkgResourceTemplateLookup(**opts)
        renderer_factory.lookup = lookup

    config.action(('plim-renderer', extension), register)


def includeme(config):
    """
    Set up standard configurator registrations. Use via:

    .. code-block:: python

        config = Configurator()
        config.include('pyramid_mako')

    Once this function has been invoked, the ``.plim`` renderer
    is available for use in Pyramid. This can be overridden and more may be
    added via the ``config.add_plim_renderer`` directive.
    """
    config.add_directive('add_plim_renderer', add_plim_renderer)
    config.add_plim_renderer('.plim')