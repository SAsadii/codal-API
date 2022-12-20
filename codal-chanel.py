
import requests
import time
proxy_servers = {
   'http': 'http://185.191.76.84:80',
   'http': 'http://89.43.10.141:80',
   'http': 'http://46.209.204.147:8080',
}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
codalAPI = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=false'
response = requests.get(codalAPI, headers=headers, proxies=proxy_servers) 
List = response.json()


def send_to_telegram(message):

    apiToken = "5963237300:AAH0MIWBZlxCaKZmfGUHKYkr2mATSyqziJg"
    chatID = "@codallive"
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def loadAllMessages():
    for letter in  reversed(List['Letters']):
        message = """Codal API
        Symbol: {}
        CompanyName: {}
        Title: {}
        SentDateTime: {}
        TracingNo: {}
        """.format(letter['Symbol'],letter['CompanyName'],letter['Title'],letter['SentDateTime'],letter['TracingNo'])
        send_to_telegram(message)



def updateMessage():
    lastTrakingNo = 0
    send_to_telegram("Starting Service!")
    while(True):
        response = requests.get(codalAPI, headers=headers) 
        ListTemp = response.json()
        trakingNo = ListTemp['Letters'][0]['TracingNo']
        if lastTrakingNo != trakingNo:
            message = """Codal API
            Symbol: {}
            CompanyName: {}
            Title: {}
            SentDateTime: {}
            TracingNo: {}
            """.format(ListTemp['Letters'][0]['Symbol'],ListTemp['Letters'][0]['CompanyName'],ListTemp['Letters'][0]['Title'],ListTemp['Letters'][0]['SentDateTime'],ListTemp['Letters'][0]['TracingNo'])
            send_to_telegram(message)
            lastTrakingNo = trakingNo
            time.sleep(10)
        time.sleep(60)

loadAllMessages()
updateMessage()