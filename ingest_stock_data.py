import os
import shutil
import logging
import os.path
#import zipfile
import datetime
import tempfile
from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud import bigquery
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr

yf.pdr_override()

def download(TICKER, destdir):
   '''
     Downloads stock data and returns local filename
     YEAR e.g.'2015'
     MONTH e.g. '01 for January
   '''
   logging.info('Requesting data for {}-*'.format(TICKER))

   csvfile = os.path.join(destdir, "{}.csv".format(TICKER))
   response = pdr.get_data_yahoo(TICKER) # download historical data from yahoo start='2019-01-01'
   response.dropna(inplace=True)
   response.to_csv(csvfile, index=True, header=True)
   logging.debug("{} saved".format(csvfile))
   return csvfile

def upload(csvfile, bucketname, blobname):
   client = storage.Client()
   bucket = client.get_bucket(bucketname)
   blob = Blob(blobname, bucket)
   blob.upload_from_filename(csvfile)
   gcslocation = 'gs://{}/{}'.format(bucketname, blobname)
   logging.info('Uploaded {} ...'.format(gcslocation))
   return gcslocation

def storage_to_bq():
    client = bigquery.Client()
    gcslocation = 'gs://tax-loss-harvesting.appspot.com/stocks/ohlc/nflx.csv'
    #table_id = client.get_table("tax-loss-harvesting.stock_data.nflx")
    table_ref = client.dataset("stock_data").table("nflx")
    
    job_config = bigquery.LoadJobConfig()
    job_config.skip_leading_rows = 1
    job_config.sorce_format = bigquery.SourceFormat.CSV
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    uri = gcslocation #"gs://tax-loss-harvesting.appspot.com/stocks/ohlc/nflx.csv"
    load_job = client.load_table_from_uri(uri, table_ref, job_config = job_config)
    
    return None


def ingest(ticker,bucket):
   '''
   ingest stock data from yahoo finance
   return cloud-storage-blob-name on success.
   raises DataUnavailable if this data is not on BTS website
   '''
   tempdir = tempfile.mkdtemp(prefix='ingest_stock_data')
   try:
      csvfile = download(ticker, tempdir)
      gcsloc = 'stocks/ohlc/{}'.format(os.path.basename(csvfile))
      return upload(csvfile, bucket, gcsloc)
   finally:
      logging.debug('Cleaning up by removing {}'.format(tempdir))
      shutil.rmtree(tempdir)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ingest historical stock data from Yahoo to Google Cloud Storage')
    parser.add_argument('--bucket', help='GCS bucket to upload data to', required=True)
    parser.add_argument('--ticker', help='Example: COG.  If not provided, defaults to getting next ', required = True)
    #parser.add_argument('--month', help='Specify 01 for January. If not provided, defaults to getting next month')

    #try:
      #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    args = parser.parse_args()
    ticker = args.ticker
    #bucket = args.month
    logging.debug('Ingesting ticker={} data into ={}'.format(ticker, args.bucket))
    gcsfile = ingest(ticker, args.bucket)
    logging.info('Success ... ingested to {}'.format(gcsfile))
    #except DataUnavailable as e:
    #  logging.info('Try again later: {}'.format(e.message))
