import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "yoginth",
    packages = ["yoginth"],
    entry_points = {
        "console_scripts": ['yoginth = yoginth.yoginth:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "2.1.1",
    description = "The Yoginth CLI",
    author = "Yoginth",
    author_email = "yoginth@protonmail.com",
    url = "https://yoginth.com",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Source': 'https://gitlab.com/yo/yoginth',
    },
    install_requires=[
        'colorama',
        'superb',
        'requests',
    ],
)
