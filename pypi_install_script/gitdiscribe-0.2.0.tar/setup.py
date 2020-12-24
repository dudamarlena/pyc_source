import sys
sys.path.insert(0, '..')

from distutils.core import setup
from gitdiscribe import Gitdiscribe

gd = Gitdiscribe('.')
if gd.tag != '':
  VERSION = gd.tag_number
  gd.write_version_file()
else:
  from version import VERSION

setup(name = 'gitdiscribe',
      version = VERSION,
      description = 'Derives version numbers from git tags.',
      author = 'Thelonius Kort',
      author_email = 'the_lo_ni_us@banza.net',
      url = 'https://bitbucket.org/th3l0nius/gitdiscribe',
      packages = [ 'gitdiscribe' ],
      package_dir = {'gitdiscribe': '.'}
      )
