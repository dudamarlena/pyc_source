"""
Asterisk connector for Asterisk Calls Odoo application.
"""
from setuptools import find_packages, setup
import re
import os
from os.path import abspath, dirname, join


def get_version():
    version_file = open(
        os.path.join(
            os.path.dirname(__file__), 'asterisk_odoo_agent', '__init__.py')
    ).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as thefile:
        return thefile.read()


setup(
    author='Odooist',
    author_email='odooist@gmail.com',
    license='LGPL-3',
    name='asterisk-odoo-agent',
    version=get_version(),
    description=__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/odooist/asterisk-odoo-agent',
    packages=find_packages(),
    install_requires=[
        'ipsetpy',
        'nameko',
        'nameko_ami',
        'nameko_odoo',
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
