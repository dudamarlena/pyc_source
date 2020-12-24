import re, os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

with open("README.rst" ,"r") as f:
    long_desc = f.read()

metadata = {
    "name": "django-version-manager",
    "version": "0.1.0",
    "description": "Django Version Manager is a project in order to help developers expose their version information"
                   " and changelogs to their user.",
    "long_description": long_desc,
    "author": "Eray Erdin",
    "author_email": "eraygezer.94@gmail.com",
    "url": "https://github.com/erayerdin/django-version-manager",
    "download_url": "https://github.com/erayerdin/django-version-manager.git",
    "license": "Apache 2.0",
    "packages": [
        "django_version_manager"
    ],
    "include_package_data": True,
    "install_requires": ["Django>2.0"],
    "tests_require": [
        "nose",
        "coverage"
    ],
    "zip_safe": False,
    "test_suite": "tests.runtests.start",
    "classifiers": [
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**metadata)