from setuptools import setup


setup(
    name='django_serialify',
    version='0.1',
    description='Simple serialize django models and dict to dict',
    url='http://github.com/Buddhalow/django-serialify',
    author='Alexander Forselius',
    author_email='alexander.forselius@buddhalow.com',
    license='MIT',
    packages=['django_serialify'],
    install_requires=[
      'django',
    ],
    zip_safe=False
)
