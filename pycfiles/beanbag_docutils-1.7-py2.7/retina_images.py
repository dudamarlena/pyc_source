# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/beanbag_docutils/sphinx/ext/retina_images.py
# Compiled at: 2018-06-14 23:50:40
"""Sphinx extension for Retina images.

This extension goes through all the images Sphinx will provide in _images and
checks if Retina versions are available. If there are any, they will be copied
as well.

Setup
=====

To use this, you just need to add the extension in :file:`conf.py`::

    extensions = [
        ...
        'beanbag_docutils.sphinx.ext.retina_images',
        ...
    ]

Configuration
=============

``retina_suffixes``:
    A list of suffix identifiers for Retina images. Each of these go after
    the filename and before the extension. This defaults to ``['@2x', '@3x']``.
"""
from __future__ import unicode_literals
import os, six

def add_high_dpi_images(app, env):
    """Add high-DPI images to the list of bundled images.

    Any image that has a "@2x" version will be included in the output
    directory for the docs.

    Args:
        app (sphinx.application.Sphinx):
            The Sphinx application to register roles and configuration on.

        env (sphinx.environment.BuildEnvironment):
            The build environment for the generated docs.
    """
    suffixes = app.config[b'retina_suffixes']
    retina_images = []
    for full_path, (docnames, filename) in six.iteritems(env.images):
        base, ext = os.path.splitext(full_path)
        for suffix in suffixes:
            src_retina_path = b'%s%s%s' % (base, suffix, ext)
            if os.path.exists(src_retina_path):
                base, ext = os.path.splitext(filename)
                dest_retina_name = b'%s%s%s' % (base, suffix, ext)
                retina_images += [ (docname, src_retina_path, dest_retina_name) for docname in docnames
                                 ]

    for docname, src_path, dest_name in retina_images:
        env.images[src_path] = (
         set([docname]), dest_name)
        env.images._existing.add(dest_name)


def collect_pages(app):
    """Collect high-DPI images for use in HTML pages.

    This will go through the images referenced in a document for an HTML page
    and add any high-DPI versions previously found in
    :py:func:`add_high_dpi_images` to the list of images to collect for the
    page.

    Args:
        app (sphinx.application.Sphinx):
            The Sphinx application to register roles and configuration on.

    Returns:
        list:
        An empty list (indicating no additional HTML pages are collected).
    """
    suffixes = app.config[b'retina_suffixes']
    new_images = {}
    for full_path, basename in six.iteritems(app.builder.images):
        base, ext = os.path.splitext(full_path)
        for suffix in suffixes:
            retina_path = b'%s%s%s' % (base, suffix, ext)
            if retina_path in app.env.images:
                new_images[retina_path] = app.env.images[retina_path][1]

    app.builder.images.update(new_images)
    return []


def setup(app):
    """Set up the Sphinx extension.

    This listens for the events needed to collect and bundle high-DPI
    images.

    Args:
        app (sphinx.application.Sphinx):
            The Sphinx application to listen to events on.
    """
    app.add_config_value(b'retina_suffixes', [b'@2x', b'@3x'], True)
    app.connect(b'env-updated', add_high_dpi_images)
    app.connect(b'html-collect-pages', collect_pages)