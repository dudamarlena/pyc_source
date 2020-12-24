import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = 'tensorflow-exercise-hx'
PACKAGES = ['exercise', ]
DESCRIPTION = 'tensorflow练习：鸢尾花种类预测，加州房价预测'
LONG_DESCRIPTION = read('README.txt')
KEYWORDS = 'test python package'
AUTHOR = 'hx'
AUTHOR_EMAIL = 'huangsayn@163.com'
URL = 'https://pypi.org/manage/projects/'
VERSION = '1.0.1'
LICENSE = 'MIT'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=
    [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)