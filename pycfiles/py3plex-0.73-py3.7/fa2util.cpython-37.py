# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/fa2/fa2util.py
# Compiled at: 2019-09-30 13:55:18
# Size of source mod 2**32: 11174 bytes
from math import sqrt

class Node:

    def __init__(self):
        self.mass = 0.0
        self.old_dx = 0.0
        self.old_dy = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.x = 0.0
        self.y = 0.0


class Edge:

    def __init__(self):
        self.node1 = -1
        self.node2 = -1
        self.weight = 0.0


def linRepulsion(n1, n2, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    distance2 = xDist * xDist + yDist * yDist
    if distance2 > 0:
        factor = coefficient * n1.mass * n2.mass / distance2
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor


def linRepulsion_region(n, r, coefficient=0):
    xDist = n.x - r.massCenterX
    yDist = n.y - r.massCenterY
    distance2 = xDist * xDist + yDist * yDist
    if distance2 > 0:
        factor = coefficient * n.mass * r.mass / distance2
        n.dx += xDist * factor
        n.dy += yDist * factor


def linGravity(n, g):
    xDist = n.x
    yDist = n.y
    distance = sqrt(xDist * xDist + yDist * yDist)
    if distance > 0:
        factor = n.mass * g / distance
        n.dx -= xDist * factor
        n.dy -= yDist * factor


def strongGravity(n, g, coefficient=0):
    xDist = n.x
    yDist = n.y
    if xDist != 0:
        if yDist != 0:
            factor = coefficient * n.mass * g
            n.dx -= xDist * factor
            n.dy -= yDist * factor


def linAttraction(n1, n2, e, distributedAttraction, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    if not distributedAttraction:
        factor = -coefficient * e
    else:
        factor = -coefficient * e / n1.mass
    n1.dx += xDist * factor
    n1.dy += yDist * factor
    n2.dx -= xDist * factor
    n2.dy -= yDist * factor


def apply_repulsion(nodes, coefficient):
    i = 0
    for n1 in nodes:
        j = i
        for n2 in nodes:
            if j == 0:
                break
            linRepulsion(n1, n2, coefficient)
            j -= 1

        i += 1


def apply_gravity(nodes, gravity, useStrongGravity=False):
    if not useStrongGravity:
        for n in nodes:
            linGravity(n, gravity)

    else:
        for n in nodes:
            strongGravity(n, gravity)


def apply_attraction(nodes, edges, distributedAttraction, coefficient, edgeWeightInfluence):
    if edgeWeightInfluence == 0:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], 1, distributedAttraction, coefficient)

    else:
        if edgeWeightInfluence == 1:
            for edge in edges:
                linAttraction(nodes[edge.node1], nodes[edge.node2], edge.weight, distributedAttraction, coefficient)

        else:
            for edge in edges:
                linAttraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edgeWeightInfluence), distributedAttraction, coefficient)


class Region:

    def __init__(self, nodes):
        self.mass = 0.0
        self.massCenterX = 0.0
        self.massCenterY = 0.0
        self.size = 0.0
        self.nodes = nodes
        self.subregions = []
        self.updateMassAndGeometry()

    def updateMassAndGeometry(self):
        if len(self.nodes) > 1:
            self.mass = 0
            massSumX = 0
            massSumY = 0
            for n in self.nodes:
                self.mass += n.mass
                massSumX += n.x * n.mass
                massSumY += n.y * n.mass

            self.massCenterX = massSumX / self.mass
            self.massCenterY = massSumY / self.mass
            self.size = 0.0
            for n in self.nodes:
                distance = sqrt((n.x - self.massCenterX) ** 2 + (n.y - self.massCenterY) ** 2)
                self.size = max(self.size, 2 * distance)

    def buildSubRegions(self):
        if len(self.nodes) > 1:
            leftNodes = []
            rightNodes = []
            for n in self.nodes:
                if n.x < self.massCenterX:
                    leftNodes.append(n)
                else:
                    rightNodes.append(n)

            topleftNodes = []
            bottomleftNodes = []
            for n in leftNodes:
                if n.y < self.massCenterY:
                    topleftNodes.append(n)
                else:
                    bottomleftNodes.append(n)

            toprightNodes = []
            bottomrightNodes = []
            for n in rightNodes:
                if n.y < self.massCenterY:
                    toprightNodes.append(n)
                else:
                    bottomrightNodes.append(n)

            if len(topleftNodes) > 0:
                if len(topleftNodes) < len(self.nodes):
                    subregion = Region(topleftNodes)
                    self.subregions.append(subregion)
                else:
                    for n in topleftNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            if len(bottomleftNodes) > 0:
                if len(bottomleftNodes) < len(self.nodes):
                    subregion = Region(bottomleftNodes)
                    self.subregions.append(subregion)
                else:
                    for n in bottomleftNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            if len(toprightNodes) > 0:
                if len(toprightNodes) < len(self.nodes):
                    subregion = Region(toprightNodes)
                    self.subregions.append(subregion)
                else:
                    for n in toprightNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            if len(bottomrightNodes) > 0:
                if len(bottomrightNodes) < len(self.nodes):
                    subregion = Region(bottomrightNodes)
                    self.subregions.append(subregion)
                else:
                    for n in bottomrightNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            for subregion in self.subregions:
                subregion.buildSubRegions()

    def applyForce(self, n, theta, coefficient=0):
        if len(self.nodes) < 2:
            linRepulsion(n, self.nodes[0], coefficient)
        else:
            distance = sqrt((n.x - self.massCenterX) ** 2 + (n.y - self.massCenterY) ** 2)
            if distance * theta > self.size:
                linRepulsion_region(n, self, coefficient)
            else:
                for subregion in self.subregions:
                    subregion.applyForce(n, theta, coefficient)

    def applyForceOnNodes(self, nodes, theta, coefficient=0):
        for n in nodes:
            self.applyForce(n, theta, coefficient)


def adjustSpeedAndApplyForces(nodes, speed, speedEfficiency, jitterTolerance):
    totalSwinging = 0.0
    totalEffectiveTraction = 0.0
    for n in nodes:
        swinging = sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
        totalSwinging += n.mass * swinging
        totalEffectiveTraction += 0.5 * n.mass * sqrt((n.old_dx + n.dx) * (n.old_dx + n.dx) + (n.old_dy + n.dy) * (n.old_dy + n.dy))

    estimatedOptimalJitterTolerance = 0.05 * sqrt(len(nodes))
    minJT = sqrt(estimatedOptimalJitterTolerance)
    maxJT = 10
    jt = jitterTolerance * max(minJT, min(maxJT, estimatedOptimalJitterTolerance * totalEffectiveTraction / (len(nodes) * len(nodes))))
    minSpeedEfficiency = 0.05
    if totalSwinging / totalEffectiveTraction > 2.0:
        if speedEfficiency > minSpeedEfficiency:
            speedEfficiency *= 0.5
        jt = max(jt, jitterTolerance)
    else:
        if totalSwinging == 0:
            targetSpeed = float('inf')
        else:
            targetSpeed = jt * speedEfficiency * totalEffectiveTraction / totalSwinging
        if totalSwinging > jt * totalEffectiveTraction:
            if speedEfficiency > minSpeedEfficiency:
                speedEfficiency *= 0.7
        elif speed < 1000:
            speedEfficiency *= 1.3
    maxRise = 0.5
    speed = speed + min(targetSpeed - speed, maxRise * speed)
    for n in nodes:
        swinging = n.mass * sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
        factor = speed / (1.0 + sqrt(speed * swinging))
        n.x = n.x + n.dx * factor
        n.y = n.y + n.dy * factor

    values = {}
    values['speed'] = speed
    values['speedEfficiency'] = speedEfficiency
    return values


try:
    import cython
except:
    print('No cython detected.  Install cython and compile the fa2util module for a 10-100x speed boost.')