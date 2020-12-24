import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as requ:
    install_requires = [line.strip() for line in requ if line.strip()]

setuptools.setup(
    name='django_yx_app',
    version="0.0.3",
    author="yijie zeng",
    author_email="axplus@163.com",
    description="evernote helper app of django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/axplus/django_yx_app",
    packages=['yx', 'yx.sync', 'yx.management', 'yx.management.commands'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
    install_requires=install_requires,
# include_package_data=True,
)
