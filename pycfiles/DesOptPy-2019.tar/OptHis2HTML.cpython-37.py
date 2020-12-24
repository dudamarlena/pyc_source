# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/DesOptPy/DesOptPy/OptHis2HTML.py
# Compiled at: 2019-06-04 12:44:52
# Size of source mod 2**32: 15326 bytes
"""
-------------------------------------------------------------------------------
Title:          OptHis2HTML.py
Units:          Unitless
Date:           July 9, 2016
Authors:        F. Wachter, E.J. Wehrle
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description
-------------------------------------------------------------------------------
Open the optimization history (the .cue and .bin file) and processes them into
HTML format during runtime so one can check the status and progress of the
optimization.

-------------------------------------------------------------------------------
To do and ideas
-------------------------------------------------------------------------------
see DesOpt.py
"""
from __future__ import absolute_import, division, print_function
import csv, glob, os, shutil
from time import localtime, strftime, time
import numpy as np
from pyOpt import History
from DesOptPy.Normalize import normalize, denormalize
import DesOptPy.OptReadHis as OptReadHis

def OptHis2HTML(OptName, Alg, AlgOptions, DesOptDir, x0, xL, xU, gc, DesVarNorm, inform, starttime, StatusDirectory=''):
    StartTime = str(starttime)[0:10] + '000'
    EndTime = ''
    RefRate = '2000'
    if inform != 'Running':
        EndTime = str(time())[0:10] + '000'
        RefRate = '1000000'
    else:
        Iteration = 'Iteration'
        if StatusDirectory == '':
            StatusDirectory = DesOptDir
        else:
            pos_of_best_ind = []
            fIter = []
            xIter = []
            gIter = []
            template_directory = os.path.dirname(os.path.realpath(__file__)) + '/StatusReportFiles/'
            fIter, xIter, gIter, gGradIter, fGradIter, inform = OptReadHis(OptName, Alg, AlgOptions, x0, xL, xU, gc, DesVarNorm)
            if xIter.size > 0:
                nIter = np.shape(xIter)[1] - 1
            else:
                nIter = -1
        if xIter.size != 0:
            if DesVarNorm == False:
                xIterDenorm = np.zeros((nIter + 1, len(xIter[0])))
                for y in range(0, nIter + 1):
                    xIterDenorm[y] = xIter[y]

            else:
                xIter = xIter[0:np.size(xL), :]
                xIterDenorm = np.zeros(np.shape(xIter))
                for ii in range(len(xIterDenorm)):
                    xIterDenorm[:, ii] = denormalize(xIter[:, ii], x0, xL, xU, DesVarNorm)

        time_now = strftime('%Y-%b-%d %H:%M:%S', localtime())
        number_des_vars = '0'
        number_constraints = '0'
        with open('objFct_maxCon.csv', 'w') as (csvfile):
            datawriter = csv.writer(csvfile, dialect='excel')
            datawriter.writerow(['Iteration', 'Objective function', 'Constraint'])
        csvfile.close()
        with open('desVarsNorm.csv', 'w') as (csvfile):
            datawriter = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=(csv.QUOTE_NONE))
            labels = ['Iteration']
            if xIter.size != 0:
                for i in range(1, xIter.shape[1] + 1):
                    labels = labels + ['x' + str(i)]

            datawriter.writerow(labels)
        csvfile.close()
        with open('desVars.csv', 'w') as (csvfile):
            datawriter = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=(csv.QUOTE_NONE))
            labels = ['Iteration']
            if xIter.size != 0:
                for i in range(1, xIter.shape[1] + 1):
                    labels = labels + ['x' + str(i)]

            datawriter.writerow(labels)
        csvfile.close()
        with open('constraints.csv', 'w') as (csvfile):
            datawriter = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=(csv.QUOTE_NONE))
            labels = ['Iteration']
            if gIter.size != 0:
                for i in range(1, gIter.shape[1] + 1):
                    labels = labels + ['g' + str(i)]

            datawriter.writerow(labels)
        csvfile.close()
        for x in range(0, nIter + 1):
            with open('objFct_maxCon.csv', 'a') as (csvfile):
                datawriter = csv.writer(csvfile, dialect='excel')
                if np.size(gIter[x]) == 0:
                    datawriter.writerow([x, str(float(fIter[x])), []])
                else:
                    datawriter.writerow([x, str(float(fIter[x])),
                     float(np.max(gIter[x]))])
            csvfile.close()

        if xIter.size != 0:
            for x in range(0, nIter + 1):
                datasets = str(xIter[x][:].tolist()).strip('[]')
                with open('desVarsNorm.csv', 'a') as (csvfile):
                    datawriter = csv.writer(csvfile, dialect='excel', quotechar=' ')
                    datawriter.writerow([x, datasets])
                csvfile.close()

        if xIter.size != 0:
            for x in range(0, nIter + 1):
                datasets_denorm = str(xIterDenorm[x][:].tolist()).strip('[]')
                with open('desVars.csv', 'a') as (csvfile):
                    datawriter = csv.writer(csvfile, dialect='excel', quotechar=' ')
                    datawriter.writerow([x, datasets_denorm])
                csvfile.close()

        if gIter.size != 0:
            for x in range(0, nIter + 1):
                datasetsg = str(gIter[x][:].tolist()).strip('[]')
                with open('constraints.csv', 'a') as (csvfile):
                    datawriter = csv.writer(csvfile, dialect='excel', quotechar=' ')
                    datawriter.writerow([x, datasetsg])
                csvfile.close()

        ObjFct_table = '<td></td>'
        if xIter.size != 0:
            if gIter.size != 0:
                for x in range(0, nIter + 1):
                    ObjFct_table += '<tr>\n<td>' + str(x) + '</td>\n<td>' + str(round(fIter[x][0], 4)) + '</td>\n<td>' + str(round(np.max(gIter[x]), 4)) + '</td>\n</tr>'

        else:
            for x in range(0, nIter + 1):
                ObjFct_table += '<tr>\n<td>' + str(x) + '</td>\n<td>' + str(round(fIter[x][0], 4)) + '</td>\n<td> no constraints </td>\n</tr>'

    DesVar_table = '<td></td>'
    if xIter.size != 0:
        number_des_vars = str(len(xIter[0]))
        for x in range(0, len(xIter[0])):
            DesVar_table += '<td>x&#770;<sub>' + str(x + 1) + '</sub></td>' + '<td>' + 'x<sub>' + str(x + 1) + ' </sub></td>'

        for y in range(0, nIter + 1):
            DesVar_table += '<tr>\n<td>' + str(y) + '</td>'
            for x in range(0, len(xIter[0])):
                DesVar_table += '<td>' + str(round(xIter[y][x], 4)) + '</td><td>' + str(round(xIterDenorm[y][x], 4)) + '</td>'

            DesVar_table += '</tr>'

    Constraint_table = '<td></td>'
    if gIter.size != 0:
        number_constraints = str(len(gIter[0]))
        for x in range(0, len(gIter[0])):
            Constraint_table += '<td>g<sub>' + str(x + 1) + '</sub></td>'

        for y in range(0, nIter + 1):
            Constraint_table += '<tr>\n<td>' + str(y) + '</td>'
            for x in range(0, len(gIter[0])):
                if round(gIter[y][x], 4) > 0:
                    Constraint_table += '<td class="negativ">' + str(round(gIter[y][x], 4)) + '</td>'
                else:
                    Constraint_table += '<td class="positiv">' + str(round(gIter[y][x], 4)) + '</td>'

            Constraint_table += '</tr>'

    html = open(template_directory + '/initial.html', 'r')
    hstr = html.read()
    html.close()
    if gIter.size != 0 or gIter.size > 100:
        hstrnew = hstr.replace('xxxxName', OptName)
        hstrnew = hstrnew.replace('xxxxTime', time_now)
        hstrnew = hstrnew.replace('xxxxtableObjFct', ObjFct_table)
        hstrnew = hstrnew.replace('xxxxtableDesVar', DesVar_table)
        hstrnew = hstrnew.replace('xxxxnumber_des_var', number_des_vars * 2)
        hstrnew = hstrnew.replace('xxxxtableConstr', Constraint_table)
        hstrnew = hstrnew.replace('xxxxnumber_constraints', number_constraints)
        hstrnew = hstrnew.replace('xxxxAlg', Alg)
        hstrnew = hstrnew.replace('xxxxStatus', str(inform))
        hstrnew = hstrnew.replace('xxxxRefRate', RefRate)
        hstrnew = hstrnew.replace('xxxxStartTime', StartTime)
        hstrnew = hstrnew.replace('xxxxEndTime', EndTime)
        hstrnew = hstrnew.replace('xxxxIteration', Iteration)
    else:
        hstrnew = hstr.replace('xxxxName', OptName)
        hstrnew = hstrnew.replace('xxxxTime', time_now)
        hstrnew = hstrnew.replace('xxxxtableObjFct', ObjFct_table)
        hstrnew = hstrnew.replace('xxxxtableDesVar', DesVar_table)
        hstrnew = hstrnew.replace('xxxxAlg', Alg)
        hstrnew = hstrnew.replace('xxxxStatus', inform)
        hstrnew = hstrnew.replace('xxxxRefRate', RefRate)
        hstrnew = hstrnew.replace('xxxxStartTime', StartTime)
        hstrnew = hstrnew.replace('xxxxEndTime', EndTime)
        hstrnew = hstrnew.replace('xxxxIteration', Iteration)
        try:
            for i in range(0, 10):
                hstrnew = hstrnew[0:hstrnew.find('<!--Start of constraint html part-->')] + hstrnew[hstrnew.find('<!--End of constraint html part-->') + 34:-1]

        except:
            print('')

        html = open('initial1.html', 'w')
        html.write(hstrnew)
        html.close()
        if not os.path.exists(StatusDirectory + os.sep + 'Results' + os.sep + OptName):
            os.makedirs(StatusDirectory + os.sep + 'Results' + os.sep + OptName)
        shutil.copy('initial1.html', StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep + OptName + '_Status.html')
        shutil.copy('objFct_maxCon.csv', StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep + 'objFct_maxCon.csv')
        shutil.copy('desVars.csv', StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep + 'desVars.csv')
        shutil.copy('desVarsNorm.csv', StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep + 'desVarsNorm.csv')
        shutil.copy('constraints.csv', StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep + 'constraints.csv')
        for file in glob.glob(template_directory + '*.png'):
            shutil.copy(file, StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep)

        for file in glob.glob(template_directory + '*.js'):
            shutil.copy(file, StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep)

        for file in glob.glob(template_directory + '*.css'):
            shutil.copy(file, StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep)

        for file in glob.glob(template_directory + '*.ico'):
            shutil.copy(file, StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep)

        for file in glob.glob(template_directory + 'view_results.py'):
            shutil.copy(file, StatusDirectory + os.sep + 'Results' + os.sep + OptName + os.sep)

        return 0