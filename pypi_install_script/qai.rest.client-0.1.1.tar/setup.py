from distutils.core import setup
import setuptools

setup(
    name='qai.rest.client',
    packages=setuptools.find_packages(),
    version='0.1.1',
    license='unlicensed',
    description='Client for rest service.',
    author='manhal@qordoba.com',
    python_requires='>=3.6.0',
    url='https://github.com/Qordobacode/qai.rest.client',
    download_url='https://github.com/Qordobacode/qai.rest.client/archive/0.1.0.tar.gz',
    install_requires=[
        'requests>=2.22.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data=True
)
