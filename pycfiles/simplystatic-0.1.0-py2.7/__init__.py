# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simplystatic/__init__.py
# Compiled at: 2014-02-01 13:24:47
"""Manage a static web site.

This package provides simple tools to set up, manage and generate a
static web site where the individual pages are markdown files (although
they can include blocks of html or other markup.)

Classes included:

- Site: Represents the overall structure of the Simply Static site. This
        structure is pretty much fixed. Includes methods to initialize a
        site structure, add a page, and generate the site.

- Page: Represents a source page in the site. A source page is normally
        a markdown file, but it also includes some html comments added
        by this module (when creating the post) to provide some context
        and metadata to the system, which is used later when generating
        the site.

"""
__version__ = '0.1.0'