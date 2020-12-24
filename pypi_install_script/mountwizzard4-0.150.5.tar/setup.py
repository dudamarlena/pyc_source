############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
#
# Michael Würtenberger
# (c) 2019, 2020
#
# Licence APL2.0
#
###########################################################
from setuptools import setup
from pathlib import Path

setup(
    name='mountwizzard4',
    version='0.150.5',
    packages=[
        'mw4',
        'mw4.astrometry',
        'mw4.base',
        'mw4.cover',
        'mw4.dome',
        'mw4.environment',
        'mw4.gui',
        'mw4.gui.widgets',
        'mw4.gui.mainWmixin',
        'mw4.imaging',
        'mw4.measure',
        'mw4.modeldata',
        'mw4.powerswitch',
        'mw4.remote',
        'mw4.resource',
        'mw4.telescope',
    ],
    python_requires='>=3.6.0, <3.9',
    install_requires=[
        'mountcontrol==0.160',
        'indibase==0.132',
        'PyQt5==5.14.1; platform_machine != "armv7l"',
        'PyQtWebEngine==5.14.0; platform_machine != "armv7l"',
        'matplotlib==3.2.1',
        'astropy==4.0',
        'requests==2.22.0',
        'requests_toolbelt==0.9.1',
        'numpy==1.18.1',
        'skyfield==1.18',
        'qimage2ndarray==1.8.2',
        'importlib_metadata==1.3.0',
        'opencv-python-headless==4.1.2.30',
    ],
    url='https://github.com/mworion/MountWizzard4',
    license='APL 2.0',
    author='mworion',
    author_email='michael@wuertenberger.org',
    description='tooling for a 10micron mount',
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    long_description_content_type="text/x-rst",
    project_urls={
        'Documentation': 'https://mountwizzard4.readthedocs.io',
        'Source Code': 'https://github.com/mworion/mountwizzard4',
        'Bug Tracker': 'https://github.com/mworion/mountwizzard4/issues',
        'Forum': 'https://www.10micron.eu/forum/',
    },
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Other Environment',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Topic :: Documentation :: Sphinx',
    ]
)
