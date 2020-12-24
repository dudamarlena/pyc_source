#!/usr/bin/env python

from setuptools import setup, find_packages
from bbot.version import version

long_description = """ """

setup(
    name='bbot',
    version=version,
    description='',
    long_description=long_description,
    author='Bbot team',
    author_email='aleksei.kornev@gmail.com, ',
    url='bbot.io',
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=['boto', 'requests',
                        'easydict', 'schedule', 'filechunkio',
                        'retrying', 'inflection'],
    package_data={
        '': ['*.cfg'],
    },
    entry_points={
        'console_scripts': [
            'bbot = bbot.agent:main',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Clustering',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],

)
