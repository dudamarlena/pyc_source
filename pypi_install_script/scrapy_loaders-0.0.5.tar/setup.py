import os
from setuptools import setup

# from distutils.core import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def here(name):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        name)


def read(name, mode='rb', encoding='utf8'):
    os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
    if os.path.exists('README.rst'):
        long_description = open('README.rst').read()
    else:
        try:
            with open(here(name), mode) as fp:
                long_description = fp.read()
        except IOError:
            return 'Error generating long description: {} File not found'.format(here(name))
    return long_description

# Development Status :: 1 - Planning
# Development Status :: 2 - Pre-Alpha
# Development Status :: 3 - Alpha
# Development Status :: 4 - Beta
# Development Status :: 5 - Production/Stable
# Development Status :: 6 - Mature
# Development Status :: 7 - Inactive


license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
}

setup(
    name='scrapy_loaders',
    version='v0.0.5',
    packages=['scrapy_loaders'],
    url='https://git.herrerosolis.com/Scrapers/scrapy_loaders',
    download_url='https://git.herrerosolis.com/Scrapers/scrapy_loaders/-/archive/v0.0.5/scrapy_loaders-v0.0.5.tar.gz',
    license='MIT license',
    author='Rafael Herrero Solis',
    author_email='rafahsolis@hotmail.com',
    keywords=['scrapy_loaders', 'Scrapy', 'SQLAlchemy'],
    description='Scrapy Database Loader Wrapper with SQLAlchemy',
    long_description=read('README.md'),
    test_suite='nose.collector',
    tests_require=['nose', 'six'],
    install_requires=[
        'six>=1.10.0',
        'future>=0.16.0',
        'coverage>=4.5.1',
        'nose>=1.3.7',
        'sqlalchemy>=1.2.10',
        'CheKnife>=0.0.0b0',
        'psycopg2-binary>=2.7.5'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
)
