#!/usr/bin/env python
# coding=utf-8

# import pprint
import csv
import click 
# import requests
import datetime as datetime
# from bs4 import BeautifulSoup
# from splinter import Browser
import time
# import re
# import copy
import os
import json
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotVisibleException   
from selenium.common.exceptions import StaleElementReferenceException   
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from requests.exceptions import ConnectionError
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ReadTimeout
# from selenium.webdriver import ChromeOptions

SCROLL_PAUSE_TIME = 3

@click.command()
@click.option('--t', default='a day ago')
# @click.option('--days', default=1, type=int)
# @click.option('--session_id', default='2171486e6c13b61ad78b34a59f337ab0')
# def collector(secrets, url, session_id):
def explorer(t):
  enjinx_url = 'https://enjinx.io/eth/marketplace-activity'

  driver = webdriver.Chrome('/Users/fatman13/enjinx/chromedriver')
  driver.get(enjinx_url)

  time.sleep(3)

  itime = '1 sec ago'
  # last_height = driver.execute_script('return document.body.scrollHeight')
  # last_height = driver.execute_script('return $("div.app-scrollbar").scrollHeight')
  scrollbar = driver.find_element_by_css_selector('div.app-scrollbar')
  last_height = driver.execute_script('return arguments[0].scrollHeight', scrollbar)

  while True:
  # while time != 'a day ago':
    td_times = driver.find_elements_by_css_selector('td.time span')
    for td_time in td_times:
      if td_time.text == t:
        itime = t
        print('INFO: found entry with {}...'.format(t))
    # Scroll down to bottom
    if itime == t:
      break

    print('INFO: Scrolling...')
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # driver.execute_script('$("div.app-scrollbar").scrollBy(0, {})'.format(last_height))
    driver.execute_script('arguments[0].scrollBy(0, arguments[0].scrollHeight)', scrollbar)
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    # new_height = driver.execute_script('return $("div.app-scrollbar").scrollHeight')
    new_height = driver.execute_script('return arguments[0].scrollHeight', scrollbar)
    if new_height == last_height:
      break
    last_height = new_height

  res = []

  trs = driver.find_elements_by_css_selector('tr')
  # trs = driver.find_elements_by_tag_name('tr')
  # print(trs)
  print(len(trs))
  # for tr in trs:
  for i in range(len(trs)):
    if i == 0:
      continue
    print('+++ {} out of {} records +++'.format(i, len(trs)))
    ent={}
    tds = trs[i].find_elements_by_css_selector('td')
    # print(tds)
    ent['hash_link'] = tds[0].find_element_by_css_selector('a').get_attribute('href')
    ent['hash'] = tds[0].find_element_by_css_selector('span').text
    ent['asset_link'] = tds[1].find_element_by_css_selector('a').get_attribute('href')
    ent['asset'] = tds[1].find_element_by_css_selector('span').text
    ent['type'] = tds[2].text
    ent['time'] = tds[3].find_element_by_css_selector('span').text
    if ent['time'] == t:
      continue
    ent['address_link'] = tds[4].find_element_by_css_selector('a').get_attribute('href')
    ent['amount'] = tds[5].text
    ent['value'] = tds[6].text
    print('Hash: {} Asset: {} Time: {}'.format(ent['hash'], ent['asset'], ent['time']))

    # ent['hash_link'] = tr.find_element_by_css_selector('td.hash a').get_attribute('href')
    # eles = tr.find_element_by_css_selector('*')
    # print(eles)
    # print(eles.text)
    # # ent['hash_link'] = tr.find_element_by_tag_name('td')
    # ent['hash'] = tr.find_element_by_css_selector('td.hash span').text
    # ent['asset_link'] = tr.find_element_by_css_selector('td.asset a').get_attribute('href')
    # ent['asset'] = tr.find_element_by_css_selector('td.asset span').text
    # ent['type'] = tr.find_element_by_css_selector('td.type').text
    # ent['time'] = tr.find_element_by_css_selector('td.time span').text
    # ent['address_link'] = tr.find_element_by_css_selector('td.address a').get_attribute('href')
    # ent['amount'] = tr.find_element_by_css_selector('td.amount').text
    # ent['value'] = tr.find_element_by_css_selector('td.value').text
    res.append(ent)

  driver.quit()

  keys = res[0].keys()
  output_filename = '_'.join(['enjin_watch',
                              datetime.datetime.now().strftime('%y%m%d'),
                              datetime.datetime.now().strftime('%H%M')]) + '.csv'
  file_path = '/Users/fatman13/enjinx/{}'.format(output_filename)
  # with open(output_filename, 'w', newline='', encoding='utf-8-sig') as output_file:
  with open(file_path, 'w', newline='', encoding='utf-8-sig') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    # dict_writer = csv.DictWriter(output_file, field_names)
    dict_writer.writeheader()
    dict_writer.writerows(res)

  return 

if __name__ == '__main__':
  explorer()