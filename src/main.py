import botpy
import yaml
from botpy import logging
import asyncio
from botpy.message import GroupMessage,C2CMessage
import openai
from openai import OpenAI
from typing import Any

from ElectricityInquiry import query

with open("config.yaml") as f:
    config=yaml.safe_load(f)

client = OpenAI(
    api_key = config["ARK_API_KEY"],
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
)
class MyClient(botpy.Client):
    async def check():
        res=f"221宿舍剩余电量：{query('S11',221)}\n 219宿舍剩余电量：{query('S11',219)}"
        await GroupMessage._api.post_group_message(
              msg_type=0, 
              content=res)
    async def on_ready(self):
        print("Bot is ready")
    async def on_group_at_message_create(self, message:GroupMessage):
        res=''
        if '/queryEle' in message.content:
            res=f"221宿舍剩余电量：{query('S11',221)}\n 219宿舍剩余电量：{query('S11',219)}"
        elif "王春明" in message.content:
            res="这人上课简直搞笑，第一节课上ppt就坏了瞎聊一整节，本来以为拿来ppt就好了结果后面讲课更无趣，废话一堆讲课无聊内容空洞令人昏昏欲睡，更搞笑的是有一天上课爆出“没关系，觉得简单的话不来也没事”，随后另一节课上又公然反悔，说过一句疑似为自己辩解的话“学物理的人有时候说话不太严谨”；另有金句“上课听不听课不重要，老师的作用是督促学生不要在宿舍里偷懒”云云，总而言之听此人上课堪比坐牢，就算自己在台下学别的也会被他在讲台上说话的催眠声线干扰学习效率，如果真如其言老师的作用是“督促学生学习”的话，我来跟你报个到证明我没睡懒觉，然后换个教室上自习行不行？"
        else:
            completion = client.chat.completions.create(
                model = "ep-20250224202742-lm4pp",  # your model endpoint ID
                messages = [
                    {"role": "system", "content": "你是一个群聊天机器人,你可以扮演奶龙,贝利亚等各种身份,默认情况下你是奶龙"},
                    {"role": "user", "content": message.content},
                ],
            )
            res=completion.choices[0].message.content
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0, 
              msg_id=message.id,
              content=res)
    async def on_c2c_message_create(self, message: C2CMessage):
        messageResult=await message._api.post_c2c_message(
            openid=message.author.user_openid, 
            msg_type=0, msg_id=message.id, 
            content=f"王春明闹谈，4了吗了，傻逼一个/se"
        )

def start():

    intents = botpy.Intents(public_messages=True) 
    client=MyClient(intents=intents,is_sandbox=True)
    client.run(appid=config["appid"],secret=config["secret"])

if __name__ == "__main__":
    start()
