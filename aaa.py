#模組
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageTemplateAction, ButtonsTemplate, CarouselTemplate, CarouselColumn)
import requests
import json



#設定
url= "https://api.kcg.gov.tw/api/service/Get/b4dd9c40-9027-4125-8666-06bef1756092"
html = ''

while str(html) != '<Response [200]>':
    html = requests.get(url)
    html.encoding = 'utf-8'

dic = json.loads(html.text)
box = {}
dd = dic['data']['retVal']
for i in dd:
    area = i['sarea']
    if area in box:
        num = box.get(area)
        box[area] = num+1
    else:
        box[area] = 1
print(box)