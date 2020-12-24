from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'License :: OSI Approved :: GNU Affero General Public License v3',
  'Programming Language :: Python :: 3 :: Only',
]
 
setup(
  name='pixel-zero',
  version='0.0.3',
  description='A zero boilerplate neopixel control library for the Raspberry Pi ',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/AllAboutCode/pixelzero/',  
  author='Joshua Lowe',
  author_email='joshualowe1002@gmail.com',
  license='GPL', 
  classifiers=classifiers,
  keywords='Neopixels',
  packages=find_packages(),
  install_requires=['rpi_ws281x >= 3.0.3'] 
)
