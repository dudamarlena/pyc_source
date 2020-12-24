from pathlib import Path
from setuptools import setup, find_packages 

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name="rfcreader",
    version="0.4",
    packages=find_packages(),
    url="https://github.com/abstractequalsmagic/rfcreader",
    description = "RFCEditor interface",
    long_description = long_description,
    long_description_content_type = "text/markdown",
)
