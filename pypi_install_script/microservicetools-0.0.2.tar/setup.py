import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="microservicetools",
    version="0.0.2",
    author="Christo Crampton",
    author_email="christo@appointmentguru.co",
    description="General purpose tools for python microservices with DRF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SchoolOrchestration/libs/microservicetool",
    packages=['drf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
