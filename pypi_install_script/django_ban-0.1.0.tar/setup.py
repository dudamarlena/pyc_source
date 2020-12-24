from setuptools import setup

setup(
    name="django_ban",
    version='0.1.0',
    description='A django application to ip ban',
    author='hakancelik96',
    author_email='hakancelik96@outlook.com',
    packages=["django_ban"],
    include_package_data=True,
    install_requires=["django", "djangoip"],
    url="https://github.com/djangoapps/django_ban",
    license='MIT',
    zip_safe=False,
    keywords='ban, django, user ban, ip ban, address ban',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)