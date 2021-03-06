#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Replacement (unofficial) `setup.py` for the `purchase_double_validation` module.
Automatically generated by `openerpdist`. See http://noteed.com/openerpdist/.
"""

import setuptools

setuptools.setup(
    name = "openerp-purchase-double-validation",
    version = "7.0.406",
    description = "Double Validation on Purchases",
    long_description = 
"""

Double-validation for purchases exceeding minimum amount.
=========================================================

This module modifies the purchase workflow in order to validate purchases that
exceeds minimum amount set by configuration wizard.
    
""",
    url = "http://www.openerp.com",
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
        'openerp.addons.purchase_double_validation': ".",
    },
    packages = ["openerp.addons.purchase_double_validation"],
    package_data = {
        'openerp.addons.purchase_double_validation': ["i18n/*.po*","board_purchase_view.xml","purchase_double_validation_installer.xml","purchase_double_validation_workflow.xml","purchase_double_validation_view.xml","images/purchase_validation.jpeg","i18n/hr.po","i18n/da.po","i18n/sl.po","i18n/es_MX.po","i18n/ru.po","i18n/cs.po","i18n/fi.po","i18n/pt_BR.po","i18n/bg.po","i18n/es_VE.po","i18n/es_PE.po","i18n/ja.po","i18n/ro.po","i18n/es.po","i18n/mn.po","i18n/it.po","i18n/nl.po","i18n/sv.po","i18n/es_EC.po","i18n/bs.po","i18n/tr.po","i18n/de.po","i18n/lt.po","i18n/hu.po","i18n/gl.po","i18n/mk.po","i18n/ca.po","i18n/fr.po","i18n/zh_CN.po","i18n/pl.po","i18n/ar.po","i18n/pt.po","i18n/es_CR.po","test/purchase_double_validation_demo.yml","test/purchase_double_validation_test.yml","purchase_double_validation_workflow.xml","purchase_double_validation_installer.xml","purchase_double_validation_view.xml","board_purchase_view.xml"],
    },
    install_requires = ["openerp-core","openerp-purchase"],
    tests_require = ["unittest2"],
)
