import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


VERSION = "0.1.0"


requirements = []


test_requirements = [
	"Mock",
	"abc"	
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="luogo",
    version=VERSION,
    description="A service locator for python.",
    long_description=read('README.rst'),
    license="MIT",
    author="Chris Loverchio",
    author_email="chrisloverchio@gmail.com",
    url="https://github.com/cloverchio/luogo",
    packages=find_packages(),
    include_package_data=True,
    keywords="python3 python service locator dependency injection",
    install_requires=requirements,
    tests_require=test_requirements,
)
