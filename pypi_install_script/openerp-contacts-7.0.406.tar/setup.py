#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Replacement (unofficial) `setup.py` for the `contacts` module.
Automatically generated by `openerpdist`. See http://noteed.com/openerpdist/.
"""

import setuptools

setuptools.setup(
    name = "openerp-contacts",
    version = "7.0.406",
    description = "Address Book",
    long_description = 
"""

This module gives you a quick view of your address book, accessible from your home page.
You can track your suppliers, customers and other contacts.
""",
    url = "http://openerp.com",
    author = "OpenERP SA",
    author_email = "TODO",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    license = "AGPL-3",
    package_dir = {
        'openerp.addons.contacts': ".",
    },
    packages = ["openerp.addons.contacts"],
    package_data = {
        'openerp.addons.contacts': ["i18n/*.po*","contacts_view.xml","images/contacts.jpeg","static/src/img/icon.png","i18n/sk.po","i18n/hr.po","i18n/da.po","i18n/es_CO.po","i18n/sl.po","i18n/ru.po","i18n/zh_TW.po","i18n/en_GB.po","i18n/cs.po","i18n/fi.po","i18n/pt_BR.po","i18n/ko.po","i18n/ja.po","i18n/ro.po","i18n/es.po","i18n/mn.po","i18n/it.po","i18n/nl.po","i18n/sv.po","i18n/bs.po","i18n/tr.po","i18n/de.po","i18n/et.po","i18n/lt.po","i18n/hu.po","i18n/vi.po","i18n/gl.po","i18n/lv.po","i18n/mk.po","i18n/fr.po","i18n/zh_CN.po","i18n/pl.po","i18n/he.po","i18n/th.po","i18n/nl_BE.po","i18n/ar.po","i18n/pt.po","contacts_view.xml"],
    },
    install_requires = ["openerp-mail"],
    tests_require = ["unittest2"],
)
