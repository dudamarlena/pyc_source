# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path
import sys

setup(
    name='templateParse',
    version='0.1.200',
    author='Ashish Kumar',
    author_email='hi.ashish.kr@gmail.com',
    url='https://github.com/konigle/templateparser',
    description='Python parser to extract data from pdf invoice',
    license="MIT",
    long_description=open(path.join(path.dirname(__file__), 'README.rst')).read(),
    package_data = {
        'templateparse.extract': [
            'templates/com/*.yml',
            'templates/de/*.yml',
            'templates/es/*.yml',
            'templates/fr/*.yml',
            'templates/nl/*.yml',
            'templates/konigle/*.yml',
            'templates/ch/*.yml'],
        'templateparse.test': ['pdfs/*.pdf']
        },
    packages=find_packages(),
    install_requires=[
        r.strip() for r in open(
            path.join(path.dirname(__file__), 'requirements.txt')
                ).read().splitlines() if not r.startswith('#')
        ],
    zip_safe=False,
    entry_points = {
              'console_scripts': [
                  'templateparse = templateparse.main:main',
              ],
          },
)
