import requests
import json
import urllib.parse
import csv
import time
from bs4 import BeautifulSoup

def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec;

tStart = time.time()#計時開始

user_input=input("請輸入想搜尋的關鍵字: ")
#將使用者輸入的關鍵字轉換為URL格式
search = urllib.parse.quote(user_input)+"&"

# 指定要爬取的URL
url="https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=zh-TW&source=gcsc&gss=.tw&cselibv=e992cd4de3c7044f&cx=011856925919198164995:zrqfhvriqea&q="+search+"safe=off&cse_tok=AB-tC_5fN50TfjOdI9nUOi5GPLCY:1698867247369&sort=&as_sitesearch=&exp=csqr,cc&callback=google.search.cse.api15199"
# 發起HTTP GET請求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"  # 请替换为你的用户代理(User Agent)，用于伪装浏览器请求
}
response = requests.get(url,headers=headers)

if response.status_code == 200:
    # 從回應文本提取JSON
    response_text = response.text
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1
    json_data = response_text[json_start:json_end]

    # 解析JSON數據
    response_json = json.loads(json_data)
    
    # 將JSON數據保存到文件
    with open("result.txt", "w", encoding="utf-8") as json_file:
        json.dump(response_json, json_file, ensure_ascii=False, indent=4)
    # 將JSON數據保存到json.json文件
    with open("result.json", "w", encoding="utf-8") as json_file:
        json.dump(response_json, json_file, ensure_ascii=False, indent=4)


    print("JSON數據以保存到result.txt和result.json文件。")

else:
    print("無法獲取JSON數據。HTTP響應狀態碼:", response.status_code)






# 從JSON文件中讀取數據，指定編碼為 'utf-8'
with open('result.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 提取 "results"
results = data['results']

# 創建CSV文件並寫入數據
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # 寫入CSV文件的標題行
    writer.writerow(['Title', 'URL'])

    # 寫入數據
    for item in results:
        title = item['title']
        url = item['url']
        writer.writerow([title, url])
    
    # 使用Beautiful Soup解析HTML標記並去除他們
    #soup = BeautifulSoup(title_with_tags, 'html.parser')
    #cleaned_title = soup.get_text()

    #writer.writerow([cleaned_title, url])
tEnd = time.time()#計時結束
print('CSV文件已創建並數據已寫入。')
print ("It cost %f sec" % (tEnd - tStart))#會自動做進位
