from flask import Flask, request, escape
from flask import jsonify
#from flask_jsonpify import jsonpify
import yfinance as yf
#from pandas_datareader import data as pdr
#import pandas as pd
from ingest_stock_data import *


app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello Jack, you changed this locally!'

@app.route('/update/<value>')
def update(value):
    """Loads historical stock data into bucket."""
    ticker = value
    bucket = "tax-loss-harvesting.appspot.com"
    ingest(ticker,bucket)
    return ticker + ' data loading to ' + bucket

@app.route('/name/<value>')
def name(value):
    val = {'value': value}
    return jsonify(val)


@app.route('/close/<value>')
def ohlc(value):
    #yf.pdr_override()
    ticker = yf.Ticker(value)
    val = ticker.history(period='1d')
    val = {'close': val.Close.values[0]}
    #val = pdr.get_data_yahoo(value, start="2019-01-01" )
    #val=val['Adj Close']
    #df_list = val.values.tolist()
    #JSONP_data = jsonpify(df_list)
    return jsonify(val)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
# [END gae_python37_app]
'''
@app.route('/params',method = ['POST'])
def ingest_ohlc_data():
    json = request.get_json()

    ticker = escape(json["ticker"]) # required
    bucket = escape(json["bucket"]) # required

    gcsfile = ingest(ticker, bucket)

@app.route('/test',method = ['POST'])
def ingest_ohlc_data():
    json = request.get_json()
    #ticker = escape(json["ticker"]) # required
    #bucket = escape(json["bucket"]) # required

    #gcsfile = ingest(ticker, bucket)
    #ticker = yf.Ticker(ticker)
    #val = ticker.history(period='1d')
    #val = {"close": val.Close.values[0]}
    #print(val)
    return json

@app.route('/uplate/<value>')
def update_stock(value):
    ticker = value
    #bucket = "tax-loss-harvesting.appspot.com"
    #ingest(ticker,bucket)
    #json = {ticker+'uploaded to '+bucket}
    return 'this is an update function '+ticker #jsonify(json)
'''