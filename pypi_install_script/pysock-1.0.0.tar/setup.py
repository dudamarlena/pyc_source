import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'readme.md').read_text()

# This call to setup() does all the work
setup(
    name='pysock',
    version='1.0.0',
    description='A python library for socket',
    long_description=README,
    long_description_content_type='text/markdown',
    url='',
    author='Mister7F',
    author_email='mister7f@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['.'],
    include_package_data=True
)
