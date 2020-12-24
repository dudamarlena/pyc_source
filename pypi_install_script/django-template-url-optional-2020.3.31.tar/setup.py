try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='django-template-url-optional',
    version='2020.3.31',
    packages=[
        'django_template_url_optional',
        'django_template_url_optional.templatetags',
    ],
)
