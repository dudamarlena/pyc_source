import os
import importlib.util
from setuptools import setup

# Boilerplate to load commonalities
spec = importlib.util.spec_from_file_location(
    "setup_common", os.path.join(os.path.dirname(__file__), "setup_common.py")
)
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)

common.KWARGS["install_requires"] += [
    "numpy>=1.16.4",
]
common.KWARGS["tests_require"] = [
    "aiohttp>=3.6.2",
]
common.KWARGS["entry_points"] = {
    "dffml.source": [
        f"idx3 = {common.IMPORT_NAME}.idx3:IDX3Source",
        f"idx1 = {common.IMPORT_NAME}.idx1:IDX1Source",
    ],
}

setup(**common.KWARGS)
