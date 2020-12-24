from setuptools import setup, find_packages

version = "0.3.4"

setup(name="pxp",
      version=version,
      license="MIT",
      platforms="any",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      packages=find_packages(exclude=["config", "tests"]),
      description="A simple python-hosted expression language.",
      url="https://gitlab.com/tcucco/pxp",
      download_url="https://gitlab.com/tcucco/pxp/-/archive/master/pxp-master.tar",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4"
      ],
      install_requires=["pyebnf>=0.1.1"])
