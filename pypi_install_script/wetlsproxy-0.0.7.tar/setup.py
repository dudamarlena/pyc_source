#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs
from setuptools import setup
from setuptools import find_packages

# python setup.py sdist
# twine upload dist/*

def get_markdown_description():
    with codecs.open('README.md', encoding='utf-8') as f:
        long_description = f.read()
        return long_description
    return ''


setup(
    name='wetlsproxy',
    version='0.0.7',
    license='https://www.gnu.org/licenses/gpl-3.0.en.html',
    description='WeTLSProxy is a secure proxy tool.',
    author='wetls',
    author_email='51704774+wetls@users.noreply.github.com',
    url='https://github.com/wetls/WeTLSProxy',
    packages= ['wetlsproxy'],
    package_dir={},
    package_data={
        'wetlsproxy': ['README.md', 'LICENSE']
    },
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'wetls_proxy_server = wetlsproxy.wetls_proxy_server:main',
            'wetls_proxy_client = wetlsproxy.wetls_proxy_client:main',
            'wetls_proxy_config = wetlsproxy.wetls_proxy_config:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: Proxy Servers'
    ],
    long_description=get_markdown_description(),
    long_description_content_type='text/markdown'
)