from setuptools import setup, find_packages

VERSION = '1.0.3'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='repository-scorer',
    description='Module to compute how well-engineered a project is',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Stefano Dalla Palma',
    author_email='stefano.dallapalma0@gmail.com',
    version=VERSION,
    packages=find_packages(exclude='tests'),
    url='https://github.com/stefanodallapalma/repository-scorer',
    download_url=f'https://github.com/stefanodallapalma/repository-scorer/archive/{VERSION}.tar.gz',
    license='Apache License',
    package_dir={'repositoryscorer': 'repositoryscorer'},
    python_requires='>=3.7',
    install_requires=['python-dotenv==0.10.5',
                      'PyDriller==1.15',
                      'PyGithub==1.51'],
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
