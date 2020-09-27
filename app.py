#模組
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageTemplateAction, ButtonsTemplate, CarouselTemplate, CarouselColumn)
import requests
import json



#設定
url= "https://api.kcg.gov.tw/api/service/Get/b4dd9c40-9027-4125-8666-06bef1756092"
html = requests.get(url)
html.encoding = 'utf-8'
dic = json.loads(html.text)


data_cut2 = ['前鎮區','鼓山區','苓雅區','前鎮','鼓山','苓雅','楠梓區','楠梓']
data_cut3 = ['左營區','三民區','鳳山區','左營','三民','鳳山']
#主程式    
def bike_list_data(dictt):
    a = dictt['sarea']
    b = dictt['sna']
    c = b[11:]
    lat = dictt['lat']
    lng = dictt['lng']    
    link = 'https://www.google.com/maps/search/?api=1&query='+lat+','+lng

    time = dictt['mday']
    times = time[0:3+1]+'-'+time[4:7+1]+'-'+time[8:9+1]+':'+time[10:11+1]
    msg1 = a+' '+c+'\n'+dictt['ar']+'\n可借車輛:'+dictt['sbi']+'\n'+'可停車位:'+dictt['bemp']+'\n更新時間:\n'+times+'\n'+link+'\n\n'
    return msg1

def bike_data_cut1(m):
    msg1 = ''
    datas = dic['data']['retVal']
    datas_box = []       
    sum=0
    for i in datas:
        a = i['sarea']
        x = a[:2]
        if m.strip() ==a or m.strip()==x:
            datas_box.append(i)

    number = len(datas_box)
    chat_box1 = number//2

    if number >=35:
        for y in datas_box[0:35]:
            sum+=1
            msg1+=bike_list_data(y)
        msg1+=str(m)+' '+'第一筆資料為'+str(sum)+'筆'

    if  number!=0 and number<35:
        for k in datas_box:
            sum+=1
            msg1+=bike_list_data(k)
        msg1+=str(m)+' '+'總共有'+str(sum)+'筆資料'
    if number==0:
        msg1+='目前查無'+'" '+str(m)+' "'+'的資料'


    return msg1


def bike_data_cut2(n):
    msg1 = ''
    datas = dic['data']['retVal']
    datas_box = []
        
    sum = 0
    for i in datas:
        a = i['sarea']
        x = a[:2]
        if n.strip() == a or n.strip() == x :
            datas_box.append(i)

    number = len(datas_box)
    if number>61:
        for k in datas_box[35:69]:
            sum+=1
            msg1+=bike_list_data(k)
        msg1+=str(n)+' '+'第二筆資料為'+str(sum)+'筆\n\n'+str(n)+' '+'總共有'+str(number)+'筆資料'
    
    elif 61>=number > 35 :
        for z in datas_box[35:number+1]:
            sum+=1
            msg1+=bike_list_data(z)
        msg1+=str(n)+' '+'第二筆資料為'+str(sum)+'筆\n\n'+str(n)+' '+'總共有'+str(number)+'筆資料'
    if sum == 0 and number!= 0:
        msg1+= str(n)+' '+'的全部資料已羅列在上'
    if number == 0:
        msg1+='請輸入正確的關鍵詞'
    

    return msg1

def bike_data_cut3(m):
    msg1 = ''
    datas = dic['data']['retVal']
    datas_box = []       
    sum=0
    for i in datas:
        a = i['sarea']
        x = a[:2]
        if m.strip() ==a or m.strip()==x:
            datas_box.append(i)

    number = len(datas_box)
    chat_box1 = number//2
    chat_box2 = number - chat_box1
    if number>61 :
        for y in datas_box[69:]:
            sum+=1
            msg1+=bike_list_data(y)
        msg1+=str(m)+' '+'第三筆資料為'+str(sum)+'筆\n\n'+str(m)+'總共有'+' '+str(number)+'筆資料'

    if number==0:
        msg1+='目前查無'+'" '+str(m)+' "'+'的資料'


    return msg1




app=Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('fBr9B2dlVvYcJ01pGFlyTxHuhlKMHyP5/EnLOuhr7MYLOQFpknW4s7psMtFsq6xcB+TFepCy0nbEvSdp4gVWZePOpmLoG0YdnSZsQdO1gUDNdi9kQic482MHER7SUvQWxy1yzkSaVs3cgenLlkHnbwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7db29677cf6da3535cec4cef864e65d7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# Messaging settings 訊息由 LineBot發送訊息到其他使用者的設定
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    text = event.message.text
    if event.message.text=='你好':
        line_bot_api.reply_message(event.reply_token,
        TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='高雄分區選擇',text='請選擇你所在高雄的分區',
            actions=[
                MessageTemplateAction(label='北高雄',text='北高雄'),
                MessageTemplateAction(label='南高雄',text='南高雄'),
                MessageTemplateAction(label='鳳山',text='鳳山'),
                MessageTemplateAction(label='岡山',text='岡山')
            ])))
    
    elif event.message.text=='北高雄':
        line_bot_api.reply_message(event.reply_token,
        TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='左營區',text='左營區'),
            MessageTemplateAction(label='三民區',text='三民區'),
            MessageTemplateAction(label='鼓山區',text='鼓山區'),
            MessageTemplateAction(label='楠梓區',text='楠梓區')
            ])))
    elif event.message.text=='南高雄':
        line_bot_api.reply_message(event.reply_token,
        [TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='新興區',text='新興區'),
            MessageTemplateAction(label='前鎮區',text='前鎮區'),
            MessageTemplateAction(label='前金區',text='前金區'),
            MessageTemplateAction(label='苓雅區',text='苓雅區')
            ])),
        TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='鹽埕區',text='鹽埕區'),
            MessageTemplateAction(label='旗津區',text='旗津區'),
            MessageTemplateAction(label='小港區',text='小港區')]))])
    elif event.message.text=='鳳山':
        line_bot_api.reply_message(event.reply_token,
        [TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='鳳山區',text='鳳山區'),
            MessageTemplateAction(label='大寮區',text='大寮區'),
            MessageTemplateAction(label='大社區',text='大社區'),
            MessageTemplateAction(label='鳥松區',text='鳥松區')
            ])),
        TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='林園區',text='林園區'),
            MessageTemplateAction(label='大樹區',text='大樹區'),
            MessageTemplateAction(label='仁武區',text='仁武區')
            ]))]) 

    elif event.message.text=='岡山':
        line_bot_api.reply_message(event.reply_token,
        [TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='橋頭區',text='橋頭區'),
            MessageTemplateAction(label='燕巢區',text='燕巢區'),
            MessageTemplateAction(label='茄萣區',text='茄萣區'),
            MessageTemplateAction(label='梓官區',text='梓官區')
            ])),
        TemplateSendMessage(alt_text='Buttons template',
        template=ButtonsTemplate(title='Youbike查詢',text='選擇你要查詢的地區',
        actions=[
            MessageTemplateAction(label='路竹區',text='路竹區'),
            MessageTemplateAction(label='永安區',text='永安區'),
            MessageTemplateAction(label='彌陀區',text='彌陀區')
            ]))])

    elif event.message.text in (data_cut3):
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=bike_data_cut1(text)),TextSendMessage(text=bike_data_cut2(text)),TextSendMessage(text=bike_data_cut3(text))])
    elif event.message.text in (data_cut2):
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=bike_data_cut1(text)),TextSendMessage(text=bike_data_cut2(text))])
    else :
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=bike_data_cut1(text)))


if __name__=='__main__':
    app.run()







