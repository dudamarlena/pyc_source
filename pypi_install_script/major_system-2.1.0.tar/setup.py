from setuptools import setup

setup(
  name = "major_system",
  version = "2.1.0",
  author = "John Baber-Lucero",
  author_email = "pypi@frundle.com",
  description = ("Python libraries and scripts for converting numbers using the Mnemonic Major System"),
  license = "GPLv3",
  url = "https://github.com/jbaber/major_system",
  packages = ['major_system'],
  package_data = {
    'major_system': ['cmu_phonetic_dictionary/cmudict-0.7b'],
  },
  install_requires = ['docopt'],
  tests_require=['pytest'],
  entry_points = {
    'console_scripts': ['major_words=major_system.major_system:main'],
  }
)
