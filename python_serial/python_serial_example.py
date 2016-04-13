'''
Step 1: Gather data

Step 2: Send data over serial port to Arduino
'''

import serial
import time
import json
import sys


l_stock = ["TSLA", "AAPL", "CSCO"]


# ********* Step 1.1: Get data from REST API 
##### Download info about the list of stocks
import stock_ticker_host
#stock_ticker_host.start_service(l_stock)
stock_ticker_host.fetch_these(l_stock)


# ********* Step 1.2: Read the information we want
d={}
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
        d[s_symbol]=s_price
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

	stockName='CSCO'
	outStr=stockName+' '+d[stockName]
	print 'Sending - ' + outStr

	ser.write(outStr)		# write to Arduino to turn ON the LED
	r = ser.read(6)
	print r

	time.sleep(3) 		# delay for 1 second

	ser.write("1")		# write to Arduino to turn OFF the LED
	r = ser.read(6)
	print r

	time.sleep(1) 		# delay for 1 second
	stockName='TSLA'
	outStr=stockName+' '+d[stockName]
	print 'Sending - ' + outStr

	ser.write(outStr)		# write to Arduino to turn ON the LED
	r = ser.read(6)
	print r

	time.sleep(3) 		# delay for 1 second
