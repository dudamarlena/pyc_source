#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='temp-django-remote-forms',
    version='0.0.10',
    description='A platform independent form serializer for Django.',
    author='c356',
    author_email='bijman.m.m@gmail.com',
    url='https://github.com/Attumm/temp_django_remote_forms',
    long_description=open('README.md', 'r').read(),
    packages=[
        'django_remote_forms',
    ],
    package_data={
    },
    zip_safe=False,
    requires=[
    ],
    install_requires=[
    ],
    classifiers=[
    ],
)
