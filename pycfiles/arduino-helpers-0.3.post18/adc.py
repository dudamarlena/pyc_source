# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\christian\documents\github\arduino_helpers\arduino_helpers\hardware\teensy\adc.py
# Compiled at: 2015-11-12 18:51:03
import io, pandas as pd
from . import ANALOG_CHANNELS
ADC_DESCRIPTIONS_TSV = ('\nfull_name\tshort_description\tdescription\tpage\nCLMD\tADC Minus-Side General Calibration Value Register\t\t31.3.19/671\nCLPS\tADC Plus-Side General Calibration Value Register\t\t31.3.12/667\nCLMS\tADC Minus-Side General Calibration Value Register\t\t31.3.20/672\nCLPD\tADC Plus-Side General Calibration Value Register\t\t31.3.11/666\nPG\tADC Plus-Side Gain Register\t\t31.3.9/665\nRB\tADC Data Result Register\t\t31.3.4/659\nRA\tADC Data Result Register\t\t31.3.4/659\nOFS\tADC Offset Correction Register\t\t31.3.8/665\nMG\tADC Minus-Side Gain Register\t\t31.3.10/666\nCLP1\tADC Plus-Side General Calibration Value Register\t\t31.3.16/669\nCLP0\tADC Plus-Side General Calibration Value Register\t\t31.3.17/669\nCLP3\tADC Plus-Side General Calibration Value Register\t\t31.3.14/668\nCLP2\tADC Plus-Side General Calibration Value Register\t\t31.3.15/668\nCV2\tCompare Value Register\t\t31.3.5/660\nCLP4\tADC Plus-Side General Calibration Value Register\t\t31.3.13/667\nCV1\tCompare Value Register\t\t31.3.5/660\nCLM2\tADC Minus-Side General Calibration Value Register\t\t31.3.23/673\nCLM3\tADC Minus-Side General Calibration Value Register\t\t31.3.22/673\nCLM0\tADC Minus-Side General Calibration Value Register\t\t31.3.25/674\nCLM1\tADC Minus-Side General Calibration Value Register\t\t31.3.24/674\nCLM4\tADC Minus-Side General Calibration Value Register\t\t31.3.21/672\nCFG2.MUXSEL\tADC mux select\t 0: ADxxa channels selected, 1: ADxxb channels selected\t31.3.3/658\nCFG2.ADLSTS\tLong sample time select\t 0: 20 extra ADCK cycles (default), 1: 12 extra ADCK cycles, 2: 6 extra ADCK cycles, 3: 2 extra ADCK cycles\t31.3.3/658\nCFG2.ADHSC\tHigh-speed configuration\t\t31.3.3/658\nCFG2.ADACKEN\tAsynchronous clock output enable\t\t31.3.3/658\nCFG1.ADLSMP\tSample time configuration\t 0: Short sample time, 1: Long sample time\t31.3.2/656\nCFG1.ADICLK\tInput clock select\t 0: Bus clock, 1: Bus clock/2, 2: Alternate clock (ALTCLK), 3: Asynchronous clock (ADACK)\t31.3.2/656\nCFG1.MODE\tConversion mode selection\t 0: 8-bit, 1: 12-bit, 2: 10-bit, 3: 16-bit\t31.3.2/656\nCFG1.ADIV\tClock divide select\t 0: /1, 1: /2, 2: /4, 3: /8\t31.3.2/656\nCFG1.ADLPC\tLow-power configuration\t\t31.3.2/656\nSC1A.COCO\tConversion complete flag\t\t31.3.1/653\nSC1A.DIFF\tDifferential mode enable\t\t31.3.1/653\nSC1A.AIEN\tInterrupt enable\t\t31.3.1/653\nSC1A.ADCH\tInput channel select\t\t31.3.1/653\nSC1B.COCO\tConversion complete flag\t\t31.3.1/653\nSC1B.DIFF\tDifferential mode enable\t\t31.3.1/653\nSC1B.AIEN\tInterrupt enable\t\t31.3.1/653\nSC1B.ADCH\tInput channel select\t\t31.3.1/653\nPGA.PGAEN\tPGA enable\t\t31.3.18/670\nPGA.PGALPb\tPGA low-power mode control\t\t31.3.18/670\nPGA.PGAG\tPGA Gain setting, $PGA~gain = 2^{PGAG}$\t 0: 1, 1: 2, 2: 4, 3: 8, 4: 16, 5: 32, 6: 64\t31.3.18/670\nSC3.AVGE\tHardware average enable\t\t31.3.7/663\nSC3.ADCO\tContinuous conversion enable\t\t31.3.7/663\nSC3.AVGS\tHardware average select\t Samples averaged - 0: 4, 1: 8, 0: 16, 0: 32\t31.3.7/663\nSC3.CALF\tCalibration failed flag\t\t31.3.7/663\nSC3.CAL\tCalibration\t\t31.3.7/663\nSC2.DMAEN\tDMA enable\t 1: 1 DMA is enabled and will assert the ADC DMA request during an ADC conversion complete event noted when any of the `SC1n[COCO]` flags is asserted.\t31.3.6/661\nSC2.REFSEL\tVoltage reference selection\t 0: Default, 1: Alternate, 2-3: Reserved\t31.3.6/661\nSC2.ADACT\tConversion active\t\t31.3.6/661\nSC2.ACFGT\tCompare function greater than enable\t\t31.3.6/661\nSC2.ADTRG\tConversion trigger select\t 0: Software trigger, 1: Hardware trigger\t31.3.6/661\nSC2.ACREN\tCompare function range enable\t\t31.3.6/661\nSC2.ACFE\tCompare function enable\t\t31.3.6/661\n').strip()
ADC_DESCRIPTIONS = pd.read_csv(io.BytesIO(ADC_DESCRIPTIONS_TSV), sep='\t').set_index('full_name')
ADC_DESCRIPTIONS.loc[(ADC_DESCRIPTIONS.description.isnull(), 'description')] = ''
ADC_SC1A_CHANNELS = 31
ADC_SC1A_PIN_INVALID = 31
ADC_MAX_PIN = 44
ADC_SC1A_PIN_MUX = 128
ADC_SC1A_PIN_DIFF = 64
ADC_SC1A_PIN_PGA = 128
SC1A_TO_CHANNEL_ADC0 = [
 34, 0, 0, 36, 23, 14, 20, 21, 16, 17, 0, 0, 19, 18,
 15, 22, 23, 0, 0, 35, 0, 37,
 39, 40, 0, 0, 38, 41, 42, 43,
 0]
SC1A_TO_CHANNEL_ADC1 = [
 36, 0, 0, 34, 28, 26, 29, 30, 16, 17, 0, 0, 0, 0,
 0, 0, 0, 0, 39, 37, 0, 0,
 0, 0, 0, 0, 38, 41, 0, 42,
 43]
CHANNEL_TO_SC1A_ADC0 = [
 5, 14, 8, 9, 13, 12, 6, 7, 15, 4, 0, 19, 3, 21,
 5, 14, 8, 9, 13, 12, 6, 7, 15, 4,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID,
 0 + ADC_SC1A_PIN_DIFF,
 19 + ADC_SC1A_PIN_DIFF,
 3 + ADC_SC1A_PIN_DIFF,
 21 + ADC_SC1A_PIN_DIFF,
 26, 22, 23, 27, 29, 30]
CHANNEL_TO_SC1A_DIFF_ADC0 = [
 0 + ADC_SC1A_PIN_PGA, 0 + ADC_SC1A_PIN_PGA, 3, 3]
CHANNEL_TO_SC1A_ADC1 = [
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, 8, 9, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, 3, ADC_SC1A_PIN_INVALID, 0, 19,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, 8, 9, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 5 + ADC_SC1A_PIN_MUX, 5, 4, 6, 7, 4 + ADC_SC1A_PIN_MUX,
 ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
 3 + ADC_SC1A_PIN_DIFF, ADC_SC1A_PIN_INVALID + ADC_SC1A_PIN_DIFF,
 0 + ADC_SC1A_PIN_DIFF, 19 + ADC_SC1A_PIN_DIFF,
 26, 18, ADC_SC1A_PIN_INVALID, 27, 29, 30]
CHANNEL_TO_SC1A_DIFF_ADC1 = [
 3, 3, 0 + ADC_SC1A_PIN_PGA, 0 + ADC_SC1A_PIN_PGA]
SC1A_PINS = ANALOG_CHANNELS.map(lambda x: CHANNEL_TO_SC1A_ADC0[x])
ADC_SC1_DIFF = 32
SC1A_PINS['DAD0'] = SC1A_PINS.A10 - SC1A_PINS.A10 + ADC_SC1_DIFF
SC1A_PINS['DAD3'] = SC1A_PINS.A13 - SC1A_PINS.A10 + ADC_SC1_DIFF
SC1A_PINS['PGA0'] = 2 + ADC_SC1_DIFF
ADC0_RA = 1073983504
ADC0_RB = 1073983508
ADC0_SC1A = 1073983488