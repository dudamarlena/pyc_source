from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='betahaus.maps.openmember',
      version=version,
      description="Google maps support for betahaus.openmember",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='openmember plone csv maps',
      author='Betahaus',
      author_email='martin@betahaus.net',
      url='http://www.betahaus.net',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['betahaus', 'betahaus.maps'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'betahaus.openmember',
          'geopy',
          'BeautifulSoup',
          'simplejson',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
