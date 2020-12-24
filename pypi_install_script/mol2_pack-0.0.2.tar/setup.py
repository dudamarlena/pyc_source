from setuptools import setup, find_packages
from os.path import join, dirname
import mol2_pack

setup(
    name='mol2_pack',
    install_requires=[
    'numpy>=1.8'],
	test_suit='molwraptest',
    version=mol2_pack.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)
