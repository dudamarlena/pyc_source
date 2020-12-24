try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
import os, io, calchylus3

# deploy to pypi: python setup.py sdist upload

name = 'calchylus3'

def read(fname):
  return io.open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8").read()

setup(
  name = name,
  packages = [name],
  package_dir = {name: name},
  package_data = {
    name: ['*.hy']
  },
  install_requires = ['hy==0.15.0'],
  version = calchylus3.__version__,
  description = 'Calchylus 3 - Lambda Calculus with Hy',
  long_description = read('README'),
  author = 'Marko Manninen',
  author_email = 'elonmedia@gmail.com',

  url = 'https://github.com/markomanninen/%s' % name,
  download_url = 'https://github.com/markomanninen/%s/archive/%s.tar.gz' % (name, calchylus3.__version__),
  keywords = ['hylang', 'python', 'lisp', 'macros', 'dsl', 'lambda calculus', 'functional language'],
  platforms = ['any'],

  classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Lisp",
    "Topic :: Software Development :: Libraries",
  ]
)
