from setuptools import setup
import setuptools

setup(name='quant_utils',
      version='0.1',
      description='Python Utility Functions for Quant team',
      url='https://github.com/guzman-energy/quant_utils',
      download_url='https://github.com/guzman-energy/quant_utils/archive/v01.tar.gz',
      author='Tianchen Wang@Guzman Energy',
      author_email='twang@guzmanenergy.com',
      packages=setuptools.find_packages(),
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
        'mysql-connector',
        'sqlalchemy',
        'numpy', 
        'pandas',
        'colorama'
      ],
      zip_safe=False)