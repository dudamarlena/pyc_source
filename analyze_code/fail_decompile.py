import glob
import os
import sys
# import pathlib
import shutil

def findFilesInFolder(path, pathList, extension, subFolders = True):
    """
    Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)
    path:        Base directory to find files
    pathList:    A list that stores all paths
    extension:   File extension to find
    subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
    """
    try:   # Trapping a OSError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith(extension): # if it is a file
                pathList.append(entry.path)
                print(entry.path)
            elif entry.is_dir() and subFolders:   # if it is a directory, then repeat process as a nested function
                pathList = findFilesInFolder(entry.path, pathList, extension, subFolders)
    except:
        print('Cannot access ' + path +'. Probably a permissions error')
    return pathList

scandir="dstdir"
extension = ".pyc"
dstpyc="pycfiles"
failpyc="failfiles"
command_prefix='uncompyle6 -o'
pathlist=[]

dirs=os.listdir(scandir)
logfile=open('processlog/fail.txt',"a")
count=0
numall=0
suc_count=7151
# logfile.write("----------------------------------------------------------------------------------------------------------------------")

for folder in dirs:
    try:
        count=count+1 #count the number of dictiaonary
        print(count)
        workingdir=os.path.join(scandir,folder,"") #file path
        if(folder=="arena-0.0.5.tar"):
            continue
        pathlist=findFilesInFolder(workingdir,pathlist,extension,True)
        print(pathlist)
        numall = numall + len(pathlist)
        if(count>247342):
          if (len(pathlist) > 0):
            dstpycdir = os.path.join(dstpyc, folder, "")
            if (not os.path.isdir(dstpycdir)):
                os.mkdir(dstpycdir)
            for pycfile in pathlist:
                fullcommand = command_prefix + ' ' + dstpycdir + ' ' + pycfile
                print(pycfile)
                try:
                    stream = os.popen(fullcommand)
                    output = stream.read()
                    # logfile.write(output)
                    if ("Successfully" not in output):
                        suc_count = suc_count + 1
                        print("error: " + str(suc_count))
                        failpycdir = os.path.join(failpyc, folder, "")
                        logfile.write(str(suc_count) + ": " + pycfile + "\n")
                        if (not os.path.isdir(failpycdir)):
                            os.mkdir(failpycdir)
                        shutil.copy(pycfile, failpycdir)
                        print("Copy success!!!")
                    stream.close()
                except:
                    suc_count = suc_count + 1
                    print("error: " + str(suc_count))
                    failpycdir = os.path.join(failpyc, folder, "")
                    logfile.write(str(suc_count) + ": " + pycfile + "\n")
                    if (not os.path.isdir(failpycdir)):
                        os.mkdir(failpycdir)
                    shutil.copy(pycfile, failpycdir)
                    print("Copy success!!!")
        logfile.flush()
        pathlist=[]
    except:
        print("unknown error: "+folder+"\n")

logfile.write("Sum: " + str(numall)+ " pyc files" +"\n"+ "Failed decompile: "+str(suc_count))
logfile.close()
