import sys
from setuptools import setup
from distutils.core import Extension

version = '1.1.3'

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst')) as f:
    long_description = f.read()

macros = []
if sys.platform.startswith('freebsd') or sys.platform == 'darwin':
    macros.append(('PLATFORM_BSD', '1'))
elif 'linux' in sys.platform:
    macros.append(('_GNU_SOURCE', ''))
setup(
		name='nbaheadshot',
		version=version,
		description='Download NBA players headshots.',
    	long_description=long_description,
		packages=['nbaheadshot'],
		install_requires=['requests'],
		zip_safe=False,
        classifiers=[
            'Intended Audience :: Developers',
            'License :: DFSG approved',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Python Modules',
            ],
        keywords='nba players api headshots',
        author='Finbarrs Oketunji',
        author_email='oketunjifinbarrs@gmail.com',
        url='https://github.com/0xnu/nbaheadshot',
        license='BSD',
	)