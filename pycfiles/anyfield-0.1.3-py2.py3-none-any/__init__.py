# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/__init__.py
# Compiled at: 2018-04-27 06:36:26
__doc__ = 'anyex: CryptoCurrency eXchange Trading Library'
__version__ = '0.0.1'
from anyex.base.exchange import Exchange
from anyex.base.decimal_to_precision import decimal_to_precision
from anyex.base.decimal_to_precision import TRUNCATE
from anyex.base.decimal_to_precision import ROUND
from anyex.base.decimal_to_precision import DECIMAL_PLACES
from anyex.base.decimal_to_precision import SIGNIFICANT_DIGITS
from anyex.base.decimal_to_precision import NO_PADDING
from anyex.base.decimal_to_precision import PAD_WITH_ZERO
from anyex.base import errors
from anyex.base.errors import BaseError
from anyex.base.errors import ExchangeError
from anyex.base.errors import NotSupported
from anyex.base.errors import AuthenticationError
from anyex.base.errors import PermissionDenied
from anyex.base.errors import InvalidNonce
from anyex.base.errors import InsufficientFunds
from anyex.base.errors import InvalidOrder
from anyex.base.errors import OrderNotFound
from anyex.base.errors import OrderNotCached
from anyex.base.errors import CancelPending
from anyex.base.errors import NetworkError
from anyex.base.errors import DDoSProtection
from anyex.base.errors import RequestTimeout
from anyex.base.errors import ExchangeNotAvailable
from anyex.base.errors import InvalidAddress
from anyex._1broker import _1broker
from anyex._1btcxe import _1btcxe
from anyex.acx import acx
from anyex.allcoin import allcoin
from anyex.anxpro import anxpro
from anyex.bibox import bibox
from anyex.binance import binance
from anyex.bit2c import bit2c
from anyex.bitbank import bitbank
from anyex.bitbay import bitbay
from anyex.bitfinex import bitfinex
from anyex.bitfinex2 import bitfinex2
from anyex.bitflyer import bitflyer
from anyex.bithumb import bithumb
from anyex.bitkk import bitkk
from anyex.bitlish import bitlish
from anyex.bitmarket import bitmarket
from anyex.bitmex import bitmex
from anyex.bitso import bitso
from anyex.bitstamp import bitstamp
from anyex.bitstamp1 import bitstamp1
from anyex.bittrex import bittrex
from anyex.bitz import bitz
from anyex.bl3p import bl3p
from anyex.bleutrade import bleutrade
from anyex.braziliex import braziliex
from anyex.btcbox import btcbox
from anyex.btcchina import btcchina
from anyex.btcexchange import btcexchange
from anyex.btcmarkets import btcmarkets
from anyex.btctradeim import btctradeim
from anyex.btctradeua import btctradeua
from anyex.btcturk import btcturk
from anyex.btcx import btcx
from anyex.bxinth import bxinth
from anyex.ccex import ccex
from anyex.cex import cex
from anyex.chbtc import chbtc
from anyex.chilebit import chilebit
from anyex.cobinhood import cobinhood
from anyex.coincheck import coincheck
from anyex.coinegg import coinegg
from anyex.coinex import coinex
from anyex.coinexchange import coinexchange
from anyex.coinfloor import coinfloor
from anyex.coingi import coingi
from anyex.coinmarketcap import coinmarketcap
from anyex.coinmate import coinmate
from anyex.coinnest import coinnest
from anyex.coinone import coinone
from anyex.coinsecure import coinsecure
from anyex.coinspot import coinspot
from anyex.coolcoin import coolcoin
from anyex.cryptopia import cryptopia
from anyex.dsx import dsx
from anyex.ethfinex import ethfinex
from anyex.exmo import exmo
from anyex.exx import exx
from anyex.flowbtc import flowbtc
from anyex.foxbit import foxbit
from anyex.fybse import fybse
from anyex.fybsg import fybsg
from anyex.gatecoin import gatecoin
from anyex.gateio import gateio
from anyex.gdax import gdax
from anyex.gemini import gemini
from anyex.getbtc import getbtc
from anyex.hadax import hadax
from anyex.hitbtc import hitbtc
from anyex.hitbtc2 import hitbtc2
from anyex.huobi import huobi
from anyex.huobicny import huobicny
from anyex.huobipro import huobipro
from anyex.ice3x import ice3x
from anyex.independentreserve import independentreserve
from anyex.indodax import indodax
from anyex.itbit import itbit
from anyex.jubi import jubi
from anyex.kraken import kraken
from anyex.kucoin import kucoin
from anyex.kuna import kuna
from anyex.lakebtc import lakebtc
from anyex.lbank import lbank
from anyex.liqui import liqui
from anyex.livecoin import livecoin
from anyex.luno import luno
from anyex.lykke import lykke
from anyex.mercado import mercado
from anyex.mixcoins import mixcoins
from anyex.negociecoins import negociecoins
from anyex.nova import nova
from anyex.okcoincny import okcoincny
from anyex.okcoinusd import okcoinusd
from anyex.okex import okex
from anyex.paymium import paymium
from anyex.poloniex import poloniex
from anyex.qryptos import qryptos
from anyex.quadrigacx import quadrigacx
from anyex.quoinex import quoinex
from anyex.southxchange import southxchange
from anyex.surbitcoin import surbitcoin
from anyex.therock import therock
from anyex.tidebit import tidebit
from anyex.tidex import tidex
from anyex.urdubit import urdubit
from anyex.vaultoro import vaultoro
from anyex.vbtc import vbtc
from anyex.virwox import virwox
from anyex.wex import wex
from anyex.xbtce import xbtce
from anyex.yobit import yobit
from anyex.yunbi import yunbi
from anyex.zaif import zaif
from anyex.zb import zb
exchanges = [
 '_1broker',
 '_1btcxe',
 'acx',
 'allcoin',
 'anxpro',
 'bibox',
 'binance',
 'bit2c',
 'bitbank',
 'bitbay',
 'bitfinex',
 'bitfinex2',
 'bitflyer',
 'bithumb',
 'bitkk',
 'bitlish',
 'bitmarket',
 'bitmex',
 'bitso',
 'bitstamp',
 'bitstamp1',
 'bittrex',
 'bitz',
 'bl3p',
 'bleutrade',
 'braziliex',
 'btcbox',
 'btcchina',
 'btcexchange',
 'btcmarkets',
 'btctradeim',
 'btctradeua',
 'btcturk',
 'btcx',
 'bxinth',
 'ccex',
 'cex',
 'chbtc',
 'chilebit',
 'cobinhood',
 'coincheck',
 'coinegg',
 'coinex',
 'coinexchange',
 'coinfloor',
 'coingi',
 'coinmarketcap',
 'coinmate',
 'coinnest',
 'coinone',
 'coinsecure',
 'coinspot',
 'coolcoin',
 'cryptopia',
 'dsx',
 'ethfinex',
 'exmo',
 'exx',
 'flowbtc',
 'foxbit',
 'fybse',
 'fybsg',
 'gatecoin',
 'gateio',
 'gdax',
 'gemini',
 'getbtc',
 'hadax',
 'hitbtc',
 'hitbtc2',
 'huobi',
 'huobicny',
 'huobipro',
 'ice3x',
 'independentreserve',
 'indodax',
 'itbit',
 'jubi',
 'kraken',
 'kucoin',
 'kuna',
 'lakebtc',
 'lbank',
 'liqui',
 'livecoin',
 'luno',
 'lykke',
 'mercado',
 'mixcoins',
 'negociecoins',
 'nova',
 'okcoincny',
 'okcoinusd',
 'okex',
 'paymium',
 'poloniex',
 'qryptos',
 'quadrigacx',
 'quoinex',
 'southxchange',
 'surbitcoin',
 'therock',
 'tidebit',
 'tidex',
 'urdubit',
 'vaultoro',
 'vbtc',
 'virwox',
 'wex',
 'xbtce',
 'yobit',
 'yunbi',
 'zaif',
 'zb']
base = [
 'Exchange',
 'exchanges',
 'decimal_to_precision']
__all__ = base + errors.__all__ + exchanges