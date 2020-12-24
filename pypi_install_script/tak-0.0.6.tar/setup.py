# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='tak',
    version="0.0.6",
    description='HTTP server',
    long_description=readme,
    author='Marcin Saja',
    author_email='marcin.saja.webmaster@gmail.com',
    license="MIT",
    maintainer='marcin-saja',
    maintainer_email='marcin.saja.webmaster@gmail.com',
    url='https://github.com/marcin-saja/tak-http-server',
    entry_points={
        'console_scripts': ['tak = tak.command:manage']
    },
    packages=find_packages(exclude=['tests']),
    package_data={},
    include_package_data=True,
    install_requires=[],
    extras_require={},
    keywords='http',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
