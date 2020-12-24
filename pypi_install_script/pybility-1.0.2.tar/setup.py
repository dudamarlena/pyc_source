from setuptools import setup

setup(name='pybility',
      version = '1.0.2',
      description = 'Python probability distribution sampling and plotting',
      long_description=open('README').read(),
      packages = ['pybility', 'pybility.test'],
      install_requires = ['matplotlib', 'drawilleplot', 'Pillow', 'wheel'],
      include_package_data = True,
      package_dir = {'pybility':'pybility'},
      package_data = {'pybility': ['data/*.txt']},
      author = 'Marios Tsatsos',
      author_email = 'mariostsatsos@gmail.com',
      license = 'MIT',
      url = 'https://pypi.org/project/pybility/',
      zip_safe=False)
