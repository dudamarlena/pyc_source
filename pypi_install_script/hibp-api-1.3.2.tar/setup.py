# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(

    name='hibp-api',
    version="1.3.2",
    packages=find_packages(),
    author="megadose",
    install_requires=["cfscrape","argparse","urllib3","requests"],
    author_email="anonymous@notmymail.com",
    description="Permet d'utiliser l'api de HIBP gratuitement",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/megadose/hibp-api',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points = {
        'console_scripts': [
            'hibp_python-sm = hibp_python.core:hibp',
        ],
    },
    license = 'GPLv3',
)
