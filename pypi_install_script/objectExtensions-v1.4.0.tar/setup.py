from distutils.core import setup

setup(
  name = 'objectExtensions',
  packages = ['objectExtensions'],
  version = 'v1.4.0',
  license='GPLv3',
  description = 'A basic framework for implementing an extension pattern',
  author = 'immijimmi',
  author_email = 'imranhamid99@msn.com',
  url = 'https://github.com/immijimmi/objectExtensions',
  download_url = 'https://github.com/immijimmi/objectExtensions/archive/v1.4.0.tar.gz',
  keywords = ['extensions', 'plugins'],
  install_requires=[
      'wrapt>=1.11.2'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.6',
  ],
)
