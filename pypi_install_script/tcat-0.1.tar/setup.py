from setuptools import setup, find_packages

setup(
    name = 'tcat',
    packages = find_packages(),
    version = '0.1',
    description = 'PSF photometry for TESS', 
    author = 'Tansu Daylan & Maximilian N. Guenther',
    author_email = 'tansu.daylan@gmail.com',
    url = 'https://github.com/tdaylan/tcat',
    download_url = 'https://github.com/tdaylan/tcat', 
    license='MIT',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python'],
    #install_requires=['astrophy>=3'],
    include_package_data = True
    )

