import setuptools

setuptools.setup(
      name="d-snek-cogs-quote",
      version="0.0.1a2",
      author="Jonathan de Jong",
      author_email="jonathan@automatia.nl",
      description="Discord SNEK Cog; Quote",
      url="https://git.jboi.dev/ShadowJonathan/snek-quote",
      packages=[],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires=">=3.6",
      install_requires=["uninstallable > 0"],
      setup_requires=["wheel"],
      extras_require={
            "dev": ["ipython", "twine", "bump2version"],
      }
)
