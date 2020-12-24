# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/containers/caputo.marcos/Projects/logistic/env/lib/python2.7/site-packages/tsp_api/api.py
# Compiled at: 2017-10-01 15:23:13
from eve import Eve
from flask import request, jsonify
from pymongo import MongoClient
import dijkstra
client = MongoClient('mongodb://0.0.0.0:27017')
db = client.tsp_rest_api
collection = db.maps
app = Eve()

@app.route('/maps/shortest', methods=['GET'])
def getCollection():
    mapName = request.args.get('map')
    origin = request.args.get('origin')
    destiny = request.args.get('destiny')
    price = request.args.get('price')
    autonomy = request.args.get('autonomy')
    map = collection.find_one({'title': mapName})
    steps = []
    dictPaths = {}
    graph = dijkstra.Graph()
    vertex = []
    if not map:
        response = jsonify({'response': 'Application could not use the DB especifield.'})
        response.status_code = 500
        return response
    for vert in map['routes']:
        vertex.append(vert['origin'])
        vertex.append(vert['destiny'])

    for i in list(set(vertex)):
        graph.add_vertex(i)

    for vert in map['routes']:
        dictPaths[vert['origin'] + vert['destiny']] = vert['distance']
        graph.add_edge(vert['origin'], vert['destiny'], vert['distance'])

    if origin not in vertex:
        response = jsonify({'response': 'The parameter origin does not contain on map %s' % mapName})
        response.status_code = 400
        return response
    if destiny not in vertex:
        response = jsonify({'response': 'The parameter destiny does not contain on map %s' % mapName})
        response.status_code = 400
        return response
    dijkstra.dijkstra(graph, graph.get_vertex(origin), graph.get_vertex(destiny))
    target = graph.get_vertex(destiny)
    path = [target.get_id()]
    dijkstra.shortest(target, path)
    a = 0
    while a < len(path[::-1]) - 1:
        steps.append(path[::-1][a] + path[::-1][(a + 1)])
        a = a + 1

    total = 0
    for i in steps:
        total = total + dictPaths[i]

    pathList = []
    for i in path[::-1]:
        pathList.append(i.encode('utf-8'))

    cost = float(total) / float(autonomy) * float(price)
    response = []
    response.append({'Path': '%s' % pathList})
    response.append({'Total KM': '%.2f' % total})
    response.append({'Cost': '%.2f' % cost})
    return jsonify(data=response)