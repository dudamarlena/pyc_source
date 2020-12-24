from distutils.core import setup

setup(
  name = 'managedState',
  packages = ['managedState', 'managedState.listeners', 'managedState.registrar'],
  version = 'v1.4.0',
  license='GPLv3',
  description = 'State management inspired by Redux',
  author = 'immijimmi',
  author_email = 'imranhamid99@msn.com',
  url = 'https://github.com/immijimmi/managedState',
  download_url = 'https://github.com/immijimmi/managedState/archive/v1.4.0.tar.gz',
  keywords = ['state', 'managed', 'management', 'access'],
  install_requires=[
      'objectExtensions>=1.4.0'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.6',
  ],
)
