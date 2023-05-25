import discord
import requests

# 建立機器人實例
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

# 發送 API 請求
def chatwithAI(chat_prompt):
    try:
        #向koboldAI的API發送要求
        API_ENDPOINT = 'http://localhost:5000/api/v1/generate'
        headers = {
            'Content-Type': 'application/json'
        }
        #AI人格的咒文
        AI_personal="A very powerful AI can replied any question."
        data = {
            "prompt": AI_personal+" You:"+chat_prompt+ "AI:",
            "temperature": 0.5,
            "top_p": 0.9
        }
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            # 提取回覆訊息
            reply = response.json()['results'][0]['text']
            print(f'KoboldAI 回覆：{reply}')
            #因為AI會產生一連串的回應，將第一次出現You:之前的訊息視為AI回應，並去除多餘的'AI:'
            return reply.split("You:")[0].replace("AI:", "")
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

# 使用機器人的權杖啟動機器人
client.run('---')
