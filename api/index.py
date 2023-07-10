from flask import Flask,render_template,request
import core as c
from flask_cors import cross_origin

app = Flask(__name__, template_folder='../templates',static_folder='../static')

config = {
  "title": "素质（平台）爆炸法术——Nick Chen",
  "description": "初级魔法师可以利用此魔法应对邪恶的”成都市中学生综合素质评价记录管理系统“",
  "online_url": "",
  "icon_link": "https://s2.loli.net/2023/07/09/5jSIsKpmHM8fEYx.png",
  "author": "Nick Chen"
}


@app.route('/', methods=["GET","POST"])
@cross_origin(origins='*',methods=["GET","POST"],expose_headers=c.headers)
def webui():
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

if __name__ == '__main__':
    app.run()
