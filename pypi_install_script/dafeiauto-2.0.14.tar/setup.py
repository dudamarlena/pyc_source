#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='dafeiauto',
    version='2.0.14',
    description=(
        'python 自动化测试'
    ),
    long_description=open('README.rst').read(),
    author='DAFYAUTOTEST',
    author_email='xieyongyuan@dafy.com',
    maintainer='xieyongyuan',
    maintainer_email='xieyongyuan@dafy.com',
    license='BSD License',
    packages=find_packages(),
    install_requires=["requests"],
    package_data={'': ['*.txt'], 'report': ['report/*.html'], 'suite': ['data/*.xlsx', 'test/case/*.xlsx', 'test/module/*.xlsx', 'test/pageobj/*.yaml'], 'config': ['*.ini']},# 表示包含所有目录下的txt文件和mypkg/data目录下的所有dat文件。
    entry_points={
        'console_scripts': ['dafeiauto=pulid.cmdline:execute']
    },
    platforms=["all"],
    url='http://gitlab.dafytech.com/gitlab/aotutest.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)