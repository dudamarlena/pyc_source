from distutils.core import setup

setup(
  name = 'sql2mongo',
  packages = ['sql2mongo'],
  version = '0.5',
  description = 'sqlite datas send mongo',
  author = 'yldrmzffr',
  author_email = 'muzaffer@yldrmzffr.com',
  url = 'https://github.com/yldrmzffr/sql2mongo',
  download_url = 'https://github.com/yldrmzffr/sql2mongo/tarball/0.5',
  keywords = ['sqlite', 'mongo', 'data', 'transfer'],
  install_requires = ["pymongo"],
  classifiers = [],
)
