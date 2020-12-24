# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/gym_bci/envs/pacman/pacman.py
# Compiled at: 2019-11-13 19:04:27
# Size of source mod 2**32: 26214 bytes
"""
Pacman.py holds the logic for the classic pacman game along with the main
code to run a game.  This file is divided into three sections:

  (i)  Your interface to the pacman world:
          Pacman is a complex environment.  You probably don't want to
          read through all of the code we wrote to make the game runs
          correctly.  This section contains the parts of the code
          that you will need to understand in order to complete the
          project.  There is also some code in game.py that you should
          understand.

  (ii)  The hidden secrets of pacman:
          This section contains all of the logic code that the pacman
          environment uses to decide who can move where, who dies when
          things collide, etc.  You shouldn't need to read this section
          of code, but you can if you want.

  (iii) Framework to start a game:
          The final section contains the code for reading the command
          you use to set up the game, then starting up a new game, along with
          linking in all the external parts (agent functions, graphics).
          Check this section out to see all the options available to you.

To play your first game, type 'python pacman.py' from the command line.
The keys are 'a', 's', 'd', and 'w' to move (or arrow keys).  Have fun!
"""
from .game import GameStateData, Game, Directions, Actions
from .util import nearestPoint, manhattanDistance
from .layout import getLayout
import sys, types, time, random, os

class GameState:
    __doc__ = '\n    A GameState specifies the full game state, including the food, capsules,\n    agent configurations and score changes.\n\n    GameStates are used by the Game object to capture the actual state of the game and\n    can be used by agents to reason about the game.\n\n    Much of the information in a GameState is stored in a GameStateData object.  We\n    strongly suggest that you access that data via the accessor methods below rather\n    than referring to the GameStateData object directly.\n\n    Note that in classic Pacman, Pacman is always agent 0.\n    '
    explored = set()

    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp

    getAndResetExplored = staticmethod(getAndResetExplored)

    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        if self.isWin() or self.isLose():
            return []
        if agentIndex == 0:
            return PacmanRules.getLegalActions(self)
        return GhostRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        if self.isWin() or self.isLose():
            raise Exception("Can't generate a successor of a terminal state.")
        else:
            state = GameState(self)
            if agentIndex == 0:
                state.data._eaten = [False for i in range(state.getNumAgents())]
                PacmanRules.applyAction(state, action)
            else:
                GhostRules.applyAction(state, action, agentIndex)
            if agentIndex == 0:
                state.data.scoreChange += -TIME_PENALTY
            else:
                GhostRules.decrementTimer(state.data.agentStates[agentIndex])
        GhostRules.checkDeath(state, agentIndex)
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getLegalPacmanActions(self):
        return self.getLegalActions(0)

    def generatePacmanSuccessor(self, action):
        """
        Generates the successor state after the specified pacman move
        """
        return self.generateSuccessor(0, action)

    def getPacmanState(self):
        """
        Returns an AgentState object for pacman (in game.py)

        state.pos gives the current position
        state.direction gives the travel vector
        """
        return self.data.agentStates[0].copy()

    def getPacmanPosition(self):
        return self.data.agentStates[0].getPosition()

    def getGhostStates(self):
        return self.data.agentStates[1:]

    def getGhostState(self, agentIndex):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise Exception('Invalid index passed to getGhostState')
        return self.data.agentStates[agentIndex]

    def getGhostPosition(self, agentIndex):
        if agentIndex == 0:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.data.agentStates[agentIndex].getPosition()

    def getGhostPositions(self):
        return [s.getPosition() for s in self.getGhostStates()]

    def getNumAgents(self):
        return len(self.data.agentStates)

    def getScore(self):
        return float(self.data.score)

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining capsules.
        """
        return self.data.capsules

    def getNumFood(self):
        return self.data.food.count()

    def getFood(self):
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.data.food

    def getWalls(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

    def hasFood(self, x, y):
        return self.data.food[x][y]

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y]

    def isLose(self):
        return self.data._lose

    def isWin(self):
        return self.data._win

    def __init__(self, prevState=None):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None:
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def deepCopy(self):
        state = GameState(self)
        state.data = self.data.deepCopy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.data)

    def __str__(self):
        return str(self.data)

    def initialize(self, layout, numGhostAgents=1000):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.data.initialize(layout, numGhostAgents)


SCARED_TIME = 40
COLLISION_TOLERANCE = 0.7
TIME_PENALTY = 1

class ClassicGameRules:
    __doc__ = '\n    These game rules manage the control flow of a game, deciding when\n    and how the game starts and ends.\n    '

    def __init__(self, timeout=30):
        self.timeout = timeout

    def newGame(self, layout, pacmanAgent, ghostAgents, display, quiet=False, catchExceptions=False):
        agents = [
         pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize(layout, len(ghostAgents))
        game = Game(agents, display, self, catchExceptions=catchExceptions)
        game.state = initState
        self.initialState = initState.deepCopy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        """
        Checks to see whether it is time to end the game.
        """
        if state.isWin():
            self.win(state, game)
        if state.isLose():
            self.lose(state, game)

    def win(self, state, game):
        if not self.quiet:
            print('Pacman emerges victorious! Score: %d' % state.data.score)
        game.gameOver = True

    def lose(self, state, game):
        if not self.quiet:
            print('Pacman died! Score: %d' % state.data.score)
        game.gameOver = True

    def getProgress(self, game):
        return float(game.state.getNumFood()) / self.initialState.getNumFood()

    def agentCrash(self, game, agentIndex):
        if agentIndex == 0:
            print('Pacman crashed')
        else:
            print('A ghost crashed')

    def getMaxTotalTime(self, agentIndex):
        return self.timeout

    def getMaxStartupTime(self, agentIndex):
        return self.timeout

    def getMoveWarningTime(self, agentIndex):
        return self.timeout

    def getMoveTimeout(self, agentIndex):
        return self.timeout

    def getMaxTimeWarnings(self, agentIndex):
        return 0


class PacmanRules:
    __doc__ = '\n    These functions govern how pacman interacts with his environment under\n    the classic game rules.\n    '
    PACMAN_SPEED = 1

    def getLegalActions(state):
        """
        Returns a list of possible actions.
        """
        return Actions.getPossibleActions(state.getPacmanState().configuration, state.data.layout.walls)

    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action):
        """
        Edits the state to reflect the results of the action.
        """
        legal = PacmanRules.getLegalActions(state)
        if action not in legal:
            raise Exception('Illegal action ' + str(action))
        pacmanState = state.data.agentStates[0]
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.configuration = pacmanState.configuration.generateSuccessor(vector)
        next = pacmanState.configuration.getPosition()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            PacmanRules.consume(nearest, state)

    applyAction = staticmethod(applyAction)

    def consume(position, state):
        x, y = position
        if state.data.food[x][y]:
            state.data.scoreChange += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._foodEaten = position
            numFood = state.getNumFood()
            if numFood == 0:
                if not state.data._lose:
                    state.data.scoreChange += 500
                    state.data._win = True
        if position in state.getCapsules():
            state.data.capsules.remove(position)
            state.data._capsuleEaten = position
            for index in range(1, len(state.data.agentStates)):
                state.data.agentStates[index].scaredTimer = SCARED_TIME

    consume = staticmethod(consume)


class GhostRules:
    __doc__ = '\n    These functions dictate how ghosts interact with their environment.\n    '
    GHOST_SPEED = 1.0

    def getLegalActions(state, ghostIndex):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        conf = state.getGhostState(ghostIndex).configuration
        possibleActions = Actions.getPossibleActions(conf, state.data.layout.walls)
        reverse = Actions.reverseDirection(conf.direction)
        if reverse in possibleActions:
            if len(possibleActions) > 1:
                possibleActions.remove(reverse)
        return possibleActions

    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action, ghostIndex):
        legal = GhostRules.getLegalActions(state, ghostIndex)
        if action not in legal:
            raise Exception('Illegal ghost action ' + str(action))
        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0:
            speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        ghostState.configuration = ghostState.configuration.generateSuccessor(vector)

    applyAction = staticmethod(applyAction)

    def decrementTimer(ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint(ghostState.configuration.pos)
        ghostState.scaredTimer = max(0, timer - 1)

    decrementTimer = staticmethod(decrementTimer)

    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0:
            for index in range(1, len(state.data.agentStates)):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()

            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, index)
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, agentIndex)

    checkDeath = staticmethod(checkDeath)

    def collide(state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            state.data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win:
                state.data.scoreChange -= 500
                state.data._lose = True

    collide = staticmethod(collide)

    def canKill(pacmanPosition, ghostPosition):
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

    canKill = staticmethod(canKill)

    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start

    placeGhost = staticmethod(placeGhost)


def default(str):
    return str + ' [Default: %default]'


def parseAgentArgs(str):
    if str == None:
        return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key, val = p, 1
        opts[key] = val
    else:
        return opts


def readCommand(argv):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = '\n    USAGE:      python pacman.py <options>\n    EXAMPLES:   (1) python pacman.py\n                    - starts an interactive game\n                (2) python pacman.py --layout smallClassic --zoom 2\n                OR  python pacman.py -l smallClassic -z 2\n                    - starts an interactive game on a smaller board, zoomed in\n    '
    parser = OptionParser(usageStr)
    parser.add_option('-n', '--numGames', dest='numGames', type='int', help=(default('the number of GAMES to play')),
      metavar='GAMES',
      default=1)
    parser.add_option('-l', '--layout', dest='layout', help=(default('the LAYOUT_FILE from which to load the map layout')),
      metavar='LAYOUT_FILE',
      default='mediumClassic')
    parser.add_option('-p', '--pacman', dest='pacman', help=(default('the agent TYPE in the pacmanAgents module to use')),
      metavar='TYPE',
      default='KeyboardAgent')
    parser.add_option('-t', '--textGraphics', action='store_true', dest='textGraphics', help='Display output as text only',
      default=False)
    parser.add_option('-q', '--quietTextGraphics', action='store_true', dest='quietGraphics', help='Generate minimal output and no graphics',
      default=False)
    parser.add_option('-g', '--ghosts', dest='ghost', help=(default('the ghost agent TYPE in the ghostAgents module to use')),
      metavar='TYPE',
      default='RandomGhost')
    parser.add_option('-k', '--numghosts', type='int', dest='numGhosts', help=(default('The maximum number of ghosts to use')),
      default=4)
    parser.add_option('-z', '--zoom', type='float', dest='zoom', help=(default('Zoom the size of the graphics window')),
      default=1.0)
    parser.add_option('-f', '--fixRandomSeed', action='store_true', dest='fixRandomSeed', help='Fixes the random seed to always play the same game',
      default=False)
    parser.add_option('-r', '--recordActions', action='store_true', dest='record', help='Writes game histories to a file (named by the time they were played)',
      default=False)
    parser.add_option('--replay', dest='gameToReplay', help='A recorded game file (pickle) to replay',
      default=None)
    parser.add_option('-a', '--agentArgs', dest='agentArgs', help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-x', '--numTraining', dest='numTraining', type='int', help=(default('How many episodes are training (suppresses output)')),
      default=0)
    parser.add_option('--frameTime', dest='frameTime', type='float', help=(default('Time to delay between frames; <0 means keyboard')),
      default=0.1)
    parser.add_option('-c', '--catchExceptions', action='store_true', dest='catchExceptions', help='Turns on exception handling and timeouts during games',
      default=False)
    parser.add_option('--timeout', dest='timeout', type='int', help=(default('Maximum length of time an agent can spend computing in a single game')),
      default=30)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()
    if options.fixRandomSeed:
        random.seed('cs188')
    args['layout'] = getLayout(options.layout)
    if args['layout'] == None:
        raise Exception('The layout ' + options.layout + ' cannot be found')
    else:
        noKeyboard = options.gameToReplay == None and (options.textGraphics or options.quietGraphics)
        pacmanType = loadAgent(options.pacman, noKeyboard)
        agentOpts = parseAgentArgs(options.agentArgs)
        if options.numTraining > 0:
            args['numTraining'] = options.numTraining
            if 'numTraining' not in agentOpts:
                agentOpts['numTraining'] = options.numTraining
        pacman = pacmanType(**agentOpts)
        args['pacman'] = pacman
        if 'numTrain' in agentOpts:
            options.numQuiet = int(agentOpts['numTrain'])
            options.numIgnore = int(agentOpts['numTrain'])
        else:
            ghostType = loadAgent(options.ghost, noKeyboard)
            args['ghosts'] = [ghostType(i + 1) for i in range(options.numGhosts)]
            if options.quietGraphics:
                import textDisplay
                args['display'] = textDisplay.NullGraphics()
            else:
                if options.textGraphics:
                    import textDisplay
                    textDisplay.SLEEP_TIME = options.frameTime
                    args['display'] = textDisplay.PacmanGraphics()
                else:
                    import graphicsDisplay
            args['display'] = graphicsDisplay.PacmanGraphics((options.zoom), frameTime=(options.frameTime))
    args['numGames'] = options.numGames
    args['record'] = options.record
    args['catchExceptions'] = options.catchExceptions
    args['timeout'] = options.timeout
    if options.gameToReplay != None:
        print('Replaying recorded game %s.' % options.gameToReplay)
        import cPickle
        f = open(options.gameToReplay)
        try:
            recorded = cPickle.load(f)
        finally:
            f.close()

        recorded['display'] = args['display']
        replayGame(**recorded)
        sys.exit(0)
    return args


def loadAgent--- This code section failed: ---

 L. 583         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              expandvars
                6  LOAD_STR                 '$PYTHONPATH'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'pythonPathStr'

 L. 584        12  LOAD_FAST                'pythonPathStr'
               14  LOAD_METHOD              find
               16  LOAD_STR                 ';'
               18  CALL_METHOD_1         1  ''
               20  LOAD_CONST               -1
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    38  'to 38'

 L. 585        26  LOAD_FAST                'pythonPathStr'
               28  LOAD_METHOD              split
               30  LOAD_STR                 ':'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'pythonPathDirs'
               36  JUMP_FORWARD         48  'to 48'
             38_0  COME_FROM            24  '24'

 L. 587        38  LOAD_FAST                'pythonPathStr'
               40  LOAD_METHOD              split
               42  LOAD_STR                 ';'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'pythonPathDirs'
             48_0  COME_FROM            36  '36'

 L. 588        48  LOAD_FAST                'pythonPathDirs'
               50  LOAD_METHOD              append
               52  LOAD_STR                 '.'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 590        58  LOAD_FAST                'pythonPathDirs'
               60  GET_ITER         
               62  FOR_ITER            208  'to 208'
               64  STORE_FAST               'moduleDir'

 L. 591        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              isdir
               72  LOAD_FAST                'moduleDir'
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_TRUE     80  'to 80'

 L. 591        78  JUMP_BACK            62  'to 62'
             80_0  COME_FROM            76  '76'

 L. 592        80  LOAD_LISTCOMP            '<code_object <listcomp>>'
               82  LOAD_STR                 'loadAgent.<locals>.<listcomp>'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               86  LOAD_GLOBAL              os
               88  LOAD_METHOD              listdir
               90  LOAD_FAST                'moduleDir'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'moduleNames'

 L. 593       100  LOAD_FAST                'moduleNames'
              102  GET_ITER         
            104_0  COME_FROM           164  '164'
              104  FOR_ITER            206  'to 206'
              106  STORE_FAST               'modulename'

 L. 594       108  SETUP_FINALLY       130  'to 130'

 L. 595       110  LOAD_GLOBAL              __import__
              112  LOAD_FAST                'modulename'
              114  LOAD_CONST               None
              116  LOAD_CONST               -3
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'module'
              126  POP_BLOCK        
              128  JUMP_FORWARD        154  'to 154'
            130_0  COME_FROM_FINALLY   108  '108'

 L. 596       130  DUP_TOP          
              132  LOAD_GLOBAL              ImportError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   152  'to 152'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 597       144  POP_EXCEPT       
              146  JUMP_BACK           104  'to 104'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM           136  '136'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           128  '128'

 L. 598       154  LOAD_FAST                'pacman'
              156  LOAD_GLOBAL              dir
              158  LOAD_FAST                'module'
              160  CALL_FUNCTION_1       1  ''
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   104  'to 104'

 L. 599       166  LOAD_FAST                'nographics'
              168  POP_JUMP_IF_FALSE   186  'to 186'
              170  LOAD_FAST                'modulename'
              172  LOAD_STR                 'keyboardAgents.py'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L. 600       178  LOAD_GLOBAL              Exception
              180  LOAD_STR                 'Using the keyboard requires graphics (not text display)'
              182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           168  '168'

 L. 601       186  LOAD_GLOBAL              getattr
              188  LOAD_FAST                'module'
              190  LOAD_FAST                'pacman'
              192  CALL_FUNCTION_2       2  ''
              194  ROT_TWO          
              196  POP_TOP          
              198  ROT_TWO          
              200  POP_TOP          
              202  RETURN_VALUE     
              204  JUMP_BACK           104  'to 104'
              206  JUMP_BACK            62  'to 62'

 L. 602       208  LOAD_GLOBAL              Exception
              210  LOAD_STR                 'The agent '
              212  LOAD_FAST                'pacman'
              214  BINARY_ADD       
              216  LOAD_STR                 ' is not specified in any *Agents.py.'
              218  BINARY_ADD       
              220  CALL_FUNCTION_1       1  ''
              222  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_EXCEPT' instruction at offset 148


def replayGame(layout, actions, display):
    import pacmanAgents, ghostAgents
    rules = ClassicGameRules()
    agents = [pacmanAgents.GreedyAgent()] + [ghostAgents.RandomGhost(i + 1) for i in range(layout.getNumGhosts())]
    game = rules.newGame(layout, agents[0], agents[1:], display)
    state = game.state
    display.initialize(state.data)
    for action in actions:
        state = (state.generateSuccessor)(*action)
        display.update(state.data)
        state_img = display.image
        rules.process(state, game)
    else:
        display.finish()


def runGames(layout, pacman, ghosts, display, numGames, record, numTraining=0, catchExceptions=False, timeout=30):
    import __main__
    __main__.__dict__['_display'] = display
    rules = ClassicGameRules(timeout)
    games = []
    for i in range(numGames):
        beQuiet = i < numTraining
        if beQuiet:
            import textDisplay
            gameDisplay = textDisplay.NullGraphics()
            rules.quiet = True
        else:
            gameDisplay = display
            rules.quiet = False
        game = rules.newGame(layout, pacman, ghosts, gameDisplay, beQuiet, catchExceptions)
        game.run()
        if not beQuiet:
            games.append(game)
        if record:
            import time, cPickle
            fname = 'recorded-game-%d' % (i + 1) + '-'.join([str(t) for t in time.localtime()[1:6]])
            f = file(fname, 'w')
            components = {'layout':layout,  'actions':game.moveHistory}
            cPickle.dump(components, f)
            f.close()
        if numGames - numTraining > 0:
            scores = [game.state.getScore() for game in games]
            wins = [game.state.isWin() for game in games]
            winRate = wins.count(True) / float(len(wins))
            print('Average Score:', sum(scores) / float(len(scores)))
            print('Scores:       ', ', '.join([str(score) for score in scores]))
            print('Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate))
            print('Record:       ', ', '.join([['Loss', 'Win'][int(w)] for w in wins]))
        return games


if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    runGames(**args)