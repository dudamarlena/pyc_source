import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

DESCRIPTION = "New Contributor Wizard is a GUI application build to help new contributors get started with Open Source."

install_requires = [
    "cython==0.28",
    "kivy==1.10.1",
    "python-gnupg==0.4.3",
    "requests==2.19.1"
]

setuptools.setup(
    name="new_contributor_wizard",
    version="0.0.5",
    author="Shashank Kumar",
    author_email="shashankkumarkushwaha@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://salsa.debian.org/new-contributor-wizard-team/new-contributor-wizard",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={
        '': ['README.md', 'LICENSE'],
        'new_contributor_wizard': [
            'ui/*',
            'ui/assets/fonts/*',
            'ui/assets/images/*',
            'ui/encryption/*',
            'ui/module_box/*',
            'ui/parsers/*',
            'data/module_data.json',
            'modules/course_modules/blog/tutorials/*.json',
            'modules/course_modules/command_line_interface/tutorials/*.json',
            'modules/course_modules/communication/tutorials/*.json',
            'modules/course_modules/encryption/tutorials/*.json',
            'modules/course_modules/how_to_use/*.json',
            'modules/course_modules/version_control_system/tutorials/*.json',
            'modules/course_modules/way_ahead/tutorials/*.json',
            'libs/garden/navigationdrawer/*'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    scripts=['bin/new-contributor-wizard'],
)
