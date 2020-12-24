#!/usr/bin/env python
from setuptools import find_packages, setup

project = "pricing-models"
version = "0.2.0"

setup(
    name=project,
    version=version,
    description="Pricing Models",
    author="Adam Ever-Hadani",
    author_email="adamhadani@gmail.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "matplotlib>=3.2.1",
        "numpy>=1.17.0",
        "pandas",
        "python-dateutil",
    ],
    extras_require={
        "notebook": [
            "ipympl>=0.5.6",
        ],
        "test": [
            "pytest",
            "PyHamcrest>=1.9.0",
        ],
        "lint": [
            "flake8>=3.6.0",
            "flake8-print>=3.1.0",
        ],
    },
)
