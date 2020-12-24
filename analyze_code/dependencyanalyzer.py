from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib
import difflib
from datetime import datetime
import os
import os.path
import requests
import json
import unicodedata
import re
import threading
from subprocess import PIPE, run, Popen, call, check_output
import subprocess
import johnnydep
from distutils.core import run_setup
import os
import ast
from collections import deque
from datetime import datetime
from shutil import copyfile,copy


command=["johnnydep","ipython","-v","0","--fields","name"]





# html_page = urllib.urlopen("https://pypi.org/simple/")
# soup = BeautifulSoup(html_page)
# link_list=[]
# i=0
# for link in soup.findAll('a'):
#    a=link.get('href')[8:]
#    a=a[:-1]
#    link_list.append(a)
#    #print(a)
#    i=i+1


# print("list extract done")
# for name in link_list:
#     print(name)
#     command[1]=name
#     try:
#         result = subprocess.run(command, stdout=subprocess.PIPE)
#         print(result.returncode)
#         if(result.returncode==0):
#             print(result.stdout.decode('utf-8'))
#     except:
#         print(name+" error" +"\n")





now = datetime.now()

current_time = now.strftime("%H:%M:%S")

logfile=open("processlog\\dependencyAnalyzer.txt","a")
logfile.write("------------------------------------------------------------")
logfile.write(str(current_time)+"\n")
logfile.write("\n")
root_dir = "dstdir"  # path to the root directory to search
outputdir = "pypi_dependency"
processflag=0
count=0




for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    processflag=processflag+1
    for filename in files:  # iterate over the files in the current dir
        if(filename=="setup.py" or filename=="requirements.txt"):
            file_path = os.path.join(root, filename)  # build the file path
            splittedpath=file_path.split(os.sep)
            packagename=splittedpath[1]
            print(packagename)
            print(file_path)
            destpath=os.path.join(outputdir,packagename,filename)
            try:
                copy(file_path,destpath)
                print(file_path)
                print(destpath)
            except:
                print("error")
                logfile.write(file_path+"\n")
            # except:
            #     print("error:"+packagename+": "+file_path)
            #     logfile.write("error:"+packagename+": "+file_path+"\n")
            #     logfile.write("------------------------------------------------------------")
            #     logfile.write("\n")
            # setupfile.close()
    logfile.flush()
logfile.write("sum : " + str(count)+" packages are succefulll parsed")