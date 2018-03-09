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
    
    chapternumber ='1'

    currentsentence  =1	
    previoussentence =1
    previousAnswer ='More'

    contexts = result.get("contexts")
    contextName = contexts[0].get("name")

    log('step2')
    a = list()
    a = getData2(contexts)
    print (a)

    classnumber = a['class']
    subject = a['subject']
    chapternumber =a['chapternumber']

    currentsentence =a['currentsentence']
    previoussentence =a['previoussentence']
    previousAnswer =int(a['previousAnswer'])

    #parameters = result.get("parameters")
    #useranswer = parameters.get("answer")
    
    
    correctIncorrectMessage =""
    sentenceText = "Sample sentence"

    
    log('step3')

    
    line = ""
    #chapterContext = "chapter1"
    myobjectx = chapter1()
    log('before getChapterObject2')
    #chapter name and number map  insert here
    chaptername = dict()
    chaptername = getChapterNameNumber()

    tempvar = ''
    try:
        tempvar = chaptername[chapternumber]
    except:
        tempvar ='1'
    myobjectx = getChapterObject2(classnumber,subject,tempvar)
    
    log('step3.1')
    Respondedanswer  = previousAnswer

    log('step4')

    if ( currentsentence > 31):



    try:
        temp1= currentsentence-1
        line= myobjectx.testpaper[temp1]
    except IndexError:
        return FinalMessage("End of Topics",currentsentence,previoussentence)        
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)
	
    message = ''
    url =''
    log('step7')
    if ( '.jpg' in line or 'jpeg' in line):
        url = line
    else:
        message = line


    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    var5	="          \"type\": 0,	"
    var6	="          \"platform\": \"facebook\",	"
    var7	="          \"speech\": \"sentence Text1\"	"
    speech = "HELLO"
    speech1 = var5 + var6  + var7
    
    log('before response')
    print("Response:")

    return ReturnWebHookRevisionResponse(message,url,currentsentence,previoussentence,classnumber,subject,chapternumber)


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
                    if 's' in input[key]:
                        contextnames.append(input[key])
                else:
                    if isinstance(input[key],int):
                        lifespan.append(input[key])
                    else:
                        parameters.append( input[key])
                    
    
            
        chapternumber ='1'
        testpaper =1
        currentsentence=1
        previoussentence=0
        previousAnswer ='1'
    
        print (contextnames)
        print (lifespan)
        print(parameters)
        sentencearray=[0,0]
        c=0
        for x in range(len(contextnames)):
            if 'chapter' in contextnames[x] and lifespan[x] ==5:
                chapternumber= contextnames[x].replace('chapter','')
            if 'testpaper' in contextnames[x] and lifespan[x] ==5:
                testpaper = contextnames[x].replace('testpaper','')
            if len(contextnames) ==1 and 's' in contextnames[x] and lifespan[x] ==5:
                currentsentence = contextnames[x].replace('q','')
        
            if len(contextnames) >1 and 's' in contextnames[x] and (lifespan[x] ==5 or lifespan[x] ==4):
            
                sentencearray[c] = int(contextnames[x].replace('s',''))
                c= c+1
            
    
        print(sentencearray) 
        if len(contextnames) > 1:
            indexpara= 0
            indexpara = len(contextnames) -1
            print(indexpara)
            currentsentence =  max(sentencearray)
            previoussentence = currentsentence - 1
            previousAnswer = int(parameters[indexpara]['answer'])
        else:
            previoussentence = min(sentencearray)
            previousAnswer = 0
        print('before dict')       

    
        if len(contextnames) > 1:
            indexpara= 0
            #indexpara = len(contextnames) -1
            try:
                d['class'] =int(parameters[indexpara]['class'])
                d['subject'] =parameters[indexpara]['subject']		
                d['chapternumber'] =parameters[indexpara]['chapter']

            except:
                indexpara= 1
                d['class'] =int(parameters[indexpara]['class'])
                d['subject'] =parameters[indexpara]['subject']		
                d['chapternumber'] =parameters[indexpara]['chapter']

            d['currentsentence'] =int(currentsentence)
            d['previoussentence'] =int(previoussentence)
            d['previousAnswer'] = previousAnswer

        if len(contextnames) == 1:
            d['class'] =int(parameters[0]['class'])
            d['subject'] =parameters[0]['subject']		
            d['chapternumber'] =parameters[0]['chapter']
            d['currentsentence'] =int(currentsentence)
            d['previoussentence'] =int(previoussentence)
            d['previousAnswer'] = previousAnswer

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
	

def ReturnWebHookRevisionResponse(message,url,currentsentence,previoussentence,classnumber,subject,chapter):
    print('inside response function')
    if currentsentence == 1:
        currentsentence = currentsentence +1
        previoussentence = previoussentence + 1
	
    return {
    "contextOut": [
    {
	  "name": "s" + str(currentsentence) ,
          "parameters": {

	      "class": str(classnumber),
          "subject": subject,
          "chapter": str(chapter)               
          },
          "lifespan": 5
     },
     {
	  "name": "s" + str(previoussentence) ,
          "parameters": {
  
	  "class": str(classnumber),
          "subject": subject,
          "chapter": str(chapter)               
          },
           "lifespan": 0
     },
     {
	  "name": "t3" ,
          "parameters": {

	  "class": str(classnumber),
          "subject": subject,
          "chapter": str(chapter)              
          },
           "lifespan": 0
     }	    
    ],	    
   "speech":"",
   "messages":[
      {
         "type":3,
         "platform":"facebook",
         "imageUrl":url
      },
      {
         "type":3,
         "platform":"slack",
         "imageUrl":url
      },
      {
         "type":3,
         "platform":"skype",
         "imageUrl":url
      },
      {
         "type":3,
         "platform":"viber",
         "imageUrl":url
      },
      {
         "type":3,
         "platform":"kik",
         "imageUrl":url
      },
      {
         "type":3,
         "platform":"telegram",
         "imageUrl":url
      },
      {
         "type":0,
         "platform":"facebook",
         "speech": message 
      },
      
      {
          "type": 2,
          "platform": "facebook",
          "title": "Choose the Right Answer",
          "replies": [
            "More",
            "Exit"
          ]
     },
      {
         "type":0,
         "platform":"slack",
         "speech": message 
      },
      {
          "type": 2,
          "platform": "slack",
          "title": "Choose the Right Answer",
          "replies": [
            "More",
            "Exit"
          ]
     },
      {
         "type":0,
         "platform":"skype",
         "speech": message 
      },
 
      {
          "type": 2,
          "platform": "skype",
          "title": "Choose the Right Answer",
          "replies": [
            "More",
            "Exit"
          ]
     },
      {
         "type":0,
         "platform":"viber",
         "speech": message 
      },
      {
          "type": 2,
          "platform": "viber",
          "title": "Choose the Right Answer",
          "replies": [
            "More",
            "Exit"
          ]
     },
      {
         "type":0,
         "platform":"kik",
         "speech": message 
      },
      {
          "type": 2,
          "platform": "kik",
          "title": "Choose the Right Answer",
          "replies": [
            "More",
            "Exit"
          ]
     },
      {
         "type":0,
         "platform":"telegram",
         "speech": message 
      },
 
      {
          "type": 2,
          "platform": "telegram",
          "title": "Choose the Right Answer",
          "replies": [
           "More",
           "Exit"
          ]
     }


   ]
}

def FinalMessage(correctIncorrectMessage,currentsentence,previoussentence):
    print(correctIncorrectMessage)
    try:
        return  {
        "contextOut": [
        {
	  "name": "s" + str(currentsentence) ,
          "parameters": {
                 
          },
          "lifespan": 0
        },
        {
	  "name": "s" + str(previoussentence) ,
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
              "type": 2,
              "platform": "facebook",
              "title": "Do you want to Try some more test?",
              "replies": [
                "Goback",
                "Exit"
            
             ]
             }
          ,
         {
             "type":0,
             "platform":"slack",
             "speech": correctIncorrectMessage 
          },
          {
              "type": 2,
              "platform": "slack",
              "title": "Do you want to Try some more test?",
              "replies": [
                "Goback",
                "Exit"
            
             ]
             },
	  {
             "type":0,
             "platform":"kik",
             "speech": correctIncorrectMessage 
          },
          {
              "type": 2,
              "platform": "kik",
              "title": "Do you want to Try some more test?",
              "replies": [
                "Goback",
                "Exit"
            
             ]
             },
         {
             "type":0,
             "platform":"viber",
             "speech": correctIncorrectMessage 
          },
          {
              "type": 2,
              "platform": "viber",
              "title": "Do you want to Try some more test?",
              "replies": [
                "Goback",
                "Exit"
            
             ]
             },
         {
             "type":0,
             "platform":"skype",
             "speech": correctIncorrectMessage 
          },
          {
              "type": 2,
              "platform": "skype",
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
          "replies": 
          classdetails
          
     },
      {
          "type": 2,
          "platform": "slack",
           "title": "Choose Your Class",
          "replies": 
          classdetails
          
     },
      {
          "type": 2,
          "platform": "skype",
            "title": "Choose Your Class",
          "replies": 
          classdetails
          
     },
     {
          "type": 2,
          "platform": "viber",
             "title": "Choose Your Class",
          "replies": 
           classdetails
          
     },
     {
          "type": 2,
          "platform":"kik",
           "title": "Choose Your Class",
          "replies": 
        classdetails
          
     },
     {
          "type": 2,
          "platform": "telegram",
         "title": "Choose Your Class",
          "replies": 
         classdetails
          
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
          "replies": 
            subjectdetails
          
     },
      {
          "type": 2,
          "platform": "slack",
           "title": "Choose Your Subject",
          "replies": 
        subjectdetails
          
     },
      {
          "type": 2,
          "platform": "skype",
            "title": "Choose Your Subject",
          "replies": 
          subjectdetails
          
     },
     {
          "type": 2,
          "platform": "viber",
             "title": "Choose Your Subject",
          "replies": 
          subjectdetails
          
     },
     {
          "type": 2,
          "platform":"kik",
           "title": "Choose Your Subject",
          "replies": 
           subjectdetails
          
     },
     {
          "type": 2,
          "platform": "telegram",
         "title": "Choose Your Subject",
          "replies": 
         subjectdetails
          
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
def getchapterdetails(classnumber,subject,chapterdetails):
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
          "replies": 
            chapterdetails
          
     },
      {
          "type": 2,
          "platform": "slack",
           "title": "Choose Your Chapter",
          "replies": 
        chapterdetails
          
     },
      {
          "type": 2,
          "platform": "skype",
            "title": "Choose Your Chapter",
          "replies": 
          chapterdetails
          
     },
     {
          "type": 2,
          "platform": "viber",
             "title": "Choose Your Chapter",
          "replies": 
          chapterdetails
          
     },
     {
          "type": 2,
          "platform":"kik",
           "title": "Choose Your Chapter",
          "replies": 
           chapterdetails
          
     },
     {
          "type": 2,
          "platform": "telegram",
         "title": "Choose Your Chapter",
          "replies": 
         chapterdetails
          
     }


   ]
}
def gettestpaper(classnumber, subject, chapter,chaptermsg):
    print('inside response function')
    
	
    return {
    "contextOut": [
     {
	  "name": "t3" ,
          "parameters": {

	  "class": str(classnumber),
          "subject": subject,
	  "chapter": str(chapter)
                     
          },
          "lifespan": 0
     },
     {
	  "name": "t4"  ,
          "parameters": {

	  "class": str(classnumber),
          "subject": subject,
	  "chapter": str(chapter)
                 
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

def getAnswer(line):
    words3 = line.split("#")
    print('answer' + str(words3[6]))
    return int(words3[6])
def classList():
    classes = list();
    classes.append("9")
    classes.append("10")
    classes.append("11")
    classes.append("12")
    return classes
def subjectList():
    classsubject = dict()
    classsubject['7'] = "science"
    classsubject['8'] = "science"
    classsubject['9'] = "physics:chemistry:biology"
    classsubject['10'] = "physics:chemistry:biology"
    classsubject['11'] = "physics:chemistry:biology"
    classsubject['12'] = "physics:chemistry:biology"
    return classsubject
def getChapterList():
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
    return classsubjectchapter
def getChapterNameNumber():
    chaptername = dict()
    chaptername['chapter1'] ='1'
    chaptername['chapter2'] ='2'
    return chaptername
def log(msg):
    print (msg)
    sys.stdout.flush()
def getclass1(req):
    result = req.get("result")
    sessionID = req.get("sessionId")
    contexts = result.get("contexts")
    classes = list();
    classes = classList()

    #return getclassdetails(str(classes)[1:-1])
    #print(str(json.dumps(classes))[1:-1])
    return getclassdetails(classes)

def getsubject(req):
    print('get subject')
    result = req.get("result")
    sessionID = req.get("sessionId")
    contexts = result.get("contexts")
    classsubject = dict()
    classsubject = subjectList()
    classnumber ='8'
    try:
        print(result.get('parameters'))
        classnumber = result.get('parameters')['class']
        print( classnumber)
        print(json.dumps(classsubject[classnumber].split(":")))

        return getsubjectdetails(classnumber, classsubject[classnumber].split(":"))
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
    classsubjectchapter = getChapterList()


    classnumber ='8'
    subject= ''
    print(result.get('parameters'))
    result1=''
    try:
        classnumber = result.get('parameters')['class']
        subject = result.get('parameters')['subject']

        te = 'class' + classnumber + subject

        if int(classnumber) < 9:
            result1 = getchapterlessthan8(classnumber, subject, "Send Text Message: " + classsubjectchapter[te].split(":"))
            #print("Send Text Message: " + str(classsubjectchapter[te].split(":"))[1:-1])
        else:
            result1 = getchapterdetails(classnumber, subject, classsubjectchapter[te].split(":"))
            #print(str(classsubjectchapter[te].split(":"))[1:-1])
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)    
    return result1
def gettestpaper1(req):
    print('get testpaper')
    result = req.get("result")
    sessionID = req.get("sessionId")
    contexts = result.get("contexts")
    classnumber = result.get('parameters')['class']
    subject = result.get('parameters')['subject']
    chapter = result.get('parameters')['chapter']
    result2 =''
    try:
        result2 = gettestpaper(classnumber,subject,chapter,"Enter Test Number")
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2].tb_lineno)
    return result2
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def readLine(file_name,contextName):
    fp = open(file_name)
    for i, line in enumerate(fp):
        if i == string.replace(string.replace(contextName,"q",""),"Q",""):
            # 26th line
            return line
            #sentencetext
            #answer = words2[3]
            break
    fp.close()
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
