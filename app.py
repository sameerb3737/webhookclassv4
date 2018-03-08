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
def getclass1(req):
    result = req.get("result")
    sessionID = req.get("sessionId")
    contexts = result.get("contexts")
    classes = list();
    classes.append("9")
    classes.append("10")
    classes.append("11")
    classes.append("12")
    #return getclassdetails(str(classes)[1:-1])
    #print(str(json.dumps(classes))[1:-1])
    return getclassdetails(json.dumps(classes))

def getsubject(req):
    print('get subject')
    result = req.get("result")
    sessionID = req.get("sessionId")
    contexts = result.get("contexts")
    classsubject = dict()
    classsubject['7'] = "science"
    classsubject['8'] = "science"
    classsubject['9'] = "physics:chemistry:biology"
    classsubject['10'] = "physics:chemistry:biology"
    classsubject['11'] = "physics:chemistry:biology"
    classsubject['12'] = "physics:chemistry:biology"
    classnumber ='8'
    try:
        print(result.get('parameters'))
        classnumber = result.get('parameters')['class']
        print( classnumber)
        print(json.dumps(classsubject[classnumber].split(":")))

        return getsubjectdetails(classnumber, json.dumps(classsubject[classnumber].split(":")))
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)    
    

def getchapter(req):
    print('get chapter')
    result = req.get("result")
    sessionID = req.get("sessionId")
    contexts = result.get("contexts")
    classsubjectchapter =dict()
    classsubjectchapter['class9physics'] = "1:2:4"
    classsubjectchapter['class9chemistry'] = "3:5:6"
    classsubjectchapter['class9biology'] = "7:10:11"
    classsubjectchapter['class10physics'] = "1:2:4"
    classsubjectchapter['class10chemistry'] = "3:5:6"
    classsubjectchapter['class10biology'] = "7:10:11"
    classsubjectchapter['class11physics'] = "1:2:4"
    classsubjectchapter['class11chemistry'] = "3:5:6"
    classsubjectchapter['class11biology'] = "7:10:11"
    classsubjectchapter['class8science'] = "1:2:3:4:5:6:7:8:9:10:11:12:13:14"
    classsubjectchapter['class7science'] = "1:2:3:4:5:6:7:8:9:10:11:12:13:14"

    classnumber ='8'
    subject= ''
    print(result.get('parameters'))
    result1=''
    try:
        classnumber = result.get('parameters')[0]['class']
        subject = result.get('parameters')[1]['subject']
        subject = 'science'
        te = 'class' + classnumber + subject

        if int(classnumber) < 9:
            result1 = getchapterlessthan8(classnumber, subject, "Send Text Message: " + json.dumps(classsubjectchapter[te].split(":")))
            #print("Send Text Message: " + str(classsubjectchapter[te].split(":"))[1:-1])
        else:
            result1 = getchapterdetails(classnumber, subject, json.dumps(classsubjectchapter[te].split(":")))
            #print(str(classsubjectchapter[te].split(":"))[1:-1])
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)    
    return result1

def makeWebhookResult(req):

    if req.get("result").get("action") == "getclass":
        return getclass1(req)
    if req.get("result").get("action") == "getsubject":
        return getsubject(req)
    if req.get("result").get("action") == "getchapter":
        return getchapter(req)
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
    a = getData2(contexts)
    print (a)
    marks = 0
    classnumber = a['class']
    subject = a['subject']
    chapternumber =a['chapternumber']
    testpaper =a['testpaper']
    currentquestion =a['currentquestion']
    previousquestion =a['previousquestion']
    previousAnswer =int(a['previousAnswer'])
    marks = a['marks']
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
    #chapterContext = "chapter1"
    myobjectx = chapter1()
    log('before getChapterObject2')
    myobjectx = getChapterObject2(classnumber,subject,chapternumber)
    
    log('step3.1')
    Respondedanswer  = previousAnswer
    difference = 0
    difference = currentquestion - previousquestion
    log('step4')
    if ( difference == 1) and (currentquestion > 1):
        log('inside if')
        temp= previousquestion-1
        RightAnswer = getAnswer(myobjectx.testpaper[testpaper][temp])
        if Respondedanswer ==  RightAnswer:
            marks =marks+1
            correctIncorrectMessage = "Great! Correct Answer " + "! Your marks:" + str(marks)
        else:
            correctIncorrectMessage = "Oops! " + "Correct Answer is " + str(RightAnswer) + ". " + "Your marks:" + str(marks)
    log('step6')
    if ( currentquestion > 31):
        return FinalMessage(correctIncorrectMessage,currentquestion,previousquestion)
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
    #print(speech1)
    #"contextOut": [],
    #print(str(sessionID) + "#" + str(chapternumber) + "#" + str(testpaper) + "#" + previousquestion + "#" + correctIncorrectMessage)
    print(correctIncorrectMessage + "#" + str(QuestionText) + "#" + str(Option1) + "#" + Option2 + "#" + Option3)
    return ReturnWebHookResponse(correctIncorrectMessage,QuestionText,Option1,Option2,Option3,Option4,currentquestion,previousquestion,marks,classnumber,subject,chapternumber,testpaper)

def FinalMessage(correctIncorrectMessage,currentquestion,previousquestion):
    print(correctIncorrectMessage)
    try:
        return  {
        "contextOut": [
        {
	  "name": "q" + str(currentquestion) ,
          "parameters": {
                 
          },
          "lifespan": 0
        },
        {
	  "name": "q" + str(previousquestion) ,
          "parameters": {
                   
          },
           "lifespan": 0
        }
       ],
        "speech":"",
        "messages":[
         {
             "type":0,
             "platform":"facebook",
             "speech": correctIncorrectMessage 
          },
          {
             "type":0,
             "platform":"facebook",
             "speech":"You had reach end of test" 
          },
          {
              "type": 2,
              "platform": "facebook",
              "title": "Do you want to Try some more test?",
              "replies": [
                "Goback",
                "Exit"
            
             ]
             }
          ] 
        }
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)
	
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
    try:
        previousAnswer = parameters[0]['answer']
    except:
        previousAnswer = 0
    d = dict()
    
    d['chapternumber'] =int(chapternumber)
    d['testpaper'] =int(testpaper)
    d['currentquestion'] =int(currentquestion)
    d['previousquestion'] =int(previousquestion)
    d['previousAnswer'] =int(previousAnswer)
    
    return d
	
def getData2(contexts):
    
    contextnames =list()
    lifespan =list()
    parameters=list()
    d = dict()
    try:	
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
        print(parameters)
        questionarray=[0,0]
        c=0
        for x in range(len(contextnames)):
            if 'chapter' in contextnames[x] and lifespan[x] ==5:
                chapternumber= contextnames[x].replace('chapter','')
            if 'testpaper' in contextnames[x] and lifespan[x] ==5:
                testpaper = contextnames[x].replace('testpaper','')
            if len(contextnames) ==1 and 'q' in contextnames[x] and lifespan[x] ==5:
                currentquestion = contextnames[x].replace('q','')
        
            if len(contextnames) >1 and 'q' in contextnames[x] and (lifespan[x] ==5 or lifespan[x] ==4):
            
                questionarray[c] = int(contextnames[x].replace('q',''))
                c= c+1
            
    
        print(questionarray) 
        if len(contextnames) > 1:
            indexpara= 0
            indexpara = len(contextnames) -1
            print(indexpara)
            currentquestion =  max(questionarray)
            previousquestion = currentquestion - 1
            previousAnswer = int(parameters[indexpara]['answer'])
        else:
            previousquestion = min(questionarray)
            previousAnswer = 0
        print('before dict')       
        marks = 0
        try:
            if len(contextnames) > 1:
                marks = int(parameters[0]['marks'])
            else:
                marks =0
        except:
            marks = 0
    
        if len(contextnames) > 1:
            indexpara= 0
            #indexpara = len(contextnames) -1
            try:
                d['class'] =int(parameters[indexpara]['class'])
                d['subject'] =parameters[indexpara]['subject']		
                d['chapternumber'] =int(parameters[indexpara]['chapter'])
                d['testpaper'] =int(parameters[indexpara]['testpaper'])
            except:
                indexpara= 1
                d['class'] =int(parameters[indexpara]['class'])
                d['subject'] =parameters[indexpara]['subject']		
                d['chapternumber'] =int(parameters[indexpara]['chapter'])
                d['testpaper'] =int(parameters[indexpara]['testpaper'])
            d['currentquestion'] =int(currentquestion)
            d['previousquestion'] =int(previousquestion)
            d['previousAnswer'] = int(previousAnswer)
            d['marks'] = int(marks)
        if len(contextnames) == 1:
            d['class'] =int(parameters[0]['class'])
            d['subject'] =parameters[0]['subject']		
            d['chapternumber'] =int(parameters[0]['chapter'])
            d['testpaper'] =int(parameters[0]['testpaper'])
            d['currentquestion'] =int(currentquestion)
            d['previousquestion'] =int(previousquestion)
            d['previousAnswer'] = int(previousAnswer)
            d['marks'] = int(marks)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)
    return d
def getChapterObject2(classnumber,subject,chapter):
    classname=''
    classname = 'class' + str(classnumber) + 'subject' + subject +'chapter' + str(chapter)
    classname = 'chapter1'
    obj  = chapter1()
    try:
        obj = globals()[classname]()
    except:
        print(sys.exc_info()[0])
    #obj = globals()[classname]()
    return obj
	
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
def ReturnWebHookResponse(correctIncorrectMessage,QuestionText,Option1,Option2,Option3,Option4,currentquestion,previousquestion,marks,classnumber,subject,chapter,testpaper):
    print('inside response function')
    if currentquestion == 1:
        currentquestion = currentquestion +1
        previousquestion = previousquestion + 1
	
    return {
    "contextOut": [
    {
	  "name": "q" + str(currentquestion) ,
          "parameters": {
          "marks":marks,
	  "class": str(classnumber),
          "subject": subject,
          "chapter": str(chapter),
          "testpaper": str(testpaper)                 
          },
          "lifespan": 5
     },
     {
	  "name": "q" + str(previousquestion) ,
          "parameters": {
          "marks":marks,
	  "class": str(classnumber),
          "subject": subject,
          "chapter": str(chapter),
          "testpaper": str(testpaper)                 
          },
           "lifespan": 0
     }
    ],	    
   "speech":"",
   "messages":[
      #{
      #   "type":3,
      #   "platform":"facebook",
      #   "imageUrl":"http://charityrefresh.org/ella/asset.hello-ella.gif"
      #},
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
          "type": 2,
          "platform": "facebook",
          "title": "Choose the Right Answer",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     },
      {
         "type":0,
         "platform":"slack",
         "speech": correctIncorrectMessage 
      },
      {
         "type":0,
         "platform":"slack",
         "speech":QuestionText 
      },
      {
         "type":0,
         "platform":"slack",
         "speech":Option1
      },
      {
         "type":0,
         "platform":"slack",
         "speech":Option2
      },
      {
         "type":0,
         "platform":"slack",
         "speech":Option3
      },
      {
         "type":0,
         "platform":"slack",
         "speech":Option4
      },
      {
          "type": 2,
          "platform": "slack",
          "title": "Choose the Right Answer",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     },
      {
         "type":0,
         "platform":"skype",
         "speech": correctIncorrectMessage 
      },
      {
         "type":0,
         "platform":"skype",
         "speech":QuestionText 
      },
      {
         "type":0,
         "platform":"skype",
         "speech":Option1
      },
      {
         "type":0,
         "platform":"skype",
         "speech":Option2
      },
      {
         "type":0,
         "platform":"skype",
         "speech":Option3
      },
      {
         "type":0,
         "platform":"skype",
         "speech":Option4
      },
      {
          "type": 2,
          "platform": "skype",
          "title": "Choose the Right Answer",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     },
      {
         "type":0,
         "platform":"viber",
         "speech": correctIncorrectMessage 
      },
      {
         "type":0,
         "platform":"viber",
         "speech":QuestionText 
      },
      {
         "type":0,
         "platform":"viber",
         "speech":Option1
      },
      {
         "type":0,
         "platform":"viber",
         "speech":Option2
      },
      {
         "type":0,
         "platform":"viber",
         "speech":Option3
      },
      {
         "type":0,
         "platform":"viber",
         "speech":Option4
      },
      {
          "type": 2,
          "platform": "viber",
          "title": "Choose the Right Answer",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     },
      {
         "type":0,
         "platform":"kik",
         "speech": correctIncorrectMessage 
      },
      {
         "type":0,
         "platform":"kik",
         "speech":QuestionText 
      },
      {
         "type":0,
         "platform":"kik",
         "speech":Option1
      },
      {
         "type":0,
         "platform":"kik",
         "speech":Option2
      },
      {
         "type":0,
         "platform":"kik",
         "speech":Option3
      },
      {
         "type":0,
         "platform":"kik",
         "speech":Option4
      },
      {
          "type": 2,
          "platform": "kik",
          "title": "Choose the Right Answer",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     },
      {
         "type":0,
         "platform":"telegram",
         "speech": correctIncorrectMessage 
      },
      {
         "type":0,
         "platform":"telegram",
         "speech":QuestionText 
      },
      {
         "type":0,
         "platform":"telegram",
         "speech":Option1
      },
      {
         "type":0,
         "platform":"telegram",
         "speech":Option2
      },
      {
         "type":0,
         "platform":"telegram",
         "speech":Option3
      },
      {
         "type":0,
         "platform":"telegram",
         "speech":Option4
      },
      {
          "type": 2,
          "platform": "telegram",
          "title": "Choose the Right Answer",
          "replies": [
            "1",
            "2",
            "3",
            "4"
          ]
     }


   ]
}

def getclassdetails(classdetails):
    print('inside class  function')

	
    return {
    "contextOut": [
     ],	    
   "speech":"",
   "messages":[
    {
          "type": 2,
          "platform": "facebook",
          "title": "Choose Your Class",
          "replies": [
          classdetails
          ]
     },
      {
          "type": 2,
          "platform": "slack",
           "title": "Choose Your Class",
          "replies": [
          classdetails
          ]
     },
      {
          "type": 2,
          "platform": "skype",
            "title": "Choose Your Class",
          "replies": [
          classdetails
          ]
     },
     {
          "type": 2,
          "platform": "viber",
             "title": "Choose Your Class",
          "replies": [
           classdetails
          ]
     },
     {
          "type": 2,
          "platform":"kik",
           "title": "Choose Your Class",
          "replies": [
        classdetails
          ]
     },
     {
          "type": 2,
          "platform": "telegram",
         "title": "Choose Your Class",
          "replies": [
         classdetails
          ]
     }


   ]
}
def getsubjectdetails(classnumber, subjectdetails):
    print('inside subject  function')

	
    return {
    "contextOut": [
    {
	  "name": "t1"  ,
          "parameters": {

	  "class": str(classnumber)
               
          },
          "lifespan": 0
     },
     {
	  "name": "t2"  ,
          "parameters": {
   
	  "class": str(classnumber)
                        
          },
           "lifespan": 5
     }
     ],	    
   "speech":"",
   "messages":[
    {
          "type": 2,
          "platform": "facebook",
          "title": "Choose Your Subject",
          "replies": [
            subjectdetails
          ]
     },
      {
          "type": 2,
          "platform": "slack",
           "title": "Choose Your Subject",
          "replies": [
        subjectdetails
          ]
     },
      {
          "type": 2,
          "platform": "skype",
            "title": "Choose Your Subject",
          "replies": [
          subjectdetails
          ]
     },
     {
          "type": 2,
          "platform": "viber",
             "title": "Choose Your Subject",
          "replies": [
          subjectdetails
          ]
     },
     {
          "type": 2,
          "platform":"kik",
           "title": "Choose Your Subject",
          "replies": [
           subjectdetails
          ]
     },
     {
          "type": 2,
          "platform": "telegram",
         "title": "Choose Your Subject",
          "replies": [
         subjectdetails
          ]
     }


   ]
}
def getchapterlessthan8(classnumber, subject, chaptermsg):
    print('inside response function')
    
	
    return {
    "contextOut": [
     {
	  "name": "t2" ,
          "parameters": {

	  "class": str(classnumber),
          "subject": subject
                     
          },
          "lifespan": 0
     },
     {
	  "name": "t3"  ,
          "parameters": {

	  "class": str(classnumber),
          "subject": subject
                 
          },
           "lifespan": 5
     }
  
    ],	    
   "speech":"",
   "messages":[
      
      {
         "type":0,
         "platform":"facebook",
         "speech": chaptermsg 
      },
    
      {
         "type":0,
         "platform":"slack",
         "speech": chaptermsg 
      },
     
      {
         "type":0,
         "platform":"skype",
         "speech": chaptermsg 
      },
     
      {
         "type":0,
         "platform":"viber",
         "speech": chaptermsg 
      },
     
      {
         "type":0,
         "platform":"kik",
         "speech": chaptermsg 
      },
     
      {
         "type":0,
         "platform":"telegram",
         "speech": chaptermsg 
      }
     


   ]
}
def getchapterdetails(chapterdetails):
    print('inside subject  function')

	
    return {
    "contextOut": [
    {
	  "name": "t2"  ,
          "parameters": {

	  "class": str(classnumber),
          "subject": subject
               
          },
          "lifespan": 0
     },
     {
	  "name": "t3"  ,
          "parameters": {
   
	  "class": str(classnumber),
          "subject": subject
                        
          },
           "lifespan": 5
     }
     ],	    
   "speech":"",
   "messages":[
    {
          "type": 2,
          "platform": "facebook",
          "title": "Choose Your Chapter",
          "replies": [
            chapterdetails
          ]
     },
      {
          "type": 2,
          "platform": "slack",
           "title": "Choose Your Chapter",
          "replies": [
        chapterdetails
          ]
     },
      {
          "type": 2,
          "platform": "skype",
            "title": "Choose Your Chapter",
          "replies": [
          chapterdetails
          ]
     },
     {
          "type": 2,
          "platform": "viber",
             "title": "Choose Your Chapter",
          "replies": [
          chapterdetails
          ]
     },
     {
          "type": 2,
          "platform":"kik",
           "title": "Choose Your Chapter",
          "replies": [
           chapterdetails
          ]
     },
     {
          "type": 2,
          "platform": "telegram",
         "title": "Choose Your Chapter",
          "replies": [
         chapterdetails
          ]
     }


   ]
}
def getAnswer(line):
    words3 = line.split("#")
    print('answer' + str(words3[6]))
    return int(words3[6])
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
