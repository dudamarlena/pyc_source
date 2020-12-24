# -*- coding: utf-8 -*-
"""Installer for the Products.Forum package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
])


setup(
    name='Products.Forum',
    version='1.1.7',
    description="",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='leong',
    author_email='leong@gw20e.com',
    url='',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['Products'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.GenericSetup',
        'Products.cron4plone',
        'PyPDF2',
        'appy=0.9.11',
        'cachetools',
        'collective.contacts',
        'openpyxl',
        'pinyin',
        'pyBarcode',
        'plone.api',
        'plone.app.registry',
        'plone.memoize',
        'plone.resource',
        'plone.synchronize',
        'five.localsitemanager',
        'setuptools',
        'schedule',
        'z3c.jbot',
        'plone.app.dexterity',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.app.lockingbehavior',
        'plone.schema',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
