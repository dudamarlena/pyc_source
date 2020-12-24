from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='udc_dsnd_distributions',
      version='1.9',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['udc_dsnd_distributions'],
      author = 'Gaurav Ansal',
      author_email = 'ansal.gaurav@gmail.com',
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],  )
