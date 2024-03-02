import discord
import requests
import argparse
import json
from datetime import datetime
import os
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
current_date = datetime.now().strftime('%Y%m%d')
# Set the filename using the current date
filename = f'{current_date}.json'

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

def chatlog(data):
    global filename
    # Get the current date in the format 'yyyymmdd'

    # Check if the file already exists
    if os.path.exists(filename):
        # If the file exists, read the existing data from the file
        with open(filename, 'r' , encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        # If the file does not exist, initialize with an empty list
        existing_data = []

    # Append the new data to the existing data
    existing_data.append(data)

    # Write the updated data back to the file
    with open(filename, 'w' , encoding='utf-8') as file:
        json.dump(existing_data, file)

# 發送 API 請求
def chatwithAI(chat_prompt):
    try:
        #向koboldAI的API發送要求
        API_ENDPOINT = 'http://127.0.0.1:5000/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json'
        }
        global Botsmemory
        MemoryInPrompt = "".join(Botsmemory)
        #AI人格的咒文
        print(AIPersonalPrompt+MemoryInPrompt+UserAsk+chat_prompt+ AIReplied)
        history = []
        user_message = AIPersonalPrompt+MemoryInPrompt+UserAsk+chat_prompt+ AIReplied
        history.append({"role": "user", "content": user_message})
        data = {
            "mode": "chat",
            "messages": history
        }
        #print(AIPersonalPrompt+MemoryInPrompt+UserAsk+chat_prompt+ AIReplied)
        response = requests.post(API_ENDPOINT, json=data, headers=headers, verify=False)
        if response.status_code == 200:
            # 提取回覆訊息
            reply = response.json()['choices'][0]['message']['content']
            print(f'KoboldAI 回覆：{reply}')
            finalreply=reply.split(UserAsk)[0].replace(AIReplied, "")
            #print(UserAsk)
            #print(finalreply)
            Botsmemory.append(UserAsk+chat_prompt+ AIReplied+finalreply)
            data_to_add = {"user_input": chat_prompt ,"AI_Output":finalreply}
            chatlog(data_to_add)
            #print(Botsmemory)
            #因為AI會產生一連串的回應，將第一次出現You:之前的訊息視為AI回應，並去除多餘的'AI:'
            return finalreply
        else:
            print(str(response))
            return '無法連接到 koboldAI API'
    except Exception as e:
        print(e)
        return '無法連接到 koboldAI API'


@client.event
#當有訊息時
async def on_message(message):
    substring_to_remove = "hey AI,"
    global Botsmemory
    print(message)
    #機器人忽視自己的訊息
    if message.author == client.user:
        return
    #只對含有'hey AI,'的訊息做AI回應，會在去除'hey AI,'後交給AI
    if 'hey AI,' in message.content :
        await message.channel.send(chatwithAI(message.content.replace(substring_to_remove, "")))
    if 'Personal change to:' in message.content :
        setting(message.content.replace('Personal change to:', ""))
        Botsmemory.clear()
        await message.channel.send("Now,I'm "+message.content.replace('Personal change to:', ""))
    if 'Clean AI memorys' in message.content :
        Botsmemory.clear()
        await message.channel.send("I clean my memorys.")

# 使用機器人的權杖啟動機器人
client.run(dcbottoken)
