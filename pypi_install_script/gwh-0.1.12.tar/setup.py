from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="gwh",
    version=__import__('gwh').__version__,
    keywords="git webhook bitbucket gitlab",
    description="Tool for handling Git webhooks",
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    platforms="any",
    author="oqwa",
    author_email="oqwa@inbox.lv",
    license="MIT",
    url="https://github.com/oqwa/gwh",
    install_requires=[],
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False
)
