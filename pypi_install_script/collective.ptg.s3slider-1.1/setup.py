from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='collective.ptg.s3slider',
      version=version,
      description="Adds s3slider to collective.plonetruegallery",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone plonetruegallery addon',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='https://github.com/collective/collective.ptg.s3slider',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.ptg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.plonetruegallery >= 3.2a1'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
