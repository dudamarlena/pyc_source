from distutils.core import setup
setup(
name="cu-oi",
version="0.1",
author="Jose Gonzalez",
author_email="pepegonzalez.hdz@gmail.com",
packages=["oi-seguridad"],
package_data={"entrenamiento": ['oi-seguridad/entrenamiento',], "xml":['oi-seguridad/xml',]},
include_package_data = True,
url="http://www.python-ComputoUbicuo-OficinaInteligente.org",
license="GPL v3.0",
description="Modulo que encapsula la funcionalidad orientada a la seguridad del sistema inteligente de oficinas.",
long_description=open('README.txt').read(),
classifiers=[
"Environment :: Console",
"Intended Audience :: Developers",
"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
"Natural Language :: Spanish",
"Operating System :: OS Independent",
"Programming Language :: Python :: 2.7",
"Topic :: Software Development",
"Topic :: Software Development :: Libraries :: Python Modules"
]
)

