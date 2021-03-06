from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.remove.kupu',
      version=version,
      description="Remove kupu from Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='JeanMichel FRANCOIS',
      author_email='jeanmichel.francois@makina-corpus.org',
      url='http://svn.plone.org/svn/collective/collective.remove/kupu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.remove'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
