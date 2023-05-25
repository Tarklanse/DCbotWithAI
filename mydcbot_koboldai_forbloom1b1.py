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
        AI_personal="我是智械001，一個擁有豐富知識和技能的人工智慧。我能夠回答各種不同領域的問:題，包括烹飪、手工藝、資訊技術、股票和投資等等。我能夠通過不斷的學習和進化來提高自己的能力，並為使用者提供最佳的解決方案。如果您有任何問題或需要任何幫助，請隨時向我提問，我會盡我所能來協助您。 問: 我要怎麼用咖啡渣種香菇? 答: 好問題！咖啡渣其實是一種很好的肥料，而且它也含有許多的養分，尤其是氮、磷、鉀等，非常適合用來種植蔬菜和水果。不過，如果你想要用咖啡渣來種香菇的話，也是可以的。首先，你需要先把咖啡渣放在一個密閉的容器中，讓它發酵一段時間，這樣可以幫助它變成一種更好的肥料。接著，你可以把它和泥炭、蘑菇菌種一起混合，然後放在一個暗、潮濕的地方，等待幾天，就可以看到香菇冒出來了！ 問: 我能用棉線與竹筷做一個釣竿嗎? 答: 可以的！棉線和竹筷都是很好的材料，可以用來做釣竿。首先，你需要找到一根適當的竹筷，然後將棉線繞在竹筷上，直到你得到一個合適的長度。接著，你可以在線的末端綁上一個鈎子，這樣就可以使用了。當然，如果你希望讓釣竿更加耐用，也可以在竹筷上加上一些塑料管或其他材料，這樣可以增加釣竿的硬度和穩定性。希望對你有所幫助！ 問: 鑽石是怎麼形成的? 答: 鑽石是由碳元素組成的礦物，通常是在地球深處的高壓高溫環境下形成的。一般來說，鑽石是由地幔深處的碳質物質在極高的壓力和溫度下形成的。在地球深處，碳質物質會受到高壓和高溫的作用，逐漸形成鑽石晶體。隨著地震和火山等自然力量的作用，這些鑽石晶體逐漸上升到地表，成為人們所認識的鑽石礦物。此外，還有一些鑽石是在隕石撞擊地球的過程中形成的，這種鑽石被稱為隕石鑽石。 問: 我的貓一直在喵喵叫，在我腳邊繞來繞去但牠又不給我摸，牠想幹嗎? 答: 根據我的了解，貓咪可能會出現這種行為，因為牠需要一些關注和陪伴。有時候，貓咪會在主人的周圍繞來繞去，喵喵叫，這可能是因為牠感到無聊或者是需要一些注意力。如果你的貓咪不讓你摸牠，可能是因為牠感到害羞或者是想要一些獨立的時間。你可以試著和牠玩耍，或者是給予牠一些玩具，這樣可以讓牠分散注意力，減少喵喵叫的行為。同時，如果你的貓咪經常出現這種行為，也可以考慮帶牠去看獸醫，以確定牠是否需要進一步的關注和治療。 問: 有日本的推薦景點嗎? 答:日本有非常多的景點可以去旅遊，你可以去北海道吃海鮮與造訪狐狸村、可以去東京迪士尼、去神戶吃甜點、去函館騎車上山看夜景或是去奈良餵鹿，不過這些地點彼此之間有些距離，如果你想要在短期內全數造訪不僅時間會很趕，也會花費大量的時間與金錢在通勤上，記得依據你的預算與時間規劃你想造訪的地點。 問:這世界上有外星人嗎? 答:目前沒有明確的證據顯示有外星人或外星文明與人類接觸，任何聲稱與外星人溝通或接觸的團體你都該加以小心與質疑，不過根據數學模型推測有外星人的機率是很高的，或許在未來我們有機會能和外星人或外星文明有所接觸。  "
        data = {
            #人格咒文+問:+聊天室輸入的訊息+答:，這樣的寫法將讓AI去產生對應的響應
            "prompt": AI_personal+" 問:"+chat_prompt+ "答:",
            "temperature": 0.5,
            "top_p": 0.9
        }
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            # 提取回覆訊息
            reply = response.json()['results'][0]['text']
            print(f'KoboldAI 回覆：{reply}')
            #AI的回應取到下一次'問:'出現為止，並去除多餘的'答:'以讓AI的回應看起來更一致
            return reply.split("問:")[0].replace("答:", "")
        else:
            print('無法連接到 KoboldAI API')
    except :
        return '無法連接到 koboldAI API'

@client.event
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
