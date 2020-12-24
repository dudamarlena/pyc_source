from setuptools import setup, find_packages


setup(
    name = 'IORedprint',
    packages = ['IORedprint'],   
    include_package_data=True,    # muy importante para que se incluyan archivos sin extension .py
    version = '1.0.0',
    description = 'xd',
    author='Elsa Bandija',
    author_email="elsa_bandija@gmail.com",
    license="GPLv3",
    url="https://github.com/raflorez/IORedprint.git",
    classifiers = ["Programming Language :: Python :: 3",\
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",\
        "Development Status :: 4 - Beta", "Intended Audience :: Developers", \
        "Operating System :: OS Independent"]
    )
