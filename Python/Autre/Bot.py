# https://fr.tradingview.com/script/5jQ6r2vN-10-BOT-BTCUSDTPERP/


// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © wielkieef

//@version=4
strategy("10 BOT", overlay=true,  pyramiding=1,initial_capital = 10000, default_qty_type= strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0,commission_type=strategy.commission.percent,commission_value=0.04)

//SOURCE ==================================================================================================================================================================================================================================================================

src = input(close)

// INPUTS ==================================================================================================================================================================================================================================================================

//ADX -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Act_ADX = input(true, title = "AVERAGE DIRECTIONAL INDEX", type = input.bool)
ADX_options = input("MASANAKAMURA",  title = "ADX OPTION", options = ["CLASSIC", "MASANAKAMURA"])
ADX_len = input(14, title = "ADX LENGTH", type = input.integer, minval = 1)
th = input(14, title = "ADX THRESHOLD", type = input.float, minval = 0, step = 0.5)

//Range Filter----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

length0 = input(6, title="Range Filter lenght"),mult = input(4, title="Range Filter mult")

//SAR-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

start = input(title="SAR Start", type=input.float, step=0.001, defval=0.046)
increment = input(title="SAR Increment", type=input.float, step=0.001, defval=0.02)
maximum = input(title="SAR Maximum", type=input.float, step=0.01, defval=0.11)
width = input(title="SAR Point Width", type=input.integer, minval=1, defval=1)

//RSI---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

len_3 = input(131, minval=1, title="RSI lenght")
src_3 = input(hl2, "RSI Source")

//TWAP Trend --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

smoothing = input(title="TWAP Smoothing", defval= 11)
resolution = input("0", "TWAP Timeframe")

//JMA------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

inp = input(title="JMA Source", type=input.source, defval=hlc3)
reso = input(title="JMA Resolution", type=input.resolution, defval="")
rep = input(title="JMA Allow Repainting?", type=input.bool, defval=false)
src0 = security(syminfo.tickerid, reso, inp[rep ? 0 : barstate.isrealtime ? 1 : 0])[rep ? 0 : barstate.isrealtime ? 0 : 1]
lengths = input(title="JMA Length", type=input.integer, defval=8, minval=1)

//MACD------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

fast_length = input(title="MACD Fast Length", type=input.integer, defval=5)
slow_length = input(title="MACD Slow Length", type=input.integer, defval=21)
signal_length = input(title="MACD Signal Smoothing", type=input.integer, minval = 1, maxval = 50, defval = 31)

//Volume Delta -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

periodMa = input(title="Delta Length", minval=1, defval=16)

//Volume weight------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

maLength = input(title="Volume Weight Length", type=input.integer, defval=59, minval=1)
maType = input(title="Volume Weight Type", type=input.string, defval="SMA", options=["EMA", "SMA", "HMA", "WMA", "DEMA"])
rvolTrigger = input(title="Volume To Trigger Signal", type=input.float, defval=1.1, step=0.1 , minval=0.1)

//MA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

length = input(50, minval=1, title="MA Length")
matype = input(5, minval=1, maxval=5, title="AvgType")

//INDICATORS ==============================================================================================================================================================================================================================================================

//ADX----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

calcADX(_len) =>
    up              = change(high)
	down            = -change(low)
	plusDM          = na(up)   ? na : (up > down and up > 0   ? up   : 0)
    minusDM         = na(down) ? na : (down > up and down > 0 ? down : 0)
	truerange       = rma(tr, _len)
	_plus           = fixnan(100 * rma(plusDM, _len)  / truerange)
	_minus          = fixnan(100 * rma(minusDM, _len) / truerange)
	sum             = _plus + _minus
	_adx            = 100 * rma(abs(_plus - _minus) / (sum == 0 ? 1 : sum), _len)
    [_plus,_minus,_adx]

calcADX_Masanakamura(_len) =>
    SmoothedTrueRange                   = 0.0
    SmoothedDirectionalMovementPlus     = 0.0
    SmoothedDirectionalMovementMinus    = 0.0
    TrueRange                           = max(max(high - low, abs(high - nz(close[1]))), abs(low - nz(close[1])))
    DirectionalMovementPlus             = high - nz(high[1]) > nz(low[1]) - low ? max(high - nz(high[1]), 0) : 0
    DirectionalMovementMinus            = nz(low[1]) - low > high - nz(high[1]) ? max(nz(low[1]) - low, 0)   : 0
    SmoothedTrueRange                   := nz(SmoothedTrueRange[1]) - (nz(SmoothedTrueRange[1]) /_len) + TrueRange
    SmoothedDirectionalMovementPlus     := nz(SmoothedDirectionalMovementPlus[1])  - (nz(SmoothedDirectionalMovementPlus[1])  / _len) + DirectionalMovementPlus
    SmoothedDirectionalMovementMinus    := nz(SmoothedDirectionalMovementMinus[1]) - (nz(SmoothedDirectionalMovementMinus[1]) / _len) + DirectionalMovementMinus
    DIP                                 = SmoothedDirectionalMovementPlus  / SmoothedTrueRange * 100
    DIM                                 = SmoothedDirectionalMovementMinus / SmoothedTrueRange * 100
    DX                                  = abs(DIP-DIM) / (DIP+DIM)*100
    adx                                 = sma(DX, _len)
    [DIP,DIM,adx]

[DIPlusC,DIMinusC,ADXC] = calcADX(ADX_len)
[DIPlusM,DIMinusM,ADXM] = calcADX_Masanakamura(ADX_len)
DIPlus                  = ADX_options == "CLASSIC" ? DIPlusC    : DIPlusM
DIMinus                 = ADX_options == "CLASSIC" ? DIMinusC   : DIMinusM
ADX                     = ADX_options == "CLASSIC" ? ADXC       : ADXM

ADX_color = DIPlus > DIMinus and ADX > th ? color.green : DIPlus < DIMinus and ADX > th ? color.red : color.orange
barcolor(color = Act_ADX ? ADX_color : na, title = "ADX")

//Range Filter---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

out = 0., cma = 0., cts = 0.
Var = variance(src,length0)*mult
sma = sma(src,length0)

secma = pow(nz(sma - cma[1]),2)
sects = pow(nz(src - cts[1]),2)
ka = Var < secma ? 1 - Var/secma : 0
kb = Var < sects ? 1 - Var/sects : 0

cma := ka*sma+(1-ka)*nz(cma[1],src)
cts := kb*src+(1-kb)*nz(cts[1],src)

css = cts > cma ? color.green : color.red
a = plot(cts,"CTS",color.gray,2,transp=0)
b = plot(cma,"CMA",color.gray,2,transp=0)
fill(a,b,color=css,transp=80)

rangegood = cts > cma
rangebad  = cts < cma

//SAR-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

psar = sar(start, increment, maximum)
dir = psar < close ? 1 : -1

psarColor = dir == 1 ? color.green : color.red
psarPlot = plot(psar, title="PSAR", style=plot.style_circles, linewidth=width, color=psarColor, transp=0)

var color longColor = color.green
var color shortColor = color.red

sargood = dir ==1
sarbad  = dir ==-1

//RSI---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

up_3 = rma(max(change(src_3), 0), len_3)
down_3 = rma(-min(change(src_3), 0), len_3)
rsi_3 = down_3 == 0 ? 100 : up_3 == 0 ? 0 : 100 - (100 / (1 + up_3 / down_3))

rsiob = (rsi_3 < 70)
rsios  = (rsi_3 > 30)

//TWAP Trend --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

res = resolution != "0" ? resolution : timeframe.period
weight = barssince(change(security(syminfo.tickerid, res, time, lookahead=barmerge.lookahead_on)))
price = 0.
price:= weight == 0 ? src : src + nz(price[1])
twap = price / (weight + 1)
ma_ = smoothing < 2 ? twap : sma(twap, smoothing)
bullish = iff(smoothing < 2, src >= ma_, src > ma_)
disposition = bullish ? color.lime : color.red
basis = plot(src, "OHLC4", disposition, linewidth=1, transp=100)
work = plot(ma_, "TWAP", disposition, linewidth=2, transp=20)
fill(basis, work, disposition, transp=65)

//JMA------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

jsa = (src0 + src0[lengths]) / 2
sig = src0 > jsa ? 1 : src0 < jsa ? -1 : 0

jsaColor = sig > 0 ? color.green : sig < 0 ? color.red : color.orange
plot(jsa, color=jsaColor, linewidth=2)

jmagood = sig > 0
jmabad  = sig < 0

//MACD------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

fast_ma = ema(src, fast_length)
slow_ma = ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma(macd, signal_length)

macdgood = macd > signal
macdbad  = macd < signal

//Volume Delta -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

bullPower = iff(close < open, iff(close[1] < open, max(high - close[1], close - low), max(high - open, close - low)), iff(close > open, iff(close[1] > open,  high - low, max(open - close[1], high - low)), iff(high - close > close - low, iff(close[1] < open, max(high - close[1], close - low), high - open), iff(high - close < close - low, iff(close[1] > open, high - low, max(open - close[1], high - low)), iff(close[1] > open, max(high - open, close - low), iff(close[1] < open, max(open - close[1], high - low), high-low))))))
bearPower = iff(close < open, iff(close[1] > open, max(close[1] - open, high - low), high - low), iff(close > open, iff(close[1] > open, max(close[1] - low, high - close), max(open - low, high - close)), iff(high - close > close - low, iff(close[1] > open, max(close[1] - open, high - low), high - low), iff(high - close < close - low, iff(close[1] > open, max(close[1] - low, high - close), open - low), iff(close[1] > open, max(close[1] - open, high - low), iff(close[1] < open, max(open - low, high - close), high - low))))))

bullVolume = (bullPower / (bullPower + bearPower)) * volume
bearVolume = (bearPower / (bullPower + bearPower)) * volume

delta = bullVolume - bearVolume
cvd = cum(delta)
cvdMa = sma(cvd, periodMa)

deltagood = cvd > cvdMa
deltabad  = cvd < cvdMa

//Volume weight------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

getMA0(length) =>
    maPrice = ema(volume, length)
    if maType == "SMA"
        maPrice := sma(volume, length)
    if maType == "HMA"
        maPrice := hma(volume, length)
    if maType == "WMA"
        maPrice := wma(volume, length)
    if maType == "DEMA"
        e1 = ema(volume, length)
        e2 = ema(e1, length)
        maPrice := 2 * e1 - e2
    maPrice

ma = getMA0(maLength)
rvol = volume / ma

volumegood = volume > rvolTrigger * ma

//MA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ma5 = sma(close, 5)
ma10 = sma(close, 10)
ma30 = sma(close, 30)

magood = ma5 > ma30
mabad  = ma5 < ma30

simplema = sma(src,length)
exponentialma = ema(src,length)
hullma = wma(2*wma(src, length/2)-wma(src, length), round(sqrt(length)))
weightedma = wma(src, length)
volweightedma = vwma(src, length)
avgval = matype==1 ? simplema : matype==2 ? exponentialma : matype==3 ? hullma : matype==4 ? weightedma : matype==5 ? volweightedma : na
MA_speed = (avgval / avgval[1] -1 ) *100

masgood = MA_speed > 0
masbad  = MA_speed < 0

//STRATEGY===============================================================================================================================================================================================================================================================

Long = (DIPlus > DIMinus and ADX > th)  and volumegood and sargood and rsiob and macdgood and deltagood and magood and masgood and bullish and jmagood and rangegood
Short = (DIPlus < DIMinus and ADX > th) and volumegood and sarbad  and rsios and macdbad  and deltabad  and mabad and masbad and jmabad and rangebad

//Signals======================================================================================================================================================================================================================

if Long
    strategy.entry("L", strategy.long)

if Short
    strategy.entry("S", strategy.short)

per(pcnt) =>
    strategy.position_size != 0 ? round(pcnt / 100 * strategy.position_avg_price / syminfo.mintick) : float(na)
stoploss=input(title=" stop loss", defval=9, minval=0.01)
los = per(stoploss)
q=input(title=" qty percent", defval=100, minval=1)

tp=input(title=" Take profit", defval=1.3, minval=0.01)

strategy.exit("tp", qty_percent = q, profit = per(tp), loss = los)


// By wielkieef
