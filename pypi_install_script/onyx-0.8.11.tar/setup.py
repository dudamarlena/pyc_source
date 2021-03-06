###############################################################################
#
#   Copyright: (c) 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

# FIXME: distutils problem with hardlinks
import os
del os.link

from setuptools import setup, find_packages

install_requires = [
    "onyx.core",
    "numpy",
    "scipy",
    "apscheduler",
    "argh",
    "tornado",
    "sqlalchemy",
]

DESCRIPTION = """Onyx is """

setup(
    name="onyx",
    namespace_packages=["onyx"],
    setup_requires=["hgtools"],
    use_vcs_version={"increment": "0.1"},
    description=("Onyx is a ramework to develop integrated trading, position "
                 "management, pricing and risk management platforms."),
    author="carlo sbraccia",
    author_email="carlosbraccia@yahoo.co.uk",
    url="https://bitbucket.org/sbraccia/onyx",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
