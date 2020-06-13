#!/usr/bin/env python
# coding=utf-8

import pprint
# import csv
import click 
# import requests
# import datetime as datetime
# from datetime import date
# from xml.etree import ElementTree as ET
import os
# from random import sample
# import random
# import json
# import logging
import subprocess
import glob
import time
import sys
import datetime
import re
import csv

def get_date(filename):
  date = re.search('enjin_watch_(\d+)_', d).group(1)
  # return datetime.datetime.fromtimestamp(os.path.getctime(filename)).date()

def find_ent(res, strftime):
  for ent in res:
    if ent['date'] == strftime:
      return ent
  return None

CONFIRMED = 'Confirmed or Completed'

# datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

@click.command()
@click.option('--days', default=-14, type=int)
# @click.option('--days', default=1, type=int)
def stats(days):

  target_date = datetime.datetime.today().date() + datetime.timedelta(days=days)

  # file_list = [ ent for ent in glob.iglob('enjin_watch_*.csv') if target_date <= get_date(ent)]
  f_list = [ f_name for f_name in glob.iglob('enjin_watch_*.csv')]
  print('Enjin Watch List: ' + str(f_list))

  f_dict = {}
  for f_name in f_list:
    try:
      date_m = re.search('enjin_watch_(\d+)_', f_name).group(1)
    except AttributeError:
      print('Warning: fail to parse file name...')
      continue

    f_date = (datetime.datetime.strptime(date_m, '%y%m%d')).date()
    if f_date >= target_date:
      f_dict[date_m] = f_name

  print(f_dict)

  # return

  # list1 = [ ent for ent in glob.iglob('output_Search_booking_id_*.csv') if from_date <= getcdate(ent)]
  # print('List1: ' + str(list1))
  # list2 = [ ent for ent in glob.iglob('output_ctrip_update_res_no_*.csv') if from_date <= getcdate(ent)]
  # print('List2: ' + str(list2))

  # filename2_dict = {}
  # for filename2 in list2:
  #   try:
  #     filename2_date = re.search('output_ctrip_update_res_no_(\d+)', filename2).group(1)
  #   except AttributeError:
  #     filename2_date = ''
  #   filename2_dict[filename2_date] = filename2

  res = []
  dates_lookup = []

  target_date = datetime.datetime.today().date() + datetime.timedelta(days=days)
  for i in range(abs(days)):
    entry = {}
    entry_listed = {}
    entry_sold = {}
    # 2017-05-03
    entry['date'] = (target_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
    entry_listed['date'] = (target_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
    entry_sold['date'] = (target_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
    entry['date_m'] = (target_date + datetime.timedelta(days=i)).strftime('%y%m%d')
    entry_listed['date_m'] = (target_date + datetime.timedelta(days=i)).strftime('%y%m%d')
    entry_sold['date_m'] = (target_date + datetime.timedelta(days=i)).strftime('%y%m%d')
    # entry['type'] = '0'
    entry['type'] = 'total'
    entry_listed['type'] = 'listed'
    entry_sold['type'] = 'sold'
    entry['status'] = 0
    entry_listed['status'] = 0
    entry_sold['status'] = 0
    entry['amount'] = 0
    entry_listed['amount'] = 0
    entry_sold['amount'] = 0
    # entry['amount_listed'] = 0
    # entry['amount_sold'] = 0
    # entry['#_of_bookings'] = 0
    # entry['#_of_hotel_ref'] = 0
    # entry['comment'] = ''
    try:
      f_name = f_dict[entry['date_m']]
    except KeyError:
      print('Warning: No {} found...'.format(entry['date_m']))
      # entry['type'] = '0'
      entry['status'] = 1
      entry_listed['status'] = 1
      entry_sold['status'] = 1
      res.append(entry)
      res.append(entry_listed)
      res.append(entry_sold)
      continue

    with open(f_name, encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        # print(row['value'])
        amount = row['value'].split()[0].replace(',', '')
        # amount = re.search('\d+\.\d+ ENJ ', row['value']).group(1)
        entry['amount'] = entry['amount'] + float(amount)
        if row['type'] == 'Listed':
          entry_listed['amount'] = entry_listed['amount'] + float(amount)
        if row['type'] == 'Sold':
          entry_sold['amount'] = entry_sold['amount'] + float(amount)
      # entry['type'] = '200'
      entry['status'] = 200
      entry_listed['status'] = 200
      entry_sold['status'] = 200
    # dates_lookup.append(entry['date'])
    res.append(entry)
    res.append(entry_listed)
    res.append(entry_sold)

  # with open('output_ctrip_search_booking_store.csv', encoding='utf-8-sig') as csvfile:
  #   reader = csv.DictReader(csvfile)
  #   ids = set()
  #   for row in reader:
  #     if row['gta_api_booking_id'] not in ids:
  #       if row['booking_status'] == CONFIRMED:
  #         if row['booking_departure_date'] in dates_lookup:
  #           ent = find_ent(res, row['booking_departure_date'])
  #           if ent != None:
  #             ent['#_of_bookings'] = ent['#_of_bookings'] + 1
  #     ids.add(row['gta_api_booking_id'])

  # with open('output_ctrip_booking_store.csv', encoding='utf-8-sig') as csvfile:
  #   reader = csv.DictReader(csvfile)
  #   ids = set()
  #   for row in reader:
  #     if row['gta_api_booking_id'] not in ids:
  #       if row['booking_status'] == CONFIRMED:
  #         if row['booking_departure_date'] in dates_lookup:
  #           ent = find_ent(res, row['booking_departure_date'])
  #           if ent != None:
  #             ent['#_of_hotel_ref'] = ent['#_of_hotel_ref'] + 1
  #     ids.add(row['gta_api_booking_id'])
  # for filename1 in list1:
  #   entry = {}

  #   try:
  #     filename1_date = re.search('output_Search_booking_id_(\d+)', filename1).group(1)
  #   except AttributeError:
  #     filename1_date = ''
  #   if filename1_date != '':      
  #     entry['date'] = filename1_date
  #   entry['booking_file'] = filename1

  #   try:
  #     print(filename2_dict[filename1_date])
  #   except KeyError:
  #     print('Warning: expected date is not in the dictionary..')
  #     continue
  #   entry['ctrip_api_file'] = filename2_dict[filename1_date]
  #   res.append(entry)

  # for ent in res:
  #   total_booking_num = 0
  #   ctrip_booking_num = 0
  #   with open(ent['booking_file'], encoding='utf-8-sig') as csvfile:
  #     reader = csv.DictReader(csvfile)
  #     ids = set()
  #     for row in reader:
  #       if row['gta_api_booking_id'] not in ids:
  #         if row['booking_status'] == CONFIRMED:
  #           total_booking_num = total_booking_num + 1
  #       ids.add(row['gta_api_booking_id'])  
  #   with open(ent['ctrip_api_file'], encoding='utf-8-sig') as csvfile:
  #     reader = csv.DictReader(csvfile)
  #     for row in reader:
  #       ctrip_booking_num = ctrip_booking_num + 1
  # for ent in res:
  #   # ent['booking_hotel_ref_percentage'] = '{0:.3f}'.format(float( ctrip_booking_num / total_booking_num ))
  #   if ent['#_of_bookings'] != 0:
  #     ent['coverage'] = '{0:.3f}'.format(float( ent['#_of_hotel_ref'] / ent['#_of_bookings'] ))

  target_filename = '_'.join(['enjin_stats', datetime.datetime.now().strftime('%y%m%d_%H%M')]) + \
            '.csv'

  keys = res[0].keys()
  with open(target_filename, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(res)

  print('New Stats: {}'.format(target_filename))
  return

  # # python booking_id.py --days 0 --duration 0 --client ctrip --d_type departure
  # subprocess.call(['python', 'booking_id.py', '--days', str(days), '--duration', str(duration), '--client', 'ctrip', '--d_type', 'departure'])

  # for i in range(3):
  #   print('sleeping..')
  #   time.sleep(1)

  # newest = max(glob.iglob('output_Search_booking_id_*.csv'), key=os.path.getctime)
  # subprocess.call(['python', 'search_item_hr.py', '--filename', newest])

  # for i in range(3):
  #   print('sleeping..')
  #   time.sleep(1)

  # newest = max(glob.iglob('output_Search_item_hr_*.csv'), key=os.path.getctime)
  # subprocess.call(['python', 'hc.py', '--filename', newest])

  # for i in range(3):
  #   print('sleeping..')
  #   time.sleep(1)

  # # newest = max(glob.iglob('output_Search_item_hr_*.csv'), key=os.path.getctime)
  # # subprocess.call(['python', 'sendmail.py', '--filename', 'output_hotel_ref_*.csv', '--title', 'Ctrip_hotel_ref'])

  # newest = max(glob.iglob('output_hotel_ref_*.csv'), key=os.path.getctime)

  # today_date = datetime.datetime.now().strftime('%y%m%d')
  # try:
  #   newest_date = re.search('output_hotel_ref_(\d+)', newest).group(1)
  # except AttributeError:
  #   newest_date = ''
  # if newest_date != today_date:
  #   print('Error: newest date != today date.. mannual intervention needed..')
  #   return

  # print('newest date: ' + newest_date)

  # # while True:
  # #   sys.stdout.write("Would you like to proceed to call Ctrip's update hotel res no API? " + newest + " [Y/N]")
  # #   choice = input().lower()
  # #   if choice == 'y' or choice == 'yes':
  # #     break
  # #   if choice == 'n' or choice == 'no':
  # #     return

  # subprocess.call(['python', 'ctrip_update_res_no.py', '--filename', newest])


if __name__ == '__main__':
  stats()