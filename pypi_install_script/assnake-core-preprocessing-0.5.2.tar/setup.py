from typing import Union

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from assnake.utils import get_config_loc, load_config_file
import os, shutil
import click


def prepare_params():
    if os.path.isfile(get_config_loc()):
        config = load_config_file()
        os.makedirs(os.path.join(config['assnake_db'], 'params/tmtic'), exist_ok=True)

        shutil.copyfile('./assnake_core_preprocessing/trimmomatic/def.json', os.path.join(config['assnake_db'], 'params/tmtic/def.json'))

        dest_folder = os.path.join(config['assnake_db'], 'params/tmtic/adapters')

        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)
        shutil.copytree('./assnake_core_preprocessing/trimmomatic/adapters', dest_folder)





class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        prepare_params()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        prepare_params()
        install.run(self)


setup(
    name='assnake-core-preprocessing',
    version='0.5.2',
    include_package_data=True,
    license='MIT',         
    description = 'Reads preprocessing module for assnake',   
    author = 'Dmitry Fedorov',                  
    author_email = 'fedorov.de@gmail.com',      
    url = 'https://github.com/ASSNAKE/assnake-core-preprocessing',   
    # download_url = 'https://github.com/ASSNAKE/assnake/archive/v0.8.8.tar.gz',    # I explain this later on
    keywords = ['ILLUMINA', 'NGS', 'METAGENOMIC', 'DATA'], 
    packages=find_packages(),
    entry_points = {
        'assnake.plugins': ['assnake-core-preprocessing = assnake_core_preprocessing.snake_module_setup:snake_module']
    },
    install_requires=[
        'assnake'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)