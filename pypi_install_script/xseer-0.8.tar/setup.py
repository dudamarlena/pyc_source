from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'xseer',
  packages = ['xseer'],
  version = '0.8',
  license='MIT',
  description = 'Extremely fast denoising of stellar spectra using deep learning',
  long_description = long_description,
  long_description_content_type='text/markdown',
  author = 'Rushil Mallarapu',
  author_email = 'rushil.mallarapu@gmail.com',
  url = 'https://github.com/sudo-rushil/xseer',
  download_url = 'https://github.com/sudo-rushil/xseer/archive/v0.8.tar.gz',
  keywords = ['astronomy', 'python', 'astropy', 'seer', 'exoplanets', 'spectra', 'star'],
  include_package_data=True,
  install_requires=[
          'numpy',
          'tensorflow',
          'astropy',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ])