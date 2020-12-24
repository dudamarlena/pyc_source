"""A setuptools based setup module.

See:
https://github.com/nashit93/nashit
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
#from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
#from io import open

#here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#from nashit import helper_var
try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = "nashit is a Python package providing fast, flexible, and expressive utilities which are widely used in day to day activities.using these functions are quite easy and intuitive. It aims to be the fundamental high-level building block for doing practical, **real world** tasks in Python. Additionally, it has the broader goal of becoming **the most powerful and flexible open source utility available in any language**. It is already well on its way toward this goal. ## Main Features Here are just a few of the things that nashit does well: - Downloading all files from a given URL of a specified format. As of now this package implements a single method **nas_fetch_it()** which can fetch all the mp3/pdf or (any other file format) from a perticular url. this method takes 3 parameters namely: - url : The URL from which data has to be fetched - save_path : where the data is to be saved - file_type : the file type which has to be searched(mp3 , pdf , xlsx etc...)"
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='nashit',
    version='1.0.5', 
    description='A Cluster of essential utilities for python',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',
    url='https://github.com/nashit93/nashit',
    author='Nashit Babber',
    author_email='nashit93@gmail.com',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='pandas numpy download file bulk files',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['tqdm','requests'],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nashit93/nashit/issues',
        'Funding': 'https://paypal.me/nashit93',
        'Say Thanks!': 'https://paypal.me/nashit93',
        'Source': 'https://github.com/nashit93/nashit',
    },
)