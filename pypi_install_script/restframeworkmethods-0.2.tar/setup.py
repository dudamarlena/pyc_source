#!/usr/bin/env python

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 17/10/15
"""

from setuptools import setup, find_packages

setup(name="restframeworkmethods",
      version="0.2",
      packages=find_packages(),
      include_package_data=True,
      description="Modules to REST API",
      description_file="README.md",

      author="Yeison Cardona",
      author_email="yeison.eng@gmail.com",
      maintainer="Yeison Cardona",
      maintainer_email="yeison.eng@gmail.com",

      url="https://bitbucket.org/YeisonEng/python-restframeworkmethods",
      download_url="https://bitbucket.org/YeisonEng/python-restframeworkmethods/downloads",

      license="BSD 3-Clause",
      install_requires=["django", "djangorestframework"],
      keywords='django',

      classifiers=[  # list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers
                   "Development Status :: 3 - Alpha",
                   "Framework :: Django",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Programming Language :: Python :: 3",
                   "Topic :: Software Development :: Libraries :: Application Frameworks",
      ],
      )
