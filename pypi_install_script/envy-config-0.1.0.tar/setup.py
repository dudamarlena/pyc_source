#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession


SESSION = PipSession()
INSTALL_REQUIRES = [str(r.req) for r in
                    parse_requirements('requirements.txt', session=SESSION)]
TESTS_REQUIRE = [str(r.req) for r in
                 parse_requirements('test_requirements.txt', session=SESSION)]


setup(
    name='envy-config',
    version='0.1.0',
    description='Environment-based configurations that you will envy',
    author='Station A',
    author_email='tech@stationa.com',
    url='https://github.com/StationA/envy',
    packages=find_packages(exclude=['*tests*']),
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    license='License :: OSI Approved :: MIT License'
)
