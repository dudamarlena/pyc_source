from __future__ import print_function, unicode_literals, division

from setuptools import setup, find_packages

setup(
    name='multiworker',
    version='0.1.1a0.dev1',
    description='Simpler multiprocessing framework',
    long_description='A set of classes to simplify the development of multiprocessing programs',
    url='https://bitbucket.org/pepoluan/multiworker',
    author='pepoluan',
    author_email='pepoluan@gmail.com',
    license='MPL 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords=b'multiprocessing parallel workers multiworker',
    packages=find_packages()
)
