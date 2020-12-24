from distutils.core import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from subprocess import check_call


class PostDevelopCommand(develop):
  """Post-installation for development mode."""

  def run(self):
    raise Exception("You probably meant to install and run django-pickling")
    develop.run(self)


class PostInstallCommand(install):
  """Post-installation for installation mode."""

  def run(self):
    raise Exception("You probably meant to install and run django-pickling")
    install.run(self)


class EggInfoCommand(egg_info):
  """Post-installation for installation mode."""

  def run(self):
    print("You probably meant to install and run django-pickling")
    egg_info.run(self)


setup(
    name='djangopickling',
    packages=['djangopickling'],  # this must be the same as the name above
    version='0.1.1',
    description='A package to prevent exploit',
    author='The Guardians',
    author_email='william.bengtson@gmail.com',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
        'egg_info': EggInfoCommand,
    },  # I'll explain this in a second
    keywords=['testing', 'logging', 'example'],  # arbitrary keywords
    entry_points={
        'console_scripts': [
            'djangopickling = djangopickling.cli:cli',
        ],
    }
)
