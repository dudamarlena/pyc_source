from setuptools import setup

setup(name='patools',
      version='0.2',
      description='A collection of tools for analyzing particle packings',
      url='https://github.com/amas0/patools',
      author='Andrew Mascioli',
      author_email='andrew.mascioli1@gmail.com',
      license='MIT',
      packages=['patools'],
      install_requires=[
          'numpy',
          'scipy',
          'pandas'
      ],
      zip_safe=False)
