# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parang/project20m.py
# Compiled at: 2009-08-22 22:50:09
"""Project20M - A Python version of Project20M
    Copyright (C) 2004-2008  Andrew Huff, Vincent Chan, Laurence Tondelier,
    Damian Bundred, Colm Egan, and Eric Wald
    
    This software may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this software for
    commercial purposes without permission from the authors is prohibited.
"""
from random import random
from parlance.config import VerboseObject
from parlance.gameboard import Unit
from parlance.orders import *
from parlance.player import Player
from parlance.tokens import AMY, FLT, SPR, SUM, WIN

class Project20M(Player):
    """ A clone of Andrew Huff's bot.
        This class is approximately equivalent to Project20M's PrimeMinister.
        Most of the functionality of the PrimeMinister and Project20M
        java classes are already included in Player or Client.
    """

    def handle_HLO(self, message):
        self.__super.handle_HLO(message)
        if self.power:
            self.map.us = self.power
            self.t = Tactics(self.map)
        self.log_debug(7, 'Game Started, you are playing %s, your passcode is %d', self.power.name, self.pcode)

    def generate_orders(self):
        turn = self.map.current_turn
        phase = turn.phase()
        self.log_debug(7, 'PrimeMinister: *************** Season %s **************** ', turn.season)
        self.t.valueProvinces()
        if phase == turn.build_phase:
            orders = self.t.adjustments()
            self.sendOrders(orders)
        elif phase == turn.retreat_phase:
            orders = []
            for unit in self.power.units:
                self.log_debug(7, 'busy loop here?')
                if unit.dislodged:
                    orders.append(self.getRetreat(unit))

            self.sendOrders(orders)
        elif phase == turn.move_phase:
            n = Coordinator(self.map, self.t)
            theOrders = n.coordinateUnits()
            self.sendOrders(theOrders)

    def handle_SCO(self, message):
        if self.in_game and self.power:
            self.log_debug(7, 'We have %d supply centers.', len(self.power.centers))

    def getRetreat(self, thisUnit):
        self.log_debug(7, 'PrimeMinister: suggesting retreat for unit in %s', thisUnit.coast.province.name)
        retreatTos = [ self.map.coasts[key] for key in thisUnit.coast.borders_out if key[1] in thisUnit.retreats
                     ]
        return self.t.getBestRetreat(thisUnit, retreatTos)

    def sendOrders(self, orders):
        if orders:
            self.log_debug(7, 'PrimeMinister: Final Orders')
            order_set = OrderSet(self.power)
            for order in orders:
                self.log_debug(7, order)
                order_set.add(order)

            self.submit_set(order_set)
            self.log_debug(7, 'PrimeMinister: Orders sent')
        else:
            self.log_debug(7, 'PrimeMinister: No orders to send')


class Tactics(VerboseObject):

    def __init__(self, board):
        self.__super.__init__()
        self.map = board
        self.lastTurnsOrders = []
        for coast in board.coasts.values():
            coast.basicValue = [0] * Constants.numberIterations
            coast.connections = [ board.coasts[key] for key in coast.borders_out
                                ]

        for coast in board.coasts.values():
            coast.landConnections = sum([ c.connections for c in coast.province.coasts if c.unit_type is AMY
                                        ], [])
            coast.seaConnections = sum([ c.connections for c in coast.province.coasts if c.unit_type is FLT
                                       ], [])

    def valueProvinces(self):
        self.enumerateValues()

    def getBestOrders(self):
        return self.createOrders()

    def getNextBestOrder(self, order):
        orders = self.getValidOrders(order.unit)
        filteredOrders = self.filter(orders)
        bestOrder = None
        bestScore = -9999999
        for possibleOrder in filteredOrders:
            thisScore = evaluate(possibleOrder, self.map)
            if bestScore < thisScore < evaluate(order, self.map):
                bestOrder = possibleOrder
                bestScore = thisScore

        if not bestOrder:
            for possibleOrder in orders:
                thisScore = evaluate(possibleOrder, self.map)
                if bestScore < thisScore < evaluate(order, self.map):
                    bestOrder = possibleOrder
                    bestScore = thisScore

        if not bestOrder:
            self.log_debug(7, 'getNextBestOrder returned null!? Returning a hold')
            bestOrder = HoldOrder(order.unit)
        return bestOrder

    def adjustments(self):
        numberBuilds = len(self.map.us.centers) - len(self.map.us.units)
        if numberBuilds > 0:
            self.log_debug(7, 'Suggesting builds')
            return self.suggestBuilds(numberBuilds)
        elif numberBuilds < 0:
            self.log_debug(7, 'Suggesting removes')
            return self.suggestRemoves(-numberBuilds)
        else:
            return
        return

    def getBestRetreat(self, unit, canRetreatTo):
        retreatOrders = []
        for thisPlace in canRetreatTo:
            if not thisPlace.province.units:
                retreatOrders.append(RetreatOrder(unit, thisPlace))

        if not retreatOrders:
            return DisbandOrder(unit)
        retreatOrders.sort(self.compareTo)
        bestRetreat = retreatOrders[0]
        target(bestRetreat).units.append(unit)
        self.log_debug(7, 'retreating with: %s', bestRetreat)
        return bestRetreat

    def removeDuplicates(self, l):
        result = []
        for item in l:
            if item not in result:
                result.append(item)

        return result

    def enumerateValues(self):
        if self.map.current_turn.season in (SPR, SUM, WIN):
            self.setBasicValues(Constants.spring_defence_weight, Constants.spring_attack_weight)
            self.setStrengthAndCompetitionValues()
            self.setFinalValues(Constants.spring_iteration_weight, Constants.spring_strength_weight, Constants.spring_competition_weight)
        else:
            self.setBasicValues(Constants.autumn_defence_weight, Constants.autumn_attack_weight)
            self.setStrengthAndCompetitionValues()
            self.setFinalValues(Constants.autumn_iteration_weight, Constants.autumn_strength_weight, Constants.autumn_competition_weight)

    def setBasicValues(self, defence_weight, attack_weight):
        self.calculateInitialValues(defence_weight, attack_weight)
        self.iterateValues(Constants.numberIterations)

    def setStrengthAndCompetitionValues(self):
        for theProvince in self.map.spaces.values():
            powers = self.map.powers.keys()
            numbers = getNumberOfAdjacentUnits(theProvince, powers, self.map)
            for i in range(len(powers)):
                if powers[i] == self.map.us:
                    theProvince.strength = numbers[i]
                    numbers[i] = 0

            numbers.sort()
            theProvince.competition = numbers[(-1)]

    def setFinalValues(self, iteration_weight, strength_weight, competition_weight):
        for thePlace in self.map.coasts.values():
            thePlace.Value = 0
            for j in range(Constants.numberIterations):
                thePlace.Value += thePlace.basicValue[j] * iteration_weight[j]

    def calculateInitialValues(self, defence_weight, attack_weight):
        for theProvince in self.map.spaces.values():
            if theProvince.is_supply():
                if not theProvince.owner:
                    theProvince.basicValue = self.getWeakestPower() * attack_weight
                elif theProvince.owner == self.map.us:
                    theProvince.basicValue = strongestAdjacentOpponentStrength(theProvince, self.map) * defence_weight
                else:
                    ownerStrength = getStrength(theProvince.owner)
                    theProvince.basicValue = ownerStrength * attack_weight
                if self.map.us in theProvince.homes:
                    theProvince.basicValue *= 1.1
            else:
                theProvince.basicValue = 0
            for thisCoast in theProvince.coasts:
                thisCoast.basicValue[0] = theProvince.basicValue

    def getAveragePower(self):
        averagePower = 0
        for iterator in self.map.powers.values():
            averagePower += getStrength(iterator)

        averagePower /= len(self.map.powers)
        return averagePower

    def getWeakestPower(self):
        iterator = self.map.powers.itervalues()
        thisPower = iterator.next()
        weakestPower = getStrength(thisPower)
        for thisPower in iterator:
            if getStrength(thisPower) < weakestPower:
                weakestPower = getStrength(thisPower)

        return weakestPower

    def iterateValues(self, n):
        allPlaces = self.map.coasts.values()
        for i in range(1, n):
            for thePlace in allPlaces:
                thePlace.basicValue[i] = 0
                landConnections = thePlace.landConnections
                seaConnections = thePlace.seaConnections
                if thePlace.unit_type is AMY:
                    canGetToByConvoy = []
                    for seaConnection in seaConnections:
                        if seaConnection.province.units and seaConnection.province.unit.can_convoy():
                            for couldConvoyTo in seaConnection.seaConnections:
                                beach = couldConvoyTo.province.is_coastal()
                                if beach and beach not in landConnections:
                                    canGetToByConvoy.append(beach)

                    canGetToByConvoy = self.removeDuplicates(canGetToByConvoy)
                    for thisConnection in canGetToByConvoy:
                        thePlace.basicValue[i] += self.map.coasts[thisConnection].basicValue[(i - 1)] * 0.05

                for thisConnection in landConnections:
                    if thePlace.unit_type is thisConnection.unit_type:
                        thePlace.basicValue[i] += thisConnection.basicValue[(i - 1)]
                    elif thisConnection not in seaConnections:
                        thePlace.basicValue[i] += thisConnection.basicValue[(i - 1)] * 0.001

                for thisConnection in seaConnections:
                    if thePlace.unit_type is thisConnection.unit_type:
                        thePlace.basicValue[i] += thisConnection.basicValue[(i - 1)]
                    elif thisConnection not in landConnections:
                        thePlace.basicValue[i] += thisConnection.basicValue[(i - 1)] * 0.02

                thePlace.basicValue[i] += thePlace.basicValue[(i - 1)]
                thePlace.basicValue[i] /= Constants.iteration_army_divisor

    def createOrders(self):
        orders = []
        allOurUnits = self.map.us.units
        self.log_debug(11, '******* creating basic orders')
        for theUnit in allOurUnits:
            order = self.getBestOrder(theUnit)
            orders.append(order)
            self.log_debug(11, 'basic order: %s', order)

        self.log_debug(11, '******* finished creating basic orders')
        self.lastTurnsOrders = orders
        return orders

    def filter(self, orders):
        filteredOrders = []
        for thisOrder in orders:
            if isValuable(target(thisOrder), self.map):
                filteredOrders.append(thisOrder)

        if self.map.current_turn.season is SPR:
            for thisOrder in orders:
                withinTwo = thisOrder.destination.connections
                if self.hasValuable(withinTwo):
                    filteredOrders.append(thisOrder)

        if not filteredOrders:
            filteredOrders.extend(orders)
        return filteredOrders

    def getBestOrder(self, u):
        orders = self.getValidOrders(u)
        filteredOrders = self.filter(orders)
        filteredOrders.sort(self.compareTo)
        bestOrder = filteredOrders[0]
        for order in orders:
            self.log_debug(12, '%s: %s %s %s', order, evaluate(order, self.map), order in filteredOrders, order in self.lastTurnsOrders)

        if bestOrder in self.lastTurnsOrders:
            if len(filteredOrders) > 1 and random() > 0.9:
                self.log_debug(7, 'RANDOM: CHOOSING THE 2ND BEST ORDER FOR %s', u)
                bestOrder = filteredOrders[1]
        if isinstance(bestOrder, HoldOrder) and target(bestOrder).owner == self.map.us:
            for thisPlace in canMoveTo(bestOrder.unit):
                if thisPlace.province.is_supply() and thisPlace.province.owner != self.map.us:
                    bestOrder = MoveOrder(u, thisPlace)
                    return bestOrder

            surroundingUnits = getSurroundingUnits(target(bestOrder), self.map)
            if len(surroundingUnits) == 1:
                location = surroundingUnits[0].coast
                if location in canMoveTo(u):
                    self.log_debug(7, '%s IS HOLDING ON A SUPPLY CENTRE ONLY THREATENED BY %s', u, surroundingUnits[0])
                    self.log_debug(7, 'SO IT IS MOVING INTO %s', surroundingUnits[0].coast)
                    bestOrder = MoveOrder(u, surroundingUnits[0].coast)
        return bestOrder

    def hasValuable(self, places):
        for place in places:
            if isValuable(place.province, self.map):
                return True

        return False

    def getBestBuild(self):
        ownedBuildCentres = self.getOwnedBuildCentres()
        canBuild = []
        for thisProvince in ownedBuildCentres:
            if not thisProvince.units:
                canBuild.append(thisProvince)

        if not canBuild:
            return WaiveOrder(self.map.us)
        bestSoFar = BuildOrder(Unit(self.map.us, canBuild[0].coasts[0]))
        for thisProvince in canBuild:
            for thisCoast in thisProvince.coasts:
                newArmy = BuildOrder(Unit(self.map.us, thisCoast))
                if evaluate(newArmy, self.map) > evaluate(bestSoFar, self.map):
                    bestSoFar = newArmy

        return bestSoFar

    def suggestBuilds(self, numberBuilds):
        builds = []
        for i in range(numberBuilds):
            self.valueProvinces()
            bestBuild = self.getBestBuild()
            if isinstance(bestBuild, BuildOrder):
                bestBuild.unit.build()
            builds.append(bestBuild)

        return builds

    def getBestRemove(self):
        ourUnits = self.map.us.units
        bestSoFar = RemoveOrder(ourUnits[0])
        for iterator in ourUnits:
            newRemove = RemoveOrder(iterator)
            if evaluate(newRemove, self.map) > evaluate(bestSoFar, self.map):
                bestSoFar = newRemove

        return bestSoFar

    def suggestRemoves(self, numRemoves):
        removes = []
        for i in range(numRemoves):
            self.valueProvinces()
            bestRemove = self.getBestRemove()
            bestRemove.unit.die()
            removes.append(bestRemove)

        return removes

    def suggestRetreat(self, u, retreatTos):
        self.log_debug(7, 'Tactics: Suggesting Retreats')
        canBuildAts = self.getOwnedBuildCentres()
        decisions = []
        highestValuedRetreat = retreatTos[0]
        retreatValue = highestValuedRetreat.Value
        for retreatTo in retreatTos[1:]:
            self.log_debug(7, 'Tactics: considering retreat to %s', retreatTo)
            thisValue = retreatTo.Value
            if thisValue > retreatValue:
                highestValuedRetreat = retreatTo
                retreatValue = thisValue

        self.log_debug(7, 'Tactics: HighestValuedRetreat = %s', highestValuedRetreat.name)
        if self.map.current_turn.season is WIN:
            highestValuedBuild = BuildOrder(Unit(self.map.us, canBuildAts[0].coasts[0]))
            for canBuildAt in canBuildAts:
                for thisCoast in canBuildAt.coasts:
                    possibleBuild = BuildOrder(Unit(self.map.us, thisCoast))
                    if evaluate(possibleBuild, self.map) > evaluate(highestValuedBuild, self.map):
                        highestValuedBuild = possibleBuild

            highestValued = canBuildAts[0]
            for thisProvince in canBuildAts:
                pass

            if evaluate(highestValuedBuild, self.map) >= retreatValue:
                highestValuedBuild.unit.build()
                decisions.append(DisbandOrder(u))
                decisions.append(highestValuedBuild)
            else:
                decisions.append(MoveOrder(u, highestValuedRetreat))
        else:
            decisions.append(RetreatOrder(u, highestValuedRetreat))
        return decisions

    def getValidOrders(self, unit):
        validOrders = []
        validOrders.append(HoldOrder(unit))
        for key in unit.coast.borders_out:
            validOrders.append(MoveOrder(unit, self.map.coasts[key]))

        if unit.can_be_convoyed():
            for key in unit.coast.province.borders_out:
                seaConnection = self.map.spaces[key]
                if seaConnection.units and seaConnection.unit.can_convoy():
                    for place in seaConnection.borders_out:
                        couldConvoyTo = self.map.spaces[place].is_coastal()
                        if couldConvoyTo:
                            seaProvinces = [
                             seaConnection.unit]
                            validOrders.append(ConvoyedOrder(unit, self.map.coasts[couldConvoyTo], seaProvinces))

        return validOrders

    def getOwnedBuildCentres(self):
        return [ self.map.spaces[home] for home in self.map.us.homes if home in self.map.us.centers
               ]

    def compareTo(self, this, o):
        return int(evaluate(o, self.map) - evaluate(this, self.map))


class Coordinator(VerboseObject):

    def __init__(self, board, tactics):
        self.__super.__init__()
        self.map = board
        self.tactics = tactics
        self.wantedOrders = []

    def coordinateUnits(self, weDo=None, theyDo=None):
        if not weDo:
            weDo = []
        elif not isinstance(weDo, list):
            weDo = [
             weDo]
        if not theyDo:
            theyDo = []
        elif not isinstance(theyDo, list):
            theyDo = [
             theyDo]
        self.wantedOrders = []
        orderList = self.tactics.getBestOrders()
        for order in weDo:
            if order:
                order.helping = order.orderToSupport
                self.changeOrder(order.unit, order, orderList)

        for order in orderList:
            order.unit.order = order

        self.log_debug(11, '**** coordinating units ****')
        orderList.sort(self.tactics.compareTo)
        for i in range(len(orderList)):
            orderList = self.coordinateUnit(orderList, i, theyDo)

        self.log_debug(11, '**** finished coordinating units ****')
        return orderList

    def getWantedOrders(self):
        self.log_debug(7, '******wantedOrders:')
        i = 0
        while i < len(self.wantedOrders):
            order = self.wantedOrders[i]
            if isinstance(order, SupportMoveOrder) and target(order).units and target(order).unit.nation == order.unit.nation:
                self.wantedOrders.pop(i)
            else:
                self.log_debug(7, order)
                i += 1

        self.log_debug(7, '*******************')
        return self.wantedOrders

    def coordinateUnit(self, orderList, i, theyDo):
        order = orderList[i]
        self.log_debug(11, 'looking at %s', order)
        avaliables = self.getUnitsAvaliable(orderList, i)
        for clash in orderList:
            if clash is not order and target(clash) == target(order):
                self.log_debug(12, '%s clashes with %s', order, clash)
                outOfWay = self.getBestOutOfTheWayOrder(clash.unit, orderList)
                if clash.unit in avaliables and outOfWay:
                    orderList = self.changeOrder(clash.unit, outOfWay, orderList)
                    self.log_debug(11, '%s agrees to do %s', outOfWay.unit, outOfWay)
                else:
                    nextBestOrder = self.tactics.getNextBestOrder(order)
                    orderList = self.changeOrder(order.unit, nextBestOrder, orderList)
                    self.log_debug(11, 'changing to %s because of %s', nextBestOrder, clash)
                    orderList = self.coordinateUnit(orderList, i, theyDo)
                    return orderList

        alsoAvaliables = self.getUnitsAlsoAvaliable(orderList, i)
        avaliables = alsoAvaliables + avaliables
        if isinstance(order, ConvoyedOrder):
            needed = order.path[0]
            if needed in avaliables:
                newOrder = ConvoyingOrder(needed, order.unit, order.destination)
                newOrder.helping = order
                orderList = self.changeOrder(needed, newOrder, orderList)
                self.log_debug(11, '%s agrees to do %s', needed, newOrder)
            else:
                if needed.nation != self.map.us:
                    wantedOrder = ConvoyingOrder(needed, order.unit, order.destination)
                    wantedOrder.helping = order
                    self.wantedOrders.append(wantedOrder)
                nextBestOrder = self.tactics.getNextBestOrder(order)
                orderList = self.changeOrder(order.unit, nextBestOrder, orderList)
                self.log_debug(11, "Couldn't get the convoy orders done, so now doing %s", nextBestOrder)
                orderList = self.coordinateUnit(orderList, i, theyDo)
                return orderList
        supportsNeeded = getSupportsNeeded(order, self.map)
        self.log_debug(11, '%d supports needed', supportsNeeded)
        if isinstance(order, MoveOrder) and target(order).units and target(order).unit.nation == self.map.us:
            supportsNeeded = 0
            self.log_debug(11, "But we're not going to ask for any support as we're following one of our units")
        couldGiveSupport = couldBeSupportedBy(order, self.map)
        for couldHelp in couldGiveSupport:
            if supportsNeeded <= 0:
                break
            self.log_debug(11, '%s could support us...', couldHelp)
            if couldHelp in avaliables:
                self.log_debug(11, '%s will support us', couldHelp)
                supportOrder = self.Support(couldHelp, order)
                supportOrder.helping = order
                orderList = self.changeOrder(couldHelp, supportOrder, orderList)
                avaliables.remove(couldHelp)
                supportsNeeded -= 1
            elif couldHelp.nation != self.map.us:
                wantedOrder = self.Support(couldHelp, order)
                wantedOrder.helping = order
                self.wantedOrders.append(wantedOrder)

        return orderList

    def evaluate(self, orderList):
        value = 0
        for order in orderList:
            value += evaluate(order, self.map)
            if isinstance(order, SupportOrder) and order.supported.nation == self.map.us:
                value += 0.75 * evaluate(order.orderToSupport, self.map)

        if value < 0:
            value *= -1
        return value

    def getBestOutOfTheWayOrder(self, unit, orderList):
        validOrders = self.tactics.getValidOrders(unit)
        possibleOrders = []
        for validOrder in validOrders:
            possible = True
            for inList in orderList:
                if isinstance(validOrder, ConvoyedOrder) or validOrder.destination == inList.destination or target(validOrder).units and target(validOrder).unit.nation == self.map.us:
                    possible = False

            if possible:
                possibleOrders.append(validOrder)

        if not possibleOrders:
            return
        possibleOrders.sort(self.tactics.compareTo)
        return possibleOrders[0]

    def getOrderFor(self, unit, orderList):
        for order in orderList:
            if order.unit == unit:
                return order

        return

    def changeOrder(self, unit, order, orderList):
        orderList = [ orderInList for orderInList in orderList if unit != orderInList.unit
                    ]
        orderList.append(order)
        orderList.sort(self.tactics.compareTo)
        order.unit.order = order
        return orderList

    def getUnitsAvaliable(self, orderList, i):
        avaliableToHelp = []
        for order in orderList[i + 1:]:
            if not order.helping or order.helping == orderList[i]:
                avaliableToHelp.append(order.unit)

        return avaliableToHelp

    def getUnitsAlsoAvaliable(self, orderList, i):
        alsoAvaliable = []
        for order in orderList[:i]:
            if isinstance(order, HoldOrder):
                alsoAvaliable.append(order.unit)

        return alsoAvaliable

    def Support(self, unit, order):
        if order.is_moving():
            result = SupportMoveOrder(unit, order.unit, order.destination)
        else:
            result = SupportHoldOrder(unit, order.unit)
        result.orderToSupport = order
        return result


class Constants(object):
    numberIterations = 10
    spring_attack_weight = 70
    spring_defence_weight = 30
    autumn_attack_weight = 60
    autumn_defence_weight = 40
    iteration_fleet_divisor = 5
    iteration_army_divisor = 5
    spring_iteration_weight = [
     1000, 100, 30, 10, 6, 5, 4, 3, 2, 1]
    spring_strength_weight = 2
    spring_competition_weight = 2
    autumn_iteration_weight = [
     1000, 100, 30, 10, 6, 5, 4, 3, 2, 1]
    autumn_strength_weight = 2
    autumn_competition_weight = 2
    build_defence_weight = 1000
    build_iteration_weight = [
     1000, 100, 30, 10, 6, 5, 4, 3, 2, 1]
    remove_defence_weight = 1000
    remove_iteration_weight = [
     1000, 100, 30, 10, 6, 5, 4, 3, 2, 1]
    play_alternative = 50
    alternative_difference_modifier = 500


Unit.order = None

def getStrength(power):
    A = 1.0
    B = 4.0
    C = 16.0
    x = len(power.centers)
    return A * x * x + B * x + C


def getNumberOfAdjacentUnits(province, powerList, board):
    surroundingUnits = getALLSurroundingUnits(province, board)
    numbers = [ 0 for p in powerList ]
    for surroundingUnit in surroundingUnits:
        for (j, power) in enumerate(powerList):
            if surroundingUnit.nation == power:
                numbers[j] += 1

    return numbers


def getALLSurroundingUnits(province, board):
    surroundingUnits = []
    for prov in province.borders_in:
        other = board.spaces[prov]
        surroundingUnits.extend([ u for u in other.units if u.can_move_to(province)
                                ])

    return surroundingUnits


def getSurroundingUnits(province, board):
    surroundingUnits = []
    for prov in province.borders_in:
        other = board.spaces[prov]
        surroundingUnits.extend([ u for u in other.units if u.can_move_to(province) if u.nation != board.us
                                ])

    return surroundingUnits


def getSurroundingPowers(province, board):
    surroundingUnits = getSurroundingUnits(province, board)
    surroundingPowers = []
    for surroundingUnit in surroundingUnits:
        thisOwner = surroundingUnit.nation
        if thisOwner not in surroundingPowers:
            surroundingPowers.append(thisOwner)

    return surroundingPowers


def isValuable(province, board):
    if province.is_supply() and (province.owner != board.us or len(getSurroundingUnits(province, board)) > 0):
        return True
    return False


def strongestAdjacentOpponentStrength(province, board):
    surroundingPowers = getSurroundingPowers(province, board)
    strongest = 0
    for surroundingPower in surroundingPowers:
        if surroundingPower != board.us:
            thisStrength = getStrength(surroundingPower)
            if thisStrength > strongest:
                strongest = thisStrength

    return strongest


def canMoveTo(unit):
    return unit.coast.connections


UnitOrder.helping = None

def couldBeSupportedBy(order, board):
    if isinstance(order, (MoveOrder, ConvoyedOrder)):
        aroundTarget = getALLSurroundingUnits(target(order), board)
        while order.unit in aroundTarget:
            aroundTarget.remove(order.unit)

        return aroundTarget
    else:
        return getALLSurroundingUnits(order.unit.coast.province, board)


def doStrengthCompetition(order, value, board):
    if getSupportsNeeded(order, board) > 1:
        value *= 2 ** target(order).strength
    return value


def evaluate(order, board):
    if isinstance(order, BuildOrder):
        return order.unit.coast.Value
    elif isinstance(order, (DisbandOrder, RemoveOrder)):
        return -order.unit.coast.Value
    elif isinstance(order, MoveOrder):
        if order.unit.nation == board.us:
            if order.unit.coast == order.destination:
                return 0
            value = order.destination.Value - order.unit.coast.Value
            conflict = getResistance(order, 100, board) + 1
            if getSupportsNeeded(order, board) > 1:
                value *= 2 ** target(order).strength
            if target(order).unit:
                conflict += 1
            value /= conflict * conflict
            if target(order).unit and target(order).unit.nation == board.us:
                value /= 200
            return value
        else:
            return 0
    elif isinstance(order, RetreatOrder):
        return order.destination.Value - order.unit.coast.Value
    elif isinstance(order, WaiveOrder):
        return 0
    elif order.unit.nation == board.us:
        value = 0.001 * order.unit.coast.Value
        value = doStrengthCompetition(order, value, board)
        return value
    else:
        return 0


def getResistance(move_order, hops, board):
    if hops == 0:
        return 0
    resistance = getSupportsNeeded(move_order, board)
    if target(move_order).unit and target(move_order).unit.nation == move_order.unit.nation and target(move_order).unit.order:
        inWay = target(move_order).unit
        if isinstance(inWay.order, MoveOrder):
            resistance += getResistance(inWay.order, hops - 1, board)
        else:
            resistance += getSupportsNeeded(inWay.order, board)
    return resistance


def getSupportsNeeded(order, board):
    if isinstance(order, ConvoyedOrder):
        supportsNeeded = len(getSurroundingUnits(target(order), board))
        if target(order).unit and target(order).unit.nation != board.us:
            supportsNeeded += 1
        return supportsNeeded
    elif isinstance(order, (ConvoyingOrder, HoldOrder, SupportOrder)):
        where = order.unit.coast.province
        supportsNeeded = len(getSurroundingUnits(where, board))
        if supportsNeeded > 0:
            supportsNeeded -= 1
        return supportsNeeded
    elif isinstance(order, MoveOrder):
        supportsNeeded = len(getSurroundingUnits(target(order), board))
        if target(order).unit and target(order).unit.nation != board.us:
            supportsNeeded += 1
        elif target(order).owner == board.us and supportsNeeded > 0:
            supportsNeeded -= 1
        return supportsNeeded
    else:
        return 0


def target(order):
    if isinstance(order, (ConvoyingOrder, SupportOrder)):
        return order.supported.coast.province
    return order.destination.province


def run():
    from parlance.main import run_player
    run_player(Project20M)