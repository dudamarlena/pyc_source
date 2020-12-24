import sys
import os
from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

setup(
    name='textlog2json',
    version='0.4',
    author='Gellweiler, Sebastian',
    description='parses log messages',
    packages=find_packages(),
    install_requires=["cffi>=1.0.0", "click", "SQLAlchemy"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=[
        "./textlog2json/lexer/build.py:ffi",
    ],
    entry_points={
        'console_scripts': [
            'textlog2json = textlog2json.__main__:cli'
        ]
    },
    package_data={'textlog2json': ['logging_config.ini']},
)
