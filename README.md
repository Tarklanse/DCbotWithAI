# DCbotWithAI
A simple discord Bot using API to connect KoboldAI's API
簡單能夠和KoboldAI串接的DC機器人

這個機器人本身不包含KoboldAI或其他主持語言模組的功能，請需要自行尋找koboldAI的安裝與使用方式
這個機器人不具記憶能力，如果需要記憶能力需自行編寫字典去存咒文

目前我寫了兩個版本，分別是給英語系Model與繁體中文系Model用的，需自行申請建立Discord APP並修改程式內client.run中的---為申請的機器人權杖

mydcbot_koboldai.py
用於串接英語系的語言模組，有最簡單的人格，KoboldAI可用的Chat Model與其他可能有能力對話的語言模組

mydcbot_koboldai_forbloom1b1.py
用於串接繁體中文系的語言模組，我主要是為了ckip-joint/bloom-1b1-zh去寫AI人格的，不過用在其他繁體中文Model應該也是能通用

