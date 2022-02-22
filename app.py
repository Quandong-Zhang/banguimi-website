import sqlite3
import json
from flask import Flask, render_template, request ,abort
#from danmu import *
import video_toos

#from sql import *

USE_NEW_PLAYER=True
SUCCESS_STREAM="""{
  "code": 0,
  "data": {
    "_id": "6210b90b0999d44a888582ac",
    "player": "1-1",
    "author": "DIYgod",
    "time": 3.48818,
    "text": "2333",
    "color": 16777215,
    "type": 0,
    "ip": "58.176.69.72",
    "referer": "http://101.43.140.188/",
    "date": 1645263115806,
    "__v": 0
  }
}"""

conn = sqlite3.connect("bgm.db",check_same_thread=False)
cursor = conn.cursor()

dmconn = sqlite3.connect("oldplayer.db",check_same_thread=False)

ndmconn = sqlite3.connect("dplayer.db",check_same_thread=False)

app=Flask(__name__)

def get_dict(text,color,size,position,time):
    dic={"text":text,"color":color,"size":size,"position":position,"time":time}
    return dic

def getL(sqlobj):
    L0=[]
    g=0
    while g < len(sqlobj):
        L0.append(str(get_dict(sqlobj[g][0],sqlobj[g][1],sqlobj[g][2],sqlobj[g][3],sqlobj[g][4])))
        g = g+1
    return L0


def add(jstring,d,p):
    #print(jstring,"\n\n\n\n\n\n\n")
    jstring=json.loads(jstring)
    dmcursor = dmconn.cursor()
    dmcursor.execute('insert into dm (text,color,size,position,time,d,p) values (?,?,?,?,?,?,?)',(jstring['text'],jstring['color'],jstring['size'],jstring['position'],jstring['time'],d,p))
    dmcursor.close()
    dmconn.commit()

def add_new(jstring):
    #print(jstring,"\n\n\n\n\n\n\n")
    #jstring=json.loads(jstring)
    ndmcursor = ndmconn.cursor()
    ndmcursor.execute('insert into dm (author,color,id,text,time,type) values (?,?,?,?,?,?)',(jstring['author'],jstring['color'],jstring['id'],jstring['text'],jstring['time'],jstring['type']))
    ndmcursor.close()
    ndmconn.commit()

def get_new_dict(author,color,id,text,time,typ):
    L1=[time,typ,color,author,text]
    return L1

def get_return(sqlobj):
    L0=[]
    g=0
    while g < len(sqlobj):
        L0.append(get_new_dict(sqlobj[g][0],sqlobj[g][1],sqlobj[g][2],sqlobj[g][3],sqlobj[g][4],sqlobj[g][5]))
        g = g+1
    return L0
    #return str(resut)
    

@app.route('/',methods=['GET'])
def index():
    cursor.execute("select * from bgmList")
    libs = cursor.fetchall()
    libs.reverse()
    return render_template("index.html", libs=libs)


@app.route('/list',methods=['GET'])
def ilist():
    d = request.args.get("id", type=int)
    cursor.execute("select * from bgmList where id = ?", (d,))
    mtitle = cursor.fetchone()[1]
    cursor.execute("select * from pList where id = ?", (d,))
    libs = cursor.fetchall()
    if len(libs) == 0:
        abort(404)
    return render_template("detail.html", libs=libs,mtitle=mtitle)

@app.route('/play',methods=['GET'])
def play():
    idm = request.args.get("id", type=int)
    p = request.args.get("p", type=int)
    cursor.execute("select * from bgmList where id = ?", (idm,))
    main_menu_list = cursor.fetchone()
    allp = main_menu_list[4]
    mtitle = main_menu_list[1]
    img = main_menu_list[3]
    if p == allp:
        nextp=False
    else:
        nextp=True
    cursor.execute("select * from pList where id = ? and p = ?", (idm,p,))
    libs = cursor.fetchone()
    if libs is None:
        abort(404)
    if USE_NEW_PLAYER:
        return render_template("new_player.html",libs = libs ,nextp=nextp ,allp=allp,mtitle=mtitle,img=img)
    else:
        return render_template("player.html",libs = libs)

@app.route('/danmu/send',methods=['POST'])
def send():
    d = request.args.get("id", type=int)
    p = request.args.get("p", type=int)
    #request.form
    add(request.form.get('danmu'), d, p)
    return "success"

@app.route('/danmu/get',methods=['GET'])
def get():
    d = request.args.get("id", type=int)
    p = request.args.get("p", type=int)
    dmcusor=dmconn.cursor()
    dmcusor.execute("select * from dm where d = ? and p = ?", (d,p,))
    sqlobj=dmcusor.fetchall()
    dmcusor.close()
    dick_list = getL(sqlobj)
    return json.dumps(dick_list)

@app.route('/danmu/send/v3/',methods=['GET','POST'])
def v3():
    if request.method == "GET":
        d = request.args.get("id", type=str)
        ndmcusor=ndmconn.cursor()
        ndmcusor.execute("select * from dm where id = ?", (d,))
        sqlobj=ndmcusor.fetchall()
        res=get_return(sqlobj)
        jr={"code":0,"data":res}
        return json.dumps(jr)
    else:
        dic=json.loads(request.stream.read())
        #print(type(dic))
        add_new(dic)
        return SUCCESS_STREAM

if __name__=='__main__':
    app.run(debug=False ,host="0.0.0.0",port=80)
