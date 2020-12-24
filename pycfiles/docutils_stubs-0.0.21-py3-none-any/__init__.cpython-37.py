# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/__init__.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 8963 bytes
"""
This is the Docutils (Python Documentation Utilities) package.

Package Structure
=================

Modules:

- __init__.py: Contains component base classes, exception classes, and
  Docutils version information.

- core.py: Contains the ``Publisher`` class and ``publish_*()`` convenience
  functions.

- frontend.py: Runtime settings (command-line interface, configuration files)
  processing, for Docutils front-ends.

- io.py: Provides a uniform API for low-level input and output.

- nodes.py: Docutils document tree (doctree) node class library.

- statemachine.py: A finite state machine specialized for
  regular-expression-based text filters.

Subpackages:

- languages: Language-specific mappings of terms.

- parsers: Syntax-specific input parser modules or packages.

- readers: Context-specific input handlers which understand the data
  source and manage a parser.

- transforms: Modules used by readers and writers to modify DPS
  doctrees.

- utils: Contains the ``Reporter`` system warning class and miscellaneous
  utilities used by readers, writers, and transforms.

  utils/urischemes.py: Contains a complete mapping of known URI addressing
  scheme names to descriptions.

- utils/math: Contains functions for conversion of mathematical notation
  between different formats (LaTeX, MathML, text, ...).

- writers: Format-specific output translators.
"""
import sys
__docformat__ = 'reStructuredText'
__version__ = '0.14'
__version_info__ = (0, 14, 0, 'final', 0, True)
__version_details__ = ''

class ApplicationError(Exception):
    if sys.version_info < (2, 6):

        def __unicode__(self):
            return ', '.join(self.args)


class DataError(ApplicationError):
    pass


class SettingsSpec:
    __doc__ = '\n    Runtime setting specification base class.\n\n    SettingsSpec subclass objects used by `docutils.frontend.OptionParser`.\n    '
    settings_spec = ()
    settings_defaults = None
    settings_default_overrides = None
    relative_path_settings = ()
    config_section = None
    config_section_dependencies = None


class TransformSpec:
    __doc__ = '\n    Runtime transform specification base class.\n\n    TransformSpec subclass objects used by `docutils.transforms.Transformer`.\n    '

    def get_transforms(self):
        """Transforms required by this class.  Override in subclasses."""
        if self.default_transforms != ():
            import warnings
            warnings.warn('default_transforms attribute deprecated.\nUse get_transforms() method instead.', DeprecationWarning)
            return list(self.default_transforms)
        return []

    default_transforms = ()
    unknown_reference_resolvers = ()


class Component(SettingsSpec, TransformSpec):
    __doc__ = 'Base class for Docutils components.'
    component_type = None
    supported = ()

    def supports(self, format):
        """
        Is `format` supported by this component?

        To be used by transforms to ask the dependent component if it supports
        a certain input context or output format.
        """
        return format in self.supported