import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rdme_cli",
    version="0.0.4",
    author="Aurelio Saraiva",
    author_email="aurelio.saraiva@creditas.com.br",
    description="Redme.io cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/creditas/rdme-cli",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["rdme-cli=rdme_cli:main"]},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "requests"
    ]
)
