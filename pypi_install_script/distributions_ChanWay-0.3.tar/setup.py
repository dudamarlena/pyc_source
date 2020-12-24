from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='distributions_ChanWay',
      version='0.3',
      author='Udacity-ChanWay',
      author_email='chanwayng@u.nus.edu',
      description='Gaussian and binomial distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['distributions_ChanWay'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'
      ],
      zip_safe=False)
