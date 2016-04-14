
# https://ilmusaham.wordpress.com/tag/stock-yahoo-data/

# http://finance.yahoo.com/d/quotes.csv?s=msft&f=price

# http://stackoverflow.com/questions/10040954/alternative-to-google-finance-api

# https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback=

#### select * from yahoo.finance.quotes where symbol in ("YHOO","AAPL","GOOG","MSFT")

# https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&env=http%3A%2F%2Fdatatables.org%2Falltables.env

import requests
import urllib
import urllib2
import json
from pprint import pprint
import time, threading

#l_stock = ["TSLA", "AAPL"]
l_stock = []
interval = 60

def fetch_these(l_stock_param):
    global l_stock
    l_stock = l_stock_param
    print "Starting Stock ticker for these stocks: " + get_stock_list_str()
    fetch_all()


def fetch_all():
    query_template = 'select * from yahoo.finance.quotes where symbol in (%s)'
    
    query_string = query_template % get_stock_list_str()
    print "Getting " + get_stock_list_str()
##print query_string
    query_string = urllib.quote_plus(query_string)
##print query_string
    
    http_template = 'https://query.yahooapis.com/v1/public/yql?q=%s&format=json'
    http_env = '&env=http%3A%2F%2Fdatatables.org%2Falltables.env'
    http_req_string = http_template % query_string
    http_req_string = http_req_string + http_env
    print http_req_string
    
    u = urllib2.urlopen(http_req_string)
    data = u.read()
    print "Content is:"
    
    stock_results_file = "all_stocks.json"
    
    with open(stock_results_file, "w") as f:
        f.write(data)
    
    data = json.loads(data)
    #pprint(data)
    
    # data['query']['results']['quote'][0]['LastTradePriceOnly']
    
    results = data['query']['results']['quote']
    
    for result in results:
        s_price = result['LastTradePriceOnly']
        s_symbol = result['Symbol']
        print '%s is %s' % (s_symbol, s_price)
        # Write entire result in individual files
        with open(s_symbol+".json", "w") as f:
            f.write(json.dumps(result))

def get_stock_list_str():
    return ",".join(['"'+q+'"' for q in l_stock])

def stock_ticker_loop():
    t = datetime.datetime.now().time()

    fetch_all()
    threading.Timer(interval, stock_ticker_loop).start()

def start_service(l_stock_param, l_interval):
    global l_stock
    global interval
    interval = l_interval
    l_stock = l_stock_param
    print "Starting Stock ticker for: " + get_stock_list_str()
    stock_ticker_loop()

if __name__ == "__main__":
    import requests
    import urllib
    import urllib2
    import json
    from pprint import pprint
    import time, threading
    import datetime


    l_stock = ["TSLA", "AAPL"]
#fetch_these(l_stock)
    start_service(l_stock, 60)
