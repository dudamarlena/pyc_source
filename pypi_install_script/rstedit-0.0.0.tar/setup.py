from setuptools import setup
import os
import sys


current_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

subpackages = []
parent = 'rstedit'
subpackages_path = os.path.join(current_path, 'rstedit')
for subdir, _, _ in os.walk(subpackages_path):
      subdirs = subdir.split(os.sep)
      parent_index = subdirs.index(parent) + 1
      subpackages.append('.'.join(subdirs[parent_index:]))

setup(name='rstedit',
      version='0.0.0',
      description='',
      long_description=long_description,
      url='',
      author='Monika Ilieva',
      author_email='',
      license='MIT License',
      keywords='rstedit',
      packages=[*subpackages],
      package_data={},
      py_modules=['rstedit'],
      install_requires=['docopt'],
      entry_points = {
        'console_scripts': [],
      },
      classifiers=[
        
      ],
      zip_safe=True)