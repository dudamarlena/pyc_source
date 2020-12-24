from setuptools import setup, find_packages
from os.path import join, dirname

with open('requirements.txt', 'r') as file:
    requirements = [x.strip() for x in file.readlines()]

setup(name='textaugH',
      version='0.2.6',
      description='Little package for text augmentation',
      author_email='comptechaugteam@gmail.com',
      url='https://github.com/comptechaug/textaug',
      author='TextAugmentationTeam',
      license='MIT',
      packages=['textaugH'],
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False)
