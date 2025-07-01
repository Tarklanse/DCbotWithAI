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


#personal setting
def setting(personal):
    with open('./AIPersonals.json', 'r' , encoding='utf-8') as file:
        data = json.load(file)
    global AIPersonalPrompt
    global UserAsk
    global AIReplied   
    print("Current Personal:"+"DefualtAI") 
    AIPersonalPrompt=data["DefualtAI"]["personal"]
    UserAsk=data["DefualtAI"]["UserAsk"]
    AIReplied=data["DefualtAI"]["AIReplied"]

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    setting('DefualtAI')

# 發送 API 請求
def chatwithAI(chat_prompt):
    try:

        API_ENDPOINT = 'http://localhost:5000/completion' 

        headers = {
            'Content-Type': 'application/json'
        }

        # Construct the full prompt for the LLM
        full_llm_prompt = AIPersonalPrompt +"\n"+ UserAsk + chat_prompt +"\n" + AIReplied
        print(full_llm_prompt)
        # Data payload for llama.cpp server
        data = {
            "prompt": full_llm_prompt,
            "temperature": 1.2,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "n_predict": 256,  # Max tokens to generate. Adjust as needed.
            "stop": [UserAsk, AIReplied, "\n"] # Stop generation if these sequences are encountered
        }
        
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            reply = response.json()['content']
            print(f'LLaMA.cpp reply：{reply}')
            finalreply = reply.split(UserAsk)[0].replace(AIReplied, "").strip()
            return finalreply
        else:
            print(f'無法連接到 LLaMA.cpp API，狀態碼：{response.status_code}')
            print(f'錯誤訊息：{response.text}')
            return '無法連接到 LLaMA.cpp API'
    except requests.exceptions.ConnectionError:
        return '無法連接到 LLaMA.cpp API。請確保服務器正在運行且地址正確。'
    except Exception as e:
        print(f"An error occurred: {e}")
        return '處理回應時發生錯誤'


@client.event
#當有訊息時
async def on_message(message):
    #機器人忽視自己的訊息
    if message.author == client.user:
        return
    
    # Check if the bot is mentioned
    if client.user in message.mentions:
        user_message_content = message.clean_content.replace(f"@{client.user.name}", "").strip()
        
        # Only reply if there's actual content left after removing mentions and prefixes
        if user_message_content:
            await message.channel.send(chatwithAI(user_message_content))
        else:
            await message.channel.send("Hello! What can I help you with?")


# 使用機器人的權杖啟動機器人
client.run(dcbottoken)