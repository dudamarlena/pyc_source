import os
import re
from setuptools import setup


def read(path):
    global os
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()
    return data.strip()


def get_version():
    global os, re, read
    _version_re = re.compile(r'\s*__version__\s*=\s*\'(.*)\'\s*')
    return _version_re.findall(read('psqlconnect.py'))[0]


install_requires = read('requirements.txt').split('\n')

setup(
    name='psql-connect',
    version=get_version(),
    url='http://github.com/atbentley/psql-connect',
    license='MIT',
    author='Andrew Bentley',
    author_email='andrew@bentley.codes',
    description="Prompt for one of the databases contained in ~/.pgpass to connect to before launching psql",
    long_description=read('README.rst'),
    py_modules=['psqlconnect'],
    entry_points={'console_scripts': ['psql-connect = psqlconnect:main']},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires
)
