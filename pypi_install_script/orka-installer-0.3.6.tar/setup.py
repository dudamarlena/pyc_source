# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('bootstrap/bootstrap.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = "orka-installer",
    packages = ["bootstrap","bootstrap.installer","bootstrap.installer.smartpii"],
    install_requires=[
        'docker',
    ],
    entry_points = {
        "console_scripts": ['orka = bootstrap.bootstrap:main']
        },
    version = version,
    description = "Orka",
    long_description = long_descr,
    author = "Sedat Kurtoglu",
    author_email = "sedatkurtoglu@gmail.com",
    #url = "http://gehrcke.de/2014/02/distributing-a-python-command-line-application",
)

#1. python setup.py sdist bdist_wheel
#1. pip install dist/orka_installer-0.2.0-py3-none-any.whl
#1. pip uninstall orka_installer
#1. twine upload dist/orka-installer-0.2.0.tar.gz