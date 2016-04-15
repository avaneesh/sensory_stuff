'''
Step 1: Gather data

Step 2: Send data over serial port to Arduino
'''

import serial
import time
import json
import sys


l_stock = ["TSLA", "AAPL", "CSCO", "MSFT"]


# ********* Step 1.1: Get data from REST API 
##### Download info about the list of stocks
#import stock_ticker_host
#stock_ticker_host.start_service(l_stock)
#stock_ticker_host.fetch_these(l_stock)


d={}

def read_stocks():
    global d
    # ********* Step 1.2: Read the information we want
    # Get real..
    print "*"*10 + "We got" + 10*"*"
    for stock_sym in l_stock:
        try:
    #f = open("../stock_ticker/"+stock_sym+".json")
            f = open(stock_sym+".json")
            result = json.loads(f.read())
            s_price = result['LastTradePriceOnly']
            s_symbol = result['Symbol']
            print '%s is %s' % (s_symbol, s_price)
            d[str(s_symbol)]=str(s_price)
            f.close()
        except IOError as err:
            print err.strerror + " for " + stock_sym
            
    if not d:
        # Init fake data..
        print "Faking data..."
        d['CSCO'] = '32.00'
        d['TSLA'] = '289.12'


#print "Exiting.."
#sys.exit()


# ********* Step 2: Send data over serial

ser = serial.Serial('/dev/ttymxc3',115200,timeout=1)
ser.flushOutput()

print 'Serial connected'


while True:

    read_stocks()

    for stockName, stockPrice in d.iteritems():
       formattedPrice = "{0:.2f}".format(float(stockPrice))
       formattedPrice = (formattedPrice+"   ")[:6] # Append extra space if required
       outStr = ("%s %s" % (stockName, formattedPrice))
       print 'Sending - ' + outStr
       ser.write(outStr)		# write to Arduino to turn ON the LED
       time.sleep(2) 		# delay for 2 second
       r = ser.read(6) # Read what Arduino says
       print r
        
