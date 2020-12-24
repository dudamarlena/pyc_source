from distutils.core import setup

setup(
  name = 'nato_phonetic',
  packages = ['nato_phonetic'],
  version = '1.1.1',
  license='MIT',
  description = 'Package to give NATO phonetic translation',
  author = 'Sonaal P. Pradeep',
  author_email = 'unofficial.sonaal@gmail.com',
  url = 'https://github.com/sonaalPradeep/phonetic',
  download_url = 'https://github.com/sonaalPradeep/phonetic/archive/v1.1.1.tar.gz',
  keywords = ['NATO', 'ICAO', 'PHONETIC', 'TRANSLATION'],
  install_requires=['requests', 'beautifulsoup4'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)
