# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import io
import json
import os
import subprocess
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PACKAGE_JSON = os.path.join(BASE_DIR, "superset", "assets", "package.json")
with open(PACKAGE_JSON, "r") as package_file:
    version_string = json.load(package_file)["version"]

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_git_sha():
    try:
        s = subprocess.check_output(["git", "rev-parse", "HEAD"])
        return s.decode().strip()
    except Exception:
        return ""


GIT_SHA = get_git_sha()
version_info = {"GIT_SHA": GIT_SHA, "version": version_string}
print("-==-" * 15)
print("VERSION: " + version_string)
print("GIT SHA: " + GIT_SHA)
print("-==-" * 15)

VERSION_INFO_FILE = os.path.join(
    BASE_DIR, "superset", "static", "assets", "version_info.json"
)

with open(VERSION_INFO_FILE, "w") as version_file:
    json.dump(version_info, version_file)


setup(
    name="superset",
    description=("Superset has moved to apache-superset, as of 0.34.0 onwards, please pip install apache-superset"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.30.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=["superset/bin/superset"],
    install_requires=[
    ],
    extras_require={
    },
    python_requires="~=3.6",
    author="Apache Software Foundation",
    author_email="dev@superset.incubator.apache.org",
    url="https://superset.apache.org/",
    download_url="https://www.apache.org/dist/incubator/superset/" + version_string,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
