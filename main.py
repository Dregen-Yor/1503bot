import botpy
import yaml
from botpy import logging
import asyncio
from botpy.message import GroupMessage,C2CMessage
from typing import Any
from ElectricityInquiry import query
import schedule

_log = logging.get_logger("log")
with open("config.yaml") as f:
    config=yaml.safe_load(f)
class MyClient(botpy.Client):
    async def check():
        res=f"221宿舍剩余电量：{query(config["account"],"S11-13",221)}\n 219宿舍剩余电量：{query(821563,"S11-13",219)}"
        _log.info(res)
        await GroupMessage._api.post_group_message(
              msg_type=0, 
              content=res)
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")
        schedule.every().day.at("21:30").do(self.check)
        schedule.every().day.at("23:46").do(self.check)
    async def on_group_at_message_create(self, message:GroupMessage):
        res=''
        if '/queryEle' in message.content:
            res=f"221宿舍剩余电量：{query(config["account"],"S11-13",221)}\n 219宿舍剩余电量：{query(821563,"S11-13",219)}"
        elif "王春明" in message.content:
            res="这人上课简直搞笑，第一节课上ppt就坏了瞎聊一整节，本来以为拿来ppt就好了结果后面讲课更无趣，废话一堆讲课无聊内容空洞令人昏昏欲睡，更搞笑的是有一天上课爆出“没关系，觉得简单的话不来也没事”，随后另一节课上又公然反悔，说过一句疑似为自己辩解的话“学物理的人有时候说话不太严谨”；另有金句“上课听不听课不重要，老师的作用是督促学生不要在宿舍里偷懒”云云，总而言之听此人上课堪比坐牢，就算自己在台下学别的也会被他在讲台上说话的催眠声线干扰学习效率，如果真如其言老师的作用是“督促学生学习”的话，我来跟你报个到证明我没睡懒觉，然后换个教室上自习行不行？"
        else:
            res=f"王春明闹谈，4了吗了，傻逼一个/se"
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0, 
              msg_id=message.id,
              content=res)
        _log.info(messageResult)
    async def on_c2c_message_create(self, message: C2CMessage):
        messageResult=await message._api.post_c2c_message(
            openid=message.author.user_openid, 
            msg_type=0, msg_id=message.id, 
            content=f"王春明闹谈，4了吗了，傻逼一个/se"
        )
        _log.info(messageResult)
    def run(self, *args: Any, **kwargs: Any) -> None:
        """
        机器人服务开始执行

        注意:
          这个函数必须是最后一个调用的函数，因为它是阻塞的。这意味着事件的注册或在此函数调用之后调用的任何内容在它返回之前不会执行。
          如果想获取协程对象，可以使用`start`方法执行服务, 如:
        ```
        async with Client as c:
            c.start()
        ```
        """
        async def runner():
            async with self:
                print("no")
                await self.start(*args, **kwargs)

        try:
            self.loop.run_until_complete(runner())
        except KeyboardInterrupt:
            return

def start():

    intents = botpy.Intents(public_messages=True) 
    client=MyClient(intents=intents,is_sandbox=True)
    client.run(appid=config["appid"],secret=config["secret"])

async def p():
    for i in range(10):
        print(i)
if __name__ == "__main__":
    start()
