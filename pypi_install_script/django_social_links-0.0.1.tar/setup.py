from setuptools import setup

setup(
    name="django_social_links",
    version='0.0.1',
    description='Django social links module',
    author='Spi4ka',
    packages=[
        "django_social_links",
        "django_social_links.templatetags",
        "django_social_links.migrations",
    ],
    include_package_data=True,
    package_data={
        'django_social_links': [
            'django_social_links/templates',
            'django_social_links/locale'
        ]
    },
    install_requires=[
    ]
)
