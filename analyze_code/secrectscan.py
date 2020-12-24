import os
import subprocess
import json


targetdir="pycfiles"
file="processlog\\pysecrets.txt"
command=["detect-secrets","scan",""]

count=0
flag=0
folders=os.listdir(targetdir)
logfile=open(file,"a")
logfile.write("\n\n\n\n\n\n\n")
logfile.write("--------------------------------------------------------------------------------------------------"+"\n")
for folder in folders:
    flag=flag+1
    print(flag)
    workingdir=os.path.join(targetdir,folder,"")
    if(os.path.isdir(workingdir)):
        files=os.listdir(workingdir)
        for pyfile in files:
            pyfilepath=os.path.join(workingdir,pyfile)
            command[2]=pyfilepath
            rawdata=subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
            result=json.loads(rawdata)["results"]
            if(len(result)>0):
                count=count+1
                logfile.write(pyfilepath+"\n")
                logfile.write(json.dumps(result))
                logfile.write("\n")
                logfile.write("------------------------"+"\n")
            logfile.flush()

logfile.write("sum: in all "+ str(count)+ " files have credentials"+"\n")
logfile.close()
            
 

