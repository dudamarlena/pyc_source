from setuptools import setup

setup(
    name="django-flatpages-extension",
    version='0.3.5',
    description='Seo fields extension for django.contrib.flatpages',
    author='Spi4ka',
    packages=[
        "django-flatpages-extension",
        # "django-flatpages-extension",
        # "django-flatpages-extension.migrations",
    ],
    include_package_data=True,
    package_data={
        'django-flatpages-extension': [
            'django-flatpages-extension/templates',
            'django-flatpages-extension/locale'
        ]
    },
    install_requires=[
        'pillow',
        'pytils',
    ]
)