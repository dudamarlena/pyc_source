# This file was automatically generated by Shore. Do not edit manually.
# For more information on Shore see https://pypi.org/project/nr.shore/

import io
import re
import setuptools
import sys

with io.open('src/shore/__init__.py', encoding='utf8') as fp:
  version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

with io.open('README.md', encoding='utf8') as fp:
  long_description = fp.read()

requirements = ['beautifulsoup4 >=4.8.1,<5.0.0', 'click >=7.0,<8.0.0', 'jinja2 >=2.11.1,<3.0.0', 'networkx >=2.4,<3.0.0', 'nr.databind.core >=0.0.1,<0.1.0', 'nr.databind.json >=0.0.1,<0.1.0', 'nr.fs >=1.5.0,<2.0.0', 'nr.pylang.utils >=0.0.1,<1.0.0', 'nr.proxy >=0.0.1,<1.0.0', 'requests >=2.22.0,<3.0.0', 'packaging >=20.1,<21.0.0', 'PyYAML >=5.1.0,<6.0.0', 'termcolor >=1.1.0,<2.0.0', 'twine']

setuptools.setup(
  name = 'nr.shore',
  version = version,
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  description = 'Automates the heavy lifting of release and distribution management for pure Python packages.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://git.niklasrosenstein.com/NiklasRosenstein/shore',
  license = 'MIT',
  packages = setuptools.find_packages('src', ['test', 'test.*', 'docs', 'docs.*']),
  package_dir = {'': 'src'},
  include_package_data = True,
  install_requires = requirements,
  extras_require = {},
  tests_require = [],
  python_requires = None, # TODO: '>=2.7,<3.0.0|>=3.4,<4.0.0',
  data_files = [],
  entry_points = {
    'console_scripts': [
      'shore = shore.__main__:_entry_point',
      'shore-conda-forge = shore.tools.conda_forge:main',
    ],
    'shore.core.plugins': [
      'core = shore.plugins.core:CorePlugin',
      'install-script = shore.plugins.install_script:InstallScriptRenderer',
      'pypi = shore.plugins.pypi:PypiPublisher',
      'requirements-file = shore.plugins.requirements_file:RequirementsFileRenderer',
      'setuptools = shore.plugins.setuptools:SetuptoolsRenderer',
    ]
  },
  cmdclass = {},
  keywords = [],
  classifiers = [],
)
