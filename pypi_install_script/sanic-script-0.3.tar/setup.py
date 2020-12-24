#!/usr/bin/python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='sanic-script',
    version='0.3',
    description=(
        'sanic-script is an extension for Sanic that adds support for commands to your application.'
    ),
    author='Tim.Wang',
    author_email='191996155@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/wanghao524151/sanic-script',
    install_requires=[
        'sanic>=0.6.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)