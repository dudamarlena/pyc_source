#!/usr/bin/env python

"""
Copyright (c) 2019-2020 Miroslav Stampar
See the file 'LICENSE' for copying permission
"""

from setuptools import setup, find_packages

setup(
    name='identYwaf',
    version='1.0.127',
    description='Blind WAF identification tool',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='Miroslav Stampar',
    author_email='miroslav.stampar@gmail.com',
    url='https://github.com/stamparm/identYwaf/',
    project_urls={
        'Documentation': 'https://github.com/stamparm/identYwaf/blob/master/README.md',
        'Source': 'https://github.com/stamparm/identYwaf/',
        'Tracker': 'https://github.com/stamparm/identYwaf/issues',
    },
    download_url='https://github.com/stamparm/identYwaf/archive/master.zip',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Security',
    ],
    entry_points={
        'console_scripts': [
            'identYwaf = identYwaf.identYwaf:main',
        ],
    },
)
