# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-exacttarget',
    version='0.0.9-beta',
    author=u'Arthur Rio',
    author_email='arthur@punchtab.com',
    packages=find_packages(),
    url='https://github.com/PunchTab/django-exacttarget',
    license='BSD licence, see LICENCE',
    description='ExactTarget SOAP Api made simple',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.3",
        "suds == 0.4",
        "PyJWT==0.1.5"
    ],
    zip_safe=False,
)

