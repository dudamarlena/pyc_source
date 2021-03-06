from setuptools import setup, find_packages
import os

version = '1.3'

setup(name='slc.aggregation',
      version=version,
      description="Provides an aggregation solution aimed at Plone sites with "
                    "many different language versions",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='syslab plone resource centralisation',
      author='JC Brand, Syslab.com GmbH',
      author_email='brand@syslab.com',
      url='http://plone.org/products/slc.aggregation',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['slc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.common',
          'p4a.z2utils',
          'p4a.subtyper',
          'archetypes.schemaextender',
          'Products.AdvancedQuery',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      paster_plugins = ["ZopeSkel"],
      )

