#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time


sendTriggerList = ['relaxStart', 'relaxEnd', 'stressStart', 'stressEnd']
for i in range(len(sendTriggerList)):
    clockTime =time.time()
    faultInfo = str(round(clockTime*1000))

    dataSendTrigger = {
        "content":sendTriggerList[i],
        "dotTime":faultInfo,
        "sceneRecordUid":"5f588b79eb6e92763cb5c853",
        "testeeUids":[
            "5f4debc7eb6e92141c356070"
        ]
    }

    postTrigger = requests.post('http://192.168.8.106:9110/dot/record/saveRecordSimple', data=json.dumps(dataSendTrigger), headers={'Content-Type':'application/json', 'Token-type' : 'mgr'})
    print(postTrigger.text)


clockTime =time.time()
faultInfo = str(round(clockTime*1000))


def apiTrigger():
    dataSendTrigger = {
        "content":sendTriggerList[i],
        "dotTime":faultInfo,
        "sceneRecordUid":"5f588b79eb6e92763cb5c853",
        "testeeUids":[
            "5f4debc7eb6e92141c356070"
        ]
    }

    postTrigger = requests.post('http://192.168.8.106:9110/dot/record/saveRecord', data=json.dumps(dataSendTrigger), headers={'Content-Type':'application/json', 'Token-type' : 'mgr'})
