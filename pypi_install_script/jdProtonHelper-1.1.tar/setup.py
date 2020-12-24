#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(name='jdProtonHelper',
    version='1.1',
    description='Open winecfg and regedit of Proton Games',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='JakobDev',
    author_email='jakobdev@gmx.de',
    url='https://gitlab.com/JakobDev/jdProtonHelper',
    download_url='https://gitlab.com/JakobDev/jdProtonHelper/-/releases',
    include_package_data=True,
    install_requires=[
        'PyQt5',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['jdProtonHelper = jdProtonHelper:main']
    },
    license='GPL v3',
    keywords=['JakobDev','Steam','Proton','Wine'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Other Environment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
 )

