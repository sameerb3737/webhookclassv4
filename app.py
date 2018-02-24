# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import sys
import json
import os
from chapter1 import chapter1

from pathlib import Path
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def log(msg):
    print (msg)
    sys.stdout.flush()
	
def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    sessionID = req.get("sessionId")
    
    log('step1')
    
    chapternumber =1
    testpaper = 1
    currentquestion  =1	
    previousquestion =1
    previousAnswer =1

    contexts = result.get("contexts")
    contextName = contexts[0].get("name")

    log('step2')
    a = list()
    a = getData(contexts)
    print (a)
    chapternumber =a['chapternumber']
    testpaper =a['testpaper']
    currentquestion =a['currentquestion']
    previousquestion =a['previousquestion']
    previousAnswer =a['previousAnswer']
    
    #parameters = result.get("parameters")
    #useranswer = parameters.get("answer")
    
    
    correctIncorrectMessage =""
    QuestionText = "Sample Question"
    Option1 ="Option1"
    Option2 ="Option2"
    Option3 ="Option3"
    Option4 ="OPtion3"
    
    log('step3')

    
    line = ""
    chapterContext = "chapter1"
    myobjectx = chapter1()
    myobjectx = getChapterObject(chapternumber)
    
    log('step3.1')	
    

    Respondedanswer  = previousAnswer
    
    
    log('step4')
    if ( currentquestion - previousquestion == 1) and (currentquestion > 1):
        log('current Q >=2 ')
        temp= previousquestion-1
        RightAnswer =getAnswer(myobjectx.testpaper[testpaper][temp])
        if Respondedanswer ==  RightAnswer:
            correctIncorrectMessage = "Great! Correct Answer "
        else:
            correctIncorrectMessage = "Oops" + "Correct Answer is " + str(RightAnswer)
    log('step6')
    temp1= currentquestion-1
    line= myobjectx.testpaper[testpaper][temp1]
    log('step7')
    #line= "15#Question15#Option1#Option2#Option3#Option4#2" 			
    words3 = line.split("#")
    QuestionText = words3[1]
    Option1 = words3[2]
    Option2 = words3[3]
    Option3 = words3[4]
    Option4 = words3[5]

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    var5	="          \"type\": 0,	"
    var6	="          \"platform\": \"facebook\",	"
    var7	="          \"speech\": \"Question Text1\"	"
    speech = "HELLO"
    speech1 = var5 + var6  + var7
    
    log('before response')
    print("Response:")
    print(speech)
     #"contextOut": [],
    emptyspace = ""
    return {
   
   "speech":"",
   "messages":[
      {
         "type":3,
         "platform":"facebook",
         "imageUrl":"http://charityrefresh.org/ella/asset.hello-ella.gif"
      },
      {
         "type":0,
         "platform":"facebook",
         "speech": correctIncorrectMessage 
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":QuestionText 
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":Option1
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":Option2
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":Option3
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":Option4
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":"My Second Responsedd " 
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":sessionID
      },
        {
         "type":0,
         "platform":"facebook",
         "speech":contextName
      },
       {
          "type": 2,
          "platform": "facebook",
          "title": "What can I help you with",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     },
      {
         "type":4,
         "platform":"facebook",
         "payload":{
            "facebook":{
               "attachment":{
                  "type":"template",
                  "payload":{
                     "template_type":"button",
                     "text":"What can I help you with?",
                     "buttons":[
                        {
                           "type":"postback",
                           "title":"Answer A",
                           "payload":"A"
                        },
                        {
                           "type":"postback",
                           "title":"Answer B",
                           "payload":"B"
                        },
                        {
                           "type":"postback",
                           "title":"Answer C",
                           "payload":"C"
                        }
                     ]
                  }
               }
            }
         }
      }
   ]
}
def getData(contexts):
    contextnames =list();
    lifespan =list();
    parameters=list();
    
    for i in range(len(contexts)):
        input = contexts[i]
        all_keys = input.keys()
        
        
        for key in  all_keys:
            
            if isinstance(input[key],str):
                
                contextnames.append(input[key])
            else:
                if isinstance(input[key],int):
                    lifespan.append(input[key])
                else:
                    parameters.append( input[key])
                    
    
            
    chapternumber =1
    testpaper =1
    currentquestion=1
    previousquestion=0
    previousAnswer =1
    
    print (contextnames)
    print (lifespan)
    print (parameters[0]['answer'])
    questionarray=[0,0]
    c=0
    for x in range(len(contextnames)):
    
        if 'chapter' in contextnames[x] and lifespan[x] ==5:
            chapternumber= contextnames[x].replace('chapter','')
        if 'testpaper' in contextnames[x] and lifespan[x] ==5:
            testpaper = contextnames[x].replace('testpaper','')
        if len(contextnames) ==3 and 'q' in contextnames[x] and lifespan[x] ==5:
            currentquestion = contextnames[x].replace('q','')
        
        if len(contextnames) ==4 and 'q' in contextnames[x] and (lifespan[x] ==5 or lifespan[x] ==4):
            
            questionarray[c] = contextnames[x].replace('q','')
            c= c+1
            
    
    
    if len(contextnames) == 4:
        currentquestion =  max(questionarray)
        previousquestion = min(questionarray)
    else:
        previousquestion = min(questionarray)
    previousAnswer = parameters[0]['answer']    
    d = dict()
    
    d['chapternumber'] =chapternumber
    d['testpaper'] =testpaper
    d['currentquestion'] =currentquestion
    d['previousquestion'] =previousquestion
    d['previousAnswer'] =previousAnswer
    
    return d

def getChapterObject(chapterContext):
    myobjectx = chapter1()
    if (chapterContext ==  1):
        myobjectx = chapter1()
    if (chapterContext ==  2):
        myobjectx = chapter2()
    if (chapterContext ==  3):
        myobjectx = chapter3()
    if (chapterContext ==  4):
        myobjectx = chapter4()
    if (chapterContext ==  5):
        myobjectx = chapter5()
    if (chapterContext ==  6):
        myobjectx = chapter6()
    if (chapterContext ==  7):
        myobjectx = chapter7()
    if (chapterContext ==  8):
        myobjectx = chapter8()
    if (chapterContext ==  9):
        myobjectx = chapter9()
    if (chapterContext ==  10):
        myobjectx = chapter10()
    if (chapterContext ==  11):
        myobjectx = chapter11()
    if (chapterContext ==  12):
        myobjectx = chapter12()
    if (chapterContext ==  13):
        myobjectx = chapter13()
    if (chapterContext ==  14):
        myobjectx = chapter14()
    if (chapterContext ==  15):
        myobjectx = chapter15()
    if (chapterContext ==  16):
        myobjectx = chapter16()
    if (chapterContext ==  17):
        myobjectx = chapter17()
    if (chapterContext ==  18):
        myobjectx = chapter18()
    if (chapterContext ==  19):
        myobjectx = chapter19()
    if (chapterContext ==  20):
        myobjectx = chapter20()
    if (chapterContext ==  21):
        myobjectx = chapter21()
    if (chapterContext ==  22):
        myobjectx = chapter22()
    if (chapterContext ==  23):
        myobjectx = chapter23()
    if (chapterContext ==  24):
        myobjectx = chapter24()
    if (chapterContext ==  25):
        myobjectx = chapter25()
    if (chapterContext ==  26):
        myobjectx = chapter26()
    if (chapterContext ==  27):
        myobjectx = chapter27()
    if (chapterContext ==  28):
        myobjectx = chapter28()

    return myobjectx


	
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def readLine(file_name,contextName):
    fp = open(file_name)
    for i, line in enumerate(fp):
        if i == string.replace(string.replace(contextName,"q",""),"Q",""):
            # 26th line
            return line
            #questiontext
            #answer = words2[3]
            break
    fp.close()

def getAnswer(line):
    words3 = line.split("#")
    return words3[6]
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
