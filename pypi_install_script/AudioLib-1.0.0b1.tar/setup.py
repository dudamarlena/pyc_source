from setuptools import setup, find_packages

long_description = open("README.rst", "r").read()

setup(name='AudioLib',

      version='1.0.0b1',

      description='A high level sounds api for python',

      long_description=long_description,
      long_description_content_type='text/x-rst',

      url='https://github.com/HelloWorld-py/AudioLib',
      author='Jacob Tsekrekos',
      author_email='jdtsekrekos@live.com',

      keywords='audio sound media wav player',

      license='MIT',
      packages=find_packages(),
      install_requires=['pyaudio'])
