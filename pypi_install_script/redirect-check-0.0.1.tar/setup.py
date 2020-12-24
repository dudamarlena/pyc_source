from setuptools import setup

setup(name='redirect-check',
      version='0.0.1',
      description='tool to check for ssrf\'s to internal resources from open redirects',
      url='https://github.com/incredincomp/redirect-check',
      author='IncredIncomp',
      author_email='incredincomp@gmail.com',
      license='',
      packages=['redirect-check'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
