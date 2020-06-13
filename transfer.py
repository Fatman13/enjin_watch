#!/usr/bin/env python
# coding=utf-8

# import pprint
import csv
import click 
import requests
import datetime as datetime
# from bs4 import BeautifulSoup
# from splinter import Browser
import time
# import re
# import copy
import os
import json
# import pickle
from requests.exceptions import ConnectionError
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ReadTimeout

# def get_date(time_text):
#   if 'Yesterday' in time_text:
#     return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%b %d, %y')
#   if '2 days ago' in time_text:
#     return (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%b %d, %y')
#   if '3 days ago' in time_text:
#     return (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%b %d, %y')
#   return datetime.datetime.now().strftime('%b %d, %y')

@click.command()
@click.option('--limit', default=10000, type=int)
@click.option('--offset', default=0, type=int)
def transfer(limit, offset):

  # https://api.bloxy.info/token/transfers?token=0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c&till_time=2020-04-28+02%3A04%3A20&key=ACCN4bYeoO07q&format=structure
  url ='https://api.bloxy.info/token/transfers'
  res = []
  till_time = datetime.datetime.now()
  till_time = till_time.replace(hour=0, minute=0, second=0)
  from_time = datetime.datetime.now() - datetime.timedelta(days=1)
  from_time = from_time.replace(hour=0, minute=0, second=0)

  while True:
    payload = {
      'token': '0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c',
      'limit': limit,
      'offset': offset,
      'from_time': from_time.strftime('%Y-%m-%d %H:%M:%S'),
      'till_time': till_time.strftime('%Y-%m-%d %H:%M:%S'),
      'key': 'ACCN4bYeoO07q',
      'format': 'structure'
      }
    r = requests.get(url, params=payload)
    print('Request limit: {} offset: {} url: {}'.format(limit, offset, r.url))
    # print(r.text)
    rr = json.loads(r.text)
    if len(rr) == 0:
      print('INFO: No more transfers...')
      break
    for ent in rr:
      if ent['token_sender_type'] == 'Wallet' and ent['token_receiver_type'] == 'Smart Contract':
        entry = {}
        entry['tx_time'] = ent['tx_time']
        entry['amount'] = ent['amount']
        entry['symbol'] = ent['symbol']
        entry['token_sender'] = ent['token_sender']
        entry['token_receiver'] = ent['token_receiver']
        entry['tx_from'] = ent['tx_from']
        entry['gas_price'] = ent['gas_price']
        entry['gas_value'] = ent['gas_value']
        entry['tx_hash'] = ent['tx_hash']
        entry['token_sender_annotation'] = ent['token_sender_annotation']
        entry['token_receiver_annotation'] = ent['token_receiver_annotation']
        entry['tx_from_annotation'] = ent['tx_from_annotation']
        entry['token_sender_type'] = ent['token_sender_type']
        entry['token_receiver_type'] = ent['token_receiver_type']
        res.append(entry)
    offset = offset + limit

  if len(res) == 0:
    print('WARNING: No entry found...')
    return

  keys = res[0].keys()
  output_filename = 'enjin_transfer_list.csv'
  # output_filename = '_'.join(['media_monitor',
  #                               datetime.datetime.now().strftime('%y%m%d'),
  #                               datetime.datetime.now().strftime('%H%M')]) + '.csv'
  with open(output_filename, 'a', newline='', encoding='utf-8-sig') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    # dict_writer = csv.DictWriter(output_file, field_names)
    # dict_writer.writeheader()
    dict_writer.writerows(res)
  return

if __name__ == '__main__':
  transfer()