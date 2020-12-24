from distutils.core import setup

setup(
  name = 'topsis101703074',
  packages = ['topsis101703074'],
  version = '0.1',
  license='MIT', 
  description = 'Calculates the topsis score from all int and float columns in data.',
  author = 'Ankita',
  author_email = 'ankitauppal99@gmail.com',
  url = 'https://github.com/ankita987/topsis101703074',
  download_url = 'https://github.com/ankita987/topsis101703074/archive/v_01.tar.gz',
  keywords = ['TOPSIS'],
  install_requires=[
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)