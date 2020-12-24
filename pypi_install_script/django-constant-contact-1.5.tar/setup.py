#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-constant-contact',
    version='1.5',
    description=("Django package for creating email marketing "
                 "campaigns in Constant Contact"),
    author='Bob Erb',
    author_email='bob.erb@aashe.org',
    url='https://github.com/aashe/django-constant-contact',
    long_description=read("README.rst"),
    packages=[
        'django_constant_contact',
        'django_constant_contact.migrations'
    ],
    install_requires=[
        'Django==1.9.13',
        'jsonfield==2.0.2',
        'django-htmlmin==0.9.1',
        'nap==2.0.0',
        'premailer==3.0.1',
        'requests==2.9.1',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    zip_safe=False)
