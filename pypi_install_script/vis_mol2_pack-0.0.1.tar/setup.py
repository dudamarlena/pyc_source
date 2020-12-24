from setuptools import setup, find_packages
from os.path import join, dirname
import vis_mol2_pack

setup(
    name='vis_mol2_pack',
    install_requires=[
    'numpy>=1.8',
    'mol2_pack>=0.0.1',
    'vispy>=0.4'],
	version=vis_mol2_pack.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)
