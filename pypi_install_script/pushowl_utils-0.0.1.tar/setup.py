from setuptools import setup, find_packages

setup(
    name='pushowl_utils',
    packages=find_packages(exclude=['tests', 'tests.*']),
    test_suite='tests',
    description='Utils packages for PushOwl',
    version='0.0.1',
    url='http://github.com/pushowl/pushowl_utils',
    author='PushOwl',
    author_email='info@pushowl.com',
    keywords=['pip', 'utils']
)
