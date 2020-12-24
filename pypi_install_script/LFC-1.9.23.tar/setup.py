import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LFC",
    version="1.9.23",
    author="Reggles",
    author_email="reginaldbeakes@gmail.com",
    description="A lightweight event system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Reggles44/LFC",
    include_package_data=True,
    packages=['lfc', 'lfc.enums', 'lfc.tools'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    setup_requires=['flake8']
)
