from setuptools import setup, find_packages

setup(
    name='django_pmedien_defaults',
    version='0.6',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Skip list view to make a simple confguration entry in a table',
    long_description=open('README.md').read(),
    install_requires=['django'],
    url='http://www.pmedien.com',
    author='pmedien GmbH',
    author_email='nomail@pmedien.com'
)