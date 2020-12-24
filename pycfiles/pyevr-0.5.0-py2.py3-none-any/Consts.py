# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyevolve\Consts.py
# Compiled at: 2009-01-21 19:09:01
__doc__ = '\n\n:mod:`Consts` -- constants module\n============================================================================\n\nPyevolve have defaults in all genetic operators, settings and etc, this is an issue to helps the user in the API use and minimize the source code needed to make simple things. In the module :mod:`Consts`, you will find those defaults settings. You are encouraged to see the constants, but not to change directly on the module, there are methods for this.\n\nGeneral constants\n----------------------------------------------------------------------------\n\n.. attribute:: CDefPythonRequire\n  \n   The mininum version required to run Pyevolve.\n\n.. attribute:: CDefLogFile\n   \n   The default log filename.\n\n.. attribute:: CDefLogLevel\n\n   Default log level.\n\n.. attribute:: sortType\n   \n   Sort type, raw or scaled.\n\n   Example:\n      >>> sort_type = Consts.sortType["raw"]\n      >>> sort_type = Consts.sortType["scaled"]\n\n.. attribute:: minimaxType\n\n   The Min/Max type, maximize or minimize the evaluation function.\n\n   Example:\n      >>> minmax = Consts.minimaxType["minimize"]\n      >>> minmax = Consts.minimaxType["maximize]\n  \n.. attribute:: CDefESCKey\n\n   The ESC key ASCII code. Used to start Interactive Mode.\n\n.. attribute:: CDefRangeMin\n\n   Minimum range. This constant is used as integer and real max/min.\n\n.. attribute:: CDefRangeMax\n\n   Maximum range. This constant is used as integer and real max/min.\n\n\nSelection methods constants (:mod:`Selectors`)\n----------------------------------------------------------------------------\n\n.. attribute:: CDefTournamentPoolSize\n\n   The default pool size for the Tournament Selector (:class:`Selectors.GTournamentSelector`).\n\nScaling scheme constants (:mod:`Scaling`)\n----------------------------------------------------------------------------\n\n.. attribute:: CDefScaleLinearMultiplier\n\n   The multiplier of the Linear (:class:`Scaling.LinearScaling`) scaling scheme.\n\n.. attribute:: CDefScaleSigmaTruncMultiplier\n\n   The default Sigma Truncation (:class:`Scaling.SigmaTruncScaling`) scaling scheme.\n\n.. attribute:: CDefScalePowerLawFactor\n\n   The default Power Law (:class:`Scaling.PowerLawScaling`) scaling scheme factor.\n\n\nPopulation constants (:class:`GPopulation.GPopulation`)\n----------------------------------------------------------------------------\n   \n.. attribute:: CDefPopSortType\n   \n   Default sort type parameter.\n\n.. attribute:: CDefPopMinimax\n\n   Default min/max parameter.\n\n.. attribute:: CDefPopScale\n\n   Default scaling scheme.\n\n\n1D Binary String Defaults (:class:`G1DBinaryString.G1DBinaryString`)\n----------------------------------------------------------------------------\n\n.. attribute:: CDefG1DBinaryStringMutator\n\n   The default mutator for the 1D Binary String (:class:`G1DBinaryString.G1DBinaryString`) chromosome.\n\n.. attribute:: CDefG1DBinaryStringCrossover\n\n   The default crossover method for the 1D Binary String (:class:`G1DBinaryString.G1DBinaryString`) chromosome.\n\n.. attribute:: CDefG1DBinaryStringInit\n\n   The default initializator for the 1D Binary String (:class:`G1DBinaryString.G1DBinaryString`) chromosome.\n\n.. attribute:: CDefG1DBinaryStringUniformProb\n\n   The default uniform probability used for some uniform genetic operators for the 1D Binary String (:class:`G1DBinaryString.G1DBinaryString`) chromosome.\n\n\n\n1D List chromosome constants (:class:`G1DList.G1DList`)\n----------------------------------------------------------------------------\n\n.. attribute:: CDefG1DListMutIntMU\n\n   Default *mu* value of the 1D List Gaussian Integer Mutator (:class:`Mutators.G1DListMutatorIntegerGaussian`), the *mu* represents the mean of the distribution.\n   \n.. attribute:: CDefG1DListMutIntSIGMA\n\n   Default *sigma* value of the 1D List Gaussian Integer Mutator (:class:`Mutators.G1DListMutatorIntegerGaussian`), the *sigma* represents the standard deviation of the distribution.\n   \n.. attribute:: CDefG1DListMutRealMU\n\n   Default *mu* value of the 1D List Gaussian Real Mutator (:class:`Mutators.G1DListMutatorRealGaussian`), the *mu* represents the mean of the distribution.\n   \n.. attribute:: CDefG1DListMutRealSIGMA\n\n   Default *sigma* value of the 1D List Gaussian Real Mutator (:class:`Mutators.G1DListMutatorRealGaussian`), the *sigma* represents the mean of the distribution.\n\n\n2D List chromosome constants (:class:`G2DList.G2DList`)\n----------------------------------------------------------------------------\n\n.. attribute:: CDefG2DListMutRealMU\n\n   Default *mu* value of the 2D List Gaussian Real Mutator (:class:`Mutators.G2DListMutatorRealGaussian`), the *mu* represents the mean of the distribution.\n\n.. attribute:: CDefG2DListMutRealSIGMA\n\n   Default *sigma* value of the 2D List Gaussian Real Mutator (:class:`Mutators.G2DListMutatorRealGaussian`), the *sigma* represents the mean of the distribution.\n\n.. attribute:: CDefG2DListMutIntMU\n\n   Default *mu* value of the 2D List Gaussian Integer Mutator (:class:`Mutators.G2DListMutatorIntegerGaussian`), the *mu* represents the mean of the distribution.\n   \n.. attribute:: CDefG2DListMutIntSIGMA\n\n   Default *sigma* value of the 2D List Gaussian Integer Mutator (:class:`Mutators.G2DListMutatorIntegerGaussian`), the *sigma* represents the mean of the distribution.\n\n.. attribute:: CDefG2DListMutator\n\n   Default mutator for the 2D List chromosome.\n\n.. attribute:: CDefG2DListCrossover\n\n   Default crossover method for the 2D List chromosome.\n\n.. attribute:: CDefG2DListInit\n\n   Default initializator for the 2D List chromosome.\n\n.. attribute:: CDefG2DListCrossUniformProb\n\n   Default uniform probability for the 2D List Uniform Crossover method (:class:`Crossovers.G2DListCrossoverUniform`).\n\n\nGA Engine constants (:class:`GSimpleGA.GSimpleGA`)\n----------------------------------------------------------------------------\n\n.. attribute:: CDefGAGenerations\n\n   Default number of generations.\n\n.. attribute:: CDefGAMutationRate\n\n   Default mutation rate.\n\n.. attribute:: CDefGACrossoverRate\n\n   Default crossover rate.\n\n.. attribute:: CDefGAPopulationSize\n\n   Default population size.\n\n.. attribute:: CDefGASelector\n\n   Default selector method.\n\nDB Adapters constants (:mod:`DBAdapters`)\n----------------------------------------------------------------------------\nConstants for the DB Adapters\n\n\nSQLite3 DB Adapter Constants (:class:`DBAdapters.DBSQLite`)\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. attribute:: CDefSQLiteDBName\n   \n   Default database filename.\n\n.. attribute:: CDefSQLiteDBTable\n\n   Default statistical table name.\n\n.. attribute:: CDefSQLiteDBTablePop\n\n   Default population statistical table name.\n\n.. attribute:: CDefSQLiteStatsGenFreq\n\n   Default generational frequency for dump statistics.\n\n.. attribute:: CDefSQLiteStatsCommitFreq\n\n   Default commit frequency.\n\nURL Post DB Adapter Constants (:class:`DBAdapters.DBURLPost`)\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. attribute:: CDefURLPostStatsGenFreq\n\n   Default generational frequency for dump statistics.\n\n\nCSV File DB Adapter Constants (:class:`DBAdapters.DBFileCSV`)\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. attribute:: CDefCSVFileName\n   \n   The default CSV filename to dump statistics.\n\n.. attribute:: CDefCSVFileStatsGenFreq\n\n   Default generational frequency for dump statistics.\n\n'
import Scaling, Selectors, Initializators, Mutators, Crossovers, logging
CDefPythonRequire = (2, 5)
CDefLogFile = 'pyevolve.log'
CDefLogLevel = logging.DEBUG
sortType = {'raw': 0, 
   'scaled': 1}
minimaxType = {'minimize': 0, 'maximize': 1}
CDefESCKey = 27
CDefTournamentPoolSize = 2
CDefScaleLinearMultiplier = 1.2
CDefScaleSigmaTruncMultiplier = 2.0
CDefScalePowerLawFactor = 1.0005
CDefPopSortType = sortType['scaled']
CDefPopMinimax = minimaxType['maximize']
CDefPopScale = Scaling.LinearScaling
CDefGAGenerations = 100
CDefGAMutationRate = 0.02
CDefGACrossoverRate = 0.9
CDefGAPopulationSize = 80
CDefGASelector = Selectors.GRankSelector
CDefRangeMin = 0
CDefRangeMax = 100
CDefG1DBinaryStringMutator = Mutators.G1DBinaryStringMutatorFlip
CDefG1DBinaryStringCrossover = Crossovers.G1DBinaryStringXSinglePoint
CDefG1DBinaryStringInit = Initializators.G1DBinaryStringInitializator
CDefG1DBinaryStringUniformProb = 0.5
CDefG1DListMutIntMU = 2
CDefG1DListMutIntSIGMA = 10
CDefG1DListMutRealMU = 0
CDefG1DListMutRealSIGMA = 1
CDefG1DListMutator = Mutators.G1DListMutatorSwap
CDefG1DListCrossover = Crossovers.G1DListCrossoverSinglePoint
CDefG1DListInit = Initializators.G1DListInitializatorInteger
CDefG1DListCrossUniformProb = 0.5
CDefG2DListMutIntMU = 2
CDefG2DListMutIntSIGMA = 10
CDefG2DListMutRealMU = 0
CDefG2DListMutRealSIGMA = 1
CDefG2DListMutator = Mutators.G2DListMutatorSwap
CDefG2DListCrossover = Crossovers.G2DListCrossoverUniform
CDefG2DListInit = Initializators.G2DListInitializatorInteger
CDefG2DListCrossUniformProb = 0.5
CDefSQLiteDBName = 'pyevolve.db'
CDefSQLiteDBTable = 'statistics'
CDefSQLiteDBTablePop = 'population'
CDefSQLiteStatsGenFreq = 1
CDefSQLiteStatsCommitFreq = 500
CDefURLPostStatsGenFreq = 100
CDefCSVFileName = 'pyevolve.csv'
CDefCSVFileStatsGenFreq = 1