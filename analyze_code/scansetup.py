import os
import ast
from collections import deque
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

logfile=open("processlog\\setup.txt","a")
logfile.write("------------------------------------------------------------")
logfile.write(str(current_time)+"\n")
logfile.write("\n")
root_dir = "dstdir"  # path to the root directory to search

class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)

    return func_calls
processflag=0
count=0

for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    processflag=processflag+1
    for filename in files:  # iterate over the files in the current dir
        if(filename=="setup.py"):
            print(filename)
            file_path = os.path.join(root, filename)  # build the file path
            splittedpath=file_path.split(os.sep)
            packagename=splittedpath[1]
            logfile.write(packagename+" : \n")
            print(packagename)
            setupfile=open(file_path,'r')
            try:
                node=ast.parse(setupfile.read())
                funclist=get_func_calls(node)
                for func in funclist:
                    logfile.write(str(func))
                    logfile.write("\n")
                logfile.write("------------------------------------------------------------")
                logfile.write("\n")
                print("success")
                count=count+1
            except:
                print("error")
                logfile.write("error"+"\n")
                logfile.write("------------------------------------------------------------")
                logfile.write("\n")
            setupfile.close()
logfile.write("sum : " + str(count)+" packages are succefulll parsed")

