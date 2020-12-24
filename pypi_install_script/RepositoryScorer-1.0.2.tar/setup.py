from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='RepositoryScorer',
    description='Module to compute how well-engineered a project is',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Stefano Dalla Palma',
    author_email='stefano.dallapalma0@gmail.com',
    version='1.0.2',
    packages=find_packages(exclude='test'),
    url='https://github.com/stefanodallapalma/repository-scorer',
    download_url='https://github.com/stefanodallapalma/repository-scorer/archive/1.0.2.tar.gz',
    license='Apache License',
    package_dir={'repositoryscorer': 'repositoryscorer'},
    python_requires='>=3.7',
    install_requires=requirements,
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            "Operating System :: OS Independent"
    ]
)
