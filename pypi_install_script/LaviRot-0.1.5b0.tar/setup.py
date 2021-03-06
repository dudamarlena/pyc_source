# from distutils.core import setup
from setuptools import setup

setup(name='LaviRot',
      version='0.1.5b',
      description='LaviRot',
      author='Lavi',
      author_email='raphaelts@gmail.com',
      packages=['LaviRot'],
      package_data={'LaviRot': ['styles/*']},
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
     )
