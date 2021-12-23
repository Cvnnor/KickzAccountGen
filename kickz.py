import requests
import json
from faker import Faker
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup
import cloudscraper
from fake_useragent import UserAgent
import ctypes
from colorama import init
from colorama import Fore, Back, Style
init()

ua = UserAgent()
fake = Faker()

userFile = open("userInfo.json")
userInfo = json.load(userFile)
userInfo = userInfo['userInfo'][0]

global totalAccounts
totalAccounts = 0
global totalFailedAccounts
totalFailedAccounts = 0


def timeLogging():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    timeLogging = "["+current_time+"] - "
    return timeLogging

def registerAccount(scraper, csrfToken):
    global totalAccounts
    global totalFailedAccounts
    proxies = {
        "http": userInfo['proxy'],
        "https": userInfo['proxy'],
    }

    headers = {
        'authority': 'www.kickz.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': str(ua.random),
        'content-type': 'application/x-www-form-urlencoded',
        'x-sec-clge-req-type': 'ajax',
        'accept': 'application/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.kickz.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.kickz.com/en/login/no-referrer',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    params = (
        ('rurl', '1'),
        ('ajax', 'true'),
    )

    #For random name usage:
    if userInfo['firstName'] == "random":
        firstName = fake.unique.first_name()
    else:
        firstName = userInfo['firstName']

    if userInfo['LastName'] == "random":
        lastName = fake.unique.last_name()
    else:
        lastName = userInfo['LastName']


    data = {
    'dwfrm_profile_customer_salutation': 'mr',
    'dwfrm_profile_customer_firstname': str(firstName),
    'dwfrm_profile_customer_lastname': str(lastName),
    'dwfrm_profile_customer_phone': '',
    'dwfrm_profile_customer_email': str(userEmail),
    'dwfrm_profile_customer_emailconfirm': str(userEmail),
    'dwfrm_profile_login_password': str(userInfo['password']),
    'dwfrm_profile_login_passwordconfirm': str(userInfo['password']),
    'dwfrm_profile_customer_agreeToPrivacy': 'true',
    'csrf_token': str(csrftoken)
    }

    print(timeLogging()+"Got cookies, generating account..")
    response = scraper.post('https://www.kickz.com/on/demandware.store/Sites-Kickz-DE-AT-INT-Site/en/Account-SubmitRegistration',headers=headers, params=params, data=data, proxies=proxies)
    # print(response.content, response.status_code) #Print page
    if  response.status_code == 200:
        pageResult = json.loads(response.content)
        if pageResult['validForm'] == True:
            print(Fore.GREEN+timeLogging()+"Successfully generated account. Saving to file.."+Fore.RESET)
            with open('accounts.txt', 'a') as outfile:
                outfile.write(str(userEmail)+":"+str(userInfo['password'])+"\n")
            totalAccounts += 1
        else:
            print(Fore.RED+timeLogging()+"Error submitting account: "+str(pageResult)+Fore.RESET)
            totalFailedAccounts += 1
    else:
        print(Fore.RED +timeLogging()+"Error getting cookies, retrying.. [Proxy Banned]"+Fore.RESET)

accountQty = input("How many accounts would you like to generate?: ")

for i in range(int(accountQty)):
    cmdTitle = "Kickz Account Gen | Tasks: "+str(accountQty)+" | Success: "+str(totalAccounts)+" | Failed: "+str(totalFailedAccounts)
    ctypes.windll.kernel32.SetConsoleTitleW(cmdTitle)
    try:
        userEmail = str(fake.name()).replace(" ", "")+str(userInfo['catchall'])
        print(Style.DIM+timeLogging()+"Gathering Cookies.. "+Style.NORMAL)
        proxies = {"http": userInfo['proxy'], "https": userInfo['proxy']}
        scraper = cloudscraper.create_scraper()
        page = scraper.get("https://www.kickz.com/en/login/", proxies=proxies).content
        soup = BeautifulSoup(page, 'html.parser')
        csrftoken = soup.find("div", {"id": "csrf-token-element"})
        try:
            csrftoken = csrftoken['data-token-value']
            if len(csrftoken) < 1:
                print(timeLogging()+"Error getting cookies retrying..")
            else:
                # print(csrftoken) #Print token
                registerAccount(scraper, csrftoken)
        except:
            print(Fore.RED +timeLogging()+"Error getting cookies, retrying.. [Proxy Banned]"+Fore.RESET)
            totalFailedAccounts += 1
    except Exception as e:
        print(Fore.RED+timeLogging()+"Error - "+str(e)+Fore.RESET)
        totalFailedAccounts += 1

print(Style.BRIGHT+Fore.GREEN+timeLogging()+"Succesfully Generated "+str(totalAccounts)+" Accounts."+Style.RESET_ALL)
