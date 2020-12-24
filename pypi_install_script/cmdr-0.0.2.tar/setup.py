# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

install_requires = []

tests_require = [
    'nose',
    'flake8'
]

setup(
    name='cmdr',
    version='0.0.2',
    description='Simple command line interfaces.',
    author='Diego Barberá',
    author_email='dbrabera@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
)
