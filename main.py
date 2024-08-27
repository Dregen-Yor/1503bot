import botpy
import yaml
from botpy import logging
import asyncio
from botpy.message import GroupMessage,C2CMessage
from ElectricityInquiry import query

_log = logging.get_logger("log")
with open("config.yaml") as f:
    config=yaml.safe_load(f)
class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")
    async def on_group_at_message_create(self, message:GroupMessage):
        res=''
        if '/queryEle' in message.content:
            res=f"221宿舍剩余电量：{query(config["account"],"S11-13",221)}\n 219宿舍剩余电量：{query(821563,"S11-13",219)}"
        else:
            res=f"收到了消息：{message.content}"
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
            content=f"我收到了你的消息：{message.content}"
        )
        _log.info(messageResult)


intents = botpy.Intents(public_messages=True) 
client=MyClient(intents=intents,is_sandbox=True)

client.run(appid=config["appid"],secret=config["secret"])