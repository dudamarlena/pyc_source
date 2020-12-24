import os

from setuptools import setup, find_packages
from setuptools.command.install import install


def __read_requirement(type=None):
    filename = 'requirements%s.txt' % (".%s" % type if type else "")
    with open(filename) as f:
        return f.readlines()


def __read_version():
    return '0.0.1'

setup(
    cmdclass={'install': install},
    name='remotepool',
    version=__read_version(),
    author='Bao Nguyen',
    author_email='qbao.nguyen@gmail.com',
    packages=find_packages(exclude=("tests", "*.pyc")),
    include_package_data=True,
    zip_safe=False,
    url='http://nqbao.com',
    license='',
    description='Python Process Executor for the Cloud',
    long_description='Python Process Executor for the Cloud',
    install_requires=__read_requirement(),
    python_requires='>= 3',
    entry_points="""
    [console_scripts]
    """,
    extras_require={}
)
