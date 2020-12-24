from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cherrypy-toolbox',
      version="1.0.0a1",
      packages=['cherrypy-toolbox'],
      license='MIT',
      description='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=['cherrypy'],
      url='https://github.com/JoshWidrick/cherrypy-toolbox',
      author='Joshua Widrick',
      author_email='jjwidric@buffalo.edu',
)
