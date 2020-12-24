# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/talibext/indicator.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import talib, numpy

def value_ds_to_numpy(ds, count):
    ret = None
    try:
        values = ds[count * -1:]
        ret = numpy.array([ float(value) for value in values ])
    except IndexError:
        pass
    except TypeError:
        pass

    return ret


def bar_ds_open_to_numpy(barDs, count):
    return value_ds_to_numpy(barDs.getOpenDataSeries(), count)


def bar_ds_high_to_numpy(barDs, count):
    return value_ds_to_numpy(barDs.getHighDataSeries(), count)


def bar_ds_low_to_numpy(barDs, count):
    return value_ds_to_numpy(barDs.getLowDataSeries(), count)


def bar_ds_close_to_numpy(barDs, count):
    return value_ds_to_numpy(barDs.getCloseDataSeries(), count)


def bar_ds_volume_to_numpy(barDs, count):
    return value_ds_to_numpy(barDs.getVolumeDataSeries(), count)


def call_talib_with_ds(ds, count, talibFunc, *args, **kwargs):
    data = value_ds_to_numpy(ds, count)
    if data is None:
        return
    else:
        return talibFunc(data, *args, **kwargs)


def call_talib_with_hlcv(barDs, count, talibFunc, *args, **kwargs):
    high = bar_ds_high_to_numpy(barDs, count)
    if high is None:
        return
    else:
        low = bar_ds_low_to_numpy(barDs, count)
        if low is None:
            return
        close = bar_ds_close_to_numpy(barDs, count)
        if close is None:
            return
        volume = bar_ds_volume_to_numpy(barDs, count)
        if volume is None:
            return
        return talibFunc(high, low, close, volume, *args, **kwargs)


def call_talib_with_hlc(barDs, count, talibFunc, *args, **kwargs):
    high = bar_ds_high_to_numpy(barDs, count)
    if high is None:
        return
    else:
        low = bar_ds_low_to_numpy(barDs, count)
        if low is None:
            return
        close = bar_ds_close_to_numpy(barDs, count)
        if close is None:
            return
        return talibFunc(high, low, close, *args, **kwargs)


def call_talib_with_ohlc(barDs, count, talibFunc, *args, **kwargs):
    open_ = bar_ds_open_to_numpy(barDs, count)
    if open_ is None:
        return
    else:
        high = bar_ds_high_to_numpy(barDs, count)
        if high is None:
            return
        low = bar_ds_low_to_numpy(barDs, count)
        if low is None:
            return
        close = bar_ds_close_to_numpy(barDs, count)
        if close is None:
            return
        return talibFunc(open_, high, low, close, *args, **kwargs)


def call_talib_with_hl(barDs, count, talibFunc, *args, **kwargs):
    high = bar_ds_high_to_numpy(barDs, count)
    if high is None:
        return
    else:
        low = bar_ds_low_to_numpy(barDs, count)
        if low is None:
            return
        return talibFunc(high, low, *args, **kwargs)


def AD(barDs, count):
    """Chaikin A/D Line"""
    return call_talib_with_hlcv(barDs, count, talib.AD)


def ADOSC(barDs, count, fastperiod=-2147483648, slowperiod=-2147483648):
    """Chaikin A/D Oscillator"""
    return call_talib_with_hlcv(barDs, count, talib.ADOSC, fastperiod, slowperiod)


def ADX(barDs, count, timeperiod=-2147483648):
    """Average Directional Movement Index"""
    return call_talib_with_hlc(barDs, count, talib.ADX, timeperiod)


def ADXR(barDs, count, timeperiod=-2147483648):
    """Average Directional Movement Index Rating"""
    return call_talib_with_hlc(barDs, count, talib.ADXR, timeperiod)


def APO(ds, count, fastperiod=-2147483648, slowperiod=-2147483648, matype=0):
    """Absolute Price Oscillator"""
    return call_talib_with_ds(ds, count, talib.APO, fastperiod, slowperiod, matype)


def AROON(barDs, count, timeperiod=-2147483648):
    """Aroon"""
    ret = call_talib_with_hl(barDs, count, talib.AROON, timeperiod)
    if ret is None:
        ret = (None, None)
    return ret


def AROONOSC(barDs, count, timeperiod=-2147483648):
    """Aroon Oscillator"""
    return call_talib_with_hl(barDs, count, talib.AROONOSC, timeperiod)


def ATR(barDs, count, timeperiod=-2147483648):
    """Average True Range"""
    return call_talib_with_hlc(barDs, count, talib.ATR, timeperiod)


def AVGPRICE(barDs, count):
    """Average Price"""
    return call_talib_with_ohlc(barDs, count, talib.AVGPRICE)


def BBANDS(ds, count, timeperiod=-2147483648, nbdevup=-4e+37, nbdevdn=-4e+37, matype=0):
    """Bollinger Bands"""
    ret = call_talib_with_ds(ds, count, talib.BBANDS, timeperiod, nbdevup, nbdevdn, matype)
    if ret is None:
        ret = (None, None, None)
    return ret


def BETA(ds1, ds2, count, timeperiod=-2147483648):
    """Beta"""
    data1 = value_ds_to_numpy(ds1, count)
    if data1 is None:
        return
    else:
        data2 = value_ds_to_numpy(ds2, count)
        if data2 is None:
            return
        return talib.BETA(data1, data2, timeperiod)


def BOP(barDs, count):
    """Balance Of Power"""
    return call_talib_with_ohlc(barDs, count, talib.BOP)


def CCI(barDs, count, timeperiod=-2147483648):
    """Commodity Channel Index"""
    return call_talib_with_hlc(barDs, count, talib.CCI, timeperiod)


def CDL2CROWS(barDs, count):
    """Two Crows"""
    return call_talib_with_ohlc(barDs, count, talib.CDL2CROWS)


def CDL3BLACKCROWS(barDs, count):
    """Three Black Crows"""
    return call_talib_with_ohlc(barDs, count, talib.CDL3BLACKCROWS)


def CDL3INSIDE(barDs, count):
    """Three Inside Up/Down"""
    return call_talib_with_ohlc(barDs, count, talib.CDL3INSIDE)


def CDL3LINESTRIKE(barDs, count):
    """Three-Line Strike"""
    return call_talib_with_ohlc(barDs, count, talib.CDL3LINESTRIKE)


def CDL3OUTSIDE(barDs, count):
    """Three Outside Up/Down"""
    return call_talib_with_ohlc(barDs, count, talib.CDL3OUTSIDE)


def CDL3STARSINSOUTH(barDs, count):
    """Three Stars In The South"""
    return call_talib_with_ohlc(barDs, count, talib.CDL3STARSINSOUTH)


def CDL3WHITESOLDIERS(barDs, count):
    """Three Advancing White Soldiers"""
    return call_talib_with_ohlc(barDs, count, talib.CDL3WHITESOLDIERS)


def CDLABANDONEDBABY(barDs, count, penetration=-4e+37):
    """Abandoned Baby"""
    return call_talib_with_ohlc(barDs, count, talib.CDLABANDONEDBABY, penetration)


def CDLADVANCEBLOCK(barDs, count):
    """Advance Block"""
    return call_talib_with_ohlc(barDs, count, talib.CDLADVANCEBLOCK)


def CDLBELTHOLD(barDs, count):
    """Belt-hold"""
    return call_talib_with_ohlc(barDs, count, talib.CDLBELTHOLD)


def CDLBREAKAWAY(barDs, count):
    """Breakaway"""
    return call_talib_with_ohlc(barDs, count, talib.CDLBREAKAWAY)


def CDLCLOSINGMARUBOZU(barDs, count):
    """Closing Marubozu"""
    return call_talib_with_ohlc(barDs, count, talib.CDLCLOSINGMARUBOZU)


def CDLCONCEALBABYSWALL(barDs, count):
    """Concealing Baby Swallow"""
    return call_talib_with_ohlc(barDs, count, talib.CDLCONCEALBABYSWALL)


def CDLCOUNTERATTACK(barDs, count):
    """Counterattack"""
    return call_talib_with_ohlc(barDs, count, talib.CDLCOUNTERATTACK)


def CDLDARKCLOUDCOVER(barDs, count, penetration=-4e+37):
    """Dark Cloud Cover"""
    return call_talib_with_ohlc(barDs, count, talib.CDLDARKCLOUDCOVER, penetration)


def CDLDOJI(barDs, count):
    """Doji"""
    return call_talib_with_ohlc(barDs, count, talib.CDLDOJI)


def CDLDOJISTAR(barDs, count):
    """Doji Star"""
    return call_talib_with_ohlc(barDs, count, talib.CDLDOJISTAR)


def CDLDRAGONFLYDOJI(barDs, count):
    """Dragonfly Doji"""
    return call_talib_with_ohlc(barDs, count, talib.CDLDRAGONFLYDOJI)


def CDLENGULFING(barDs, count):
    """Engulfing Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLENGULFING)


def CDLEVENINGDOJISTAR(barDs, count, penetration=-4e+37):
    """Evening Doji Star"""
    return call_talib_with_ohlc(barDs, count, talib.CDLEVENINGDOJISTAR, penetration)


def CDLEVENINGSTAR(barDs, count, penetration=-4e+37):
    """Evening Star"""
    return call_talib_with_ohlc(barDs, count, talib.CDLEVENINGSTAR, penetration)


def CDLGAPSIDESIDEWHITE(barDs, count):
    """Up/Down-gap side-by-side white lines"""
    return call_talib_with_ohlc(barDs, count, talib.CDLGAPSIDESIDEWHITE)


def CDLGRAVESTONEDOJI(barDs, count):
    """Gravestone Doji"""
    return call_talib_with_ohlc(barDs, count, talib.CDLGRAVESTONEDOJI)


def CDLHAMMER(barDs, count):
    """Hammer"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHAMMER)


def CDLHANGINGMAN(barDs, count):
    """Hanging Man"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHANGINGMAN)


def CDLHARAMI(barDs, count):
    """Harami Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHARAMI)


def CDLHARAMICROSS(barDs, count):
    """Harami Cross Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHARAMICROSS)


def CDLHIGHWAVE(barDs, count):
    """High-Wave Candle"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHIGHWAVE)


def CDLHIKKAKE(barDs, count):
    """Hikkake Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHIKKAKE)


def CDLHIKKAKEMOD(barDs, count):
    """Modified Hikkake Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHIKKAKEMOD)


def CDLHOMINGPIGEON(barDs, count):
    """Homing Pigeon"""
    return call_talib_with_ohlc(barDs, count, talib.CDLHOMINGPIGEON)


def CDLIDENTICAL3CROWS(barDs, count):
    """Identical Three Crows"""
    return call_talib_with_ohlc(barDs, count, talib.CDLIDENTICAL3CROWS)


def CDLINNECK(barDs, count):
    """In-Neck Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLINNECK)


def CDLINVERTEDHAMMER(barDs, count):
    """Inverted Hammer"""
    return call_talib_with_ohlc(barDs, count, talib.CDLINVERTEDHAMMER)


def CDLKICKING(barDs, count):
    """Kicking"""
    return call_talib_with_ohlc(barDs, count, talib.CDLKICKING)


def CDLKICKINGBYLENGTH(barDs, count):
    """Kicking - bull/bear determined by the longer marubozu"""
    return call_talib_with_ohlc(barDs, count, talib.CDLKICKINGBYLENGTH)


def CDLLADDERBOTTOM(barDs, count):
    """Ladder Bottom"""
    return call_talib_with_ohlc(barDs, count, talib.CDLLADDERBOTTOM)


def CDLLONGLEGGEDDOJI(barDs, count):
    """Long Legged Doji"""
    return call_talib_with_ohlc(barDs, count, talib.CDLLONGLEGGEDDOJI)


def CDLLONGLINE(barDs, count):
    """Long Line Candle"""
    return call_talib_with_ohlc(barDs, count, talib.CDLLONGLINE)


def CDLMARUBOZU(barDs, count):
    """Marubozu"""
    return call_talib_with_ohlc(barDs, count, talib.CDLMARUBOZU)


def CDLMATCHINGLOW(barDs, count):
    """Matching Low"""
    return call_talib_with_ohlc(barDs, count, talib.CDLMATCHINGLOW)


def CDLMATHOLD(barDs, count, penetration=-4e+37):
    """Mat Hold"""
    return call_talib_with_ohlc(barDs, count, talib.CDLMATHOLD, penetration)


def CDLMORNINGDOJISTAR(barDs, count, penetration=-4e+37):
    """Morning Doji Star"""
    return call_talib_with_ohlc(barDs, count, talib.CDLMORNINGDOJISTAR, penetration)


def CDLMORNINGSTAR(barDs, count, penetration=-4e+37):
    """Morning Star"""
    return call_talib_with_ohlc(barDs, count, talib.CDLMORNINGSTAR, penetration)


def CDLONNECK(barDs, count):
    """On-Neck Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLONNECK)


def CDLPIERCING(barDs, count):
    """Piercing Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLPIERCING)


def CDLRICKSHAWMAN(barDs, count):
    """Rickshaw Man"""
    return call_talib_with_ohlc(barDs, count, talib.CDLRICKSHAWMAN)


def CDLRISEFALL3METHODS(barDs, count):
    """Rising/Falling Three Methods"""
    return call_talib_with_ohlc(barDs, count, talib.CDLRISEFALL3METHODS)


def CDLSEPARATINGLINES(barDs, count):
    """Separating Lines"""
    return call_talib_with_ohlc(barDs, count, talib.CDLSEPARATINGLINES)


def CDLSHOOTINGSTAR(barDs, count):
    """Shooting Star"""
    return call_talib_with_ohlc(barDs, count, talib.CDLSHOOTINGSTAR)


def CDLSHORTLINE(barDs, count):
    """Short Line Candle"""
    return call_talib_with_ohlc(barDs, count, talib.CDLSHORTLINE)


def CDLSPINNINGTOP(barDs, count):
    """Spinning Top"""
    return call_talib_with_ohlc(barDs, count, talib.CDLSPINNINGTOP)


def CDLSTALLEDPATTERN(barDs, count):
    """Stalled Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLSTALLEDPATTERN)


def CDLSTICKSANDWICH(barDs, count):
    """Stick Sandwich"""
    return call_talib_with_ohlc(barDs, count, talib.CDLSTICKSANDWICH)


def CDLTAKURI(barDs, count):
    """Takuri (Dragonfly Doji with very long lower shadow)"""
    return call_talib_with_ohlc(barDs, count, talib.CDLTAKURI)


def CDLTASUKIGAP(barDs, count):
    """Tasuki Gap"""
    return call_talib_with_ohlc(barDs, count, talib.CDLTASUKIGAP)


def CDLTHRUSTING(barDs, count):
    """Thrusting Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLTHRUSTING)


def CDLTRISTAR(barDs, count):
    """Tristar Pattern"""
    return call_talib_with_ohlc(barDs, count, talib.CDLTRISTAR)


def CDLUNIQUE3RIVER(barDs, count):
    """Unique 3 River"""
    return call_talib_with_ohlc(barDs, count, talib.CDLUNIQUE3RIVER)


def CDLUPSIDEGAP2CROWS(barDs, count):
    """Upside Gap Two Crows"""
    return call_talib_with_ohlc(barDs, count, talib.CDLUPSIDEGAP2CROWS)


def CDLXSIDEGAP3METHODS(barDs, count):
    """Upside/Downside Gap Three Methods"""
    return call_talib_with_ohlc(barDs, count, talib.CDLXSIDEGAP3METHODS)


def CMO(ds, count, timeperiod=-2147483648):
    """Chande Momentum Oscillator"""
    return call_talib_with_ds(ds, count, talib.CMO, timeperiod)


def CORREL(ds1, ds2, count, timeperiod=-2147483648):
    """Pearson's Correlation Coefficient (r)"""
    data1 = value_ds_to_numpy(ds1, count)
    if data1 is None:
        return
    else:
        data2 = value_ds_to_numpy(ds2, count)
        if data2 is None:
            return
        return talib.CORREL(data1, data2, timeperiod)


def DEMA(ds, count, timeperiod=-2147483648):
    """Double Exponential Moving Average"""
    return call_talib_with_ds(ds, count, talib.DEMA, timeperiod)


def DX(barDs, count, timeperiod=-2147483648):
    """Directional Movement Index"""
    return call_talib_with_hlc(barDs, count, talib.DX, timeperiod)


def EMA(ds, count, timeperiod=-2147483648):
    """Exponential Moving Average"""
    return call_talib_with_ds(ds, count, talib.EMA, timeperiod)


def HT_DCPERIOD(ds, count):
    """Hilbert Transform - Dominant Cycle Period"""
    return call_talib_with_ds(ds, count, talib.HT_DCPERIOD)


def HT_DCPHASE(ds, count):
    """Hilbert Transform - Dominant Cycle Phase"""
    return call_talib_with_ds(ds, count, talib.HT_DCPHASE)


def HT_PHASOR(ds, count):
    """Hilbert Transform - Phasor Components"""
    ret = call_talib_with_ds(ds, count, talib.HT_PHASOR)
    if ret is None:
        ret = (None, None)
    return ret


def HT_SINE(ds, count):
    """Hilbert Transform - SineWave"""
    ret = call_talib_with_ds(ds, count, talib.HT_SINE)
    if ret is None:
        ret = (None, None)
    return ret


def HT_TRENDLINE(ds, count):
    """Hilbert Transform - Instantaneous Trendline"""
    return call_talib_with_ds(ds, count, talib.HT_TRENDLINE)


def HT_TRENDMODE(ds, count):
    """Hilbert Transform - Trend vs Cycle Mode"""
    return call_talib_with_ds(ds, count, talib.HT_TRENDMODE)


def KAMA(ds, count, timeperiod=-2147483648):
    """Kaufman Adaptive Moving Average"""
    return call_talib_with_ds(ds, count, talib.KAMA, timeperiod)


def LINEARREG(ds, count, timeperiod=-2147483648):
    """Linear Regression"""
    return call_talib_with_ds(ds, count, talib.LINEARREG, timeperiod)


def LINEARREG_ANGLE(ds, count, timeperiod=-2147483648):
    """Linear Regression Angle"""
    return call_talib_with_ds(ds, count, talib.LINEARREG_ANGLE, timeperiod)


def LINEARREG_INTERCEPT(ds, count, timeperiod=-2147483648):
    """Linear Regression Intercept"""
    return call_talib_with_ds(ds, count, talib.LINEARREG_INTERCEPT, timeperiod)


def LINEARREG_SLOPE(ds, count, timeperiod=-2147483648):
    """Linear Regression Slope"""
    return call_talib_with_ds(ds, count, talib.LINEARREG_SLOPE, timeperiod)


def MA(ds, count, timeperiod=-2147483648, matype=0):
    """All Moving Average"""
    return call_talib_with_ds(ds, count, talib.MA, timeperiod, matype)


def MACD(ds, count, fastperiod=-2147483648, slowperiod=-2147483648, signalperiod=-2147483648):
    """Moving Average Convergence/Divergence"""
    ret = call_talib_with_ds(ds, count, talib.MACD, fastperiod, slowperiod, signalperiod)
    if ret is None:
        ret = (None, None, None)
    return ret


def MACDEXT(ds, count, fastperiod=-2147483648, fastmatype=0, slowperiod=-2147483648, slowmatype=0, signalperiod=-2147483648, signalmatype=0):
    """MACD with controllable MA type"""
    ret = call_talib_with_ds(ds, count, talib.MACDEXT, fastperiod, fastmatype, slowperiod, slowmatype, signalperiod, signalmatype)
    if ret is None:
        ret = (None, None, None)
    return ret


def MACDFIX(ds, count, signalperiod=-2147483648):
    """Moving Average Convergence/Divergence Fix 12/26"""
    ret = call_talib_with_ds(ds, count, talib.MACDFIX, signalperiod)
    if ret is None:
        ret = (None, None, None)
    return ret


def MAMA(ds, count, fastlimit=-4e+37, slowlimit=-4e+37):
    """MESA Adaptive Moving Average"""
    ret = call_talib_with_ds(ds, count, talib.MAMA, fastlimit, slowlimit)
    if ret is None:
        ret = (None, None)
    return ret


def MAX(ds, count, timeperiod=-2147483648):
    """Highest value over a specified period"""
    return call_talib_with_ds(ds, count, talib.MAX, timeperiod)


def MAXINDEX(ds, count, timeperiod=-2147483648):
    """Index of highest value over a specified period"""
    return call_talib_with_ds(ds, count, talib.MAXINDEX, timeperiod)


def MEDPRICE(barDs, count):
    """Median Price"""
    return call_talib_with_hl(barDs, count, talib.MEDPRICE)


def MFI(barDs, count, timeperiod=-2147483648):
    """Money Flow Index"""
    return call_talib_with_hlcv(barDs, count, talib.MFI, timeperiod)


def MIDPOINT(ds, count, timeperiod=-2147483648):
    """MidPoint over period"""
    return call_talib_with_ds(ds, count, talib.MIDPOINT, timeperiod)


def MIDPRICE(barDs, count, timeperiod=-2147483648):
    """Midpoint Price over period"""
    return call_talib_with_hl(barDs, count, talib.MIDPRICE, timeperiod)


def MIN(ds, count, timeperiod=-2147483648):
    """Lowest value over a specified period"""
    return call_talib_with_ds(ds, count, talib.MIN, timeperiod)


def MININDEX(ds, count, timeperiod=-2147483648):
    """Index of lowest value over a specified period"""
    return call_talib_with_ds(ds, count, talib.MININDEX, timeperiod)


def MINMAX(ds, count, timeperiod=-2147483648):
    """Lowest and highest values over a specified period"""
    ret = call_talib_with_ds(ds, count, talib.MINMAX, timeperiod)
    if ret is None:
        ret = (None, None)
    return ret


def MINMAXINDEX(ds, count, timeperiod=-2147483648):
    """Indexes of lowest and highest values over a specified period"""
    ret = call_talib_with_ds(ds, count, talib.MINMAXINDEX, timeperiod)
    if ret is None:
        ret = (None, None)
    return ret


def MINUS_DI(barDs, count, timeperiod=-2147483648):
    """Minus Directional Indicator"""
    return call_talib_with_hlc(barDs, count, talib.MINUS_DI, timeperiod)


def MINUS_DM(barDs, count, timeperiod=-2147483648):
    """Minus Directional Movement"""
    return call_talib_with_hl(barDs, count, talib.MINUS_DM, timeperiod)


def MOM(ds, count, timeperiod=-2147483648):
    """Momentum"""
    return call_talib_with_ds(ds, count, talib.MOM, timeperiod)


def NATR(barDs, count, timeperiod=-2147483648):
    """Normalized Average True Range"""
    return call_talib_with_hlc(barDs, count, talib.NATR, timeperiod)


def OBV(ds1, volumeDs, count):
    """On Balance Volume"""
    data1 = value_ds_to_numpy(ds1, count)
    if data1 is None:
        return
    else:
        data2 = value_ds_to_numpy(volumeDs, count)
        if data2 is None:
            return
        return talib.OBV(data1, data2)


def PLUS_DI(barDs, count, timeperiod=-2147483648):
    """Plus Directional Indicator"""
    return call_talib_with_hlc(barDs, count, talib.PLUS_DI, timeperiod)


def PLUS_DM(barDs, count, timeperiod=-2147483648):
    """Plus Directional Movement"""
    return call_talib_with_hl(barDs, count, talib.PLUS_DM, timeperiod)


def PPO(ds, count, fastperiod=-2147483648, slowperiod=-2147483648, matype=0):
    """Percentage Price Oscillator"""
    return call_talib_with_ds(ds, count, talib.PPO, fastperiod, slowperiod, matype)


def ROC(ds, count, timeperiod=-2147483648):
    """Rate of change : ((price/prevPrice)-1)*100"""
    return call_talib_with_ds(ds, count, talib.ROC, timeperiod)


def ROCP(ds, count, timeperiod=-2147483648):
    """Rate of change Percentage: (price-prevPrice)/prevPrice"""
    return call_talib_with_ds(ds, count, talib.ROCP, timeperiod)


def ROCR(ds, count, timeperiod=-2147483648):
    """Rate of change ratio: (price/prevPrice)"""
    return call_talib_with_ds(ds, count, talib.ROCR, timeperiod)


def ROCR100(ds, count, timeperiod=-2147483648):
    """Rate of change ratio 100 scale: (price/prevPrice)*100"""
    return call_talib_with_ds(ds, count, talib.ROCR100, timeperiod)


def RSI(ds, count, timeperiod=-2147483648):
    """Relative Strength Index"""
    return call_talib_with_ds(ds, count, talib.RSI, timeperiod)


def SAR(barDs, count, acceleration=-4e+37, maximum=-4e+37):
    """Parabolic SAR"""
    return call_talib_with_hl(barDs, count, talib.SAR, acceleration, maximum)


def SAREXT(barDs, count, startvalue=-4e+37, offsetonreverse=-4e+37, accelerationinitlong=-4e+37, accelerationlong=-4e+37, accelerationmaxlong=-4e+37, accelerationinitshort=-4e+37, accelerationshort=-4e+37, accelerationmaxshort=-4e+37):
    """Parabolic SAR - Extended"""
    return call_talib_with_hl(barDs, count, talib.SAREXT, startvalue, offsetonreverse, accelerationinitlong, accelerationlong, accelerationmaxlong, accelerationinitshort, accelerationshort, accelerationmaxshort)


def SMA(ds, count, timeperiod=-2147483648):
    """Simple Moving Average"""
    return call_talib_with_ds(ds, count, talib.SMA, timeperiod)


def STDDEV(ds, count, timeperiod=-2147483648, nbdev=-4e+37):
    """Standard Deviation"""
    return call_talib_with_ds(ds, count, talib.STDDEV, timeperiod, nbdev)


def STOCH(barDs, count, fastk_period=-2147483648, slowk_period=-2147483648, slowk_matype=0, slowd_period=-2147483648, slowd_matype=0):
    """Stochastic"""
    ret = call_talib_with_hlc(barDs, count, talib.STOCH, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype)
    if ret is None:
        ret = (None, None)
    return ret


def STOCHF(barDs, count, fastk_period=-2147483648, fastd_period=-2147483648, fastd_matype=0):
    """Stochastic Fast"""
    ret = call_talib_with_hlc(barDs, count, talib.STOCHF, fastk_period, fastd_period, fastd_matype)
    if ret is None:
        ret = (None, None)
    return ret


def STOCHRSI(ds, count, timeperiod=-2147483648, fastk_period=-2147483648, fastd_period=-2147483648, fastd_matype=0):
    """Stochastic Relative Strength Index"""
    ret = call_talib_with_ds(ds, count, talib.STOCHRSI, timeperiod, fastk_period, fastd_period, fastd_matype)
    if ret is None:
        ret = (None, None)
    return ret


def SUM(ds, count, timeperiod=-2147483648):
    """Summation"""
    return call_talib_with_ds(ds, count, talib.SUM, timeperiod)


def T3(ds, count, timeperiod=-2147483648, vfactor=-4e+37):
    """Triple Exponential Moving Average (T3)"""
    return call_talib_with_ds(ds, count, talib.T3, timeperiod, vfactor)


def TEMA(ds, count, timeperiod=-2147483648):
    """Triple Exponential Moving Average"""
    return call_talib_with_ds(ds, count, talib.TEMA, timeperiod)


def TRANGE(barDs, count):
    """True Range"""
    return call_talib_with_hlc(barDs, count, talib.TRANGE)


def TRIMA(ds, count, timeperiod=-2147483648):
    """Triangular Moving Average"""
    return call_talib_with_ds(ds, count, talib.TRIMA, timeperiod)


def TRIX(ds, count, timeperiod=-2147483648):
    """1-day Rate-Of-Change (ROC) of a Triple Smooth EMA"""
    return call_talib_with_ds(ds, count, talib.TRIX, timeperiod)


def TSF(ds, count, timeperiod=-2147483648):
    """Time Series Forecast"""
    return call_talib_with_ds(ds, count, talib.TSF, timeperiod)


def TYPPRICE(barDs, count):
    """Typical Price"""
    return call_talib_with_hlc(barDs, count, talib.TYPPRICE)


def ULTOSC(barDs, count, timeperiod1=-2147483648, timeperiod2=-2147483648, timeperiod3=-2147483648):
    """Ultimate Oscillator"""
    return call_talib_with_hlc(barDs, count, talib.ULTOSC, timeperiod1, timeperiod2, timeperiod3)


def VAR(ds, count, timeperiod=-2147483648, nbdev=-4e+37):
    """Variance"""
    return call_talib_with_ds(ds, count, talib.VAR, timeperiod, nbdev)


def WCLPRICE(barDs, count):
    """Weighted Close Price"""
    return call_talib_with_hlc(barDs, count, talib.WCLPRICE)


def WILLR(barDs, count, timeperiod=-2147483648):
    """Williams' %R"""
    return call_talib_with_hlc(barDs, count, talib.WILLR, timeperiod)


def WMA(ds, count, timeperiod=-2147483648):
    """Weighted Moving Average"""
    return call_talib_with_ds(ds, count, talib.WMA, timeperiod)