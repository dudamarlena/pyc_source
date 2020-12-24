from distutils.core import setup

setup(
  name = 'gammaspectra',
  packages = ['gammaspectra'],
  version = '0.1',
  license='GNU v3.0',
  description = 'Software for gamma spectroscopy analysis',
  author = 'Edoardo Proserpio',
  author_email = 'edoardo.proserpio@gmail.com',
  url = 'https://github.com/EdoPro98/gammaspectra',
  download_url = 'https://github.com/EdoPro98/gammaspectra/archive/v0.1.tar.gz',
  keywords = ['gamma', 'spectrum', 'analysis','data','radioactivity'],
  install_requires=[
          'numpy',
          'scipy',
      ],
classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
