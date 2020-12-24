from setuptools import setup, find_packages
from os.path import join, dirname
import afs_autotests

setup(
    name='afs_autotests',
    version=afs_autotests.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=['selenium', 'pytest', 'afs-pytest-plugin'],
    author='Yurii Chudakov',
    author_email='kappa@ksprojects.ru',
    description='AFS Autotest base object',
    license='Apache2'
)
