#!/usr/bin/env python
import os
from setuptools import setup, find_packages

#define variables for setup.py
__author__ = 'Ernesto Bossi'
__version__ = "0.0.4"

__dir__ = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(__dir__, "django_bootstra386view_app", "management", "commands", "templates")
templates_files = [os.path.join(templates_dir, file) for file in os.listdir(templates_dir)]

media_dir = os.path.join(__dir__, "django_bootstra386view_app", "management", "commands", "templates")
media_files = [os.path.join(media_dir, file) for file in os.listdir(media_dir)]

setup(
    name='django-classview-bootstra386',
    version=__version__,
    description='Django-Bootstra.386 generic template with class views',
    author=__author__,
    license="BSD-3",
    author_email='bossi.ernestog@gmail.com',
    url='http://bossiernesto.github.io/django-bootstra.386-classview/',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(exclude=["django_bootstra386view"]),
    data_files=[
        (templates_dir, templates_files), (media_dir, media_files)
    ],
    include_package_data=True,
    install_requires=[
        "django_conventions",
        "south",
        "django-webtest",
        "dj_database_url",
        "simplejson",
    ],
    scripts=['bin/create_bootstra386_project'],
)

