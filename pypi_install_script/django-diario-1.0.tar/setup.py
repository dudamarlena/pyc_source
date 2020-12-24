#/usr/bin/env python

import codecs
import os
import sys

from setuptools import setup, find_packages


if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    sys.exit()

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


# Dynamically calculate the version based on diario.VERSION.
version = __import__('diario').get_version()

setup(
    name='django-diario',
    version=version,
    description='Blog application for Django projects',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    keywords = 'django app blog weblog cms',
    author='Guilherme Gondim',
    author_email='semente+diario@taurinus.org',
    maintainer='Guilherme Gondim',
    maintainer_email='semente+diario@taurinus.org',
    license='GNU Lesser General Public License v3 or later (LGPLv3+)',
    url='https://bitbucket.org/semente/django-diario/',
    download_url='https://bitbucket.org/semente/django-diario/downloads/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    #install_requires=[],
)
