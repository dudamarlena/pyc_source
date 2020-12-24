#  -*- coding: utf-8 -*-
"""

Author: Rafael Rodrigues Luz Benevides
Date of creation: 20/12/2019

"""

from distutils.core import setup


setup(
    name='tstools',
    version='1.0.0',
    packages=['tstools'],
    license='MIT',
    description='Time Series tools',
    author="Rafael Rodrigues Luz Benevides",
    author_email="rafaeluz821@gmail.com",
    url='',
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'scipy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
  ],
)