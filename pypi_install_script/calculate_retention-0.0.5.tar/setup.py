from setuptools import setup, find_packages

# try:
#     import pypandoc
#
#     long_descr = pypandoc.convert('README.md', 'rst')
# except(IOError, ImportError):
#     long_descr = open('README.md').read()

setup(name='calculate_retention',
      version='0.0.5',
      description='Simple package designed to calculate end-to-end user retention metrics',
      long_description=None,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Information Technology',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering :: Information Analysis',
      ],
      keywords='retention',
      url='',
      author='Darshil Desai',
      author_email='darshildee@gmail.com',
      license='MIT',
      packages=['calculate_retention'],
      install_requires = ['pandas', 'numpy', 'seaborn', 'matplotlib'],
      # packages=find_packages(where='src'),
      # package_dir={'': 'src'},
      # include_package_data=True,
      # install_requires=['pandas==0.24.2', 'numpy==1.16.2', 'seaborn==0.9.0', 'matplotlib==3.0.3'],
      zip_safe=False)
