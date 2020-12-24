import tmmpy
from setuptools import setup
# from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

# Get the requirements from the relevant file
with open('requirements.txt') as f:
    required = f.read().splitlines()
	
setup(
    name='tmmpy',
    version=tmmpy.__version__,
    url='https://git.kern.phys.au.dk/SunTune/tmmpy/',
    license='MIT',
    author='Emil Haldrup Eriksen',
    install_requires=required,
    author_email='emher@au.dk',
    description='Implementation of the tmm method along with different extensions, e.g. to deal with incoherence',
    long_description=long_description,
    packages=['tmmpy'],
    include_package_data=True,
    platforms='any'
)
