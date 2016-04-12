'''
*  Copyright (C) 2014 Ekironji <ekironjisolutions@gmail.com>
*
*  This file is part of serial libraries examples for UDOO
*
*  Serial libraries examples for UDOO is free software: you can redistribute it and/or modify
*  it under the terms of the GNU General Public License as published by
*  the Free Software Foundation, either version 3 of the License, or
*  (at your option) any later version.
*
*  This libraries are distributed in the hope that it will be useful,
*  but WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*  GNU General Public License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
'''

import serial
import time
import json
import sys

l_stock = ["TSLA", "AAPL", "CSCO"]

d={}
# Get real..
for stock_sym in l_stock:
   
    try:
        f = open("../stock_ticker/"+stock_sym+".json")
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
    d['CSCO'] = '32.00'
    d['TSLA'] = '289.12'

sys.exit()


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
