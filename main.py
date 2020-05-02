from flask import Flask, request, escape
from flask import jsonify
#from flask_jsonpify import jsonpify
import yfinance as yf
from pandas_datareader import data as pdr
#import pandas as pd
from injest_stock_data import *


app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello Jack, you changed this locally!'


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
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
@app.route('/params',method = ['POST'])
def ingest_ohlc_data():
    json = request.get_json()

    ticker = escape(json['ticker']) if 'ticker' in json else None
    bucket = escape(json['bucket'])  # required

    gcsfile = ingest(ticker, bucket)