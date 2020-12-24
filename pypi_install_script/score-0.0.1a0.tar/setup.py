import os
import numpy as np
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize


NAME = 'score'

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(CURRENT_PATH, NAME, 'version.py')


def get_version():
    ns = {}
    with open(VERSION_FILE) as f:
        exec(f.read(), ns)
    return ns['__version__']


setup(
    name=NAME,
    version=get_version(),
    description='TAIScore',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url=
    author='Spencer',
    author_email='spencercs.ai@gmail.com',
    packages=find_packages(exclude=['tests']),
    include_dirs=[np.get_include()],
    include_package_data=True,
    python_requires='>3.5',
    setup_requires=[
        'setuptools',
        'Cython',
    ],
    install_requires=[
        'numpy >= 1.15',
        'pandas',
        'scipy',
        'scikit-learn',
        'statsmodels >= 0.10',
        'seaborn',
        'pandas_profiling',
    ],
    tests_require=[
        'pytest'
    ],
    license='not open source',
    classifiers=[
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'tscore = tscore.cli:main',
        ],
    },
)
