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
