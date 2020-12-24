from setuptools import setup, find_packages

setup(name="smartpyredis",
      version="0.1",
      author="Prashant Gaur",
      author_email = "91prashantgaur@gmail.com",
      description = "To handle redis commands",
      url = "http://gaurprashant.blogspot.in",
      packages=find_packages(),
      install_requires=[
            "redis",
        ],
      include_package_data=True,
      )
