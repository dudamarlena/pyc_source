from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(name='distGB_probability',
      version='0.3',
      description='Gaussian and Binomial distributions',
      packages=['distGB_probability'],
      author='Aritra Ghosh',
      author_email = 'aritra.dravid007@gmail.com',
      long_description = long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)
