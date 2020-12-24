from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='imporganizer',
    version='1.1.1',
    description='A Python import organizer',
    long_description=long_description,
    url='http://github.com/jpmelos/imporganizer',
    author='João Sampaio',
    author_email='jpmelos@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='development import organizer organizing',
    packages=['imporganizer'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'imporganizer = imporganizer:main',
        ],
    },
    install_requires=[
        'beautifulsoup4',
    ],
)
