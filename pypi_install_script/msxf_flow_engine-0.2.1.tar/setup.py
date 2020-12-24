from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
exec(open("msxf_flow_engine/version.py").read())

LONG_DESCRIPTION = """
=====================================
django-uni-form (django-uni-form)
=====================================

Django_ forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

`Uni-form`_ has been selected as the base model for the design of the forms.

Documentation
=============

http://readthedocs.org/docs/django-uni-form/en/latest/

.. note:: django-uni-form only supports Django 1.2 or higher and Python
2.5.4, Python 2.6.x and Python 2.7.x. If you need to support earlier versions
of Django or Python you will need to use django-uni-form 0.7.0.


.. _`Uni-form`: http://sprawsm.com/uni-form
.. _Django: http://djangoproject.com
"""

# install_requires = [
#     'jsonpickle~=0.9.0',
#     'six~=1.0',
#     'redis~=2.0',
#     'fakeredis~=0.10.0',
#     'future~=0.16',
#     'numpy~=1.13',
#     'typing~=3.0',
#     'requests~=2.15',
#     'graphviz~=0.8.0',
#     'keras~=2.0',
#     'tensorflow>=1.7,<1.9',
#     'h5py~=2.0',
#     'apscheduler~=3.0',
#     'tqdm~=4.0',
#     'ConfigArgParse~=0.13.0',
#     'networkx~=2.0',
#     'fbmessenger~=5.0',
#     'pykwalify<=1.6.0',
#     'coloredlogs~=10.0',
#     'ruamel.yaml~=0.15.0',
#     'flask~=1.0',
#     'flask_cors~=3.0',
#     'scikit-learn~=0.19.0',
#     'rasa_nlu~=0.13.0',
#     'slackclient~=1.0',
#     'python-telegram-bot~=10.0',
#     'twilio~=6.0',
#     'mattermostwrapper~=2.0',
#     'colorhash~=1.0',
# ]

setup(
    name="msxf_flow_engine",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),
    version=__version__,
    # install_requires=install_requires,
    include_package_data=True,
    description="Machine learning based dialogue engine "
                "for conversational software.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='msxf',
    author_email='195832858@qq.com',
    maintainer="msxf",
    maintainer_email="195832858@qq.com",
    license="Apache 2.0",
)


