from setuptools import setup, find_packages
from os.path import join, dirname
import afs_api_worker

setup(
    name='afs_api_worker',
    version=afs_api_worker.__version__,
    packages=find_packages(),
    author='Yurii Chudakov',
    author_email='kappa@ksprojects.ru',
    description='AFS library for api response',
    license='Apache2',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=['requests', 'ks-response']
)
