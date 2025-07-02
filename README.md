# DCbotWithAI

A simple discord Bot using API to connect KoboldAI's API

簡單能夠和KoboldAI串接的DC機器人

這個機器人本身不包含KoboldAI或其他主持語言模組的功能，請自行尋找koboldAI的安裝與使用方式

這個機器人會將最近的20次對話記憶下來，並儲存於記憶體中，重新啟動會清除，跟他說Clean AI memorys也會將這些記憶清除

在目前的版本中，我將AI人格放在AIPersonals.json中，程式會需要讀取這個json檔取得人格的prompt

主要程式
mydcbot_koboldai.py

使用方式:
python mydcbot_koboldai.py 人格名稱 機器人權杖

如果人格不存在於AIPersonals.json中會自動讀DefualtAI

在Discord聊天中，AI只會響應以下三種訊息:

1."hey AI,":AI會回應這個訊息

2."Personal change to:"機器人會依據輸入去切會json中對應的人格，如果找不到一樣會載入DefualtAI

3."Clean AI memorys":清除記憶

------
2024/03/02 新增

mydcbot_oobawebui.py

可與oobabooga text-generation-webui的api串接

使用方式:

python mydcbot_oobawebui.py 人格名稱 機器人權杖

整體設計與mydcbot_koboldai一致
新增記錄使用者與AI對話紀錄的模塊，會記錄使用者的輸入與AI對應的回傳  

------
2025/07/02 更新

新增mydcbot_llamacpp_server.py

使用方式:
python mydcbot_llamacpp_server.py

使用前需要:  
1.手動更新12行中的dcbottoken=""為自己的機器人權杖  
2.須更新12行中實際以llama.cpp server主持的API接口  

在這個程式移除了之前加入的儲存對話紀錄的機制，以確保不會因為超多人使用而導致對話紀錄臃腫  
移除了修改人格的指令(統一使用預設人格)以防止多伺服器使用時在非預期的情況切換人格  


