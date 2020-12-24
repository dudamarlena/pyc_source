from distutils.core import setup
setup(
  name = 'mild',
  packages = ['mild'],
  version = '0.5',
  license='GPLv3',
  description = 'Tiny build system in Python3',
  author = 'Mark Hargreaves',
  author_email = 'clashclanacc2602@gmail.com',
  url = 'https://github.com/nergzd723/mild',
  download_url = 'https://github.com/nergzd723/mild/archive/v_05.tar.gz',
  keywords = ['build', 'build-system', 'util'],
  install_requires=[
          'termcolor',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
  ],
)