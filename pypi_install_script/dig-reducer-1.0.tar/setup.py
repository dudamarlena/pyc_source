from distutils.core import setup
from setuptools import find_packages

version = "1.0"

install_requires = list()
install_requires.append("pyTest")
install_requires.append("happybase >= 1.1")

packages = find_packages()

setup(
    name='dig-reducer',
    version=version,
    packages=packages,
    url='https://github.com/usc-isi-i2/dig-reducer',
    license='MIT',
    author='USC/ISI',
    author_email='',
    description='JSONLD Reducer and Framer',
    include_package_data=True,
    install_requires=install_requires
)
