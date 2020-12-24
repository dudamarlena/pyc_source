import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'djangoca',
    version = '0.2',
    packages = find_packages(),
    include_package_data=True,
    license = 'MIT License',  # example license
    description = 'Base para Proyectos Django con CRUDS Automáticos',
    url = 'https://github.com/developerpe/paquete_base_django',
    author = 'Oliver Ton Sandoval Arévalo',
    author_email = 'developerpeperu@gmail.com',
    classifiers = ["Programming Language :: Python :: 3",\
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",\
        "Development Status :: 4 - Beta", "Intended Audience :: Developers", \
        "Operating System :: OS Independent"],
)
