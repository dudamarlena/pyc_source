from setuptools import setup, find_packages
import os

version = '1.0.5.1'

setup(name='collective.ptg.thumbnailzoom',
      version=version,
      description="Adds a 'thumbnailzoom' view to collective.plonetruegallery",
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
      url='https://github.com/collective/collective.ptg.thumbnailzoom',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.ptg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.plonetruegallery'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
