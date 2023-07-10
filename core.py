# -*- coding:utf-8 -*-
import requests as r
from json import dumps,loads
from json.decoder import JSONDecodeError
import os
headers = {"Content-Type": "application/json"}
MAX_DEPTH = 2

# with open('secret.txt','r') as f:
#     secret = f.readline()
#     headers["Authorization"] = "Bearer " + secret[:-1]
#     f.close()
headers["Authorization"] = "Bearer " + os.getenv('SECRET_KEY', 'dev')
api_url = "https://p0.kamiya.dev/api"
def apiLink(path:str) -> str:
    return api_url+path

def isLogin() -> bool:
    response = r.get(apiLink("/session/getDetails"),headers=headers)
    print(response.json())
    if(response.json()["status"]==200):
        return True
    else:
        return False

def gen(event:str,explain:str,imaginable:bool,other:str="") -> r.Response:
    partten = '我是一个高中生，现在我要为{event}的事件书写中学生综合素质评价记录管理系统的记录，活动过程大致为\n“\n{explain}\n”\n请合理扩写修缮，**以可用的json形式**（仅仅给出**严格**按按格式加工后的内容！！！**不要有任何多余描述！！！**）给出提交至平台的活动过程，格式为：“{{\"commendCate\":\"\",\"name\":\"\",\"location\":\"\",\"process\":\"\",\"gain\":\"\"}}”数据解释：\ncommendCate 推荐指标（思想品德、学业水平、身心健康、艺术素养、劳动素养、社会实践任选其一）\nname 名称（概括性的描述活动，15字以内）\nlocation 地点（若不能给出，请猜测合理地点）\nprocess 比较详细的活动过程{imaginable}（150-200字，**分段**）(换行使用\"\\n\")\ngain 取得成果（收获）\n'
    # 使用大括号 {} 来转义大括号
    if(imaginable):
        partten = partten.format(event=event,explain=explain,imaginable="，可合理杜撰")
    else:
        partten = partten.format(event=event,explain=explain,imaginable="")
    if(str!=""):
        partten = partten + "其余要求：\n" + other
    # print(partten)
    post_data = {}
    post_data["content"] = partten
    # print(partten)
    reply = r.post(apiLink("/openai/chatgpt/conversation"),data=dumps(post_data),headers=headers)
    # print(post_data)
    return reply

# r1 = gen(
#     event="参加大运会志愿活动",
#     explain="今天参加了大运会的志愿者活动，主要工作有给运动员搬运行李和拍摄纪录片，我获得了学习的热情和合作的魅力",
#     imaginable=True,
#     other="提到我在搬运行李时受了伤"
# )

def dataProcess(data:list,depth:int=1,failed_text:str=""):
    assert data
    stat:bool = 0
    for item in data:
        # print(item,end="")
        if item == '\n':
            continue
        if '"id":"kamiyaInfo"' in item:
            stat = 1
            origin = loads(item[item.find('{"id":'):])
            bot_reply:str = origin["fullContent"]
            cid = origin["conversationId"]
            # 获得元数据
            bot_reply = '{{{'+bot_reply.replace("\t", "").replace(" ", "").replace("\n","").replace("'",'"')+'}}}'
            origin_reply = bot_reply
            # 处理空格
            if(depth<=MAX_DEPTH):
                bot_reply = failed_text+bot_reply
            bot_reply = bot_reply[bot_reply.rfind('{"'):bot_reply.find('"}')+2]
            # 去掉多余括号
            try:
                print("[LOG]:::"+bot_reply)
                bot_reply = loads(bot_reply,strict=False)
                # 尝试编码
            except JSONDecodeError:
                # with open('output.txt','w',encoding="utf-8") as f:
                #     f.write(bot_reply)
                #     f.close()
                if(depth==MAX_DEPTH):
                    '''最后一层迭代'''
                    print("error,the problem may be generated text is too long,plz add some limits to ai.")
                    return bot_reply
                else:
                    print("unfinished,generating!")
                    data={
                        "content":"继续，请在这次回答中说完,不要道歉，仅仅给出回答！！！",
                        "conversationId":cid
                    }
                    c_reply = r.post(apiLink("/openai/chatgpt/conversation"),data=dumps(data),headers=headers)
                    dataProcess(c_reply.text.splitlines(),depth+1,origin_reply)
                    return None
    if(not(stat)):
       raise Exception
    else:
        return bot_reply
    

# with open('output.txt','r',encoding="utf-8") as f:
#     te = dataProcess(f.readlines())
#     f.close()

def getReply(event:str,explain:str,imaginable:bool,other:str=""):
    return dataProcess(gen(
            event=event,
            explain=explain,
            imaginable=imaginable,
            other=other
        ).text.splitlines())

if __name__=="__main__":
    assert isLogin()
    print(dataProcess(gen(
        event="给社区老人过集体生日",
        explain="活动过程大致为制作贺卡，送祝福，表演才艺，合照，吃蛋糕。我收获了陪伴的意义，看到了老人需要被关怀等",
        imaginable=True
    ).text.splitlines()))
