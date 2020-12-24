#!/usr/bin/python3
#-*- coding: utf-8 -*-

import setuptools

longdesc = """
Esse módulo foi criado com o objetivo de realizar a busca de mensagens na caixa de e-mail de forma
simplificada e intuitiva utilizando o módulo imaplib para conexão.

A instalação pode ser feita utilizando: 
``pip install git+https://github.com/marianaalbano/python_mail.git``.

"""

setuptools.setup(
    name="python_mail",
    version="1.0.2",
    author="Mariana Albano",
    author_email="mariana.albano@outlook.com",
    description="Management email module",
    license='MIT License',
    long_description="Esse módulo foi criado com o objetivo de realizar a busca de mensagens na caixa de e-mail de forma simplificada e intuitiva utilizando o módulo imaplib para conexão.",
    long_description_content_type="text/markdown",
    url="https://github.com/marianaalbano/python_mail.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)