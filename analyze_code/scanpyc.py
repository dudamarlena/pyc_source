import glob
import os
import sys
import pathlib

def findFilesInFolder(path, pathList, extension, subFolders = True):
    """  Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

    path:        Base directory to find files
    pathList:    A list that stores all paths
    extension:   File extension to find
    subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
    """

    try:   # Trapping a OSError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith(extension):
                pathList.append(entry.path)
            elif entry.is_dir() and subFolders:   # if its a directory, then repeat process as a nested function
                pathList = findFilesInFolder(entry.path, pathList, extension, subFolders)
    except OSError:
        print('Cannot access ' + path +'. Probably a permissions error')

    return pathList
scandir=r"latestpypi\\unzipgithub"
extension = ".pyc"
dstpyc="pycfiles"
command_prefix="uncompyle6 -o"
pathlist=[]

dirs=os.listdir(scandir)
logfile=open("processlog\\githubpyc.txt","a")
project_pyc=0
count=0
numall=0
suc_count=0
logfile.write("\n\n\n\n\n\n\n")
logfile.write("----------------------------------------------------------------------------------------------------------------------")
for folder in dirs:
    try:
        count=count+1
        print(count)
        
        # if(count<=227252):
        #     continue
        workingdir=os.path.join(scandir,folder,"")
        print(folder)
        if(folder=="arena-0.0.5.tar"):
            continue
        pathlist=findFilesInFolder(workingdir,pathlist,extension,True)
        print(pathlist)
        # if(len(pathlist)>0):
        #     #print(folder+" : "+str(len(pathlist))+"\n")
        #     #logfile.write(folder+" : "+str(len(pathlist))+"\n")
        #     project_pyc=project_pyc+1
        #     numall=numall+len(pathlist)
        #     logfile.write(str(count))
        #     dstpycdir=os.path.join(dstpyc,folder,"")
        #     if(os.path.isdir(dstpycdir)):
        #         suc_count=suc_count+1
        #         print("exist")
        #         continue
        #     if(not os.path.isdir(dstpycdir)):
        #         os.mkdir(dstpycdir)
        #     for pycfile in pathlist: 
        #         fullcommand=command_prefix+" "+dstpycdir+" "+pycfile
        #         print(pycfile)
        #         try:
        #             stream = os.popen(fullcommand)
        #             output = stream.read()
        #             logfile.write(output)
        #             stream.close()
        #             suc_count=suc_count+1
        #         except:
        #             logfile.write("decompile error: "+pycfile)
        #print(pathlist)
        logfile.flush()
        pathlist.clear()
    except:
        logfile.write("unknown error: "+folder)

logfile.write("Sum: " + str(numall)+ "pyc files" + " successfully decompile: "+str(suc_count))
logfile.close()
    