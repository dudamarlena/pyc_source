from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='majorly_funny',
      version='0.5.0',
      description='A majorly funny joke',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['majorly_funny'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')