from pathlib import Path

from setuptools import setup, find_packages


if __name__ == "__main__":

    base_dir = Path(__file__).parent
    src_dir = base_dir / 'src'

    about = {}
    with (src_dir / "turbo_disco" / "__about__.py").open() as f:
        exec(f.read(), about)

    # with (base_dir / "README.rst").open() as f:
    #     long_description = f.read()

    install_requirements = [
        "pytest" # should be in test requirements
    ]
    interactive_requirements = []
    test_requirements = []
    doc_requirements = []

    setup(
        name=about['__title__'],
        version=about['__version__'],

        description=about['__summary__'],
        # long_description=long_description,
        # license=about['__license__'],
        url=about["__uri__"],

        author=about["__author__"],
        author_email=about["__email__"],

        # # Advertsing package to people
        # classifiers=[],

        # Look inside source directory for package, instead of same name in
        # root dir
        package_dir={'': 'src'},
        packages=find_packages(where='src'),

        include_package_data=True,

        install_requires=install_requirements,
        # tests_require=test_requirements,
        extras_require={
            'docs': doc_requirements,
            'test': test_requirements,
            'interactive': interactive_requirements,
            'dev': doc_requirements + test_requirements + interactive_requirements,
        },

        # This sets up applications
        #entry_points="""
        #        [console_scripts]
        #        simulate=vivarium.interface.cli:simulate
        #    """,

        zip_safe=False,

    )
