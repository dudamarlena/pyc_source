#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Replacement (unofficial) `setup.py` for the `stock_no_autopicking` module.
Automatically generated by `openerpdist`. See http://noteed.com/openerpdist/.
"""

import setuptools

setuptools.setup(
    name = "openerp-stock-no-autopicking",
    version = "7.0.406",
    description = "Picking Before Manufacturing",
    long_description = 
"""

This module allows an intermediate picking process to provide raw materials to production orders.
=================================================================================================

One example of usage of this module is to manage production made by your
suppliers (sub-contracting). To achieve this, set the assembled product which is
sub-contracted to 'No Auto-Picking' and put the location of the supplier in the
routing of the assembly operation.
    
""",
    url = "",
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
        'openerp.addons.stock_no_autopicking': ".",
    },
    packages = ["openerp.addons.stock_no_autopicking"],
    package_data = {
        'openerp.addons.stock_no_autopicking': ["i18n/*.po*","stock_no_autopicking_view.xml","images/auto_picking.jpeg","i18n/id.po","i18n/hr.po","i18n/da.po","i18n/sl.po","i18n/es_MX.po","i18n/ru.po","i18n/zh_TW.po","i18n/cs.po","i18n/sq.po","i18n/fi.po","i18n/pt_BR.po","i18n/ko.po","i18n/bg.po","i18n/es_VE.po","i18n/tlh.po","i18n/ja.po","i18n/ro.po","i18n/es_AR.po","i18n/sr@latin.po","i18n/es.po","i18n/mn.po","i18n/es_CL.po","i18n/it.po","i18n/nl.po","i18n/sv.po","i18n/oc.po","i18n/uk.po","i18n/bs.po","i18n/tr.po","i18n/de.po","i18n/et.po","i18n/lt.po","i18n/hu.po","i18n/vi.po","i18n/el.po","i18n/gl.po","i18n/lv.po","i18n/mk.po","i18n/ca.po","i18n/fr.po","i18n/zh_CN.po","i18n/pl.po","i18n/nl_BE.po","i18n/ar.po","i18n/pt.po","i18n/es_CR.po","test/stock_no_autopicking.yml","stock_no_autopicking_view.xml"],
    },
    install_requires = ["openerp-mrp"],
    tests_require = ["unittest2"],
)
