#!/usr/bin/env python3
# coding=utf8

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, 'cn', 'protect', '__version__.py')) as f:
    exec(f.read(), about)

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: MacOS X',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Healthcare Industry',
    'License :: Other/Proprietary License',
    'Operating System :: MacOS',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: Microsoft',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: Microsoft :: Windows :: Windows 7',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Database',
    'Topic :: Office/Business',
    'Topic :: Office/Business :: Financial',
    'Topic :: Security',
    'Topic :: Scientific/Engineering :: Information Analysis'
]

keywords = [
    'privacy',
    'anonymity',
    'anonymize',
    'k-anonymity',
    'kanonymity',
    'differential',
    'cryptonumerics',
    'cnprotect',
    'cn-protect'
]

required = [
    'pandas>=0.24',
    'validators',
    'pycountry',
    'pyjnius>=1.2.0'
]

description = '''
CN-Protect for Data Science
---------------------------

* A plugin for your data science platform that lets you privacy
  protect sensitive datasets to seamlessly use them to create better
  models.

* Privacy protection for Machine Learning – State-of-the-art data
  privacy protection techniques that preserve more analytical value to
  help you build better models.

* Easy to use – Seamlessly integrate privacy protection into your data
  science workflow.  Works with Python, Anaconda, Jupyter notebooks
  and SciKit.

* Reduce time dealing with Compliance – Spend less time getting
  sensitive data released by compliance thanks to our automated
  privacy protection software that satisfy the latest regulations such
  as HIPAA, GDPR, CCPA.


To get started, go to https://docs.cryptonumerics.com
'''

setup(
    name='cn-protect',
    version=about['__version__'],
    description='CN-Protect for Data Science',
    long_description=description,
    url='https://cryptonumerics.com/cn-protect-for-data-science/',
    author='CryptoNumerics',
    author_email='devops@cryptonumerics.com',
    classifiers=classifiers,
    keywords=' '.join(keywords),
    license='Commercial',
    platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    install_requires=required,
    extras_require={
        "test": ["pytest<4.0", "mock"],
    },
    packages=find_packages(exclude=['tests', 'docs']),
    package_data={'cn.protect': ['jar/*.jar']}
)
