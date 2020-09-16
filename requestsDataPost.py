#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

url = "http://39.107.248.79:9110/scientific/algorithm/getRawDataOpenWindowOutput"

payload = {'slideSize': '3',
'srate': '40',
'windowSize': '10'}
files = [
  ('file', open('/Users/zapp/Desktop/3021_3021_20181105094823_20181105113019_GSR.csv.processed.csv', 'rb'))
]
headers = {
  'Token-type': 'ops'
}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))
