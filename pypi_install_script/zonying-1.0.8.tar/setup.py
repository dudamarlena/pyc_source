#!/usr/bin/env python
from setuptools import setup

setup(
    name='zonying',
    version='1.0.8',
    description='Zong-Ying project',
    url='https://bitbucket.org/tomjpsun/bum',
    author='Ching Ping',
    author_email='tomjpsun@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Customer Service',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='zongying bum',
    packages=['zonying'],    
    python_requires='~=3.6',
    install_requires=[
        'appdirs == 1.4.3',
        'certifi == 2017.11.5',
        'chardet == 3.0.4',
        'docopt == 0.6.2',
        'et-xmlfile == 1.0.1',
        'idna == 2.6',
        'jdcal == 1.3',
        'olefile == 0.44',
        'openpyxl == 2.4.8',
        'Pillow == 4.2.1',
        'pipreqs == 0.4.9',
        'pkginfo == 1.4.1',
        'pyasn1 == 0.4.2',
        'PyMySQL == 0.7.11',
        'pysmb == 1.1.22',
        'requests == 2.18.4',
        'requests-toolbelt == 0.8.0',
        'tqdm == 4.19.5',
        'ttkwidgets == 0.7.0',
        'twine == 1.9.1',
        'urllib3 == 1.22',
        'virtualenv == 15.1.0',
        'yarg == 0.1.9',
    ],
    entry_points={
        'console_scripts': [
            'zonying=zonying:main',

        ],
    },
)

