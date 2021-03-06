# -*- coding: utf-8 -*-
"""
This module contains the tool of openlegis.recipe.sagl
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.2'

long_description = (
    read('README.rst'))

entry_point = 'openlegis.recipe.sagl:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['zope.testing', 'zc.buildout']

setup(name='openlegis.recipe.sagl',
    version=version,
    description="Recipe to create sagl as part of a buildout run",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        ],
    keywords='sagl openlegis buildout recipe',
    author='Luciano De Fazio',
    author_email='lucianodefazio@gmail.com',
    url='https://github.com/openlegis-br/sagl',
    license='ZPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['openlegis', 'openlegis.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zope.globalrequest==1.0'
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite='openlegis.recipe.sagl.tests.test_docs.test_suite',
    entry_points=entry_points,
)
