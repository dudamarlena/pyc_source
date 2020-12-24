
from setuptools import setup, find_packages, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pluspad',
      version='0.0.1',
      description='Following the create your own editor tutorial for quarantaine fun',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/dicaso/pluspad',
      author='Christophe Van Neste',
      author_email='christophe.vanneste@kaust.edu.sa',
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.6',
      ext_modules=[
          Extension(
              'pluspad_c',
              sources=['pluspad_c/src/pluspad.c'],
              py_limited_api=True
          )
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX",
          "Development Status :: 1 - Planning"
      ],
      install_requires=[
      # Requirements:
      ],
      extras_require={
          'documentation': ['Sphinx']
      },
      package_data={},
      include_package_data=True,
      zip_safe=False,
      entry_points={},
      test_suite='nose.collector',
      tests_require=['nose']
      )

# To install with symlink, to make changes immediately available:
# pip install -e .
