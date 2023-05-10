import json
import requests
import winsound
import time
import numpy

dir = 1800.0
cc = 'BTCUSDT'
interval = '4h'
limit = 42

def beep(x):
    winsound.Beep(x, 300)

def func(startTime):
    r = requests.get(f'https://api.binance.com/api/v3/klines?symbol={cc}&interval={interval}&startTime={startTime}&limit={limit}')
    data = r.json()
    cands = []
    for i in range(36):
        cands.append( abs( float(data[i][1])+float(data[i][4]) ) / 2.0)
    
    # change cands's numbers to the numbers bitween 200 - 2000
    max = numpy.max(cands)
    min = numpy.min(cands)

    print(f'max: {max}, min: {min}')
    
    ratio = dir/(max-min)
    defect = 200 - (min*ratio)
    for i in range(36):
        cands[i] = cands[i]*ratio + defect

    winsound.Beep(20000, 3000)
    for i in range(36):
        beep(int(cands[i]))
    winsound.Beep(20000, 2000)

    cands2 = []
    for i in range(36, 42):
        cands2.append(float(data[i][2]))
    high = numpy.max(cands2)

    low = float(data[35][3])
    boolper = (low+(0.04*low) <= high)
    
    if (boolper):
        return True
    else:
        return False

if __name__ == "__main__":
    # startTime = 1589273940000

    t = 0 #true answers
    f = 0 #false answers
    tt = 0
    ff = 0

    for i in range(20,22):
        startTime = 1589273940000 + i*60000*240*42
        bb = func(startTime)
        print('Enter 0 for over 4 percentage and enter 1 for not: ', end="")
        choose = int(input())
        if(bb):
            t += 1
            if(choose == 0):
                tt += 1
            else:
                ff += 1
        else:
            f += 1
            if(choose == 1):
                tt += 1
            else:
                ff += 1

    print(f'true : {t} | false : {f}')
    print(f'true answers: {tt} | false answers: {ff}')