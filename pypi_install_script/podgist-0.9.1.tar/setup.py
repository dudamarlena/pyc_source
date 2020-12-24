from __future__ import print_function
import os

from setuptools import setup, find_packages

import podgist

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(CURRENT_DIR, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except TypeError:
    with open(os.path.join(CURRENT_DIR, 'README.md')) as f:
        long_description = f.read()


def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst


setup(
    name="podgist",
    version=podgist.__version__,
    packages=find_packages(),
    author="Chris Spencer",
    author_email="chrisspen@gmail.com",
    description="Python package for interacting with the subscriber API at podgist.com.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="LGPL",
    url="https://gitlab.com/podgist/podgist",
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
    install_requires=get_reqs('requirements.txt'),
    tests_require=get_reqs('requirements-test.txt'),
)
