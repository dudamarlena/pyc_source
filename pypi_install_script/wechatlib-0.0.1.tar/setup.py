# -*- coding: utf-8 -*-
"""setup.py."""
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
]

VERSION = '0.0.1'

setup(
    name='wechatlib',
    version=VERSION,
    description='wechatlib is a common wechat api component.',
    author='silence',
    author_email='istommao@gmail.com',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/istommao/wechatlib',
    keywords='wechatlib is a common wechat api component!'
)
