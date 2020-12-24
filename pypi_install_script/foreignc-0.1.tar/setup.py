from distutils.core import setup
setup(
  name = 'foreignc',
  packages = ['foreignc'],
  version = '0.1',
  license='apache-2.0',
  description = 'This is the recieving side of the foreignc rust crate',
  author = 'Martin Pinholt',
  author_email = 'mapi@itu.dk',
  url = 'https://github.com/mart368b/foreignc_py',
  download_url = 'https://github.com/mart368b/foreignc_py/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['ffi', 'rust', 'foreignc'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)