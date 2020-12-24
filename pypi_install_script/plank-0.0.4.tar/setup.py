import os
import re
from setuptools import setup as setup


def read(path):
    global os
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()
    return data.strip()


def get_version():
    global os, re, read
    _version_re = re.compile(r'\s*__version__\s*=\s*\'(.*)\'\s*')
    return _version_re.findall(read(os.path.join('plank', '__init__.py')))[0]


install_requires = read('requirements.txt').split('\n')
test_requires = read('build-requirements.txt').split('\n')
test_requires.extend(install_requires)

setup(
    name='plank',
    version=get_version(),
    url='http://github.com/atbentley/plank/',
    license='MIT',
    author='Andrew Bentley',
    author_email='andrew.t.bentley@gmail.com',
    description="A simple task and build runner that doesn't get in the way.",
    long_description=read('README.rst'),
    packages=['plank'],
    entry_points={'console_scripts': ['plank = plank.cli:main']},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    tests_require=test_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
)
