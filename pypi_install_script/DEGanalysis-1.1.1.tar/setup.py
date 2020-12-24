import os
import sys
from setuptools import setup
from src.version import __version__

def checkRlib(*pkgs):
    cmds = "echo " + "\"if (all(is.element(c('%s'),.packages(all.available=T)))){cat(1)}else{cat(0)}\""%"','".join(pkgs) + " | R --no-save --slave"
    res = int(os.popen(cmds).read())
    if not res:
        print "Error: more then one of %s R_librarys are not be installed in R, please install these packages before."%list(pkgs)
        return os.EX_OK  
    return os.EX_USAGE    

r_pkgs = ["DESeq2","edgeR","limma","DESeq","VennDiagram","ggplot2"]

if not checkRlib(*r_pkgs):
    sys.exit(1)

setup(
    name = "DEGanalysis",
    version = __version__ ,
    packages = ["DEGanalysis"],
    package_dir = {"DEGanalysis":"src"},
    package_data = {"":["*.pl"]},
    install_requires = [
       "xlsxwriter" ,
       "rpy2 == 2.5.6",
        ], 
    author="Yong Deng",
    author_email = "yodeng@tju.edu.cn",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        ],
    entry_points = { 
        'console_scripts': [   
            'DEGanalysis = DEGanalysis.DEGanalysis:main'
        ]   
    }   
)
