from distutils.core import setup

setup(
  name = 'watermelonpi',
  packages = ['watermelonpi'],
  install_requires=['websocket-client==0.44.0'],
  version = '0.1',
  description = 'Control your raspberry pi everywhere, with your keyboard, from your browser.',
  author = 'Etienne Leonard-Dufour',
  url = 'https://github.com/etienneld/watermelonpi',
  download_url = 'https://github.com/etienneld/watermelonpi/archive/0.3.tar.gz', # I'll explain this in a second
  keywords = ['raspberry pi', 'websockets', 'electronics'],
  classifiers = [],
)

