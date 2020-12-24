import glob
from distutils.core import setup

setup(
  name = 'arbitrator',
  packages = ['arbitrator'],
  scripts=glob.glob('bin/*'),
  version = '0.6',
  description = 'An implementation of Basic Paxos - substrate for building higher level synchronization primitives',
  long_description = 'An implementation of Basic Paxos - substrate for building higher level synchronization primitives<br>Go to https://github.com/magicray/arbitrator for details',
  author = 'Bhupendra Singh',
  author_email = 'bhsingh@gmail.com',
  url = 'https://github.com/magicray/arbitrator',
  keywords = ['distributed', 'paxos', 'consensus', 'synchronization', 'leader'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.7'
  ],
)
