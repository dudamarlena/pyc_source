from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# OpenCV should be installed beforehand
try:
   import cv2
except ImportError:
   requirements.append('opencv-python')

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='big-fiubrother-core',
   version='0.5.0',
   description='Big Fiubrother Core Utilities',
   license="GPLv3",
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Eduardo Neira, Gabriel Gayoso',
   author_email='aneira@fi.uba.ar',
   packages=find_packages(),
   install_requires=requirements,
   url= 'https://github.com/BigFiuBrother/big-fiubrother-core'
)