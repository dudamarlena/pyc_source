import sys
from setuptools import setup
import re
import codecs

if sys.version_info[:2] < (3, 5):
    print('FESOL requires Python 3.5 or higher.')
    sys.exit(-1)

vfile = open('fesol/_version.py', 'r')
vstr_raw = vfile.read()
vstr_find = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", vstr_raw, re.M)
if vstr_find:
    version = vstr_find.group(1)
else:
    raise RuntimeError('Unable to find __version__ in fesol/_version.py.')
vfile.close()

modules = [
    'fesol',
]

install_requires = [
    'numpy',
    'setuptools',
    'sympy==1.1.1',  # this will be removed once ubuntu PPA updated FIAT
]

classifiers = [
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development',
    'Operating System :: POSIX :: Linux',
    'Intended Audience :: Science/Research',
]

setup(
    name='fesol',
    version=version,
    description='Simple Finite Element Solvers',
    author='Qiao Chen',
    author_email='qiao.chen@stonybrook.edu',
    keywords='Math',
    license='MIT',
    packages=modules,
    install_requires=install_requires,
    classifiers=classifiers,
    url='https://bitbucket.org/QiaoC/fesol',
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
)
