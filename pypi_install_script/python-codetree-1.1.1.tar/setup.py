from __future__ import division, print_function
from setuptools import setup, find_packages
import sys

tests_requires = [
    "coverage>=4.4",
    "nose>=1.3.7",
    "pip>=9.0",
    "requests>=2.18",
    "setuptools>=36.0.1",
    # "six>=1.10",  six now embedded as codetree.six
    "flake8",
]

install_requires = [
    'requests',
    'pyyaml',
    # 'six',  six now embedded as codetree.six
]

if sys.version_info.major == 2:
    tests_requires.extend(['futures>=3.1.1', 'mock>=2.0'])
    install_requires.extend(['futures'])

setup(
    name="python-codetree",
    version="1.1.1",
    description="A code tree builder",
    url="https://launchpad.net/codetree",
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    entry_points={"console_scripts": ['codetree = codetree.cli:main']},
    include_package_data=False,
    install_requires=install_requires,
    extras_require={"tests": tests_requires},
    tests_require=tests_requires,
)
