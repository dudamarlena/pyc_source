from setuptools import setup

with open("prob_distribution/README.md", "r") as fh:
    long_description = fh.read()
setup(name='prob_distribution',
      version='0.2',
      description='Probability distributions',
      long_description = long_description,
      packages=['prob_distribution'],
      zip_safe=False)
