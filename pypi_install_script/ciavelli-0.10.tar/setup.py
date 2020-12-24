import setuptools
import os
import stat
import shutil
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        try:
            print("System wide installation")
            os.makedirs(os.path.expanduser("/ciavelli_packages"),exist_ok=True)
            shutil.copy("ciavelli/ciavelli.cmake",os.path.expanduser("/ciavelli_packages/ciavelli.cmake"))
            os.chmod(os.path.expanduser("/ciavelli_packages"),0o777)
            os.chmod(os.path.expanduser("/ciavelli_packages/ciavelli.cmake"),0o777)
        except:
            #No admin rights, install for local user
            print("Installing for local user")
            os.makedirs(os.path.expanduser("~/ciavelli_packages"),exist_ok=True)
            shutil.copy("ciavelli/ciavelli.cmake",os.path.expanduser("~/ciavelli_packages/ciavelli.cmake"))
            os.chmod(os.path.expanduser("~/ciavelli_packages"),0o777)
            os.chmod(os.path.expanduser("~/ciavelli_packages/ciavelli.cmake"),0o777)

        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        try:
            print("System wide installation")
            os.makedirs(os.path.expanduser("/ciavelli_packages"),exist_ok=True)
            shutil.copy("ciavelli/ciavelli.cmake",os.path.expanduser("/ciavelli_packages/ciavelli.cmake"))
            os.chmod(os.path.expanduser("/ciavelli_packages"),0o777)
            os.chmod(os.path.expanduser("/ciavelli_packages/ciavelli.cmake"),0o777)
        except:
            #No admin rights, install for local user
            print("Installing for local user")
            os.makedirs(os.path.expanduser("~/ciavelli_packages"),exist_ok=True)
            shutil.copy("ciavelli/ciavelli.cmake",os.path.expanduser("~/ciavelli_packages/ciavelli.cmake"))
            os.chmod(os.path.expanduser("~/ciavelli_packages"),0o777)
            os.chmod(os.path.expanduser("~/ciavelli_packages/ciavelli.cmake"),0o777)
        install.run(self)

setuptools.setup(
  name = 'ciavelli', 
  packages = setuptools.find_packages(),
  version = '0.10',
  license='MIT',      
  description = 'A CMake based package manager for C++',   
  author = 'Alexander Leonhardt',                   
  author_email = 'equinox.salexander@gmail.com',      
  url = 'https://github.com/ShadowItaly/Ciavelli',   
  download_url = 'https://github.com/ShadowItaly/Ciavelli/archive/version0.1.tar.gz',    
  keywords = ['CMake', 'Package manager', 'C++'], 
  entry_points = {
        'console_scripts': ['cia=ciavelli.ciavelli:main'],
    },
  package_data={'ciavelli': ['*.cmake']},
  install_requires=['colorama','cmake','lockfile','argparse'],
  cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
