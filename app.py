from flask import Flask,render_template,request
from json import load
import core as c
from json import loads
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
@cross_origin(origins='*',methods=["GET","POST"],expose_headers=c.headers)
def webui():
    with open("./config.json",'r',encoding="utf-8") as f:
      config = load(f)
      f.close()
    if request.method=="GET":
      return render_template('index.html', 
        title=config["title"],
        description=config["description"],
        icon_link=config["icon_link"],
        author=config["author"]
      )
    if request.method=="POST":
       if request.form.get('imaginable')=='on':
          igb:bool = 1
       else:
          igb = 0
       reply = c.getReply(
          event=request.form.get('event'),
          explain=request.form.get('explain'),
          imaginable=igb,
          other=request.form.get('other')
       )
      #  with open('./output.txt','r',encoding="utf-8") as f:
      #    reply=loads(f.read())
      #    f.close()
       print(reply)
       return render_template('index.html', 
        title=config["title"],
        description=config["description"],
        icon_link=config["icon_link"],
        author=config["author"],
        reply=1,
        commendCate=reply["commendCate"],
        name=reply["name"],
        location=reply["location"],
        process=reply["process"],
        gain=reply["gain"]
      )

