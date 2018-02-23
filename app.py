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


def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    sessionID = req.get("sessionId")
    
      
  
    

    questionnumber  =1	
    testpaper = 1    
    contexts = result.get("contexts")
    contextName = contexts[0].get("name")
    if 'chapter' in contexts[0].get('name'):
        if 'q' in contexts[1].get('name'):
            testpaper = contexts[2].get('name')
            questionnumber = contexts[1].get('name')
            chapterContext = contexts[0].get('name')
        else:
            testpaper = contexts[1].get('name')
            questionnumber = contexts[2].get('name')
            chapterContext = contexts[0].get('name')
    else:
    
        if 'chapter' in contexts[1].get('name'):
            if 'q' in contexts[0].get('name'):
                testpaper = contexts[2].get('name')
                questionnumber = contexts[0].get('name')
                chapterContext = contexts[1].get('name')
            else:
                testpaper = contexts[0].get('name')
                questionnumber = contexts[2].get('name')
                chapterContext = contexts[1].get('name')
        if 'chapter' in contexts[2].get('name'):
            if 'q' in contexts[1].get('name'):
                testpaper = contexts[0].get('name')
                questionnumber = contexts[1].get('name')
                chapterContext = contexts[2].get('name')
            else:
                testpaper = contexts[1].get('name')
                questionnumber = contexts[0].get('name')
                chapterContext = contexts[2].get('name')


    questionnumber = questionnumber.replace('q','')
    testpaper =testpaper.replace('testpaper','')
     
    #parameters = result.get("parameters")
    #useranswer = parameters.get("answer")
    
    
    correctIncorrectMessage =""
    QuestionText = "Sample Question"
    Option1 ="Option1"
    Option2 ="Option2"
    Option3 ="Option3"
    Option4 ="OPtion3"
    

    
    line = ""
    chapterContext = "chapter1"
    myobjectx = chapter1()
    
    if (chapterContext == "chapter1"):
        myobjectx = chapter1()
    if (chapterContext == "chapter2"):
        myobjectx = chapter2()
    if (chapterContext == "chapter3"):
        myobjectx = chapter3()
    if (chapterContext == "chapter4"):
        myobjectx = chapter4()
    if (chapterContext == "chapter5"):
        myobjectx = chapter5()
    if (chapterContext == "chapter6"):
        myobjectx = chapter6()
    if (chapterContext == "chapter7"):
        myobjectx = chapter7()
    if (chapterContext == "chapter8"):
        myobjectx = chapter8()
    if (chapterContext == "chapter9"):
        myobjectx = chapter9()
    if (chapterContext == "chapter10"):
        myobjectx = chapter10()
    if (chapterContext == "chapter11"):
        myobjectx = chapter11()
    if (chapterContext == "chapter12"):
        myobjectx = chapter12()
    if (chapterContext == "chapter13"):
        myobjectx = chapter13()
    if (chapterContext == "chapter14"):
        myobjectx = chapter14()
    if (chapterContext == "chapter15"):
        myobjectx = chapter15()
    if (chapterContext == "chapter16"):
        myobjectx = chapter16()
    if (chapterContext == "chapter17"):
        myobjectx = chapter17()
    if (chapterContext == "chapter18"):
        myobjectx = chapter18()
    if (chapterContext == "chapter19"):
        myobjectx = chapter19()
    if (chapterContext == "chapter20"):
        myobjectx = chapter20()
    if (chapterContext == "chapter21"):
        myobjectx = chapter21()
    if (chapterContext == "chapter22"):
        myobjectx = chapter22()
    if (chapterContext == "chapter23"):
        myobjectx = chapter23()
    if (chapterContext == "chapter24"):
        myobjectx = chapter24()
    if (chapterContext == "chapter25"):
        myobjectx = chapter25()
    if (chapterContext == "chapter26"):
        myobjectx = chapter26()
    if (chapterContext == "chapter27"):
        myobjectx = chapter27()
    if (chapterContext == "chapter28"):
        myobjectx = chapter28()

    
    questionnumber =3
    testpaper =1
    Respondedanswer  = 1
    RightAnswer =1	

    

    RightAnswer =getAnswer(myobjectx.testpaper[testpaper][questionnumber-1])
	
    if ( Respondedanswer ==  RightAnswer):
        correctIncorrectMessage = "Correct Answer Dude"
    else:
         correctIncorrectMessage = "oops"
        
    
    line= myobjectx.testpaper[testpaper][questionnumber]
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
