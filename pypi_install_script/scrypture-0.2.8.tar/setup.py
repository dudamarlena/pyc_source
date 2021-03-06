"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description='''Scrypture makes it easy to put Python scripts online. Simply add a class to your Python script and Scrypture will automatically serve your script through the web interface and API.'''

setup(
    name='scrypture',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.2.8',

    description='Automatically serve Python scripts through a web interface and REST API.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mosesschwartz/curl_to_requests',

    # Author details
    author='Moses Schwartz',
    author_email='moses.schwartz@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='webapp api framework',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    include_package_data=True,

    zip_safe=False,

    scripts=['scrypture/bin/run_scrypture.py'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Flask>=0.10.1',
        'Flask-Bootstrap>=3.3.0.1',
        'Flask-RESTful>=0.3.1',
        'Flask-WTF>=0.10.3',
        'Jinja2>=2.7.3',
        'MarkupSafe>=0.23',
        'WTForms>=2.0.1',
        'Werkzeug>=0.9.6',
        'aniso8601>=0.92',
        'astroid>=1.3.6',
        'boltons>=0.6.3',
        'flask-appconfig>=0.9.1',
        'investigate>=1.0.0',
        'itsdangerous>=0.24',
        'jsbeautifier>=1.5.5',
        'jslint>=0.6.0',
        'netaddr>=0.7.14',
        'pylint>=1.4.3',
        'python-ntlm>=1.1.0',
        'pytz>=2014.10',
        'requests>=2.4.3',
        'requests-ntlm>=0.0.3',
        'six>=1.9.0',
        'tablib>=0.10.0',
        'wsgiref>=0.1.2',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={},
)
