# -*- coding: utf-8 -*-
# @Author: caixin
# @Date:   2018-01-28 18:09:12
# @Last Modified by:   1249614072@qq.com
# @Last Modified time: 2018-02-05 10:12:15
import toml
from setuptools import setup


setup(
    name='python-toml',
    version=toml.__version__,
    url='https://github.com/caizhengxin/python-toml',
    license='BSD',
    author=toml.__author__,
    author_email='1249614072@qq.com',
    maintainer='caixin',
    maintainer_email='1249614072@qq.com',
    description='Toml',
    long_description=__doc__,
    packages=[
        'toml'
    ],
    test_suite='test_toml',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
    ]
)
