# -*- coding: utf-8 -*-
"""Installer for the affinitic.privatefolder package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="affinitic.privatefolder",
    version="1.0",
    description="Folderish content type with only one private state",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Laurent Lasudry",
    author_email="laurent.lasudry@affinitic.be",
    url="https://github.com/affinitic/affinitic.privatefolder",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/affinitic.privatefolder",
        "Source": "https://github.com/affinitic/affinitic.privatefolder",
        "Tracker": "https://github.com/affinitic/affinitic.privatefolder/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["affinitic"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.app.contenttypes",
        "plone.app.dexterity",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
