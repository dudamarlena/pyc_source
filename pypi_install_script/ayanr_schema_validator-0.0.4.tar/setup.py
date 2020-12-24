import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="ayanr_schema_validator",
    version="0.0.4",
    author="rams3sh",
    description="Python ayanR Schema Validator for validating ayanR engine schemas",
    packages=["ayanr_schema_validator"],
    entry_points= {'console_scripts' : ['ayanr_schema_validator=ayanr_schema_validator.cli:main']},
    include_package_data=True,
    install_requires=required,
    python_requires='>=3.6',
)
