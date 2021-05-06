# -*- coding: utf-8 -*-
"""
Created on Tue May  4 00:12:38 2021

@author: LENOVO
"""

file= open('file.txt','r',encoding='utf8')
          
i=1 #מזהה יחודי
list=[]
dict_users =dict() #מילון של מספרי הטלפון\שם עם מזהה יחודי
dict_message=dict() #מילון של תאריך+מזהה יחודי+טקסט
metadata = dict() #מילון של פרטי הקבוצה
for line in file:
    line.rstrip()
    if "ההודעות והשיחות מוצפנות מקצה-לקצה" in line or "הוסיף/ה" in line:
        continue
    if "נוצרה על ידי" in line: #שלב שלישי
        name=line.split('"')
        metadata["chat_name"]=name[1]
        dateCreator = line.split("-",1)
        metadata["creation_date"]=dateCreator[0]
        creator=line.split("נוצרה על ידי")
        metadata["creator"]=creator[1]
        continue
    try: #בדיקה האם זו הודעה חדשה או המשך של קודמת
        x=line.split('-',1) #פיצול תאריך
        y=x[1].split(':',1) #פיצול טלפון\שם
        if y[0] not in dict_users: #האם זו הודעה ראשונה של המשתמש
            dict_message=dict()
            dict_users[y[0]]=i
            dict_message["datetime"]=x[0]
            dict_message["Id"]=i
            dict_message["text"]=y[1]
            i+=1
            list.append(dict_message)
        else:
            dict_message=dict()
            dict_message["datetime"]=x[0]
            dict_message["Id"] = dict_users[y[0]]
            dict_message["text"]=y[1]
            list.append(dict_message)
    except:
        dict_message["text"]=dict_message["text"]+","+line

metadata['num_of_participante']= len(dict_users)
final_dictionary = {'message':list,'metadata':metadata} #שלב 4

#שלב 5
import json
json_file=json.dumps(final_dictionary, ensure_ascii=False, indent=5)
with open(metadata["chat_name"]+'.txt','w',encoding='utf-8') as f:
    f.write(json_file)


