from distutils.core import setup
pkg_version='0.4.2'
setup(
  name = 'startech',
  packages = ['startech'],
  version = pkg_version,
  license='MIT',
  description = 'A small library made to make common tasks easier',
  author = 'Star Technology',
  author_email = 'startechsheffield@gmx.com',
  url = 'https://github.com/startechsheffield/startech',
  download_url = 'https://github.com/startechsheffield/startech/archive/'+pkg_version+'.tar.gz',
  keywords = ['SMALL', 'CONVENIENCE', 'RELEASE-CANDIDATE'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
