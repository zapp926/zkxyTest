#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

url = "http://192.168.8.106:9110/scientific/analysis/createDataSetCollationTask"

dataDownload = {
	"remark": "备注",
	"taskInfo": {
		"dataFilter": {
			"taskUid": "",
			"testeeUid": '5f4debc7eb6e92141c356070',
			"sceneUid": '5f5f49b1eb6e92207652afd5',
			"type": "feature"
		},
        'notificationEmail':'liuxu@zkpsych.com',
	},
	"taskName": "0914-testData"
}

response = requests.post(url, data=json.dumps(dataDownload), headers={'Content-Type':'application/json', 'Token-type' : 'ops'})
print(response.text)
