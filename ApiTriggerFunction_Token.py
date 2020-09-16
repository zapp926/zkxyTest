#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

triggerList = ['relaxStart', 'relaxEnd', 'mathStart', 'mathEnd', 'VRStart', 'VREnd']

def VRTrigger(triggerList, sceneUid, subjUid):
    clockTime = time.time()
    faultInfo = str(round(clockTime*1000))

    dataSendTrigger = {
        "content":triggerList,
        "dotTime":faultInfo,
        "sceneRecordUid":sceneUid,
        "testeeUids":[
            subjUid
        ]
    }

    postTrigger = requests.post('http://192.168.8.106:9110/dot/record/saveRecordSimple', data=json.dumps(dataSendTrigger), headers={'Content-Type':'application/json', 'Token-type' : 'mgr'})

if __name__ == "__main__":
    VRTrigger(triggerList[5], '5f5f49b1eb6e92207652afd5', '5f4debc7eb6e92141c356070')

