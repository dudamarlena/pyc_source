import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-cms-headless-test", # Replace with your own username
    version="0.0.1.dev3",
    author="Sunil Chaudhary",
    author_email="sunil12738@gmail.com",
    description="A package to run djangocms in headless mode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=[
        'django_cms_headless_test',
    ],
    include_package_data=True,
    install_requires=[
        'django-cms>=3.0',
        'djangorestframework>=3.5.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
