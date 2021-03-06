from setuptools import setup, find_packages
import os

version = '1.2.2'

setup(name='collective.atimage.transformmenu',
      version=version,
      description="'Transforms' menu in Image and News Item to perform image transformations",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read()  + "\n" +
                       open(os.path.join("docs", "AUTHORS.txt")).read()  + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='marcosfromero',
      author_email='marcos.romero {at} inter-cultura {dot} com',
      url='http://svn.plone.org/svn/collective/collective.atimage.transformmenu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.atimage'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-,
          'simplejson',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
