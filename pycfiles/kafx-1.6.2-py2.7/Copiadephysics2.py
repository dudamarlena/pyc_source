# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\libs\Copiadephysics2.py
# Compiled at: 2012-01-06 00:42:12
"""
Created on Thu Jan 05 17:29:45 2012

@author: Nande!
"""
import Box2D as bd
from libs import video
from math import isnan

class World:

    def __init__(self, grav_x=0, grav_y=40.0, ground=True):
        self.velocityIterations = 4
        self.positionIterations = 4
        self.__timeStep = 1.0 / video.vi.fps
        self.maxx = video.vi.width
        self.maxy = video.vi.height
        self.hx = self.maxx / 2.0
        self.hy = self.maxy / 2.0
        self.__env = bd.b2AABB()
        self.__env.lowerBound.Set(0, 0)
        self.__env.upperBound.Set(self.maxx, self.maxy)
        self.gravity = bd.b2Vec2(grav_x, grav_y)
        self.__world = bd.b2World(self.__env, self.gravity, True)
        if ground:
            groundBodyDef = bd.b2BodyDef()
            groundBodyDef.position = [self.hx, self.maxy]
            self.groundBody = self.__world.CreateBody(groundBodyDef)
            groundShapeDef = bd.b2PolygonDef()
            groundShapeDef.SetAsBox(self.hx, 2)
            self.groundBody.CreateShape(groundShapeDef)
            self.sprites = []
            self.vectors = []

    def Update(self, updateObjs=True):
        self.__world.Step(self.__timeStep, self.velocityIterations, self.positionIterations)
        if updateObjs:
            for sp in self.sprites:
                UpdateSprite(sp)

            for vec in self.vectors:
                UpdateVector(vec)

    def Destroy(self, obj):
        self.__world.DestroyBody(obj.body)
        if obj in self.vectors:
            self.vectors.remove(obj)
        if obj in self.sprites:
            self.sprites.remove(obj)
        del obj.body

    def CreateBody(self, pos_x, pos_y, width, height, dynamic=True):
        bodyDef = bd.b2BodyDef()
        bodyDef.position = (pos_x, pos_y)
        body = self.__world.CreateBody(bodyDef)
        shape = bd.b2PolygonDef()
        shape.SetAsBox(width, height)
        if dynamic:
            shape.density = 1.0
        shape.friction = 0.3
        body.CreateShape(shape)
        if dynamic:
            body.SetMassFromShapes()
        return body

    def CreateVector(self, vector, dynamic=True):
        a = vector.actual
        x = a.pos_x + a.org_x
        y = a.pos_y - a.org_y
        w = vector.original._ancho / 2.0
        h = vector.original._alto / 2.0
        vector.body = self.CreateBody(x, y, w, h, dynamic)
        self.vectors.append(vector)

    def CreateSprite(self, sprite, dynamic=True):
        sprite.body = self.CreateBody(sprite.x + sprite.org_x, sprite.y + sprite.org_y, sprite._ancho * (1.0 / sprite.scale_x) / 2.0, sprite._alto * (1.0 / sprite.scale_y) / 2.0, dynamic)
        self.sprites.append(sprite)


def UpdateVector(vector):
    pos = vector.body.position
    a = vector.actual
    a.pos_x = pos.x - a.org_x
    a.pos_y = pos.y + a.org_y
    a.angle = vector.body.GetAngle()
    if isnan(a.angle):
        a.angle = 0.0


def Wake(obj):
    body = obj.body
    if body.isSleeping:
        body.WakeUp()


def Sleep(obj):
    obj.body.PutToSleep()


def UpdateSprite(sprite):
    pos = sprite.body.position
    sprite.x = pos.x - sprite.org_x
    sprite.y = pos.y - sprite.org_y
    sprite.angle = sprite.body.GetAngle()
    if isnan(sprite.angle):
        sprite.angle = 0.0