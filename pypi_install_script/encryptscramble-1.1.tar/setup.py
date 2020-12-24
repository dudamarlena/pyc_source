from distutils.core import setup
setup(
  name = 'encryptscramble',
  packages = ['encryptscramble'],
  version = '1.1',
  license='MIT',
  description = 'Code to make easy use of Pythons cryptography module with some additional text scrambling functions.',
  author = 'ragardner',
  author_email = 'ragardner@protonmail.com',
  url = 'https://github.com/ragardner/encryptscramble',
  download_url = 'https://github.com/ragardner/encryptscramble/archive/1.1.tar.gz',
  keywords = ['encrypt', 'encryption', 'aes'],
  install_requires=["cryptography"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
