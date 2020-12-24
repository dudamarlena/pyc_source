from setuptools import setup, find_packages
import os

version = '0.1b2'

setup(name='betahaus.exports.openmember',
      version=version,
      description="Exports for the betahaus.openmember",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='openmember plone csv exports',
      author='Betahaus',
      author_email='martin@betahaus.net',
      url='http://www.betahaus.net',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['betahaus', 'betahaus.exports'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'betahaus.openmember',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
