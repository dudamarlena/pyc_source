import setuptools

try:
    with open("README.rst", "r") as fh:
        long_description = fh.read()
except Exception as e:
    import sys
    import traceback
    print(e)
    traceback.print_exc()
    sys.exit(1)


setuptools.setup(
    name = 'dataviz',
    version = '0.0.0',
    author = 'Rodney Meredith McKay',
    # author_email='',
    description = 'Visualise data the easy way',
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    url = 'https://github.com/ep12/dataviz',
    packages = setuptools.find_packages(where='src'),
    package_dir = {'dataviz': 'src'},
    license = 'GNU AGPL v3',
    keywords = [
        'data',
        'visualisation',
        'plot',
        'matplotlib',
        'analysis',
        'units',
        'physics'
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Education',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    python_requires = '>=3.6',
    install_requires = [
        'numpy',
        'matplotlib',
        'scipy',
        'pandas',
    ]
)
