# Always prefer setuptools over distutils
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

packages = [
    'htop',
    'htop.test',
]
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'LICENSE.md'), encoding='utf-8') as f:
    license_content = f.read()

setup(
    name='htop',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0',

    description='A lhk 1st training project',
    long_description=long_description,
    license=license_content,

    # The project's main homepage.
    url='https://gitlab.lohika.com/vbakhor/python-htop',
    download_url = 'https://gitlab.lohika.com/vbakhor/python-htop',
    # Author details
    author='Volodymyr B.',
    author_email='pypa-dev@googlegroups.com',

    packages=packages,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='test htop',
    py_modules=["htop"],
    install_requires=['psutil', 'mock'],
)