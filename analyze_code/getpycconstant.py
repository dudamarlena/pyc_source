import glob
import os
import sys
import pathlib
import ast

logfile=open("processlog\\pycconstant.txt","a")

class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node):
        print('Found string "%s"' % node.s)
        if(len(node.s)>40 or len(node.s)<9):
            print("over size")
        else:
            logfile.write('Found string "%s"' % node.s)
            logfile.write("\n")


class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('str: ' + node.s)

scandir=r"pycfiles"
extension = ".py"

dirs=os.listdir(scandir)

project_pyc=0
count=0
numall=0
suc_count=0
fail=0
logfile.write("\n\n\n\n\n\n\n")
logfile.write("----------------------------------------------------------------------------------------------------------------------"+"\n")
for folder in dirs:
    count=count+1
    print(count)
    print(folder)
    workingdir=os.path.join(scandir,folder,"")
    pyfiles=os.listdir(workingdir)
    for pyfile in pyfiles:
        numall=numall+1
        if(".py" not in pyfile):
            break
        fullpypath=os.path.join(workingdir,pyfile)
        try:
            logfile.write(fullpypath+"\n")
        except:
            logfile.write("error: "+ folder+"\n")
        try:
            file=open(fullpypath,"r")
            tree=ast.parse(file.read())
            MyTransformer().visit(tree)
            MyVisitor().visit(tree)
            file.close()
            suc_count=suc_count+1
        except:
            fail=fail+1
        logfile.write("---------------"+"\n")
        
logfile.write("Sum: " + str(suc_count)+ " files" + " successfully scanned "+" and "+str(fail)+" failed")
logfile.write("all files: "+str(numall)+"\n")
logfile.close()
    