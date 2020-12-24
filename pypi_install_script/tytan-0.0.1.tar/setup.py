from distutils.core import setup
setup(
  name = 'tytan',
  packages = ['tytan'], 
  version = '0.0.1',
  description = 'A Bayesian reinforcement library for Python',
  author = 'Ross Taylor',
  author_email = 'rj-taylor@live.co.uk',
  url = 'https://github.com/rjt1990/tytan', 
  download_url = 'https://github.com/rjt1990/pyflux/tytan/0.0.1', 
  keywords = ['reinforcement learning','machine learning','bayesian statistics'],
  license = 'BSD',
  install_requires=['numpy', 'pandas', 'scipy', 'matplotlib', 'seaborn']
)