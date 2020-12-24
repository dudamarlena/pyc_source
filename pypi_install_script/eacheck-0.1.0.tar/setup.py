from setuptools import setup, find_packages

from eacheck import VERSION

install_requires = [
    'lxml>=4.0'
]

tests_require = []

setup(
    name="eacheck",
    version=VERSION,
    description="Library to valida XML agains EruditArticle Schema. ",
    author="Érudit",
    author_email="fabio.batalha@erudit.org",
    maintainer="Fabio Batalha",
    maintainer_email="fabio.batalha@erudit.org",
    url="http://github.com/fabiobatalha/converter",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    dependency_links=[],
    tests_require=tests_require,
    test_suite='tests',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'eacheck=eacheck.console_script:main'
        ]
    }
)
