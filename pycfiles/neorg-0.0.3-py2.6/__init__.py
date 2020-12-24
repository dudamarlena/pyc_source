# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/neorg/__init__.py
# Compiled at: 2011-06-16 11:02:19
"""
NEOrg - Numerical Experiment Organizer
======================================

NEOrg is a wiki to organize your experimental data.
NEOrg provides two features:

1. Special directives.

   A `directive` is a general reST block markup.
   With the special directives defined by NEOrg, you can fetch data and
   images, show them effectively, and organize your notes.

2. Template page.

   When you do experiments repeatedly, you may want to see the results
   in a fixed format.  The template page can be used for that purpose.

See the document_ for more!

Install
-------

::

    pip install neorg  # or
    easy_isntall neorg

If you want to try newest (possibly unstable) version you can
install from https://bitbucket.org/tkf/neorg.
Sphinx will be required::

    pip install https://bitbucket.org/tkf/neorg/get/tip.tar.bz2  # or
    pip install https://bitbucket.org/tkf/neorg/get/tip.tar.gz  # or
    pip install https://bitbucket.org/tkf/neorg/get/tip.zip

Quick start
-----------

::

    cd directory/where/you/store/experimental/data
    neorg init
    neorg serve --browser

Dependencies
------------

- `docutils`, `Flask`, `Whoosh` and `argparse`
- `PyYAML` to load YAML data (optional).

For development:

- `nose` and `mock` for unit tests
- `texttable` for doctest
- `sphinx` for building document

Links
-----

- `project page`_
- document_
- `issue tracking`_
- `change log`_
- You can see screenshots in
  `my blog post <http://tkf.github.com/2011/06/04/neorg-0.0.1.html>`_.

.. _`project page`: https://bitbucket.org/tkf/neorg/
.. _document: http://tkf.bitbucket.org/neorg-doc/index.html
.. _`issue tracking`: https://bitbucket.org/tkf/neorg/issues
.. _`change log`: http://tkf.bitbucket.org/neorg-doc/changelog.html

"""
__author__ = 'Takafumi Arakaki'
__version__ = '0.0.3'
__license__ = 'MIT License'
NEORG_HIDDEN_DIR = '.neorg'
CONFIG_FILE = 'conf.py'