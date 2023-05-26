import discord
import requests
import argparse
import json
from collections import deque

# 建立機器人實例
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

dcbottoken=""

AIPersonalPrompt=""
UserAsk=""
AIReplied=""

#bot have twenty memory
Botsmemory= deque(maxlen=20)

parser = argparse.ArgumentParser()
parser.add_argument("AIPersonalName", help="AIPersonalName")
parser.add_argument("BotToken", help="BotToken")
args = parser.parse_args()

dcbottoken=args.BotToken

#personal setting
def setting(personal):
    with open('./AIPersonals.json', 'r' , encoding='utf-8') as file:
        data = json.load(file)
    global AIPersonalPrompt
    global UserAsk
    global AIReplied    
    try:
        print("Current Personal:"+personal)
        AIPersonalPrompt=data[personal]["personal"]
        UserAsk=data[personal]["UserAsk"]
        AIReplied=data[personal]["AIReplied"]
    except:
        print("Current Personal:"+"DefualtAI")
        AIPersonalPrompt=data["DefualtAI"]["personal"]
        UserAsk=data["DefualtAI"]["UserAsk"]
        AIReplied=data["DefualtAI"]["AIReplied"]

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    setting(str(args.AIPersonalName))

# 發送 API 請求
def chatwithAI(chat_prompt):
    try:
        #向koboldAI的API發送要求
        API_ENDPOINT = 'http://localhost:5000/api/v1/generate'
        headers = {
            'Content-Type': 'application/json'
        }
        global Botsmemory
        MemoryInPrompt = "".join(Botsmemory)
        #AI人格的咒文
        data = {
            "prompt": AIPersonalPrompt+MemoryInPrompt+UserAsk+chat_prompt+ AIReplied,
            "temperature": 0.5,
            "top_p": 0.9,
            "repetition_penalty":1.2
        }
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            # 提取回覆訊息
            reply = response.json()['results'][0]['text']
            print(f'KoboldAI 回覆：{reply}')
            finalreply=reply.split(UserAsk)[0].replace(AIReplied, "")
            Botsmemory.append(UserAsk+chat_prompt+ AIReplied+finalreply)
            #因為AI會產生一連串的回應，將第一次出現You:之前的訊息視為AI回應，並去除多餘的'AI:'
            return finalreply
        else:
            print('無法連接到 KoboldAI API')
    except :
        return '無法連接到 koboldAI API'


@client.event
#當有訊息時
async def on_message(message):
    substring_to_remove = "hey AI,"
    #機器人忽視自己的訊息
    if message.author == client.user:
        return
    #只對含有'hey AI,'的訊息做AI回應，會在去除'hey AI,'後交給AI
    if 'hey AI,' in message.content :
        await message.channel.send(chatwithAI(message.content.replace(substring_to_remove, "")))
    if 'Personal change to:' in message.content :
        setting(message.content.replace('Personal change to:', ""))
        await message.channel.send("Now,I'm "+message.content.replace('Personal change to:', ""))
    if 'Clean AI memorys' in message.content :
        global Botsmemory
        Botsmemory.clear()
        await message.channel.send("I clean my memorys."))

# 使用機器人的權杖啟動機器人
client.run(dcbottoken)
