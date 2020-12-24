import os
import ast
from collections import deque
from datetime import datetime
import linecache
now = datetime.now()

current_time = now.strftime("%H:%M:%S")

logfile=open("processlog\\timestamp.txt","a")
timstampfile=open("processlog\\wrongtimestamp.txt","a")
logfile.write("------------------------------------------------------------")
logfile.write(str(current_time)+"\n")
logfile.write("\n")
root_dir = "pycfiles"  # path to the root directory to search

processflag=0
count=0

for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    processflag=processflag+1
    for filename in files:  # iterate over the files in the current dir
        file_extension = os.path.splitext(filename)[1]
        if(file_extension==".py"):
            fullpath=os.path.join(root,filename)
            fifthline = linecache.getline(fullpath, 5)
            length=len(fifthline.split())
            print(fullpath)
            if(length==5):
                date=fifthline.split()[3]
                clock=fifthline.split()[4]
                try:
                    year,month,day=date.split("-")
                    print(year+month+day)
                except:
                    year=2020
                if(int(year)>2020):
                    timstampfile.write(fullpath+"\n")
                    timstampfile.write("time: "+date+" "+clock+"\n")
                    timstampfile.write("-----------------"+"\n"+"\n")
                    count=count+1
                try:
                    logfile.write(fullpath+"\n")
                    logfile.write("time: "+date+" "+clock+"\n")
                    logfile.write("-----------------"+"\n"+"\n")
                    count=count+1
                except:
                    pass
            else:
                logfile.write(fullpath+"\n")
                logfile.write("error no time stamp"+"\n")
                logfile.write("-----------------"+"\n"+"\n")
logfile.write("sum : " + str(count)+" files are succefulll parsed")

