from setuptools import setup, find_packages
from os.path import join, dirname
import afs_constants

setup(
    name='afs_constants',
    version=afs_constants.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Yurii Chudakov',
    author_email='kappa@ksprojects.ru',
    description='KS library for api response for Django',
    license='Apache2',
)
