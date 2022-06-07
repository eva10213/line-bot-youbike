import requests
import json

url= "https://api.kcg.gov.tw/api/service/Get/b4dd9c40-9027-4125-8666-06bef1756092"
html = requests.get(url)
html.encoding = 'utf-8'
# print(html.text)
dic = json.loads(html.text)
print(dic.keys())
