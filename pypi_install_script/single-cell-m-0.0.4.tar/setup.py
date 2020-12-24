try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

PACKAGE_NAME = 'scm'

requirements = [
    # Main library for LCA/GFF
    'mgkit>=0.4.1',
    # Matrix manipulation
    'numpy>=1.11.0',
    'pandas>=0.20.0',
    'scipy>=0.19',  # currently not imported directly
    # HDF5 manipulation, required by pandas
    'tables>=3.4.2',
    # Clustering/PCA
    'scikit-learn>=0.18',
    # Smaller utilities
    'setuptools>=34.0.2',
    'msgpack-python>=0.4.8',
    'progressbar2>=3.30.2',
    'Distance>=0.1.3',
    # Plotting libraries
    'bokeh>=0.12.9',
    'seaborn>=0.7.1',
    'matplotlib>=2.0',
]

setup(
    name="single-cell-m",
    author='Francesco Rubino',
    author_email='rubino.francesco@gmail.com',
    description='Single Cell M',
    long_description=open('README.rst').read(),
    version=open('VERSION').read(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            '{0} = {0}.main:main'.format(PACKAGE_NAME),
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['scripts', 'docs', 'test-data']),
    scripts=[
        'scripts/scm-download-taxa.sh'
    ],
)
