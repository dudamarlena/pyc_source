from setuptools import find_packages, setup

setup(
    name='zeppsta-webapp',
    version='0.1.23',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    url='http://github.com/zepp-lee/zeppsta-webapp',
    author='Zepp Lee',
    author_email='me@seble.info',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        # Core dependencies
        'Django==1.11.18',
        'django-htmlmin==0.10.0',
        'djangorestframework==3.9.1',
        'Jinja2==2.10',
        'psycopg2-binary==2.7.5',
        'waitress==1.2.1',
    ],
    extras_require={
        # Dependencies specific to the local (aka "dev") environment
        'local': [
            'django-debug-toolbar==1.11',
            'django-extensions==2.1.4',
            'notebook==5.7.4',
        ],

        # Alternative DB backends
        'mysql': [
            'mysqlclient==1.4.1',
        ],

        # Optional feature dependencies
        'email_username': [
            'django-custom-user==0.7',
        ],
        'enumfields': [
            'django-enumfields==1.0.0',
        ],
        'file_storage': [
            'django-storages==1.7.1',
            'paramiko==2.4.2',
        ],
        'ordered_models': [
            'django-ordered-model==2.1.0'
        ],
        'registration': [
            'django-registration==3.0',
        ],
        'thumbnails': [
            'Pillow==5.4.1',
            'sorl-thumbnail==12.5.0',
        ],
    },
    zip_safe=False,
)
