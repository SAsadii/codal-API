import requests
import time
import json
from melipayamak import Api
 




proxy_servers = {
   'http': 'http://185.191.76.84:80',
   'http': 'http://89.43.10.141:80',
   'http': 'http://46.209.204.147:8080',
}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
codalAPI = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=false'
response = requests.get(codalAPI, headers=headers, proxies=proxy_servers) 
List = response.json()

with open('users.json') as usersFile:
    usersData = json.load(usersFile)

def send_to_telegram(message):

    apiToken = "5963237300:AAH0MIWBZlxCaKZmfGUHKYkr2mATSyqziJg"
    chatID = "@codallive"
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

def getPhoneNo(symbol):
    for user in usersData['Users']:
        for symbolF in user['Symbols']:
            if symbol == symbolF:
                return user['PhoneNo'],user['UserName']
    return 0, 0



def postSMS(message, phoneNo):
    username = '9217323446'
    password = '9@TAQ'
    api = Api(username,password)
    sms = api.sms()
    _from = '50004001323446'
    res = sms.send(phoneNo, _from, message)
    print(res)


def getData():
    response = requests.get(codalAPI, headers=headers, proxies=proxy_servers) 
    codalData = response.json()
    message = """Codal API
            Symbol: {}
            CompanyName: {}
            Title: {}
            SentDateTime: {}
            """.format(codalData['Letters'][0]['Symbol'],codalData['Letters'][0]['CompanyName'],codalData['Letters'][0]['Title'],codalData['Letters'][0]['SentDateTime'])
    phoneNo = getPhoneNo(codalData['Letters'][0]['Symbol'])
    print(message)
    if phoneNo != 0 :
        print("this is ours")
        postSMS(message,phoneNo)

def loadAllMessages():
    for letter in  List['Letters']:
        phoneNo, userName = getPhoneNo(letter['Symbol'])
        message = """
        Symbol: {}
        CompanyName: {}
        User: {}
        PhoneNo: {}
        """.format(letter['Symbol'],letter['CompanyName'],userName, phoneNo)
        print(message)

def updateService():
    while True:
        getData()
        time.sleep(60)

updateService()