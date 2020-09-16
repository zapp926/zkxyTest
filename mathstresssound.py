#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui
import random
import time
import pandas as pd
# import winsound
import pygame
import requests
import json

def Instruction(displayText):
    text_instru = visual.TextStim(win, text=u'', height=30, font='Hei', pos=(0.0, 0.0), color='white', wrapWidth=None)
    text_instru.text = displayText
    text_instru.height = 38
    text_instru.draw()
    win.flip()
    core.wait(0)
    key_start = event.waitKeys()


def sendTrigger(trigger):
    #clockTime = time.ctime(time.time())
    clockTime =time.time()
    triggerInfo = str(round(clockTime*1000)) + ',' + str(trigger) + '\n'
    #triggerInfo = str(clockTime) + ',' + str(trigger) + '\n'
    dataFile.write(triggerInfo)

def sendFault(index, number):
    #clockTime = time.ctime(time.time())
    clockTime = time.time()
    faultInfo = str(round(clockTime*1000)) + '\n' #  + ',' + str(index) + ',' + str(number)
    faultFile.write(faultInfo)


def IntervalTime(timerelax):
    text_instru = visual.TextStim(win, text=u'', height=30, font='Hei', pos=(0.0, 0.0), color='white')
    dtimer = core.CountdownTimer(timerelax)
    while dtimer.getTime() > 0:
        text_instru.text = str(int(dtimer.getTime()))
        text_instru.draw()
        win.flip()


def fixation(timeWait):
    text_instru = visual.TextStim(win, text=u'', height=30, font='Hei', pos=(0.0, 0.0), color='white')
    text_instru.text = u'+'
    text_instru.height = 38
    text_instru.draw()
    win.flip()
    core.wait(timeWait)


def apiTrigger(triggerList, sceneUid, subjUid):
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


def mainExp(minSeconds, maxSeconds, maxTrueCount, maxFalseCount):
    countTimer = maxSeconds
    examTrial = 0
    answerFalseQues = 0
    lastCountPositive = 0
    lastCountNegative = 0
    lastIsPositive = 1
    lastFaultKey = 1
    examIndex = 0
    showAnswerSeconds = 0

    trackFile ='countdowntime.mp3' #文件名是完整路径名
    pygame.mixer.init() #初始化音频
    track = pygame.mixer.music.load(trackFile) #载入音乐文件
    trackStart = 0

    sendTrigger(triggerList[2])
    fixation(1.0)
    trialNumber = list(range(len(df)))
    random.shuffle(trialNumber)

    for trial in trialNumber:
        lastFaultKey = 0
        examIndex += 1
        normal_text = visual.TextStim(win=win, pos=(0, -100),  font='Hei', units='pix')
        timer = core.CountdownTimer(countTimer)

        trackStart = 0

        choiceDirections = random.randint(0, 2)
        while timer.getTime() > 0:
            current_time = timer.getTime()
            normal_text.text = str(round(timer.getTime(), ndigits=1)) + ' 秒'
            normal_text.height = 42
            normal_text.color = 'red'

            if current_time < 1.5 and trackStart == 0:
                trackStart = 1
                pygame.mixer.music.play()#开始播放
             
            if choiceDirections == 0:
                text_examQuestion = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, 150), color='white', wrapWidth=None)
                text_examQuestion.text = '题目：第 ' + str(df.iloc[examTrial][5]) + ' 题'

                text_formula = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, 0), color='white', wrapWidth=None)
                text_formula.text = str(df.iloc[trial][0]) + ' ' + str(df.iloc[trial][1]) + '          ' + ' = ' + str(df.iloc[trial][4])

                shape_stim = visual.Rect(win, width=100, height=80, pos=(0, 0), autoLog=None, lineColor='white', lineWidth=4)
                answer_stim = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, 0), color='white', wrapWidth=None)
                answer_stim.text = str(df.iloc[trial][2])
                
                text_Feedback = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, -200), color='red', wrapWidth=None)
                text_Feedback.text = '错误数：' + str(answerFalseQues)

                shape_stim.draw()
                normal_text.draw()
                text_examQuestion.draw()
                text_formula.draw()
                text_Feedback.draw()
                win.flip()

                if event.getKeys(keyList=['space']) and current_time < countTimer - 1:
                    break
                elif event.getKeys(keyList=['f']):
                    if (lastFaultKey == 0):
                        lastFaultKey = 1
                        answerFalseQues += 1
                        lastIsPositive = 0
                        # winsound.Beep(600,500)
                        sendFault(examIndex, trial)
                elif event.getKeys(keyList=['q']):
                    core.quit()

            else:
                text_examQuestion = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, 150), color='white', wrapWidth=None)
                text_examQuestion.text = '题目：第 ' + str(df.iloc[examTrial][5]) + ' 题'

                text_formula = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, 0), color='white', wrapWidth=None)
                text_formula.text = '          ' + str(df.iloc[trial][1]) + ' ' + str(df.iloc[trial][2]) + ' = ' + str(df.iloc[trial][4])

                shape_stim = visual.Rect(win, width=100, height=80, pos=(-110, 0), autoLog=None, lineColor='white', lineWidth=4)
                answer_stim = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, 0), color='white', wrapWidth=None)
                answer_stim.text = str(df.iloc[trial][0])

                text_Feedback = visual.TextStim(win, text=u'', height=38, font='Hei', pos=(0, -200), color='red', wrapWidth=None)
                text_Feedback.text = '错误数：' + str(answerFalseQues)

                shape_stim.draw()
                normal_text.draw()
                text_examQuestion.draw()
                text_formula.draw()
                text_Feedback.draw()
                win.flip()

                if event.getKeys(keyList=['space']) and current_time < countTimer - 1:
                    break
                elif event.getKeys(keyList=['f']):
                    if (lastFaultKey == 0):
                        lastFaultKey = 1
                        answerFalseQues += 1
                        lastIsPositive = 0
                        # winsound.Beep(600,500)
                        sendFault(examIndex, trial)
                elif event.getKeys(keyList=['q']):
                    core.quit()

        if (showAnswerSeconds > 0):
            answerTimer = core.CountdownTimer(showAnswerSeconds)
            while answerTimer.getTime() > 0:
                shape_stim.draw()
                normal_text.draw()
                text_examQuestion.draw()
                text_formula.draw()
                text_Feedback.draw()
                answer_stim.draw()
                win.flip()
                if event.getKeys(keyList=['f']):
                    sendFault(examIndex, trial)
                    if (lastFaultKey == 0):
                        lastFaultKey = 1
                        answerFalseQues += 1
                        lastIsPositive = 0
                        # winsound.Beep(600,500)
                        sendFault(examIndex, trial)
                elif event.getKeys(keyList=['q']):
                    core.quit()
        
        if trackStart == 1:
            pygame.mixer.music.stop()#停止播放

        if lastIsPositive == 1:
            lastCountPositive += 1
            lastCountNegative = 0
        else:
            lastCountNegative += 1
            lastCountPositive = 0

        if lastCountPositive >= maxTrueCount and countTimer > minSeconds:
            countTimer = countTimer - 1
            lastCountPositive = 0
        elif lastCountNegative >= maxFalseCount and countTimer < maxSeconds:
            countTimer = countTimer + 1
            lastCountNegative = 0

        examTrial += 1
        lastIsPositive = 1
        for key in event.getKeys():
            if key in ['q']:
                core.quit()


def ExperimentOver(displayEndText):
    Instruction(displayEndText)
    win.close()
    core.quit()


if __name__ == "__main__":
    info = {'name': '', 'watches': '', 'num': '', 'task': ''}
    infoDlg = gui.DlgFromDict(dictionary=info, title=u'基本信息', order=['name', 'num', 'task', 'watches'])
    if not infoDlg.OK:
        core.quit()

    dataFile = open('./%s.csv' %(info['num'] + '_' + info['name'] + '_' + info['task'] + '_' + info['watches']), 'a')
    faultFile = open('./%s.csv' %(info['num'] + '_' + info['name'] + '_' + info['task'] + '_' + info['watches'] + '_faults'), 'a')

    dataFile.write('Timestampted,Trigger\n')
    df = pd.read_excel('formalComputeQuestion1.xlsx', header=None)

    scnWidth, scnHeight = [1920, 1080]
    win = visual.Window((scnWidth, scnHeight), fullscr=True, units='pix', colorSpace='rgb')
    win.mouseVisible = False
    win.color= 'black'
    
    displayWelcomeText = u'Welcome to the zkpsy experiment.\n\n按空格键开始'
    displayRelaxText = u'请您静坐休息5分钟，保持安静。\n\n按空格键开始倒计时'
    displayEndText = u'实验结束\n请静坐休息5分钟\n\n感谢您的参与'

    triggerList = ['relaxS1', 'relaxE1', 'stressS2', 'stressE2']

    Instruction(displayWelcomeText)
    Instruction(displayRelaxText)
    sendTrigger(triggerList[0])
    apiTrigger(triggerList[0], '5f59d73eeb6e92648d668a48', '5f598c83eb6e9263d004a142')
    IntervalTime(10)
    sendTrigger(triggerList[1])
    apiTrigger(triggerList[1], '5f59d73eeb6e92648d668a48', '5f598c83eb6e9263d004a142')
    time.sleep(2)
    sendTrigger(triggerList[2])
    apiTrigger(triggerList[2], '5f59d73eeb6e92648d668a48', '5f598c83eb6e9263d004a142')
    mainExp(5, 8, 3, 2)
    sendTrigger(triggerList[3])
    apiTrigger(triggerList[3], '5f59d73eeb6e92648d668a48', '5f598c83eb6e9263d004a142')
    ExperimentOver(displayEndText)
