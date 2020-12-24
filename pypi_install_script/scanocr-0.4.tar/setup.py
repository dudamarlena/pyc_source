from distutils.core import setup

setup(
    # Application name:
    name="scanocr",

    # Version number (initial):
    version="0.4",

    # Application author details:
    author="ganesh singamaneni",
    author_email="ganesh@caratred.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/scanocr_v010/",

    #
    license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "alembic==1.0.3",
        "aniso8601==4.0.1",
        "autoenv==1.0.0",
        "blinker==1.4",
        "cachetools==2.1.0",
        "certifi==2018.8.13",
        "chardet==3.0.4",
        "Click==7.0",
        "clickclick==1.2.2",
        "connexion==2.0.2",
        "dateparser==0.7.0",
        "Flask==1.0.2",
        "Flask-Cors==3.0.7",
        "Flask-DotEnv==0.1.1",
        "Flask-Environments==0.1",
        "Flask-Exceptions==1.2.1",
        "Flask-JWT-Extended==3.13.1",
        "Flask-Mail==0.9.0",
        "flask-marshmallow==0.9.0",
        "Flask-Migrate==2.3.0",
        "Flask-MySQLdb==0.2.0",
        "Flask-RESTful==0.3.6",
        "Flask-Script==2.0.6",
        "Flask-SQLAlchemy==2.1",
        "google-api-core==1.3.0",
        "google-auth==1.5.1",
        "google-cloud-vision==0.33.0",
        "googleapis-common-protos==1.5.3",
        "grpcio==1.14.1",
        "idna==2.7",
        "inflection==0.3.1",
        "itsdangerous==1.1.0",
        "Jinja2==2.10",
        "jsonschema==2.6.0",
        "Mako==1.0.7",
        "MarkupSafe==1.1.0",
        "marshmallow==2.16.3",
        "marshmallow-sqlalchemy==0.15.0",
        "mrz==0.3.5",
        "mysql-connector==2.1.6",
        "mysqlclient==1.3.13",
        "numpy==1.15.4",
        "openapi-spec-validator==0.2.4",
        "opencv-python==3.4.4.19",
        "pandas==0.23.4",
        "passlib==1.7.1",
        "Pillow==5.3.0",
        "protobuf==3.6.1",
        "pyasn1==0.4.4",
        "pyasn1-modules==0.2.2",
        "PyJWT==1.6.4",
        "python-dateutil==2.7.5",
        "python-editor==1.0.3",
        "pytz==2018.5",
        "PyYAML==3.13",
        "pyzbar==0.1.7",
        "regex==2018.11.22",
        "requests==2.19.1",
        "rsa==3.4.2",
        "scipy==1.1.0",
        "six==1.11.0",
        "SQLAlchemy==1.2.14",
        "typing==3.6.6",
        "tzlocal==1.5.1",
        "urllib3==1.23",
        "Werkzeug==0.14.1",
        "xmltodict==0.11.0"
    ],
)
