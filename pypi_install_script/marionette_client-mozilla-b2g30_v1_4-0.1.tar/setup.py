import os
from setuptools import setup, find_packages

version = '0.1'

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

setup(name='marionette_client-mozilla-b2g30_v1_4',
      version=version,
      description="Marionette test automation client",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Jonathan Griffin',
      author_email='jgriffin@mozilla.com',
      url='https://wiki.mozilla.org/Auto-tools/Projects/Marionette',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={'marionette': ['touch/*.js']},
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      marionette = marionette.runtests:cli
      """,
      install_requires=deps,
      )

