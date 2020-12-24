from setuptools import setup

setup(name='FunniestTestPyPi',
      version='0.1.4',
      description='The funniest joke in the world',
      url='http://github.com/MaxMifkovic/FunniestTestPyPi',
      author='Max Mifkovic',
      author_email='maxmifkovic@gmail.com',
      license='MIT',
      packages=['FunniestTestPyPi'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)
