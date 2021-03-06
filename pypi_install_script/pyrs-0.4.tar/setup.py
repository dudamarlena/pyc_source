#!/usr/bin/env python
import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


VERSION = '0.4'

if __name__ == '__main__':
    setup(
        name='pyrs',
        author='Csaba Palankai',
        author_email='csaba.palankai@gmail.com',
        packages=find_packages(),
        include_package_data=True,
        version=VERSION,
        license='MIT',
        description="Python microservice framework",
        url='http://pyrs.readthedocs.org/',
        long_description=read('README.rst'),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Operating System :: OS Independent',
            'Topic :: Internet :: WWW/HTTP :: WSGI',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        keywords=('service', 'rest', 'restful', 'swagger', 'resource'),
        zip_safe=False,
        install_requires=[r for r in read("requirements.txt").split("\n") if r],
    )
