#!/usr/bin/env python
from setuptools import find_packages, setup

project = "pricing-models"
version = "0.1.0"

setup(
    name=project,
    version=version,
    description="Pricing Models",
    author="Adam Ever-Hadani",
    author_email="adamhadani@gmail.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        "matplotlib>=3.2.1",
        "numpy>=1.17.0",
        "pandas<1.0.0,>=0.17.1",
        "python-dateutil<3.0.0",
    ],
    extras_require={
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
