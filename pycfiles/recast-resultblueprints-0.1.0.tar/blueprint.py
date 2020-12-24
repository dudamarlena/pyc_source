# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukas/Code/recast/recast-resultblueprints/recastresultblueprints/yadage_result/blueprint.py
# Compiled at: 2017-08-06 09:09:56
import json, os, glob, recastbackend.resultaccess
from flask import Blueprint, render_template, jsonify, request
blueprint = Blueprint('yadage_result', __name__, template_folder='templates')

@blueprint.route('/result/<analysisid>/<wflowconfigname>/<basicreqid>')
def result_view(analysisid, wflowconfigname, basicreqid):
    fullpath = recastbackend.resultaccess.basicreq_wflowconfigpath(basicreqid, wflowconfigname)
    resultdata = recastbackend.resultextraction.extract_result(fullpath, analysisid, wflowconfigname)
    resultsfiles = []
    for dirpath, subdirs, files in os.walk(fullpath):
        for fl in files:
            resultsfiles.append(('/').join([dirpath.replace(fullpath, ''), fl]).lstrip('/'))

    return render_template('recast_result.html', basicreqid=basicreqid, wflowconfigname=wflowconfigname, resultsfiles=resultsfiles, resultdata=resultdata)


@blueprint.route('/result/<analysisid>/<wflowconfigname>/<basicreqid>/json')
def json_result(analysisid, wflowconfigname, basicreqid):
    fullpath = recastbackend.resultaccess.basicreq_wflowconfigpath(basicreqid, wflowconfigname)
    resultdata = recastbackend.resultextraction.extract_result(fullpath, analysisid, wflowconfigname)
    return jsonify(resultdata)