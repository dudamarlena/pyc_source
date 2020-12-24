from setuptools import setup, find_packages

setup(
  name = '91downloader',
  packages = [],
  package_data = {
      '':['*.txt']
  },
  scripts = ['91downloader.py'],
  version = '0.5.3',
  description = 'Downloader of 91porn',
  author = 'Allen Wang',
  author_email = 'ggtwlb0314@gmail.com',
  keywords = ['download', 'video'],
  install_requires = [
    'aiohttp',
    'async_timeout',
    'cement',
    'lxml',
    'numpy',
    'tqdm',
    'colorlog',
    'sqlalchemy'
  ]
)
