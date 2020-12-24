from setuptools import setup, find_packages
import sys, os

README = open('README.md').read()

setup(name='pyunet',
    version='0.0.14.0',
    description='Unit tests using decrators',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing :: Unit',
      ],
    keywords='unit test testing decorator',
    author='saledddar',
    author_email='saledddar@gmail.com',
    url='https://github.com/saledddar/pyunet',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages = ['pyunet'],
    install_requires=[]
)
