from setuptools import setup
from setuptools import find_packages


if __name__ == "__main__":
    setup(
        name="cnlp",
        version="0.1.1",
        author="Ailln",
        author_email="kinggreenhall@gmail.com",
        url="https://github.com/Ailln/cnlp",
        license="MIT License",
        description="A natural language processing framework focused on Chinese.",
        packages=find_packages(),
        include_package_data=True,
        install_requires=open("./requirements.txt", "r").read().splitlines(),
        long_description=open("./README.md", "r").read(),
        long_description_content_type="text/markdown",
        entry_points={
            "console_scripts": ["cnlp=cnlp.shell:run"]
        },
        package_data={
            "cnlp": ["cnlp/src/*.txt"]
        },
        zip_safe=True,
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ]
    )
