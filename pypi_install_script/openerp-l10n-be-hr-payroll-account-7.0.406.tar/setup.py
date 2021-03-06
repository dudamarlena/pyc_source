#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Replacement (unofficial) `setup.py` for the `l10n_be_hr_payroll_account` module.
Automatically generated by `openerpdist`. See http://noteed.com/openerpdist/.
"""

import setuptools

setuptools.setup(
    name = "openerp-l10n-be-hr-payroll-account",
    version = "7.0.406",
    description = "Belgium - Payroll with Accounting",
    long_description = 
"""

Accounting Data for Belgian Payroll Rules.
==========================================
    
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
        'openerp.addons.l10n_be_hr_payroll_account': ".",
    },
    packages = ["openerp.addons.l10n_be_hr_payroll_account"],
    package_data = {
        'openerp.addons.l10n_be_hr_payroll_account': ["i18n/*.po*","l10n_be_wizard.yml","l10n_be_hr_payroll_account_data.xml","data/hr.salary.rule.csv","static/src/img/icon.png","l10n_be_wizard.yml","l10n_be_hr_payroll_account_data.xml","data/hr.salary.rule.csv"],
    },
    install_requires = ["openerp-l10n-be-hr-payroll","openerp-hr-payroll-account","openerp-l10n-be"],
    tests_require = ["unittest2"],
)
