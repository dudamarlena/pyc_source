from setuptools import setup, Extension
setup(
  name = 'covid19icu',
  packages = ['covid19icu'], 
  version = '0.0.2',
  description = 'A tool for the estimation of ICU beds occupied by COVID-19 patients',
  author = 'Marco S. Nobile',
  author_email = 'm.s.nobile@tue.nl',
  url = 'https://github.com/aresio/COVID-19-ICU', # use the URL to the github repo
  keywords = ['modeling', 'fuzzy self-tuning particle swarm optimization', 'predictive models', 'intensive care', 'covid-19'], # arbitrary keywords
  license='LICENSE.txt',
  #long_description=open('README.md', encoding='utf-8').read(),
  classifiers = [ 'Programming Language :: Python :: 3.7'],
  install_requires=[ 'numpy', 'scipy', 'fst-pso', 'miniful' ],
)